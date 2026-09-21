"""Análise exploratória e preparação dos dados das partidas do Brasileirão Série A (2020-2023).

Uso pela linha de comando (a partir da raiz do projeto):

    python src/data_analysis.py

O CSV original nunca é alterado. As saídas são gravadas em ``data/processed``,
``reports`` e ``reports/figures``.
"""

from __future__ import annotations

import difflib
import json
import logging
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

import matplotlib

matplotlib.use("Agg")  # backend sem janela: funciona em terminal e no notebook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# --------------------------------------------------------------------------- #
# Configurações gerais
# --------------------------------------------------------------------------- #
RANDOM_STATE = 42

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
CSV_ORIGINAL = RAIZ_PROJETO / "partidas_20_23.csv"
DIR_PROCESSADO = RAIZ_PROJETO / "data" / "processed"
CSV_PROCESSADO = DIR_PROCESSADO / "partidas_processadas.csv"
DIR_RELATORIOS = RAIZ_PROJETO / "reports"
RELATORIO_MD = DIR_RELATORIOS / "analise_exploratoria.md"
DIR_FIGURAS = DIR_RELATORIOS / "figures"

TOTAL_PARTIDAS_ESPERADO = 1520
PARTIDAS_POR_TEMPORADA = 380
TEMPORADAS = (2020, 2021, 2022, 2023)
JANELA = 5  # jogos anteriores usados nas médias móveis
MIN_JOGOS_CONTEXTO = 3  # mínimo de jogos em casa/fora para o aproveitamento por mando
MIN_PARTIDAS_RANKING = 38  # ao menos uma temporada completa para rankings de médias

COLUNAS_LISTAS_JSON = [
    "yellow_cards_home", "red_cards_home", "gols_home",
    "yellow_cards_away", "red_cards_away", "gols_away",
    "sec_card_home", "sec_card_away",
]

MAPA_MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}
DIAS_SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
               "sexta-feira", "sábado", "domingo"]

CLASSES = ["home_win", "draw", "away_win"]
CODIGO_RESULTADO = {"home_win": 0, "draw": 1, "away_win": 2}
ROTULO_RESULTADO = {"home_win": "Vitória do mandante", "draw": "Empate",
                    "away_win": "Vitória do visitante"}

# Colunas que descrevem o que aconteceu na própria partida: não podem ser usadas
# como entrada para prever essa mesma partida (vazamento de dados).
COLUNAS_PROIBIDAS_OBRIGATORIAS = [
    "home_team_score", "away_team_score", "gols_home", "gols_away",
    "yellow_cards_home", "yellow_cards_away", "red_cards_home", "red_cards_away",
    "sec_card_home", "sec_card_away", "total_gols", "total_amarelos",
    "total_expulsoes", "resultado", "resultado_codigo",
]
COLUNAS_PROIBIDAS_ADICIONAIS = [
    "gols_eventos_mandante", "gols_eventos_visitante",
    "amarelos_mandante", "amarelos_visitante",
    "vermelhos_diretos_mandante", "vermelhos_diretos_visitante",
    "segundos_amarelos_mandante", "segundos_amarelos_visitante",
    "expulsoes_mandante", "expulsoes_visitante",
    "penaltis_convertidos_mandante", "penaltis_convertidos_visitante",
    "gols_contra_mandante", "gols_contra_visitante",
    "saldo_gols_mandante", "teve_expulsao", "teve_penalti_convertido",
    "teve_gol_contra", "publico", "public",
]

# Métricas históricas (nome-base); recebem o sufixo _mandante / _visitante.
METRICAS_HISTORICAS = [
    "pontos_media_ultimos_5", "vitorias_ultimos_5", "empates_ultimos_5",
    "derrotas_ultimos_5", "gols_marcados_media_ultimos_5",
    "gols_sofridos_media_ultimos_5", "saldo_gols_media_ultimos_5",
    "amarelos_media_ultimos_5", "expulsoes_media_ultimos_5",
    "aproveitamento_ultimos_5",
]
COLUNAS_HISTORICAS = (
    [f"{m}_{lado}" for lado in ("mandante", "visitante") for m in METRICAS_HISTORICAS]
    + ["aproveitamento_mandante_em_casa", "aproveitamento_visitante_fora"]
)

ORDEM_COLUNAS = [
    "id_partida", "id_partida_fonte", "temporada", "data_partida", "ano_calendario", "mes", "dia_semana", "hora",
    "home_team", "away_team", "stadium", "ref", "public", "publico", "game_date",
    "home_team_score", "away_team_score", "resultado", "resultado_codigo",
]

# Paleta validada (azul, cinza neutro, laranja; quatro tons para as temporadas).
COR_RESULTADO = {"home_win": "#2a78d6", "draw": "#8a8985", "away_win": "#eb6834"}
COR_TEMPORADA = {2020: "#2a78d6", 2021: "#eb6834", 2022: "#1baf7a", 2023: "#4a3aa7"}
COR_PRINCIPAL = "#2a78d6"
COR_SECUNDARIA = "#eb6834"
COR_TEXTO = "#0b0b0b"
COR_TEXTO_SUAVE = "#52514e"
COR_GRADE = "#e3e2de"

logger = logging.getLogger("analise")


class ValidacaoError(AssertionError):
    """Erro levantado quando uma validação obrigatória falha."""


def configurar_log(nivel: int = logging.INFO) -> None:
    """Envia as mensagens de processamento para a saída padrão (uma única vez)."""
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(handler)
    logger.setLevel(nivel)
    logger.propagate = False


# --------------------------------------------------------------------------- #
# Utilidades de formatação
# --------------------------------------------------------------------------- #
def num(valor, casas: int = 2) -> str:
    """Formata número no padrão brasileiro (vírgula decimal, ponto de milhar)."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)) or valor is pd.NA:
        return "—"
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def mil(valor) -> str:
    """Inteiro com ponto como separador de milhar (1.520)."""
    return f"{int(valor):,}".replace(",", ".")


def pct(valor: float, casas: int = 1) -> str:
    """Formata proporção (0-1) como percentual no padrão brasileiro."""
    return f"{num(valor * 100, casas)}%"


def df_para_markdown(df: pd.DataFrame, index: bool = False, casas: int = 2) -> str:
    """Converte um DataFrame em tabela Markdown, sem depender de bibliotecas extras."""
    tabela = df.reset_index() if index else df
    cabecalho = [str(c) for c in tabela.columns]
    linhas = ["| " + " | ".join(cabecalho) + " |", "|" + "|".join(["---"] * len(cabecalho)) + "|"]
    for _, linha in tabela.iterrows():
        celulas = []
        for coluna, v in linha.items():
            if isinstance(v, (float, np.floating)):
                celulas.append(num(float(v), casas))
            elif isinstance(v, (int, np.integer)):
                celulas.append(str(int(v)) if "emporada" in str(coluna) or "ano" in str(coluna).lower() else mil(v))
            else:
                celulas.append("—" if v is pd.NA or v is None else str(v))
        linhas.append("| " + " | ".join(celulas) + " |")
    return "\n".join(linhas)


# --------------------------------------------------------------------------- #
# 4. Carregamento inicial
# --------------------------------------------------------------------------- #
def carregar_dados_brutos(caminho: Path | str = CSV_ORIGINAL, como_texto: bool = False) -> pd.DataFrame:
    """Lê o CSV original (somente leitura).

    Com ``como_texto=True`` todas as colunas são lidas como texto e nenhum valor é
    convertido em ausente, o que preserva marcadores como ``No data``.
    """
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"CSV original não encontrado em: {caminho}")
    if como_texto:
        return pd.read_csv(caminho, dtype=str, keep_default_na=False)
    return pd.read_csv(caminho)


def resumo_carga_inicial(bruto: pd.DataFrame, bruto_texto: pd.DataFrame) -> dict:
    """Reúne as informações descritivas pedidas na carga inicial."""
    times = pd.concat([bruto["home_team"], bruto["away_team"]])
    temporadas = extrair_temporada(bruto_texto["link"])
    datas = converter_data_ptbr(bruto_texto["game_date"])
    return {
        "linhas": bruto.shape[0],
        "colunas": bruto.shape[1],
        "nomes_colunas": list(bruto.columns),
        "tipos": bruto.dtypes.astype(str).rename("tipo").to_frame(),
        "cabeca": bruto.head(5),
        "cauda": bruto.tail(5),
        "ausentes_leitura_padrao": bruto.isna().sum().rename("ausentes").to_frame(),
        "duplicadas": int(bruto.duplicated().sum()),
        "memoria_mb": float(bruto.memory_usage(deep=True).sum() / 1024**2),
        "n_equipes": int(times.nunique()),
        "data_min": datas.min(),
        "data_max": datas.max(),
        "partidas_por_temporada": temporadas.value_counts().sort_index().rename("partidas").to_frame(),
    }


def verificar_marcadores_ausentes(bruto_texto: pd.DataFrame) -> pd.DataFrame:
    """Procura ausência "disfarçada": texto vazio, ``No data`` e listas vazias.

    Um valor pode não ser nulo para o Pandas e mesmo assim não conter informação.
    """
    linhas = []
    for col in bruto_texto.columns:
        s = bruto_texto[col].astype(str).str.strip()
        linhas.append({
            "coluna": col,
            "texto_vazio": int((s == "").sum()),
            "no_data": int(s.str.lower().eq("no data").sum()),
            "lista_vazia": int((s == "[]").sum()),
        })
    tabela = pd.DataFrame(linhas).set_index("coluna")
    tabela["total_sem_informacao"] = tabela.sum(axis=1)
    return tabela


# --------------------------------------------------------------------------- #
# 6. Datas e temporada
# --------------------------------------------------------------------------- #
_REGEX_DATA = re.compile(
    r"^\s*(?P<dia>\d{1,2})\s+de\s+(?P<mes>[A-Za-zÀ-ÿ]+)\s+de\s+(?P<ano>\d{4})\s+(?P<hora>\d{1,2}):(?P<minuto>\d{2})\s*$"
)


def converter_data_ptbr(serie: pd.Series) -> pd.Series:
    """Converte datas como ``25 de fevereiro de 2021 21:30`` em ``datetime64``.

    O mês é traduzido por dicionário (independe do idioma configurado no sistema).
    Textos fora do padrão, meses desconhecidos ou datas inexistentes viram ``NaT``
    e podem ser contados pelo chamador.
    """
    partes = serie.astype(str).str.extract(_REGEX_DATA)
    mes = partes["mes"].str.lower().map(MAPA_MESES)
    componentes = pd.DataFrame({
        "year": pd.to_numeric(partes["ano"], errors="coerce"),
        "month": mes,
        "day": pd.to_numeric(partes["dia"], errors="coerce"),
        "hour": pd.to_numeric(partes["hora"], errors="coerce"),
        "minute": pd.to_numeric(partes["minuto"], errors="coerce"),
    })
    return pd.to_datetime(componentes, errors="coerce")


def extrair_temporada(links: pd.Series) -> pd.Series:
    """Extrai a temporada do identificador da competição presente no link."""
    decodificado = links.astype(str).map(unquote)
    ano = decodificado.str.extract(r"s[ée]rie-a-(\d{4})", flags=re.IGNORECASE)[0]
    return pd.to_numeric(ano, errors="coerce").astype("Int64")


# --------------------------------------------------------------------------- #
# 7. Público
# --------------------------------------------------------------------------- #
_REGEX_PUBLICO = re.compile(r"^\d{1,3}(\.\d{3})*$")


def converter_publico(serie: pd.Series) -> tuple[pd.Series, int]:
    """Converte ``12.089`` em 12089 e ``No data`` em ausente (nunca em zero).

    Retorna a série numérica e a quantidade de textos que não seguiam nenhum dos
    dois formatos esperados (que também viram ausentes).
    """
    texto = serie.astype(str).str.strip()
    e_ausente = texto.str.lower().isin(["no data", "", "nan"])
    e_numero = texto.str.match(_REGEX_PUBLICO)
    valores = pd.to_numeric(texto.where(e_numero).str.replace(".", "", regex=False), errors="coerce")
    inesperados = int((~e_ausente & ~e_numero).sum())
    return valores.astype("Int64"), inesperados


# --------------------------------------------------------------------------- #
# 8. Listas JSON
# --------------------------------------------------------------------------- #
def converter_lista_json(valor, coluna: str = "", indice=None, registro: list | None = None) -> list:
    """Converte o conteúdo de uma célula em lista de dicionários, sem usar ``eval``.

    Qualquer problema (texto vazio, JSON inválido, conteúdo que não é lista,
    elementos que não são objetos) devolve o que for aproveitável e adiciona uma
    linha em ``registro`` para que a inconsistência seja auditada depois.
    """
    def avisar(motivo: str) -> None:
        if registro is not None:
            registro.append({"coluna": coluna, "linha": indice, "motivo": motivo,
                             "conteudo": str(valor)[:80]})

    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        avisar("valor nulo")
        return []
    if isinstance(valor, str):
        if valor.strip() == "":
            avisar("texto vazio")
            return []
        try:
            valor = json.loads(valor)
        except json.JSONDecodeError as erro:
            avisar(f"JSON inválido ({erro.msg})")
            return []
    if not isinstance(valor, list):
        avisar(f"conteúdo não é lista ({type(valor).__name__})")
        return []
    validos = [e for e in valor if isinstance(e, dict)]
    if len(validos) != len(valor):
        avisar("elementos que não são objetos")
    return validos


def converter_colunas_json(df: pd.DataFrame) -> tuple[dict[str, pd.Series], pd.DataFrame]:
    """Aplica :func:`converter_lista_json` a todas as colunas de listas."""
    registro: list = []
    listas = {
        col: pd.Series(
            [converter_lista_json(v, col, i, registro) for i, v in df[col].items()],
            index=df.index,
        )
        for col in COLUNAS_LISTAS_JSON
    }
    inconsistencias = pd.DataFrame(registro, columns=["coluna", "linha", "motivo", "conteudo"])
    if len(inconsistencias):
        logger.warning("%d células com conteúdo JSON problemático (veja o registro).", len(inconsistencias))
    return listas, inconsistencias


def _contar(lista: list, chave: str | None = None) -> int:
    """Conta os eventos de uma lista, ou apenas os que têm ``chave == 1``."""
    if chave is None:
        return len(lista)
    return sum(1 for e in lista if e.get(chave) == 1)


# --------------------------------------------------------------------------- #
# Pipeline de processamento
# --------------------------------------------------------------------------- #
def processar_partidas(bruto_texto: pd.DataFrame, janela: int = JANELA,
                       reiniciar_por_temporada: bool = False) -> tuple[pd.DataFrame, dict]:
    """Transforma o CSV bruto (lido como texto) na base processada.

    Retorna a base e um dicionário ``auxiliares`` com listas convertidas, registro
    de inconsistências JSON e contagens de conversões que falharam.
    """
    df = bruto_texto.copy()

    for col in ("home_team", "away_team"):
        df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)
    df["home_team_score"] = pd.to_numeric(df["home_team_score"], errors="coerce").astype("Int64")
    df["away_team_score"] = pd.to_numeric(df["away_team_score"], errors="coerce").astype("Int64")

    df["data_partida"] = converter_data_ptbr(df["game_date"])
    df["temporada"] = extrair_temporada(df["link"])
    df["publico"], publico_inesperado = converter_publico(df["public"])

    # Ordem cronológica determinística (desempate pelo link) e identificador único.
    df = df.sort_values(["data_partida", "link"], kind="mergesort").reset_index(drop=True)
    df.insert(0, "id_partida", np.arange(1, len(df) + 1))
    df["id_partida_fonte"] = df["link"].str.extract(r"/match/view/([A-Za-z0-9]+)")[0]

    df["ano_calendario"] = df["data_partida"].dt.year
    df["mes"] = df["data_partida"].dt.month
    df["dia_semana"] = df["data_partida"].dt.dayofweek.map(dict(enumerate(DIAS_SEMANA)))
    df["hora"] = df["data_partida"].dt.hour

    listas, inconsistencias_json = converter_colunas_json(df)
    for lado, sufixo in (("home", "mandante"), ("away", "visitante")):
        df[f"gols_eventos_{sufixo}"] = listas[f"gols_{lado}"].map(_contar)
        df[f"amarelos_{sufixo}"] = listas[f"yellow_cards_{lado}"].map(_contar)
        df[f"vermelhos_diretos_{sufixo}"] = listas[f"red_cards_{lado}"].map(_contar)
        df[f"segundos_amarelos_{sufixo}"] = listas[f"sec_card_{lado}"].map(_contar)
        df[f"expulsoes_{sufixo}"] = df[f"vermelhos_diretos_{sufixo}"] + df[f"segundos_amarelos_{sufixo}"]
        df[f"penaltis_convertidos_{sufixo}"] = listas[f"gols_{lado}"].map(lambda l: _contar(l, "penal"))
        df[f"gols_contra_{sufixo}"] = listas[f"gols_{lado}"].map(lambda l: _contar(l, "cont"))

    # Variável-alvo: o placar registrado é a fonte única do resultado.
    diferenca = df["home_team_score"] - df["away_team_score"]
    df["resultado"] = np.select([diferenca > 0, diferenca == 0, diferenca < 0], CLASSES, default="")
    df.loc[diferenca.isna(), "resultado"] = pd.NA
    df["resultado_codigo"] = df["resultado"].map(CODIGO_RESULTADO)

    # Derivadas da própria partida (somente descrição pós-jogo).
    df["total_gols"] = df["home_team_score"] + df["away_team_score"]
    df["saldo_gols_mandante"] = diferenca
    df["total_amarelos"] = df["amarelos_mandante"] + df["amarelos_visitante"]
    df["total_expulsoes"] = df["expulsoes_mandante"] + df["expulsoes_visitante"]
    df["teve_expulsao"] = (df["total_expulsoes"] > 0).astype(int)
    df["teve_penalti_convertido"] = ((df["penaltis_convertidos_mandante"] + df["penaltis_convertidos_visitante"]) > 0).astype(int)
    df["teve_gol_contra"] = ((df["gols_contra_mandante"] + df["gols_contra_visitante"]) > 0).astype(int)

    df = adicionar_historico(df, janela=janela, reiniciar_por_temporada=reiniciar_por_temporada)
    df = df.drop(columns=COLUNAS_LISTAS_JSON)  # permanecem no CSV original; aqui ficam os contadores
    df = df[[c for c in ORDEM_COLUNAS if c in df.columns] + [c for c in df.columns if c not in ORDEM_COLUNAS]]

    listas_reordenadas = {c: s for c, s in listas.items()}
    auxiliares = {
        "listas": listas_reordenadas,
        "inconsistencias_json": inconsistencias_json,
        "publico_formato_inesperado": publico_inesperado,
        "datas_nao_interpretadas": int(df["data_partida"].isna().sum()),
        "temporadas_nao_extraidas": int(df["temporada"].isna().sum()),
    }
    logger.info("Processamento concluído: %d partidas, %d colunas.", *df.shape)
    return df, auxiliares


# --------------------------------------------------------------------------- #
# 14. Histórico dos times (janelas móveis sem vazamento)
# --------------------------------------------------------------------------- #
def construir_tabela_longa(df: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por equipe por partida (perspectiva do mandante e do visitante)."""
    partes = []
    for mando, meu, outro in (("mandante", "home", "away"), ("visitante", "away", "home")):
        suf, suf_adv = (("mandante", "visitante") if mando == "mandante" else ("visitante", "mandante"))
        gols_pro = df[f"{meu}_team_score"].astype(float)
        gols_contra = df[f"{outro}_team_score"].astype(float)
        parte = pd.DataFrame({
            "id_partida": df["id_partida"],
            "temporada": df["temporada"],
            "data_partida": df["data_partida"],
            "equipe": df[f"{meu}_team"],
            "adversario": df[f"{outro}_team"],
            "mando": mando,
            "gols_pro": gols_pro,
            "gols_contra": gols_contra,
            "amarelos": df[f"amarelos_{suf}"].astype(float),
            "expulsoes": df[f"expulsoes_{suf}"].astype(float),
        })
        parte["vitoria"] = (gols_pro > gols_contra).astype(float)
        parte["empate"] = (gols_pro == gols_contra).astype(float)
        parte["derrota"] = (gols_pro < gols_contra).astype(float)
        parte["pontos"] = 3 * parte["vitoria"] + parte["empate"]
        parte["saldo"] = gols_pro - gols_contra
        partes.append(parte)
    return pd.concat(partes, ignore_index=True)


def _nome_janela(base: str, janela: int) -> str:
    """Ajusta o sufixo ``ultimos_5`` dos nomes-base para a janela em uso."""
    return base.replace("ultimos_5", f"ultimos_{janela}")


def adicionar_historico(df: pd.DataFrame, janela: int = JANELA,
                        reiniciar_por_temporada: bool = False) -> pd.DataFrame:
    """Calcula médias móveis dos ``janela`` jogos ANTERIORES de cada equipe.

    * Cada equipe é seguida em ordem cronológica, seja como mandante ou visitante.
    * O histórico atravessa temporadas consecutivas, mas é reiniciado quando a equipe
      ficou ao menos uma temporada inteira fora da base.
    * ``shift(1)`` antes do ``rolling`` garante que a partida atual não entra na
      própria média.
    * Com menos de ``janela`` jogos anteriores o valor fica ausente (NaN): não há
      preenchimento com zero, média geral ou dados futuros.
    * O aproveitamento como mandante/visitante usa os últimos ``janela`` jogos
      naquele mando, com no mínimo ``MIN_JOGOS_CONTEXTO`` jogos.
    """
    longa = (construir_tabela_longa(df)
             .sort_values(["equipe", "data_partida", "id_partida"], kind="mergesort")
             .reset_index(drop=True))
    if reiniciar_por_temporada:
        chaves = ["equipe", "temporada"]
    else:
        # Nova "fase" quando a equipe ficou ao menos uma temporada inteira fora da base
        # (ex.: Vasco em 2020 e 2023): jogos de anos antes não descrevem a equipe atual.
        ausencia = (longa.groupby("equipe")["temporada"].diff() > 1).fillna(False).astype(int)
        longa["fase"] = ausencia.groupby(longa["equipe"]).cumsum()
        chaves = ["equipe", "fase"]

    def movel(dados: pd.DataFrame, coluna: str, operacao: str, minimo: int) -> pd.Series:
        """Média/soma dos ``janela`` jogos anteriores, dentro de cada grupo."""
        return dados.groupby(chaves, sort=False)[coluna].transform(
            lambda s: getattr(s.shift(1).rolling(janela, min_periods=minimo), operacao)()
        )

    especificacao = {  # métrica -> (coluna de origem, operação)
        "pontos_media_ultimos_5": ("pontos", "mean"),
        "vitorias_ultimos_5": ("vitoria", "sum"),
        "empates_ultimos_5": ("empate", "sum"),
        "derrotas_ultimos_5": ("derrota", "sum"),
        "gols_marcados_media_ultimos_5": ("gols_pro", "mean"),
        "gols_sofridos_media_ultimos_5": ("gols_contra", "mean"),
        "saldo_gols_media_ultimos_5": ("saldo", "mean"),
        "amarelos_media_ultimos_5": ("amarelos", "mean"),
        "expulsoes_media_ultimos_5": ("expulsoes", "mean"),
    }
    for metrica, (origem, operacao) in especificacao.items():
        longa[_nome_janela(metrica, janela)] = movel(longa, origem, operacao, janela)
    longa[_nome_janela("aproveitamento_ultimos_5", janela)] = movel(longa, "pontos", "sum", janela) / (3 * janela)
    longa["jogos_anteriores"] = longa.groupby(chaves, sort=False).cumcount()

    # Aproveitamento no mesmo mando (em casa para mandantes, fora para visitantes).
    longa["aproveitamento_mando"] = np.nan
    for mando in ("mandante", "visitante"):
        parte = longa[longa["mando"] == mando]
        longa.loc[parte.index, "aproveitamento_mando"] = movel(parte, "pontos", "mean", MIN_JOGOS_CONTEXTO) / 3

    metricas = [_nome_janela(m, janela) for m in METRICAS_HISTORICAS]
    blocos = []
    for mando in ("mandante", "visitante"):
        parte = longa[longa["mando"] == mando].set_index("id_partida")
        bloco = parte[metricas + ["jogos_anteriores"]].add_suffix(f"_{mando}")
        nome_contexto = "aproveitamento_mandante_em_casa" if mando == "mandante" else "aproveitamento_visitante_fora"
        bloco[nome_contexto] = parte["aproveitamento_mando"]
        blocos.append(bloco)

    # Remove colunas históricas de uma execução anterior antes de juntar as novas.
    obsoletas = [c for c in df.columns if c in COLUNAS_HISTORICAS
                 or c.startswith("jogos_anteriores_") or c == "utilizavel_ml"]
    df = df.drop(columns=obsoletas).join(blocos[0], on="id_partida").join(blocos[1], on="id_partida")
    colunas_janela = [f"{m}_{lado}" for lado in ("mandante", "visitante") for m in metricas]
    df["utilizavel_ml"] = df[colunas_janela].notna().all(axis=1).astype(int)
    return df


# --------------------------------------------------------------------------- #
# 5. Auditoria de qualidade
# --------------------------------------------------------------------------- #
def _chave_normalizada(nome: str) -> str:
    """Remove acentos, caixa e pontuação para detectar variações do mesmo nome."""
    sem_acento = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", sem_acento.lower())


def verificar_nomes_equipes(bruto_texto: pd.DataFrame) -> dict:
    """Procura espaços extras e possíveis variações de nome entre as equipes."""
    nomes = sorted(set(bruto_texto["home_team"]) | set(bruto_texto["away_team"]))
    espacos_extras = [n for n in nomes if n != n.strip() or "  " in n]
    grupos = defaultdict(list)
    for nome in nomes:
        grupos[_chave_normalizada(nome)].append(nome)
    variacoes_exatas = [v for v in grupos.values() if len(v) > 1]
    parecidos = []
    for i, a in enumerate(nomes):
        for b in nomes[i + 1:]:
            razao = difflib.SequenceMatcher(None, _chave_normalizada(a), _chave_normalizada(b)).ratio()
            if razao >= 0.85:
                parecidos.append((a, b, round(razao, 2)))
    return {"nomes": nomes, "espacos_extras": espacos_extras,
            "variacoes_exatas": variacoes_exatas, "nomes_parecidos": parecidos}


def verificar_eventos(df: pd.DataFrame, listas: dict[str, pd.Series]) -> pd.DataFrame:
    """Confere a plausibilidade dos eventos das listas JSON (sem alterar nada)."""
    regex_minuto = re.compile(r"^\d{1,3}(\+\d{1,2})?'$")
    total = {"eventos": 0, "minuto_fora_do_formato": 0, "minuto_acima_de_120": 0,
             "jogador_vazio": 0, "evento_duplicado_na_lista": 0}
    for serie in listas.values():
        for lista in serie:
            vistos = set()
            for e in lista:
                total["eventos"] += 1
                minuto = str(e.get("minute", ""))
                if not regex_minuto.match(minuto):
                    total["minuto_fora_do_formato"] += 1
                else:
                    base = int(minuto.rstrip("'").split("+")[0])
                    total["minuto_acima_de_120"] += int(base > 120)
                total["jogador_vazio"] += int(not str(e.get("player", "")).strip())
                chave = (e.get("player"), e.get("minute"))
                total["evento_duplicado_na_lista"] += int(chave in vistos)
                vistos.add(chave)

    # Um segundo amarelo aparece também na lista de amarelos? (possível dupla contagem)
    segundo_na_lista_amarelos = 0
    segundo_mesmo_minuto = 0
    total_segundos = 0
    vermelho_direto_e_segundo = 0
    for lado in ("home", "away"):
        for i in df.index:
            amarelos = listas[f"yellow_cards_{lado}"][i]
            jogadores_amarelo = {e.get("player") for e in amarelos}
            minutos_amarelo = {(e.get("player"), e.get("minute")) for e in amarelos}
            diretos = {e.get("player") for e in listas[f"red_cards_{lado}"][i]}
            for e in listas[f"sec_card_{lado}"][i]:
                total_segundos += 1
                segundo_na_lista_amarelos += int(e.get("player") in jogadores_amarelo)
                segundo_mesmo_minuto += int((e.get("player"), e.get("minute")) in minutos_amarelo)
                vermelho_direto_e_segundo += int(e.get("player") in diretos)
    total.update({
        "segundos_amarelos": total_segundos,
        "segundo_amarelo_jogador_tambem_na_lista_de_amarelos": segundo_na_lista_amarelos,
        "segundo_amarelo_mesmo_jogador_e_minuto_na_lista_de_amarelos": segundo_mesmo_minuto,
        "mesmo_jogador_em_vermelho_direto_e_segundo_amarelo": vermelho_direto_e_segundo,
    })
    return pd.Series(total, name="quantidade").to_frame()


def divergencias_gols(df: pd.DataFrame) -> pd.DataFrame:
    """Partidas em que o número de eventos de gol difere do placar registrado."""
    mask = ((df["gols_eventos_mandante"] != df["home_team_score"])
            | (df["gols_eventos_visitante"] != df["away_team_score"]))
    colunas = ["id_partida", "temporada", "home_team", "away_team", "home_team_score",
               "away_team_score", "gols_eventos_mandante", "gols_eventos_visitante",
               "gols_contra_mandante", "gols_contra_visitante"]
    return df.loc[mask, colunas]


def auditar_qualidade(bruto_texto: pd.DataFrame, df: pd.DataFrame, aux: dict) -> pd.DataFrame:
    """Tabela resumo: problema verificado, quantidade encontrada e tratamento adotado."""
    nomes = verificar_nomes_equipes(bruto_texto)
    contagem_temporada = df["temporada"].value_counts()
    temporadas_fora = [int(t) for t in contagem_temporada.index if contagem_temporada[t] != PARTIDAS_POR_TEMPORADA]
    times_por_temporada = pd.concat([
        df[["temporada", "home_team"]].rename(columns={"home_team": "t"}),
        df[["temporada", "away_team"]].rename(columns={"away_team": "t"}),
    ]).groupby("temporada")["t"].nunique()
    presenca = pd.concat([df["home_team"], df["away_team"]]).to_frame("t").join(
        pd.concat([df["temporada"], df["temporada"]]).rename("s").reset_index(drop=True)
    ).groupby("t")["s"].nunique()
    longa = construir_tabela_longa(df)
    jogos_simultaneos = int(longa.duplicated(["equipe", "data_partida"]).sum())
    no_data_estadio = int(bruto_texto["stadium"].str.strip().str.lower().isin(["no data", ""]).sum())
    no_data_arbitro = int(bruto_texto["ref"].str.strip().str.lower().isin(["no data", ""]).sum())
    div = divergencias_gols(df)
    fora_do_ano = int((df["ano_calendario"] != df["temporada"]).sum())

    linhas = [
        ("Linhas completamente duplicadas", int(bruto_texto.duplicated().sum()), "Nenhum tratamento necessário."),
        ("Links duplicados", int(bruto_texto["link"].duplicated().sum()), "Nenhum tratamento necessário; o link identifica a partida."),
        ("Combinações duplicadas (data, mandante, visitante)",
         int(bruto_texto.duplicated(["game_date", "home_team", "away_team"]).sum()), "Nenhum tratamento necessário."),
        ("Mandante igual ao visitante", int((df["home_team"] == df["away_team"]).sum()), "Nenhum tratamento necessário."),
        ("Placares negativos", int(((df["home_team_score"] < 0) | (df["away_team_score"] < 0)).sum()), "Nenhum tratamento necessário."),
        ("Placares não numéricos", int(df[["home_team_score", "away_team_score"]].isna().any(axis=1).sum()), "Nenhum tratamento necessário."),
        ("Gols do placar ≠ eventos de gol (mandante ou visitante)", len(div),
         "O placar é mantido como fonte principal; divergências seriam apenas documentadas."),
        ("Listas JSON inválidas ou de tipo inesperado", len(aux["inconsistencias_json"]),
         "Conversão segura sem eval; conteúdo inválido viraria lista vazia e seria registrado."),
        ("Temporadas com quantidade de partidas ≠ 380", len(temporadas_fora), "Nenhum tratamento necessário."),
        ("Temporadas com quantidade de equipes ≠ 20", int((times_por_temporada != 20).sum()), "Nenhum tratamento necessário."),
        ("Nomes de equipe com espaços extras", len(nomes["espacos_extras"]),
         "Aplicado strip e colapso de espaços (sem efeito neste arquivo)."),
        ("Variações do mesmo time (sem acento, caixa ou pontuação)", len(nomes["variacoes_exatas"]),
         "Nenhum tratamento necessário; um nome por equipe."),
        ("Pares de nomes muito parecidos (similaridade ≥ 0,85)", len(nomes["nomes_parecidos"]),
         "Revisão manual: nenhum par indica a mesma equipe." if not nomes["nomes_parecidos"] else "Revisar manualmente."),
        ("Equipes que não disputaram as quatro temporadas", int((presenca < len(TEMPORADAS)).sum()),
         "Mantidas; o histórico usa apenas os jogos disponíveis de cada equipe."),
        ("Mesma equipe em duas partidas no mesmo instante", jogos_simultaneos, "Nenhum tratamento necessário."),
        ("Estádio ausente (vazio ou No data)", no_data_estadio, "Nenhum tratamento necessário."),
        ("Árbitro ausente (vazio ou No data)", no_data_arbitro, "Nenhum tratamento necessário."),
        ("Público ausente (No data)", int(df["publico"].isna().sum()),
         "Mantido como valor ausente (NaN); nunca substituído por zero."),
        ("Público em formato inesperado", aux["publico_formato_inesperado"], "Nenhum tratamento necessário."),
        ("Datas não interpretadas", aux["datas_nao_interpretadas"], "Nenhum tratamento necessário."),
        ("Temporada não extraída do link", aux["temporadas_nao_extraidas"], "Nenhum tratamento necessário."),
        ("Partidas disputadas em ano calendário diferente da temporada", fora_do_ano,
         "Mantidas; a temporada vem do link e não do ano da data."),
    ]
    return pd.DataFrame(linhas, columns=["Verificação", "Quantidade", "Tratamento adotado"])


# --------------------------------------------------------------------------- #
# 11. Análises exploratórias
# --------------------------------------------------------------------------- #
def distribuicao_resultados(df: pd.DataFrame) -> pd.DataFrame:
    contagem = df["resultado"].value_counts().reindex(CLASSES).fillna(0).astype(int)
    return pd.DataFrame({
        "classe": contagem.index,
        "significado": [ROTULO_RESULTADO[c] for c in contagem.index],
        "codigo": [CODIGO_RESULTADO[c] for c in contagem.index],
        "partidas": contagem.values,
        "percentual": (contagem / contagem.sum() * 100).values,
    })


def estatisticas_gerais(df: pd.DataFrame) -> pd.DataFrame:
    g = df["total_gols"]
    linhas = [
        ("Partidas", len(df)),
        ("Gols por partida - média", g.mean()),
        ("Gols por partida - mediana", g.median()),
        ("Gols por partida - mínimo", g.min()),
        ("Gols por partida - máximo", g.max()),
        ("Gols dos mandantes - média", df["home_team_score"].mean()),
        ("Gols dos visitantes - média", df["away_team_score"].mean()),
        ("Cartões amarelos por partida - média", df["total_amarelos"].mean()),
        ("Expulsões por partida - média", df["total_expulsoes"].mean()),
        ("Partidas com expulsão (%)", df["teve_expulsao"].mean() * 100),
        ("Partidas com ao menos 3 gols (%)", (g >= 3).mean() * 100),
        ("Partidas com pênalti convertido (%)", df["teve_penalti_convertido"].mean() * 100),
        ("Partidas com gol contra (%)", df["teve_gol_contra"].mean() * 100),
    ]
    return pd.DataFrame(linhas, columns=["métrica", "valor"])


def analise_por_temporada(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    grupo = df.groupby("temporada")
    medias = grupo.agg(
        partidas=("id_partida", "count"),
        media_gols=("total_gols", "mean"),
        media_gols_mandante=("home_team_score", "mean"),
        media_gols_visitante=("away_team_score", "mean"),
        media_amarelos=("total_amarelos", "mean"),
        media_expulsoes=("total_expulsoes", "mean"),
        pct_com_expulsao=("teve_expulsao", lambda s: s.mean() * 100),
    )
    resultados = pd.crosstab(df["temporada"], df["resultado"]).reindex(columns=CLASSES)
    resultados_pct = resultados.div(resultados.sum(axis=1), axis=0) * 100
    publico = grupo["publico"].agg(
        disponiveis="count",
        media=lambda s: s.astype(float).mean(),
        mediana=lambda s: s.astype(float).median(),
        minimo=lambda s: s.astype(float).min(),
        maximo=lambda s: s.astype(float).max(),
    )
    return {"medias": medias, "resultados": resultados, "resultados_pct": resultados_pct,
            "publico": publico}


def estatisticas_por_equipe(df: pd.DataFrame) -> pd.DataFrame:
    """Desempenho geral, como mandante e como visitante de cada equipe."""
    longa = construir_tabela_longa(df)

    def agregar(dados: pd.DataFrame) -> pd.DataFrame:
        r = dados.groupby("equipe").agg(
            partidas=("id_partida", "count"), vitorias=("vitoria", "sum"),
            empates=("empate", "sum"), derrotas=("derrota", "sum"), pontos=("pontos", "sum"),
            gols_marcados=("gols_pro", "sum"), gols_sofridos=("gols_contra", "sum"),
            amarelos=("amarelos", "sum"), expulsoes=("expulsoes", "sum"),
        )
        r["aproveitamento"] = r["pontos"] / (3 * r["partidas"])
        return r

    geral = agregar(longa)
    geral["temporadas"] = longa.groupby("equipe")["temporada"].nunique()
    geral["saldo_gols"] = geral["gols_marcados"] - geral["gols_sofridos"]
    geral["media_gols_marcados"] = geral["gols_marcados"] / geral["partidas"]
    geral["media_gols_sofridos"] = geral["gols_sofridos"] / geral["partidas"]
    geral["media_amarelos"] = geral["amarelos"] / geral["partidas"]
    geral["media_expulsoes"] = geral["expulsoes"] / geral["partidas"]
    casa = agregar(longa[longa["mando"] == "mandante"]).add_suffix("_casa")
    fora = agregar(longa[longa["mando"] == "visitante"]).add_suffix("_fora")
    cols_mando = ["partidas", "vitorias", "empates", "derrotas", "pontos", "gols_marcados",
                  "gols_sofridos", "aproveitamento"]
    tabela = geral.join(casa[[f"{c}_casa" for c in cols_mando]]).join(fora[[f"{c}_fora" for c in cols_mando]])
    inteiras = [c for c in tabela.columns if c not in
                ("aproveitamento", "aproveitamento_casa", "aproveitamento_fora", "media_gols_marcados",
                 "media_gols_sofridos", "media_amarelos", "media_expulsoes")]
    tabela[inteiras] = tabela[inteiras].astype(int)
    return tabela.sort_values(["pontos", "saldo_gols"], ascending=False).reset_index()


def rankings(equipes: pd.DataFrame, min_partidas: int = MIN_PARTIDAS_RANKING, n: int = 10) -> dict[str, pd.DataFrame]:
    """Rankings pedidos; os baseados em médias exigem ``min_partidas`` jogos."""
    elegiveis = equipes[equipes["partidas"] >= min_partidas]
    return {
        "mais_vitorias": equipes.nlargest(n, ["vitorias", "aproveitamento"])[["equipe", "partidas", "vitorias", "aproveitamento"]],
        "melhores_aproveitamentos": elegiveis.nlargest(n, "aproveitamento")[["equipe", "partidas", "pontos", "aproveitamento"]],
        "maiores_medias_gols": elegiveis.nlargest(n, "media_gols_marcados")[["equipe", "partidas", "gols_marcados", "media_gols_marcados"]],
        "melhores_saldos": equipes.nlargest(n, "saldo_gols")[["equipe", "partidas", "gols_marcados", "gols_sofridos", "saldo_gols"]],
        "mais_amarelos": equipes.nlargest(n, ["amarelos", "media_amarelos"])[["equipe", "partidas", "amarelos", "media_amarelos"]],
        "mais_expulsoes": equipes.nlargest(n, ["expulsoes", "media_expulsoes"])[["equipe", "partidas", "expulsoes", "media_expulsoes"]],
    }


def relacoes_variaveis(df: pd.DataFrame) -> dict:
    """Associações descritivas e testes simples. Nenhuma delas prova causalidade."""
    saida: dict = {}
    n = len(df)
    vm, em, vv = (df["resultado"] == "home_win").sum(), (df["resultado"] == "draw").sum(), (df["resultado"] == "away_win").sum()
    saida["mando"] = pd.DataFrame({
        "mandante": [vm, em, vv, (3 * vm + em) / (3 * n)],
        "visitante": [vv, em, vm, (3 * vv + em) / (3 * n)],
    }, index=["vitórias", "empates", "derrotas", "aproveitamento"])
    teste = stats.binomtest(int(vm), int(vm + vv), 0.5)
    saida["teste_mando"] = {"vitorias_mandante": int(vm), "vitorias_visitante": int(vv), "p_valor": float(teste.pvalue)}

    saida["gols_por_resultado"] = df.groupby("resultado")[["home_team_score", "away_team_score", "total_gols"]].mean().reindex(CLASSES)
    saida["amarelos_por_resultado"] = df.groupby("resultado")[["amarelos_mandante", "amarelos_visitante", "total_amarelos"]].mean().reindex(CLASSES)

    linhas = []
    for rotulo, mask in (
        ("Sem expulsão na partida", df["total_expulsoes"] == 0),
        ("Expulsão apenas do mandante", (df["expulsoes_mandante"] > 0) & (df["expulsoes_visitante"] == 0)),
        ("Expulsão apenas do visitante", (df["expulsoes_visitante"] > 0) & (df["expulsoes_mandante"] == 0)),
        ("Expulsão dos dois times", (df["expulsoes_mandante"] > 0) & (df["expulsoes_visitante"] > 0)),
    ):
        sub = df[mask]
        linha = {"situação": rotulo, "partidas": len(sub)}
        for c in CLASSES:
            linha[f"{c} (%)"] = (sub["resultado"] == c).mean() * 100 if len(sub) else np.nan
        linhas.append(linha)
    saida["expulsoes_resultado"] = pd.DataFrame(linhas)

    disponivel = df.dropna(subset=["publico"]).copy()
    disponivel["publico"] = disponivel["publico"].astype(float)
    rho, p = stats.spearmanr(disponivel["publico"], disponivel["total_gols"])
    saida["publico_gols"] = {"n": len(disponivel), "rho": float(rho), "p_valor": float(p)}
    saida["publico_por_resultado"] = disponivel.groupby("resultado")["publico"].agg(["count", "mean", "median"]).reindex(CLASSES)
    grupos = [g["publico"].values for _, g in disponivel.groupby("resultado")]
    saida["kruskal_publico_resultado"] = float(stats.kruskal(*grupos).pvalue)

    tabela = pd.crosstab(df["temporada"], df["resultado"]).reindex(columns=CLASSES)
    chi2, p_chi, _, _ = stats.chi2_contingency(tabela)
    saida["chi2_resultado_temporada"] = {"chi2": float(chi2), "p_valor": float(p_chi)}
    gols_temp = [g["total_gols"].values for _, g in df.groupby("temporada")]
    saida["kruskal_gols_temporada"] = float(stats.kruskal(*gols_temp).pvalue)
    amar_temp = [g["total_amarelos"].values for _, g in df.groupby("temporada")]
    saida["kruskal_amarelos_temporada"] = float(stats.kruskal(*amar_temp).pvalue)

    numericas = ["total_gols", "total_amarelos", "total_expulsoes", "saldo_gols_mandante", "publico"]
    saida["correlacao_spearman"] = df[numericas].astype(float).corr(method="spearman")
    return saida


# --------------------------------------------------------------------------- #
# 7 e 13. Público ausente e outliers
# --------------------------------------------------------------------------- #
def analise_publico_ausente(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Investiga onde o público está ausente, sem supor o motivo."""
    aus = df["publico"].isna()
    por_temporada = df.assign(ausente=aus).groupby("temporada")["ausente"].agg(
        partidas="count", ausentes="sum", percentual=lambda s: s.mean() * 100)
    ano_mes = df.assign(ausente=aus).groupby(["temporada", "ano_calendario", "mes"])["ausente"].agg(
        partidas="count", ausentes="sum", percentual=lambda s: s.mean() * 100).reset_index()
    disponiveis = df.dropna(subset=["publico"])
    return {
        "por_temporada": por_temporada,
        "por_periodo": ano_mes,
        "disponiveis_por_temporada": disponiveis.groupby("temporada")["publico"].agg(
            partidas="count", mediana=lambda s: s.astype(float).median(),
            minimo=lambda s: s.astype(float).min(), maximo=lambda s: s.astype(float).max()),
        "primeiro_publico_disponivel": disponiveis.groupby("temporada")["data_partida"].min().to_frame("primeira_data_com_publico"),
        "ultimo_ausente": df[aus].groupby("temporada")["data_partida"].max().to_frame("ultima_data_sem_publico"),
    }


def limites_iqr(serie: pd.Series, fator: float = 1.5) -> tuple[float, float, float, float]:
    s = serie.dropna().astype(float)
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1, q3, q1 - fator * iqr, q3 + fator * iqr


def analise_outliers(df: pd.DataFrame) -> dict:
    """Estatísticas por IQR e linhas extremas (nada é removido)."""
    linhas = []
    extremos = {}
    for col, rotulo in (("total_gols", "Gols na partida"), ("total_amarelos", "Amarelos na partida"),
                        ("total_expulsoes", "Expulsões na partida"), ("publico", "Público")):
        q1, q3, inf, sup = limites_iqr(df[col])
        s = df[col].astype(float)
        acima, abaixo = s > sup, s < inf
        linhas.append({"variável": rotulo, "Q1": q1, "Q3": q3, "limite inferior": inf,
                       "limite superior": sup, "abaixo": int(abaixo.sum()), "acima": int(acima.sum()),
                       "mínimo": s.min(), "máximo": s.max()})
        extremos[col] = df.loc[acima | abaixo]
    colunas = ["id_partida", "temporada", "data_partida", "home_team", "away_team",
               "home_team_score", "away_team_score", "total_gols", "total_amarelos", "total_expulsoes", "publico", "stadium"]
    return {
        "iqr": pd.DataFrame(linhas),
        "maiores_placares": df.nlargest(8, "total_gols")[colunas],
        "mais_amarelos": df.nlargest(8, "total_amarelos")[colunas],
        "mais_expulsoes": df.nlargest(8, "total_expulsoes")[colunas],
        "menores_publicos": df.dropna(subset=["publico"]).nsmallest(8, "publico")[colunas],
        "maiores_publicos": df.dropna(subset=["publico"]).nlargest(8, "publico")[colunas],
        "extremos": extremos,
    }


# --------------------------------------------------------------------------- #
# 14 e 16. Testes contra vazamento temporal e validações obrigatórias
# --------------------------------------------------------------------------- #
MAPA_FORCA_BRUTA = {  # chave do recálculo independente -> métrica do pipeline
    "pontos_media": "pontos_media_ultimos_5", "vitorias": "vitorias_ultimos_5",
    "empates": "empates_ultimos_5", "derrotas": "derrotas_ultimos_5",
    "gols_marcados_media": "gols_marcados_media_ultimos_5",
    "gols_sofridos_media": "gols_sofridos_media_ultimos_5",
    "saldo_gols_media": "saldo_gols_media_ultimos_5",
    "amarelos_media": "amarelos_media_ultimos_5", "expulsoes_media": "expulsoes_media_ultimos_5",
    "aproveitamento": "aproveitamento_ultimos_5",
}


def _historico_por_forca_bruta(df: pd.DataFrame, janela: int) -> pd.DataFrame:
    """Recalcula o histórico de forma independente (filtrando por data estritamente anterior)."""
    longa = construir_tabela_longa(df).sort_values(["data_partida", "id_partida"])
    jogos: dict[str, list] = defaultdict(list)
    for r in longa.itertuples(index=False):
        jogos[r.equipe].append(r)
    temporadas_da_equipe = {e: {int(x.temporada) for x in lista} for e, lista in jogos.items()}

    def primeira_temporada_da_fase(equipe: str, temporada: int) -> int:
        """Recua enquanto a equipe tiver disputado a temporada imediatamente anterior."""
        while (temporada - 1) in temporadas_da_equipe[equipe]:
            temporada -= 1
        return temporada

    def resumir(anteriores: list) -> dict:
        ultimos = anteriores[-janela:]
        if len(ultimos) < janela:
            return {}
        pts = [r.pontos for r in ultimos]
        return {
            "pontos_media": np.mean(pts), "vitorias": sum(r.vitoria for r in ultimos),
            "empates": sum(r.empate for r in ultimos), "derrotas": sum(r.derrota for r in ultimos),
            "gols_marcados_media": np.mean([r.gols_pro for r in ultimos]),
            "gols_sofridos_media": np.mean([r.gols_contra for r in ultimos]),
            "saldo_gols_media": np.mean([r.saldo for r in ultimos]),
            "amarelos_media": np.mean([r.amarelos for r in ultimos]),
            "expulsoes_media": np.mean([r.expulsoes for r in ultimos]),
            "aproveitamento": sum(pts) / (3 * janela),
        }

    linhas = []
    for r in longa.itertuples(index=False):
        inicio_fase = primeira_temporada_da_fase(r.equipe, int(r.temporada))
        anteriores = [x for x in jogos[r.equipe]
                      if x.data_partida < r.data_partida and int(x.temporada) >= inicio_fase]
        mesmo_mando = [x for x in anteriores if x.mando == r.mando][-janela:]
        base = resumir(anteriores)
        base["contexto"] = (np.mean([x.pontos for x in mesmo_mando]) / 3
                            if len(mesmo_mando) >= MIN_JOGOS_CONTEXTO else np.nan)
        base.update({"id_partida": r.id_partida, "mando": r.mando, "n_anteriores": len(anteriores)})
        linhas.append(base)
    return pd.DataFrame(linhas)


def testar_vazamento_temporal(df: pd.DataFrame, janela: int = JANELA,
                              reiniciar_por_temporada: bool = False) -> pd.DataFrame:
    """Testes automáticos de que o histórico usa apenas partidas anteriores.

    1. Recalculo independente por força bruta (filtro por data anterior).
    2. Perturbação do futuro: embaralha os resultados a partir de uma data de
       corte; as variáveis históricas das partidas até o corte não podem mudar.
    3. Equipes sem jogos anteriores suficientes devem ter histórico ausente.
    """
    resultados = []
    metricas = [_nome_janela(m, janela) for m in METRICAS_HISTORICAS]

    if not reiniciar_por_temporada:
        bruto = _historico_por_forca_bruta(df, janela).set_index(["id_partida", "mando"])
        comparacoes = 0
        divergencias = 0
        for lado in ("mandante", "visitante"):
            for chave_bruta, metrica in MAPA_FORCA_BRUTA.items():
                coluna = f"{_nome_janela(metrica, janela)}_{lado}"
                esperado = bruto.xs(lado, level="mando")[chave_bruta].reindex(df["id_partida"]).to_numpy(dtype=float)
                iguais = np.isclose(esperado, df[coluna].to_numpy(dtype=float), equal_nan=True)
                divergencias += int((~iguais).sum())
                comparacoes += len(iguais)
        for lado, coluna in (("mandante", "aproveitamento_mandante_em_casa"), ("visitante", "aproveitamento_visitante_fora")):
            esperado = bruto.xs(lado, level="mando")["contexto"].reindex(df["id_partida"]).to_numpy(dtype=float)
            obtido = df[coluna].to_numpy(dtype=float)
            iguais = np.isclose(esperado, obtido, equal_nan=True)
            divergencias += int((~iguais).sum())
            comparacoes += len(iguais)
        resultados.append(("Recalculo independente por força bruta", divergencias == 0,
                           f"{comparacoes} valores comparados; {divergencias} divergências"))

    # Perturbação do futuro: a partir da data de corte os resultados são embaralhados.
    rng = np.random.default_rng(RANDOM_STATE)
    corte = df["data_partida"].sort_values().iloc[len(df) // 2]
    perturbado = df.copy()
    futuro = perturbado["data_partida"] >= corte
    for col in ("home_team_score", "away_team_score", "amarelos_mandante", "amarelos_visitante",
                "expulsoes_mandante", "expulsoes_visitante"):
        perturbado.loc[futuro, col] = rng.integers(0, 8, futuro.sum())
    recalculado = adicionar_historico(perturbado, janela=janela, reiniciar_por_temporada=reiniciar_por_temporada)
    ate_corte = df["data_partida"] <= corte
    cols = [c for c in COLUNAS_HISTORICAS if c in df.columns]
    a = df.loc[ate_corte, cols].to_numpy(dtype=float)
    b = recalculado.loc[ate_corte, cols].to_numpy(dtype=float)
    mudaram = int((~np.isclose(a, b, equal_nan=True)).sum())
    resultados.append(("Perturbação do futuro não altera o passado", mudaram == 0,
                       f"{int(ate_corte.sum())} partidas até {corte:%d/%m/%Y}, incluindo a própria do corte; {mudaram} valores alterados"))

    # A partida atual não pode influenciar o próprio histórico.
    atual = df.copy()
    ultimo = atual["data_partida"].idxmax()
    atual.loc[ultimo, ["home_team_score", "away_team_score"]] = [9, 0]
    r2 = adicionar_historico(atual, janela=janela, reiniciar_por_temporada=reiniciar_por_temporada)
    igual = np.allclose(df.loc[ultimo, cols].to_numpy(dtype=float), r2.loc[ultimo, cols].to_numpy(dtype=float), equal_nan=True)
    resultados.append(("Placar da própria partida não altera seu histórico", bool(igual),
                       f"partida id {int(df.loc[ultimo, 'id_partida'])} testada com placar 9x0"))

    # Sem jogos anteriores suficientes => ausência (sem preenchimento).
    ok_inicio = True
    for lado in ("mandante", "visitante"):
        insuficiente = df[f"jogos_anteriores_{lado}"] < janela
        ok_inicio &= bool(df.loc[insuficiente, [f"{m}_{lado}" for m in metricas]].isna().all().all())
        ok_inicio &= bool(df.loc[~insuficiente, [f"{m}_{lado}" for m in metricas]].notna().all().all())
    resultados.append((f"Histórico ausente com menos de {janela} jogos anteriores e presente a partir de {janela}", ok_inicio,
                       "contagem de jogos anteriores coerente com a presença das médias"))

    longa = construir_tabela_longa(df).sort_values(["data_partida", "id_partida"])
    primeiras = longa.drop_duplicates("equipe")  # primeira partida de cada equipe na base
    contagem_inicial = []
    for r in primeiras.itertuples(index=False):
        linha = df.loc[df["id_partida"] == r.id_partida].iloc[0]
        contagem_inicial.append(linha[f"jogos_anteriores_{r.mando}"] == 0
                                and pd.isna(linha[f"pontos_media_ultimos_{janela}_{r.mando}"]))
    resultados.append(("Primeira partida de cada equipe começa sem histórico", bool(all(contagem_inicial)),
                       f"{len(primeiras)} equipes verificadas"))
    return pd.DataFrame(resultados, columns=["teste", "aprovado", "detalhe"])


def executar_validacoes(bruto: pd.DataFrame, df: pd.DataFrame, caminho_saida: Path = CSV_PROCESSADO,
                        testes_vazamento: pd.DataFrame | None = None, levantar_erro: bool = True) -> pd.DataFrame:
    """Validações obrigatórias. Levanta :class:`ValidacaoError` se alguma falhar."""
    contagem = df["temporada"].value_counts()
    numericas_nao_negativas = ["home_team_score", "away_team_score", "total_gols", "amarelos_mandante",
                               "amarelos_visitante", "expulsoes_mandante", "expulsoes_visitante",
                               "gols_eventos_mandante", "gols_eventos_visitante", "publico"]
    saida_existe = Path(caminho_saida).exists()
    saida_ok = False
    detalhe_saida = "arquivo não encontrado"
    if saida_existe:
        lido = pd.read_csv(caminho_saida)
        saida_ok = lido.shape == df.shape and set(lido.columns) == set(df.columns) and list(lido["id_partida"]) == list(df["id_partida"])
        detalhe_saida = f"{lido.shape[0]} linhas x {lido.shape[1]} colunas em {Path(caminho_saida).name}"

    verificacoes = [
        ("Existem 1.520 partidas no arquivo original", len(bruto) == TOTAL_PARTIDAS_ESPERADO, f"{len(bruto)} linhas"),
        ("Não existem placares negativos", bool((df[["home_team_score", "away_team_score"]] >= 0).all().all()), "mínimo dos placares ≥ 0"),
        ("Classes da variável-alvo são apenas home_win, draw e away_win",
         set(df["resultado"].dropna().unique()) <= set(CLASSES) and df["resultado"].notna().all(), str(sorted(df["resultado"].unique()))),
        ("Código numérico consistente com as classes",
         bool((df["resultado_codigo"] == df["resultado"].map(CODIGO_RESULTADO)).all()), "home_win=0, draw=1, away_win=2"),
        ("Mandante diferente do visitante em todas as partidas", bool((df["home_team"] != df["away_team"]).all()), ""),
        ("Soma das partidas por temporada corresponde ao total", int(contagem.sum()) == len(df) == len(bruto), str({int(k): int(v) for k, v in contagem.sort_index().items()})),
        ("Cada temporada possui 380 partidas", bool((contagem == PARTIDAS_POR_TEMPORADA).all()), ""),
        ("Quantidades de gols, cartões e público são ≥ 0",
         bool((df[numericas_nao_negativas].dropna() >= 0).all().all()), ", ".join(numericas_nao_negativas[:3]) + ", ..."),
        ("Todas as datas foram interpretadas", int(df["data_partida"].isna().sum()) == 0, f"{int(df['data_partida'].isna().sum())} não interpretadas"),
        ("Temporada entre 2020 e 2023 em todas as linhas",
         bool(df["temporada"].notna().all() and df["temporada"].between(2020, 2023).all()), str([int(x) for x in sorted(df["temporada"].unique())])),
        ("Partidas em ordem cronológica", bool(df["data_partida"].is_monotonic_increasing), ""),
        ("Identificador de partida único", bool(df["id_partida"].is_unique), ""),
        ("Arquivo processado criado corretamente", saida_ok, detalhe_saida),
    ]
    if testes_vazamento is not None:
        verificacoes.append(("Médias históricas usam somente partidas anteriores",
                             bool(testes_vazamento["aprovado"].all()), f"{int(testes_vazamento['aprovado'].sum())}/{len(testes_vazamento)} testes aprovados"))
    tabela = pd.DataFrame(verificacoes, columns=["validação", "aprovada", "detalhe"])
    falhas = tabela[~tabela["aprovada"]]
    if len(falhas) and levantar_erro:
        mensagem = "; ".join(f"{r.validação} ({r.detalhe})" for r in falhas.itertuples())
        raise ValidacaoError(f"{len(falhas)} validação(ões) falharam: {mensagem}")
    return tabela


def resumo_base_processada(df: pd.DataFrame) -> dict:
    """Números finais pedidos para a base processada."""
    utilizaveis = df[df["utilizavel_ml"] == 1]
    return {
        "linhas": len(df),
        "colunas": df.shape[1],
        "tipos": df.dtypes.astype(str).rename("tipo").to_frame(),
        "ausentes": df.isna().sum()[lambda s: s > 0].rename("ausentes").to_frame(),
        "utilizaveis": len(utilizaveis),
        "descartadas": len(df) - len(utilizaveis),
        "alvo_completo": df["resultado"].value_counts().reindex(CLASSES),
        "alvo_utilizavel": utilizaveis["resultado"].value_counts().reindex(CLASSES),
    }


# --------------------------------------------------------------------------- #
# 12. Gráficos
# --------------------------------------------------------------------------- #
# Nomes usados apenas nos gráficos, para leitura; as tabelas mantêm o nome oficial da base.
NOME_CURTO = {
    "América FC (Minas Gerais)": "América-MG", "Atlético Goianiense": "Atlético-GO", "Avai FC": "Avaí",
    "Botafogo FR": "Botafogo", "CR Flamengo": "Flamengo", "CR Vasco da Gama": "Vasco", "Ceará SC": "Ceará",
    "Chapecoense AF": "Chapecoense", "Club Athletico Paranaense": "Athletico-PR",
    "Clube Atlético Mineiro": "Atlético-MG", "Coritiba FBC": "Coritiba", "Cruzeiro EC": "Cruzeiro",
    "Cuiabá EC": "Cuiabá", "EC Bahia": "Bahia", "EC Juventude": "Juventude", "Fluminense FC": "Fluminense",
    "Fortaleza EC": "Fortaleza", "Goiás EC": "Goiás", "Grêmio FB Porto Alegrense": "Grêmio",
    "Red Bull Bragantino": "Bragantino", "SC Corinthians Paulista": "Corinthians",
    "SC Internacional": "Internacional", "SC do Recife": "Sport", "SE Palmeiras": "Palmeiras",
    "Santos FC Sao Paulo": "Santos", "São Paulo FC": "São Paulo",
}
MESES_ABREV = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
DPI = 150


def _preparar_estilo() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": DPI, "font.size": 10,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10,
        "axes.edgecolor": COR_GRADE, "axes.labelcolor": COR_TEXTO_SUAVE,
        "text.color": COR_TEXTO, "xtick.color": COR_TEXTO_SUAVE, "ytick.color": COR_TEXTO_SUAVE,
        "grid.color": COR_GRADE, "grid.linewidth": 0.8, "axes.spines.top": False,
        "axes.spines.right": False, "legend.frameon": False,
    })


def _salvar(fig: plt.Figure, nome: str, diretorio: Path = DIR_FIGURAS) -> Path:
    """Salva com pelo menos 150 DPI, sem cortar títulos, e fecha a figura."""
    diretorio = Path(diretorio)
    diretorio.mkdir(parents=True, exist_ok=True)
    caminho = diretorio / nome
    fig.savefig(caminho, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return caminho


def _fmt_eixo_decimal(ax: plt.Axes, eixo: str = "y", casas: int = 1) -> None:
    formatador = plt.FuncFormatter(lambda v, _: num(v, casas))
    (ax.yaxis if eixo == "y" else ax.xaxis).set_major_formatter(formatador)


def _rotular(ax: plt.Axes, barras, textos: list[str], horizontal: bool = False, tamanho: int = 9) -> None:
    for barra, texto in zip(barras, textos):
        if horizontal:
            ax.annotate(texto, (barra.get_width(), barra.get_y() + barra.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=tamanho, color=COR_TEXTO)
        else:
            ax.annotate(texto, (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                        fontsize=tamanho, color=COR_TEXTO, zorder=6,
                        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2})


def _barras_agrupadas(ax, categorias, series: dict[str, list[float]], cores: dict[str, str], casas: int = 2):
    largura = 0.8 / len(series)
    x = np.arange(len(categorias))
    for i, (nome, valores) in enumerate(series.items()):
        barras = ax.bar(x + (i - (len(series) - 1) / 2) * largura, valores, largura * 0.92,
                        label=nome, color=cores[nome], edgecolor="white", linewidth=1)
        _rotular(ax, barras, [num(v, casas) for v in valores], tamanho=8)
    ax.set_xticks(x, [str(c) for c in categorias])
    ax.margins(y=0.15)


def grafico_distribuicao_resultados(df, diretorio=DIR_FIGURAS):
    dist = distribuicao_resultados(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar([ROTULO_RESULTADO[c] for c in dist["classe"]], dist["partidas"],
                    color=[COR_RESULTADO[c] for c in dist["classe"]], width=0.6)
    _rotular(ax, barras, [f"{int(n)}\n({num(p, 1)}%)" for n, p in zip(dist["partidas"], dist["percentual"])], tamanho=10)
    ax.set(title="Distribuição dos resultados das partidas (2020–2023)", xlabel="Resultado da partida",
           ylabel="Número de partidas", ylim=(0, dist["partidas"].max() * 1.18))
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    return _salvar(fig, "01_distribuicao_resultados.png", diretorio)


def grafico_resultados_por_temporada(df, diretorio=DIR_FIGURAS):
    pct_ = analise_por_temporada(df)["resultados_pct"]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    base = np.zeros(len(pct_))
    for classe in CLASSES:
        barras = ax.bar(pct_.index.astype(str), pct_[classe], bottom=base, color=COR_RESULTADO[classe],
                        label=ROTULO_RESULTADO[classe], width=0.6, edgecolor="white", linewidth=2)
        for b, v, b0 in zip(barras, pct_[classe], base):
            ax.text(b.get_x() + b.get_width() / 2, b0 + v / 2, f"{num(v, 1)}%", ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")
        base += pct_[classe].values
    ax.set(title="Distribuição dos resultados por temporada", xlabel="Temporada",
           ylabel="Percentual das partidas (%)", ylim=(0, 100))
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3)
    fig.tight_layout()
    return _salvar(fig, "02_resultados_por_temporada.png", diretorio)


def grafico_media_gols_temporada(df, diretorio=DIR_FIGURAS):
    m = analise_por_temporada(df)["medias"]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    _barras_agrupadas(ax, m.index, {"Mandante": m["media_gols_mandante"].tolist(),
                                   "Visitante": m["media_gols_visitante"].tolist(),
                                   "Total da partida": m["media_gols"].tolist()},
                      {"Mandante": COR_RESULTADO["home_win"], "Visitante": COR_RESULTADO["away_win"],
                       "Total da partida": COR_RESULTADO["draw"]})
    ax.set(title="Média de gols por partida em cada temporada", xlabel="Temporada", ylabel="Gols por partida")
    _fmt_eixo_decimal(ax)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3)
    fig.tight_layout()
    return _salvar(fig, "03_media_gols_temporada.png", diretorio)


def grafico_cartoes_temporada(df, diretorio=DIR_FIGURAS):
    g = df.groupby("temporada")[["amarelos_mandante", "amarelos_visitante", "expulsoes_mandante", "expulsoes_visitante"]].mean()
    fig, eixos = plt.subplots(1, 2, figsize=(12, 5.3))
    cores = {"Mandante": COR_RESULTADO["home_win"], "Visitante": COR_RESULTADO["away_win"]}
    _barras_agrupadas(eixos[0], g.index, {"Mandante": g["amarelos_mandante"].tolist(), "Visitante": g["amarelos_visitante"].tolist()}, cores)
    eixos[0].set(title="Cartões amarelos por equipe e partida", xlabel="Temporada", ylabel="Média de amarelos por equipe")
    _barras_agrupadas(eixos[1], g.index, {"Mandante": g["expulsoes_mandante"].tolist(), "Visitante": g["expulsoes_visitante"].tolist()}, cores, casas=3)
    eixos[1].set(title="Expulsões por equipe e partida", xlabel="Temporada", ylabel="Média de expulsões por equipe")
    for ax, casas in zip(eixos, (2, 3)):
        _fmt_eixo_decimal(ax, casas=casas)
        ax.grid(axis="x", visible=False)
    handles, rotulos = eixos[0].get_legend_handles_labels()
    fig.legend(handles, rotulos, loc="lower center", ncol=2)
    fig.suptitle("Cartões por temporada", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0.06, 1, 0.96))
    return _salvar(fig, "04_cartoes_por_temporada.png", diretorio)


def _barras_horizontais_ranking(ax, dados: pd.DataFrame, valor: str, textos: list[str], cor: str, xlabel: str, titulo: str):
    dados = dados.iloc[::-1]
    barras = ax.barh([NOME_CURTO.get(e, e) for e in dados["equipe"]], dados[valor], color=cor, height=0.7)
    _rotular(ax, barras, textos[::-1], horizontal=True)
    ax.set(title=titulo, xlabel=xlabel, ylabel="Equipe")
    ax.margins(x=0.22)
    ax.grid(axis="y", visible=False)


def grafico_times_mais_vitoriosos(equipes, diretorio=DIR_FIGURAS):
    top = rankings(equipes)["mais_vitorias"]
    fig, ax = plt.subplots(figsize=(9, 5.8))
    _barras_horizontais_ranking(ax, top, "vitorias", [f"{v} ({p} jogos)" for v, p in zip(top["vitorias"], top["partidas"])],
                                COR_PRINCIPAL, "Número de vitórias (2020–2023)", "Equipes com mais vitórias")
    fig.tight_layout()
    return _salvar(fig, "05_times_mais_vitoriosos.png", diretorio)


def grafico_times_maior_media_gols(equipes, diretorio=DIR_FIGURAS):
    top = rankings(equipes)["maiores_medias_gols"]
    fig, ax = plt.subplots(figsize=(9, 5.8))
    _barras_horizontais_ranking(ax, top, "media_gols_marcados", [num(v) for v in top["media_gols_marcados"]],
                                COR_PRINCIPAL, "Gols marcados por partida", f"Maiores médias de gols marcados (mínimo {MIN_PARTIDAS_RANKING} partidas)")
    _fmt_eixo_decimal(ax, "x")
    fig.tight_layout()
    return _salvar(fig, "06_times_maior_media_gols.png", diretorio)


def grafico_times_mais_cartoes(equipes, diretorio=DIR_FIGURAS):
    r = rankings(equipes)
    fig, eixos = plt.subplots(1, 2, figsize=(13, 5.8))
    a, e = r["mais_amarelos"], r["mais_expulsoes"]
    _barras_horizontais_ranking(eixos[0], a, "amarelos", [f"{v} ({num(m)}/jogo)" for v, m in zip(a["amarelos"], a["media_amarelos"])],
                                COR_SECUNDARIA, "Total de cartões amarelos", "Mais cartões amarelos")
    _barras_horizontais_ranking(eixos[1], e, "expulsoes", [f"{v} ({num(m, 3)}/jogo)" for v, m in zip(e["expulsoes"], e["media_expulsoes"])],
                                COR_SECUNDARIA, "Total de expulsões", "Mais expulsões")
    fig.suptitle("Equipes com mais cartões (2020–2023; entre parênteses, média por jogo)", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    return _salvar(fig, "07_times_mais_cartoes.png", diretorio)


def grafico_distribuicao_total_gols(df, diretorio=DIR_FIGURAS):
    contagem = df["total_gols"].value_counts().sort_index()
    contagem = contagem.reindex(range(int(contagem.index.max()) + 1), fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 5.3))
    barras = ax.bar(contagem.index.astype(str), contagem.values, color=COR_PRINCIPAL, width=0.7)
    _rotular(ax, barras, [f"{n}\n({num(n / len(df) * 100, 1)}%)" if n else "0" for n in contagem.values], tamanho=8)
    media = df["total_gols"].mean()
    ax.axvline(media, color=COR_SECUNDARIA, linestyle="--", linewidth=1.6, label=f"Média: {num(media)} gols", zorder=1)
    ax.axvline(df["total_gols"].median(), color=COR_TEXTO_SUAVE, linestyle=":", linewidth=1.6, zorder=1,
               label=f"Mediana: {num(df['total_gols'].median(), 0)} gols")
    ax.set(title="Distribuição do total de gols por partida", xlabel="Total de gols na partida",
           ylabel="Número de partidas", ylim=(0, contagem.max() * 1.2))
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    fig.tight_layout()
    return _salvar(fig, "08_distribuicao_total_gols.png", diretorio)


def grafico_mando_campo_resultado(df, equipes, diretorio=DIR_FIGURAS):
    fig, eixos = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1, 1.1]})
    linhas = []
    for temporada, sub in df.groupby("temporada"):
        n = len(sub)
        vm, e, vv = (sub["resultado"] == "home_win").sum(), (sub["resultado"] == "draw").sum(), (sub["resultado"] == "away_win").sum()
        linhas.append((temporada, (3 * vm + e) / (3 * n) * 100, (3 * vv + e) / (3 * n) * 100))
    apr = pd.DataFrame(linhas, columns=["temporada", "mandante", "visitante"]).set_index("temporada")
    _barras_agrupadas(eixos[0], apr.index, {"Mandante": apr["mandante"].tolist(), "Visitante": apr["visitante"].tolist()},
                      {"Mandante": COR_RESULTADO["home_win"], "Visitante": COR_RESULTADO["away_win"]}, casas=1)
    eixos[0].set(title="Aproveitamento de mandantes e visitantes", xlabel="Temporada",
                 ylabel="Aproveitamento dos pontos disputados (%)", ylim=(0, 70))
    eixos[0].grid(axis="x", visible=False)
    eixos[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2)

    ax = eixos[1]
    ax.scatter(equipes["aproveitamento_fora"] * 100, equipes["aproveitamento_casa"] * 100, s=55,
               color=COR_PRINCIPAL, edgecolor="white", linewidth=1.2, zorder=3)
    limite = max(equipes["aproveitamento_casa"].max(), equipes["aproveitamento_fora"].max()) * 100 + 5
    ax.plot([0, limite], [0, limite], color=COR_TEXTO_SUAVE, linestyle="--", linewidth=1, label="Mesmo aproveitamento em casa e fora")
    destaque = equipes.assign(dif=equipes["aproveitamento_casa"] - equipes["aproveitamento_fora"]).sort_values("dif")
    for _, r in pd.concat([destaque.head(3), destaque.tail(3)]).iterrows():
        ax.annotate(NOME_CURTO.get(r["equipe"], r["equipe"]), (r["aproveitamento_fora"] * 100, r["aproveitamento_casa"] * 100),
                    xytext=(5, 4), textcoords="offset points", fontsize=8, color=COR_TEXTO)
    ax.set(title="Aproveitamento por equipe: em casa × fora", xlabel="Aproveitamento como visitante (%)",
           ylabel="Aproveitamento como mandante (%)", xlim=(0, limite), ylim=(0, limite))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13))
    fig.suptitle("Mando de campo e desempenho (2020–2023)", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    return _salvar(fig, "09_mando_campo_resultado.png", diretorio)


def grafico_publico_por_temporada(df, diretorio=DIR_FIGURAS):
    fig, eixos = plt.subplots(1, 2, figsize=(12.5, 5.5), gridspec_kw={"width_ratios": [1.5, 1]})
    ordem = list(TEMPORADAS)
    dados = df.dropna(subset=["publico"]).assign(publico=lambda d: d["publico"].astype(float))
    ax = eixos[0]
    sns.boxplot(data=dados, x="temporada", y="publico", order=ordem, ax=ax, color=COR_PRINCIPAL,
                width=0.55, fliersize=3, linewidth=1.2, saturation=1)
    n_por_temporada = dados["temporada"].value_counts()
    for i, t in enumerate(ordem):
        if n_por_temporada.get(t, 0) == 0:
            ax.text(i, ax.get_ylim()[1] * 0.5, "sem dados\nde público", ha="center", va="center", fontsize=9, color=COR_TEXTO_SUAVE)
    ax.set_xticks(range(len(ordem)), [f"{t}\n(n = {int(n_por_temporada.get(t, 0))})" for t in ordem])
    ax.set(title="Público nas partidas com informação disponível", xlabel="Temporada", ylabel="Público (pessoas)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: num(v, 0)))
    ax.grid(axis="x", visible=False)

    ax = eixos[1]
    aus = analise_publico_ausente(df)["por_temporada"].reindex(ordem)
    barras = ax.bar([str(t) for t in ordem], aus["percentual"], color=COR_SECUNDARIA, width=0.6)
    _rotular(ax, barras, [f"{num(p, 1)}%\n({int(a)} de {int(n)})" for p, a, n in zip(aus["percentual"], aus["ausentes"], aus["partidas"])], tamanho=8)
    ax.set(title="Público ausente (No data)", xlabel="Temporada", ylabel="Partidas sem público informado (%)", ylim=(0, 125))
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.grid(axis="x", visible=False)
    fig.suptitle("Público por temporada", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    return _salvar(fig, "10_publico_por_temporada.png", diretorio)


def grafico_boxplots_outliers(df, diretorio=DIR_FIGURAS):
    fig, eixos = plt.subplots(1, 4, figsize=(14, 5))
    for ax, (col, titulo, rotulo) in zip(eixos, [
        ("total_gols", "Gols na partida", "Gols"), ("total_amarelos", "Amarelos na partida", "Cartões amarelos"),
        ("total_expulsoes", "Expulsões na partida", "Expulsões"), ("publico", "Público", "Pessoas")]):
        sns.boxplot(y=df[col].dropna().astype(float), ax=ax, color=COR_PRINCIPAL, width=0.45, fliersize=3, saturation=1, linewidth=1.2)
        ax.set(title=titulo, ylabel=rotulo, xlabel="")
        ax.set_xticks([])
        ax.grid(axis="x", visible=False)
    fig.suptitle("Boxplots das variáveis numéricas (outliers pelo critério do IQR)", fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return _salvar(fig, "11_boxplots_outliers.png", diretorio)


def grafico_publico_ausente_mes(df, diretorio=DIR_FIGURAS):
    p = analise_publico_ausente(df)["por_periodo"].copy()
    p["rotulo"] = [f"{MESES_ABREV[m - 1]}/{str(a)[2:]}" for a, m in zip(p["ano_calendario"], p["mes"])]
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(p["rotulo"], p["percentual"], color=[COR_TEMPORADA[int(t)] for t in p["temporada"]], width=0.75, edgecolor="white", linewidth=1)
    ax.set(title="Percentual de partidas sem público informado, por mês", xlabel="Mês da partida (ano calendário)",
           ylabel="Partidas sem público (%)", ylim=(0, 108))
    ax.tick_params(axis="x", rotation=90, labelsize=8)
    ax.grid(axis="x", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COR_TEMPORADA[t]) for t in TEMPORADAS]
    ax.legend(handles, [f"Temporada {t}" for t in TEMPORADAS], loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4)
    fig.tight_layout()
    return _salvar(fig, "12_publico_ausente_por_mes.png", diretorio)


def grafico_correlacao(df, diretorio=DIR_FIGURAS):
    corr = relacoes_variaveis(df)["correlacao_spearman"]
    nomes = {"total_gols": "Total de gols", "total_amarelos": "Total de amarelos", "total_expulsoes": "Total de expulsões",
             "saldo_gols_mandante": "Saldo do mandante", "publico": "Público"}
    corr = corr.rename(index=nomes, columns=nomes)
    fig, ax = plt.subplots(figsize=(7.5, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=sns.diverging_palette(250, 30, as_cmap=True, center="light"),
                vmin=-1, vmax=1, linewidths=2, linecolor="white", cbar_kws={"label": "Correlação de Spearman"}, ax=ax)
    for rotulo in ax.texts:
        rotulo.set_text(rotulo.get_text().replace(".", ","))
    ax.collections[0].colorbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: num(v, 2)))
    ax.set_title("Correlação entre variáveis da partida (Spearman)")
    fig.tight_layout()
    return _salvar(fig, "13_correlacao_variaveis.png", diretorio)


def gerar_graficos(df: pd.DataFrame, equipes: pd.DataFrame, diretorio: Path = DIR_FIGURAS) -> dict[str, Path]:
    """Gera todos os gráficos obrigatórios (01-10) e os complementares (11-13)."""
    _preparar_estilo()
    caminhos = {}
    for funcao, args in (
        (grafico_distribuicao_resultados, (df,)), (grafico_resultados_por_temporada, (df,)),
        (grafico_media_gols_temporada, (df,)), (grafico_cartoes_temporada, (df,)),
        (grafico_times_mais_vitoriosos, (equipes,)), (grafico_times_maior_media_gols, (equipes,)),
        (grafico_times_mais_cartoes, (equipes,)), (grafico_distribuicao_total_gols, (df,)),
        (grafico_mando_campo_resultado, (df, equipes)), (grafico_publico_por_temporada, (df,)),
        (grafico_boxplots_outliers, (df,)), (grafico_publico_ausente_mes, (df,)), (grafico_correlacao, (df,)),
    ):
        caminho = funcao(*args, diretorio=diretorio)
        caminhos[caminho.name] = caminho
        logger.info("Gráfico salvo: %s", caminho.name)
    return caminhos


# --------------------------------------------------------------------------- #
# Análises complementares usadas no relatório
# --------------------------------------------------------------------------- #
def desempenho_equipe_por_temporada(df: pd.DataFrame) -> pd.DataFrame:
    """Aproveitamento de cada equipe em cada temporada (colunas = temporadas)."""
    longa = construir_tabela_longa(df)
    tabela = longa.groupby(["equipe", "temporada"])["pontos"].agg(["sum", "count"])
    tabela["aproveitamento"] = tabela["sum"] / (3 * tabela["count"])
    return tabela["aproveitamento"].unstack("temporada")


def descartes_por_temporada(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("temporada")["utilizavel_ml"].agg(utilizaveis="sum", total="count").assign(
        descartadas=lambda d: d["total"] - d["utilizaveis"])


# --------------------------------------------------------------------------- #
# Orquestração
# --------------------------------------------------------------------------- #
def salvar_processado(df: pd.DataFrame, caminho: Path = CSV_PROCESSADO) -> Path:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, date_format="%Y-%m-%d %H:%M:%S")
    logger.info("Base processada salva em %s", caminho.relative_to(RAIZ_PROJETO) if caminho.is_relative_to(RAIZ_PROJETO) else caminho)
    return caminho


def executar_analise(salvar: bool = True, janela: int = JANELA) -> dict:
    """Executa todo o fluxo e devolve um dicionário com os resultados."""
    configurar_log()
    logger.info("Lendo o CSV original (somente leitura): %s", CSV_ORIGINAL.name)
    bruto = carregar_dados_brutos()
    bruto_texto = carregar_dados_brutos(como_texto=True)
    ctx: dict = {"bruto": bruto, "bruto_texto": bruto_texto}
    ctx["carga"] = resumo_carga_inicial(bruto, bruto_texto)
    ctx["marcadores"] = verificar_marcadores_ausentes(bruto_texto)

    df, aux = processar_partidas(bruto_texto, janela=janela)
    ctx.update({"df": df, "aux": aux})
    ctx["auditoria"] = auditar_qualidade(bruto_texto, df, aux)
    ctx["nomes"] = verificar_nomes_equipes(bruto_texto)
    ctx["eventos"] = verificar_eventos(df, aux["listas"])
    ctx["divergencias_gols"] = divergencias_gols(df)
    ctx["vazamento"] = testar_vazamento_temporal(df, janela=janela)
    ctx["utilizaveis_reiniciando_por_temporada"] = int(
        adicionar_historico(df, janela=janela, reiniciar_por_temporada=True)["utilizavel_ml"].sum())

    ctx["distribuicao"] = distribuicao_resultados(df)
    ctx["gerais"] = estatisticas_gerais(df)
    ctx["temporada"] = analise_por_temporada(df)
    ctx["equipes"] = estatisticas_por_equipe(df)
    ctx["rankings"] = rankings(ctx["equipes"])
    ctx["relacoes"] = relacoes_variaveis(df)
    ctx["publico_ausente"] = analise_publico_ausente(df)
    ctx["outliers"] = analise_outliers(df)
    ctx["equipe_temporada"] = desempenho_equipe_por_temporada(df)
    ctx["descartes"] = descartes_por_temporada(df)
    ctx["resumo_final"] = resumo_base_processada(df)

    if salvar:
        ctx["figuras"] = gerar_graficos(df, ctx["equipes"])
        ctx["caminho_processado"] = salvar_processado(df)
    ctx["validacoes"] = executar_validacoes(bruto, df, CSV_PROCESSADO, ctx["vazamento"], levantar_erro=False)
    falhas = ctx["validacoes"][~ctx["validacoes"]["aprovada"]]
    if len(falhas):
        raise ValidacaoError("Validações reprovadas:\n" + falhas.to_string(index=False))
    logger.info("Todas as %d validações obrigatórias foram aprovadas.", len(ctx["validacoes"]))

    if salvar:
        DIR_RELATORIOS.mkdir(parents=True, exist_ok=True)
        RELATORIO_MD.write_text(gerar_relatorio_markdown(ctx), encoding="utf-8")
        logger.info("Relatório salvo em %s", RELATORIO_MD.relative_to(RAIZ_PROJETO))
    return ctx


# --------------------------------------------------------------------------- #
# 17. Relatório em Markdown
# --------------------------------------------------------------------------- #
DICIONARIO_COLUNAS_ORIGINAIS = [
    ("home_team / away_team", "Nome do mandante e do visitante."),
    ("home_team_score / away_team_score", "Gols do mandante e do visitante no placar final."),
    ("game_date", "Data e hora da partida, em texto no formato \"25 de fevereiro de 2021 21:30\"."),
    ("stadium", "Estádio onde a partida foi disputada."),
    ("public", "Público, em texto (\"12.089\") ou o marcador \"No data\"."),
    ("ref", "Nome do árbitro."),
    ("yellow_cards_home / yellow_cards_away", "Lista JSON de cartões amarelos (jogador e minuto)."),
    ("red_cards_home / red_cards_away", "Lista JSON de cartões vermelhos diretos (jogador e minuto)."),
    ("sec_card_home / sec_card_away", "Lista JSON de expulsões por segundo cartão amarelo (jogador e minuto)."),
    ("gols_home / gols_away", "Lista JSON de gols (jogador, minuto, indicador de gol contra `cont` e de pênalti `penal`)."),
    ("link", "Endereço da página da partida; contém o identificador da competição/temporada."),
]

DICIONARIO_COLUNAS_NOVAS = [
    ("id_partida", "Identificador sequencial da partida após a ordenação cronológica."),
    ("id_partida_fonte", "Identificador da partida extraído do link (rastreabilidade)."),
    ("temporada", "Temporada extraída do link (2020 a 2023)."),
    ("data_partida", "Data e hora convertidas para `datetime`."),
    ("ano_calendario, mes, dia_semana, hora", "Componentes da data (hora inteira, 0–23)."),
    ("publico", "Público numérico; ausente quando o original é `No data`."),
    ("resultado, resultado_codigo", "Variável-alvo: home_win=0, draw=1, away_win=2."),
    ("gols_eventos_*, amarelos_*, vermelhos_diretos_*, segundos_amarelos_*, expulsoes_*",
     "Quantidades extraídas das listas JSON para mandante e visitante."),
    ("penaltis_convertidos_*, gols_contra_*", "Gols de pênalti e gols contra registrados na lista de gols de cada lado."),
    ("total_gols, saldo_gols_mandante, total_amarelos, total_expulsoes", "Derivadas da própria partida (uso descritivo)."),
    ("teve_expulsao, teve_penalti_convertido, teve_gol_contra", "Indicadores 0/1 da própria partida."),
    ("*_ultimos_5_mandante / *_ultimos_5_visitante", "Médias e contagens dos cinco jogos anteriores de cada equipe."),
    ("aproveitamento_mandante_em_casa, aproveitamento_visitante_fora", "Aproveitamento nos últimos jogos no mesmo mando (3 a 5 jogos)."),
    ("jogos_anteriores_mandante / jogos_anteriores_visitante", "Quantidade de jogos anteriores da equipe na base."),
    ("utilizavel_ml", "1 quando as duas equipes têm ao menos cinco jogos anteriores."),
]


def _p(valor: float) -> str:
    return "< 0,001" if valor < 0.001 else num(valor, 3)


def _data_br(ts) -> str:
    return pd.Timestamp(ts).strftime("%d/%m/%Y")


def gerar_relatorio_markdown(ctx: dict) -> str:
    """Monta o relatório usando somente valores calculados nesta execução."""
    df, bruto, carga = ctx["df"], ctx["bruto"], ctx["carga"]
    equipes, rel = ctx["equipes"], ctx["relacoes"]
    tp, pub, out = ctx["temporada"], ctx["publico_ausente"], ctx["outliers"]
    audit, ev, res = ctx["auditoria"], ctx["eventos"]["quantidade"], ctx["resumo_final"]
    g = ctx["gerais"].set_index("métrica")["valor"]
    dist = ctx["distribuicao"].set_index("classe")
    rk = ctx["rankings"]
    n_ausente = int(df["publico"].isna().sum())
    div = ctx["divergencias_gols"]
    n_times_4 = int((ctx["equipe_temporada"].notna().all(axis=1)).sum())
    fora_ano = int((df["ano_calendario"] != df["temporada"]).sum())
    fora_ano_2020 = int(((df["ano_calendario"] != df["temporada"]) & (df["temporada"] == 2020)).sum())
    ap = pub["por_temporada"]
    prim = pub["primeiro_publico_disponivel"]["primeira_data_com_publico"]
    med = tp["medias"]
    amp = ctx["equipe_temporada"].dropna().assign(
        amplitude=lambda d: d.max(axis=1) - d.min(axis=1)).sort_values("amplitude", ascending=False)
    top_amp = amp.iloc[0]
    kw_ap = rel["kruskal_amarelos_temporada"]
    mando = rel["mando"]
    exp = rel["expulsoes_resultado"].set_index("situação")
    n_util, n_desc = res["utilizaveis"], res["descartadas"]
    desc_temp = ctx["descartes"]
    pub_menor = out["menores_publicos"].iloc[0]
    n_parecidos = len(ctx["nomes"]["nomes_parecidos"])
    presenca = ctx["equipe_temporada"].notna()
    faltas = presenca.apply(lambda l: (lambda i: (i[-1] - i[0] + 1 - len(i)) if i else 0)(
        [k for k, v in enumerate(l.tolist()) if v]), axis=1)
    n_lacunas = int((faltas > 0).sum())
    eq_lacuna = faltas.idxmax()
    exemplo_lacuna = (f"{NOME_CURTO.get(eq_lacuna, eq_lacuna)}, que disputou apenas "
                      + " e ".join(str(int(c)) for c in presenca.columns[presenca.loc[eq_lacuna]]))
    d21 = df[df["temporada"] == 2021]
    antes21 = d21[d21["data_partida"] < prim.loc[2021]]
    depois21 = d21[d21["data_partida"] >= prim.loc[2021]]
    estadio_menor = df[(df["stadium"] == pub_menor["stadium"]) & (df["id_partida"] != pub_menor["id_partida"])]["publico"].dropna().astype(float)
    n_casa_melhor = int((equipes["aproveitamento_casa"] > equipes["aproveitamento_fora"]).sum())
    lider_apr = rk["melhores_aproveitamentos"].iloc[0]

    L: list[str] = []
    add = L.append

    add("# Análise exploratória e preparação dos dados — Brasileirão Série A (2020–2023)\n")
    add("Disciplina de Inteligência Artificial II. Este documento resume a etapa de análise exploratória (EDA) e de "
        "preparação dos dados que antecede o treinamento de um modelo de classificação do resultado das partidas. "
        "Todos os números abaixo foram calculados pelo código em `src/data_analysis.py` (executado pelo notebook "
        "`notebooks/01_eda_preparacao.ipynb` ou diretamente pela linha de comando) e correspondem exatamente aos valores encontrados na base.\n")

    add("## 1. Descrição do dataset\n")
    add(f"O arquivo `partidas_20_23.csv` reúne {mil(carga['linhas'])} partidas do Campeonato Brasileiro Série A das temporadas "
        f"de {TEMPORADAS[0]} a {TEMPORADAS[-1]}, com {PARTIDAS_POR_TEMPORADA} partidas por temporada, disputadas por {carga['n_equipes']} equipes diferentes. "
        "Cada linha representa uma partida e traz o placar, a data, o estádio, o público, o árbitro e listas de eventos "
        "(gols, cartões amarelos, vermelhos e segundos amarelos) de cada equipe.")
    add("")
    add("**Objetivo futuro:** prever a classe do resultado — vitória do mandante, empate ou vitória do visitante — antes da partida acontecer.\n")

    add("## 2. Origem e período dos dados\n")
    add("Os links de cada partida apontam para o portal `optaplayerstats.statsperform.com` (dados Stats Perform/Opta), o que indica a "
        "fonte da coleta; o arquivo não traz documentação sobre o método de coleta, portanto essa origem é inferida dos links. "
        f"A primeira partida ocorreu em {_data_br(carga['data_min'])} e a última em {_data_br(carga['data_max'])}. "
        f"A temporada 2020 teve {fora_ano_2020} partidas disputadas em 2021, por isso a temporada foi extraída do link e não do ano da data.\n")

    add("## 3. Dimensões da base\n")
    add(f"- Base original: **{mil(carga['linhas'])} linhas × {carga['colunas']} colunas** (memória aproximada de {num(carga['memoria_mb'])} MB).")
    add(f"- Base processada: **{mil(res['linhas'])} linhas × {res['colunas']} colunas** (`data/processed/partidas_processadas.csv`).")
    add(f"- Partidas por temporada: {', '.join(f'{int(t)}: {int(n)}' for t, n in carga['partidas_por_temporada']['partidas'].items())}.\n")

    add("## 4. Descrição das principais colunas\n")
    add(df_para_markdown(pd.DataFrame(DICIONARIO_COLUNAS_ORIGINAIS, columns=["Coluna original", "Descrição"])))
    add("")

    add("## 5. Qualidade dos dados\n")
    add("Cada verificação abaixo foi executada sobre os dados; \"Quantidade\" é o número de ocorrências encontradas.\n")
    add(df_para_markdown(audit))
    add("")
    add("Além dos nulos do Pandas, foram procuradas ausências \"disfarçadas\" (texto vazio, `No data` e listas vazias):\n")
    add(df_para_markdown(ctx["marcadores"].loc[["public", "stadium", "ref"] + COLUNAS_LISTAS_JSON].reset_index()))
    add("")
    add("Listas vazias em cartões e gols são, em geral, ausência legítima de eventos (por exemplo, equipe que não marcou gols). "
        f"Já {int((df['total_amarelos'] == 0).sum())} partidas não têm nenhum cartão amarelo registrado; isso é possível, mas não foi possível confirmar se houve falha de coleta, e os valores foram mantidos.\n")

    add("## 6. Valores ausentes\n")
    add(f"Na leitura padrão do Pandas nenhuma coluna possui valores nulos, porque a ausência está codificada como texto. "
        f"A única coluna com informação faltante é `public`, com **{n_ausente} partidas com `No data` ({pct(n_ausente / len(df))})**. "
        "O valor foi convertido para ausente (NaN) e nunca para zero, pois `No data` não significa público igual a zero.\n")
    add(df_para_markdown(ap.reset_index().rename(columns={"temporada": "Temporada", "partidas": "Partidas", "ausentes": "Sem público", "percentual": "% sem público"})))
    add("")
    add(f"**Padrão temporal.** Em 2020, {int(ap.loc[2020, 'ausentes'])} de {int(ap.loc[2020, 'partidas'])} partidas estão sem público. "
        f"Em 2021, a ausência ocorre em bloco: a primeira partida com público informado foi em {_data_br(prim.loc[2021])}; das {len(antes21)} partidas anteriores a essa data, {int(antes21['publico'].notna().sum())} têm público, "
        f"e a partir dela {int(depois21['publico'].notna().sum())} de {len(depois21)} têm. "
        f"Em 2022 e 2023 a ausência é residual ({int(ap.loc[2022, 'ausentes'])} e {int(ap.loc[2023, 'ausentes'])} partidas, respectivamente) — veja `figures/12_publico_ausente_por_mes.png`.\n")
    add("**Possível impacto da pandemia.** Os dados mostram que a ausência do público concentra-se exatamente no início do período (2020 e parte de 2021) e desaparece quase por completo depois. "
        "Esse padrão é compatível com partidas sem torcida, mas os dados, por si só, não permitem distinguir \"jogo com portões fechados\" de \"público não coletado\", "
        "pois a fonte usa o mesmo marcador (`No data`) nos dois casos. Por isso essa explicação é tratada como hipótese a ser confirmada com fonte externa, e não como fato. "
        f"Um indício adicional é que os primeiros públicos informados em 2021 são baixos (mínimo de {num(float(pub['disponiveis_por_temporada'].loc[2021, 'minimo']), 0)} pessoas), o que também é compatível com reabertura gradual dos estádios, sem prová-la. "
        "Consequência prática: a variável `publico` não pode ser usada como entrada do modelo sem tratamento específico, pois "
        "sua ausência está fortemente associada ao período e, por consequência, à temporada.\n")

    add("## 7. Duplicidades\n")
    add(f"Não foram encontradas linhas duplicadas ({carga['duplicadas']}), links duplicados ({int(bruto['link'].duplicated().sum())}) "
        f"nem combinações repetidas de data, mandante e visitante ({int(bruto.duplicated(['game_date', 'home_team', 'away_team']).sum())}). "
        "Nenhuma equipe aparece em duas partidas no mesmo instante.\n")

    add("## 8. Inconsistências encontradas\n")
    add(f"- **Gols × eventos:** {'não houve nenhuma divergência' if len(div) == 0 else f'houve {len(div)} divergências'} entre o placar e o número de eventos de gol "
        f"({mil(df['gols_eventos_mandante'].sum() + df['gols_eventos_visitante'].sum())} eventos contra {mil(df['total_gols'].sum())} gols no placar). "
        f"Foram registrados {int(df['gols_contra_mandante'].sum() + df['gols_contra_visitante'].sum())} gols contra, todos incluídos na lista da equipe que recebeu o gol, o que é coerente com o placar. "
        "Ainda assim, o placar registrado permanece como fonte principal do resultado e as listas não são usadas para corrigi-lo.")
    add(f"- **Segundo amarelo:** dos {int(ev.loc['segundos_amarelos'])} segundos amarelos, {int(ev.loc['segundo_amarelo_jogador_tambem_na_lista_de_amarelos'])} "
        f"têm o jogador também na lista de amarelos (o primeiro cartão) e {int(ev.loc['segundo_amarelo_mesmo_jogador_e_minuto_na_lista_de_amarelos'])} "
        "aparecem com o mesmo jogador e minuto na lista de amarelos, o que sugere que nesses casos o segundo amarelo também foi contado como amarelo. "
        "Como a duplicação é rara e não pode ser confirmada, `total_amarelos` foi mantido como a soma das listas, sem correção.")
    add(f"- **Eventos:** entre {mil(ev.loc['eventos'])} eventos verificados, nenhum tem minuto fora do formato, jogador vazio ou duplicidade dentro da mesma lista.")
    add(f"- **Público suspeito:** a partida de menor público é {pub_menor['home_team']} × {pub_menor['away_team']} ({_data_br(pub_menor['data_partida'])}), com {int(pub_menor['publico'])} pessoas. "
        f"Nas outras {len(estadio_menor)} partidas com público informado nesse estádio, o mínimo é {num(float(estadio_menor.min()), 0)} e a mediana {num(float(estadio_menor.median()), 0)}; o valor pode ser um erro de coleta, mas não há como confirmá-lo com os dados. Foi mantido e sinalizado.")
    add(f"- **Nomes de equipes:** sem espaços extras, sem variações do mesmo time e sem pares de nomes parecidos ({n_parecidos}). "
        "Os nomes são os oficiais completos (por exemplo, `Santos FC Sao Paulo`, `SC do Recife`); nos gráficos foram usados nomes curtos apenas para legibilidade.\n")

    add("## 9. Transformações realizadas\n")
    for item in [
        "Leitura do CSV como texto, para preservar marcadores como `No data`; o arquivo original não é alterado.",
        "Conversão de `game_date` para `datetime` com dicionário de meses em português (sem depender do idioma do sistema) e ordenação cronológica.",
        "Extração da temporada do `link` por expressão regular (`série-a-AAAA`), com verificação de que todas as linhas ficaram entre 2020 e 2023.",
        "Conversão de `public` para número (`12.089` → 12089) mantendo `No data` como ausente.",
        "Conversão segura das oito colunas JSON com `json.loads` (sem `eval`); conteúdo inválido viraria lista vazia e seria registrado.",
        "Criação da variável-alvo a partir do placar registrado.",
        "Criação de variáveis derivadas da partida e de médias históricas dos últimos cinco jogos (com `shift(1)`).",
    ]:
        add(f"- {item}")
    add("")

    add("## 10. Variáveis criadas\n")
    add(df_para_markdown(pd.DataFrame(DICIONARIO_COLUNAS_NOVAS, columns=["Coluna(s)", "Descrição"])))
    add("")
    add("**Significado das classes da variável-alvo** (definidas pelo placar registrado):\n")
    add(df_para_markdown(ctx["distribuicao"].rename(columns={"classe": "Classe", "significado": "Significado", "codigo": "Código", "partidas": "Partidas", "percentual": "%"}), casas=1))
    add("")

    add("## 11. Principais resultados da análise exploratória\n")
    add("### Distribuição geral\n")
    add(f"- Classes: vitória do mandante {pct(dist.loc['home_win', 'percentual'] / 100)}, empate {pct(dist.loc['draw', 'percentual'] / 100)} e vitória do visitante {pct(dist.loc['away_win', 'percentual'] / 100)}. "
        f"A classe majoritária representa {pct(dist['percentual'].max() / 100)} das partidas, valor de referência para qualquer modelo (um classificador que sempre prevê vitória do mandante acertaria essa proporção).")
    add(f"- Gols por partida: média {num(g['Gols por partida - média'])}, mediana {num(g['Gols por partida - mediana'], 0)}, mínimo {num(g['Gols por partida - mínimo'], 0)} e máximo {num(g['Gols por partida - máximo'], 0)}. "
        f"Média de {num(g['Gols dos mandantes - média'])} gols dos mandantes e {num(g['Gols dos visitantes - média'])} dos visitantes.")
    add(f"- {num(g['Partidas com ao menos 3 gols (%)'], 1)}% das partidas têm ao menos três gols; {num(g['Partidas com expulsão (%)'], 1)}% têm ao menos uma expulsão; "
        f"média de {num(g['Cartões amarelos por partida - média'])} amarelos e {num(g['Expulsões por partida - média'], 3)} expulsões por partida.")
    add(f"- {num(g['Partidas com pênalti convertido (%)'], 1)}% das partidas tiveram pênalti convertido e {num(g['Partidas com gol contra (%)'], 1)}% tiveram gol contra.\n")
    add("![Distribuição dos resultados](figures/01_distribuicao_resultados.png)\n")
    add("![Distribuição do total de gols](figures/08_distribuicao_total_gols.png)\n")

    add("### Por temporada\n")
    add(df_para_markdown(med.reset_index().rename(columns={
        "temporada": "Temporada", "partidas": "Partidas", "media_gols": "Gols/partida", "media_gols_mandante": "Gols mandante",
        "media_gols_visitante": "Gols visitante", "media_amarelos": "Amarelos/partida", "media_expulsoes": "Expulsões/partida",
        "pct_com_expulsao": "% com expulsão"})))
    add("")
    add(df_para_markdown(tp["resultados_pct"].reset_index().rename(columns={"temporada": "Temporada", "home_win": "% home_win", "draw": "% draw", "away_win": "% away_win"}), casas=1))
    add("")
    add(f"- A média de gols varia de {num(med['media_gols'].min())} ({med['media_gols'].idxmin()}) a {num(med['media_gols'].max())} ({med['media_gols'].idxmax()}); "
        f"o teste de Kruskal-Wallis não indica diferença estatisticamente significativa entre as temporadas ao nível de 5% (p = {_p(rel['kruskal_gols_temporada'])}).")
    add(f"- Os cartões amarelos por partida passam de {num(med.loc[2020, 'media_amarelos'])} em 2020 para {num(med.loc[2023, 'media_amarelos'])} em 2023, com diferença significativa entre as temporadas (Kruskal-Wallis, p {_p(kw_ap)}). "
        "Os dados não explicam a causa dessa mudança (por exemplo, critério de arbitragem ou coleta), então ela é registrada apenas como um fato observado.")
    add(f"- A distribuição dos resultados não difere significativamente entre as temporadas (qui-quadrado = {num(rel['chi2_resultado_temporada']['chi2'])}, p = {_p(rel['chi2_resultado_temporada']['p_valor'])}).")
    pt = tp["publico"]
    add(f"- Público (apenas partidas com informação): mediana de {num(float(pt.loc[2021, 'mediana']), 0)} em 2021 ({int(pt.loc[2021, 'disponiveis'])} partidas), "
        f"{num(float(pt.loc[2022, 'mediana']), 0)} em 2022 ({int(pt.loc[2022, 'disponiveis'])}) e {num(float(pt.loc[2023, 'mediana']), 0)} em 2023 ({int(pt.loc[2023, 'disponiveis'])}); "
        "2020 não tem nenhuma partida com público. Como 2021 contém sobretudo partidas de fim de temporada, as médias por temporada não são comparáveis entre si sem cuidado.\n")
    add(df_para_markdown(pt.reset_index().rename(columns={"temporada": "Temporada", "disponiveis": "Com público", "media": "Média", "mediana": "Mediana", "minimo": "Mínimo", "maximo": "Máximo"}), casas=0))
    add("")
    add("![Resultados por temporada](figures/02_resultados_por_temporada.png)\n")
    add("![Média de gols por temporada](figures/03_media_gols_temporada.png)\n")
    add("![Cartões por temporada](figures/04_cartoes_por_temporada.png)\n")
    add("![Público por temporada](figures/10_publico_por_temporada.png)\n")

    add("### Por equipe\n")
    add(f"Foram analisadas {len(equipes)} equipes; {n_times_4} disputaram as quatro temporadas. Como as equipes disputaram quantidades diferentes de jogos, rankings baseados em totais favorecem quem esteve em mais temporadas; "
        f"por isso as tabelas trazem o número de partidas, e os rankings de médias exigem no mínimo {MIN_PARTIDAS_RANKING} partidas (uma temporada completa).\n")
    nomes_rk = {"mais_vitorias": "Mais vitórias", "melhores_aproveitamentos": f"Melhores aproveitamentos (mín. {MIN_PARTIDAS_RANKING} jogos)",
                "maiores_medias_gols": f"Maiores médias de gols marcados (mín. {MIN_PARTIDAS_RANKING} jogos)", "melhores_saldos": "Melhores saldos de gols",
                "mais_amarelos": "Mais cartões amarelos", "mais_expulsoes": "Mais expulsões"}
    for chave, titulo in nomes_rk.items():
        add(f"**{titulo}**\n")
        tabela = rk[chave].head(5).copy()
        if "aproveitamento" in tabela:
            tabela["aproveitamento"] = tabela["aproveitamento"] * 100
            tabela = tabela.rename(columns={"aproveitamento": "aproveitamento (%)"})
        tabela = tabela.rename(columns={
            "equipe": "Equipe", "partidas": "Partidas", "vitorias": "Vitórias", "pontos": "Pontos",
            "gols_marcados": "Gols marcados", "gols_sofridos": "Gols sofridos", "saldo_gols": "Saldo de gols",
            "media_gols_marcados": "Gols marcados por jogo", "amarelos": "Amarelos", "media_amarelos": "Amarelos por jogo",
            "expulsoes": "Expulsões", "media_expulsoes": "Expulsões por jogo", "aproveitamento (%)": "Aproveitamento (%)"})
        add(df_para_markdown(tabela, casas=3 if chave == "mais_expulsoes" else 2))
        add("")
    add(f"Entre as equipes elegíveis, o maior aproveitamento é do {NOME_CURTO.get(lider_apr['equipe'], lider_apr['equipe'])} ({num(lider_apr['aproveitamento'] * 100, 1)}%), "
        f"e {n_casa_melhor} das {len(equipes)} equipes tiveram aproveitamento maior como mandante do que como visitante. "
        "Os totais (vitórias, cartões) favorecem as equipes que disputaram mais temporadas; por isso as colunas de média ou de partidas devem ser lidas junto.\n")
    add("A tabela completa por equipe (incluindo desempenho como mandante e visitante) está no notebook. "
        f"O aproveitamento dos mandantes foi de {pct(mando.loc['aproveitamento', 'mandante'])} e o dos visitantes de {pct(mando.loc['aproveitamento', 'visitante'])}.\n")
    add("![Times mais vitoriosos](figures/05_times_mais_vitoriosos.png)\n")
    add("![Maiores médias de gols](figures/06_times_maior_media_gols.png)\n")
    add("![Times com mais cartões](figures/07_times_mais_cartoes.png)\n")

    add("### Relações entre variáveis\n")
    add("As relações abaixo são descritivas. Correlação ou associação não implica causalidade.\n")
    add(f"- **Mando de campo:** {int(mando.loc['vitórias', 'mandante'])} vitórias de mandantes contra {int(mando.loc['vitórias', 'visitante'])} de visitantes "
        f"(teste binomial entre partidas com vencedor, p {_p(rel['teste_mando']['p_valor'])}). Mandantes marcam em média {num(g['Gols dos mandantes - média'])} gols contra {num(g['Gols dos visitantes - média'])} dos visitantes.")
    add("- **Gols e resultado:** o resultado é definido pelo próprio placar, então a relação é uma consequência direta e não uma descoberta; ela serve apenas para descrever as classes.\n")
    add(df_para_markdown(rel["gols_por_resultado"].reset_index().rename(columns={"resultado": "Resultado", "home_team_score": "Gols mandante", "away_team_score": "Gols visitante", "total_gols": "Total de gols"})))
    add("")
    add("- **Cartões amarelos e resultado:** as médias por classe ficam próximas; o total de amarelos é um pouco menor nas vitórias do mandante.\n")
    add(df_para_markdown(rel["amarelos_por_resultado"].reset_index().rename(columns={"resultado": "Resultado", "amarelos_mandante": "Amarelos mandante", "amarelos_visitante": "Amarelos visitante", "total_amarelos": "Total"})))
    add("")
    add(f"- **Expulsões e resultado:** quando só o mandante teve jogador expulso, o mandante venceu em {num(exp.loc['Expulsão apenas do mandante', 'home_win (%)'], 1)}% das {int(exp.loc['Expulsão apenas do mandante', 'partidas'])} partidas; "
        f"quando só o visitante teve expulsão, o mandante venceu em {num(exp.loc['Expulsão apenas do visitante', 'home_win (%)'], 1)}% das {int(exp.loc['Expulsão apenas do visitante', 'partidas'])}; "
        f"sem expulsões, {num(exp.loc['Sem expulsão na partida', 'home_win (%)'], 1)}% das {int(exp.loc['Sem expulsão na partida', 'partidas'])}. "
        "A base não informa em que momento o placar estava quando ocorreu cada expulsão; portanto não é possível separar o efeito da expulsão da situação de jogo que a antecedeu.\n")
    add(df_para_markdown(rel["expulsoes_resultado"], casas=1))
    add("")
    add(f"- **Público e gols:** correlação de Spearman de {num(rel['publico_gols']['rho'], 3)} (n = {rel['publico_gols']['n']}, p = {_p(rel['publico_gols']['p_valor'])}); não há evidência de relação linear/monotônica relevante.")
    pr = rel["publico_por_resultado"]
    add(f"- **Público e resultado:** a mediana do público é {num(float(pr.loc['home_win', 'median']), 0)} nas vitórias do mandante, {num(float(pr.loc['draw', 'median']), 0)} nos empates e {num(float(pr.loc['away_win', 'median']), 0)} nas vitórias do visitante "
        f"(Kruskal-Wallis p = {_p(rel['kruskal_publico_resultado'])}). Como o público depende do mandante (equipes com maior torcida têm mais público e também vencem mais em casa) e da temporada, essa associação não deve ser interpretada como causal.\n")
    add("![Mando de campo e resultado](figures/09_mando_campo_resultado.png)\n")
    add("![Correlação entre variáveis](figures/13_correlacao_variaveis.png)\n")

    add("### Valores extremos (outliers)\n")
    add("Os valores extremos foram examinados pelo intervalo interquartil (IQR) e por inspeção das linhas. **Nenhum valor foi removido.**\n")
    add(df_para_markdown(out["iqr"], casas=1))
    add("")
    mp, ma, me = out["maiores_placares"].iloc[0], out["mais_amarelos"].iloc[0], out["mais_expulsoes"].iloc[0]
    add(f"- **Placares altos:** o maior total é {int(mp['total_gols'])} gols ({mp['home_team']} {int(mp['home_team_score'])} × {int(mp['away_team_score'])} {mp['away_team']}, {_data_br(mp['data_partida'])}). "
        "Nos placares mais altos o número de eventos de gol coincide com o placar, o que sustenta que são jogos reais e não erros de coleta.")
    add(f"- **Cartões:** o máximo é {int(ma['total_amarelos'])} amarelos em uma partida ({ma['home_team']} × {ma['away_team']}, {_data_br(ma['data_partida'])}).")
    add(f"- **Expulsões:** como Q1 = Q3 = 0, o critério do IQR marca qualquer partida com expulsão como outlier, o que não é informativo para uma variável de contagem com muitos zeros; foi usada a inspeção direta. "
        f"O máximo é {int(me['total_expulsoes'])} expulsões em uma partida ({me['home_team']} × {me['away_team']}, {_data_br(me['data_partida'])}), com eventos registrados nas listas.")
    add(f"- **Público:** nenhum valor fora dos limites do IQR; o menor ({int(pub_menor['publico'])}) foi sinalizado como possível erro de coleta.")
    add("- **Decisão:** valores extremos consistentes com as listas de eventos são tratados como eventos reais e mantidos; a checagem externa não foi feita.\n")
    add("![Boxplots](figures/11_boxplots_outliers.png)\n")

    add("## 12. Gráficos mais relevantes\n")
    add("Os dez gráficos obrigatórios foram gerados em `reports/figures/` (150 DPI), além de três complementares (`11_boxplots_outliers.png`, `12_publico_ausente_por_mes.png`, `13_correlacao_variaveis.png`). "
        "Os mais relevantes para o relatório são: `01_distribuicao_resultados.png` (classes e linha de base), `02_resultados_por_temporada.png` (estabilidade entre temporadas), "
        "`09_mando_campo_resultado.png` (vantagem do mandante) e `10_publico_por_temporada.png` / `12_publico_ausente_por_mes.png` (qualidade da variável de público).\n")

    add("## 13. Preparação para Machine Learning\n")
    add(f"**Base utilizável:** {mil(n_util)} das {mil(res['linhas'])} partidas têm histórico de ao menos {JANELA} jogos anteriores para as duas equipes; "
        f"{n_desc} foram marcadas como não utilizáveis (`utilizavel_ml = 0`) e permanecem no arquivo para rastreabilidade.")
    add("")
    add(df_para_markdown(desc_temp.reset_index().rename(columns={"temporada": "Temporada", "utilizaveis": "Utilizáveis", "total": "Total", "descartadas": "Sem histórico suficiente"})))
    add("")
    add("**Distribuição da variável-alvo:**\n")
    comp = pd.DataFrame({"Classe": CLASSES, "Base completa": res["alvo_completo"].values, "Base utilizável": res["alvo_utilizavel"].values})
    comp["% completa"] = comp["Base completa"] / comp["Base completa"].sum() * 100
    comp["% utilizável"] = comp["Base utilizável"] / comp["Base utilizável"].sum() * 100
    add(df_para_markdown(comp, casas=1))
    add("")
    add("**Variáveis históricas.** Para cada partida foram calculadas, separadamente para mandante e visitante, as métricas dos cinco jogos anteriores da equipe "
        "(pontos médios, vitórias, empates, derrotas, gols marcados e sofridos, saldo, amarelos, expulsões e aproveitamento), além do aproveitamento do mandante em casa e do visitante fora. "
        "As regras adotadas foram:\n")
    for item in [
        "As partidas são ordenadas cronologicamente e cada equipe é seguida em ordem de data, independentemente de jogar como mandante ou visitante.",
        "Usa-se `shift(1)` antes da média móvel; a partida atual nunca entra no próprio histórico.",
        f"**Equipes com menos de {JANELA} jogos anteriores:** o histórico fica ausente (NaN). Não há preenchimento com zero, com a média geral ou com informação futura. A partida é marcada com `utilizavel_ml = 0` e deve ser excluída do treino ou tratada com imputação ajustada somente nos dados de treino.",
        f"O histórico atravessa temporadas consecutivas (o primeiro jogo de 2021 usa os últimos jogos de 2020), mas **é reiniciado quando a equipe ficou ao menos uma temporada inteira fora da base**: "
        f"{n_lacunas} equipes têm essa lacuna (por exemplo, {exemplo_lacuna}), e usar jogos de anos antes como \"últimos 5 jogos\" descreveria mal a equipe atual. "
        f"Essa escolha mantém {mil(n_util)} partidas utilizáveis; reiniciando o histórico a cada temporada seriam {mil(ctx['utilizaveis_reiniciando_por_temporada'])}. "
        "O custo restante é que o elenco muda entre temporadas consecutivas.",
        f"O aproveitamento em casa/fora usa os últimos {JANELA} jogos no mesmo mando, com no mínimo {MIN_JOGOS_CONTEXTO} jogos; abaixo disso fica ausente.",
    ]:
        add(f"- {item}")
    add("")
    add("**Testes contra vazamento temporal** (executados automaticamente):\n")
    add(df_para_markdown(ctx["vazamento"].assign(aprovado=lambda d: d["aprovado"].map({True: "sim", False: "não"}))))
    add("")

    add("## 14. Riscos de vazamento de dados\n")
    add("Informações que só existem depois da partida não podem ser entradas do modelo para prever essa mesma partida. As colunas abaixo são **proibidas como variáveis de entrada**:\n")
    add("`" + "`, `".join(COLUNAS_PROIBIDAS_OBRIGATORIAS) + "`\n")
    add("Pelo mesmo motivo, as colunas derivadas criadas nesta etapa a partir dos eventos da própria partida também são proibidas: `" + "`, `".join(COLUNAS_PROIBIDAS_ADICIONAIS) + "`. "
        "O `publico` entra na lista porque só é conhecido no dia do jogo e tem forte ausência no início do período.\n")
    add("Essas colunas podem ser usadas apenas para construir o histórico das equipes, considerando somente partidas anteriores à que está sendo prevista. "
        f"Colunas conhecidas antes do jogo e candidatas a entrada: equipes, `temporada`, `mes`, `dia_semana`, `hora`, estádio, árbitro e as {len(COLUNAS_HISTORICAS)} colunas históricas. "
        "Ao dividir os dados em treino e teste, a divisão deve ser cronológica (não aleatória), para que o teste represente o uso real do modelo.\n")

    add("## 15. Limitações do dataset\n")
    for item in [
        f"**Temporada × ano:** {fora_ano} partidas ({pct(fora_ano / len(df))}) foram disputadas em ano diferente da temporada (todas da temporada 2020, disputadas em 2021); a temporada precisa vir do link.",
        f"**Público:** {pct(n_ausente / len(df))} das partidas não têm público e a ausência depende do período (seção 6); não foi imputado.",
        "**Pandemia:** 2020 e parte de 2021 foram disputados em período de restrições; o comportamento das equipes, do público e das partidas pode não ser comparável ao de 2022–2023. Isso é uma hipótese de contexto, não algo medido por esta base.",
        f"**Gols × eventos:** {'nenhuma divergência foi encontrada' if len(div) == 0 else f'{len(div)} divergências foram encontradas'}; a qualidade das listas de cartões não pôde ser verificada contra uma fonte externa.",
        "**Nomenclatura:** os nomes estão padronizados neste arquivo, mas são nomes oficiais longos; uma eventual integração com outra fonte exigirá um dicionário de equivalência.",
        "**Informações ausentes:** a base não traz escalação, lesões e suspensões, posição na tabela antes do jogo, condição climática, viagem/descanso entre jogos ou odds; a posição na tabela e o descanso podem ser derivados do histórico em etapas futuras.",
        f"**Poucas temporadas:** apenas {len(TEMPORADAS)} temporadas; {n_times_4} das {len(equipes)} equipes disputaram todas. Equipes com uma única temporada têm pouco histórico e estatísticas menos estáveis.",
        f"**Mudança entre temporadas:** o aproveitamento de uma mesma equipe varia entre temporadas; entre as equipes presentes nas quatro, a maior amplitude foi de {num(float(top_amp['amplitude']) * 100, 1)} pontos percentuais ({amp.index[0]}). Médias de quatro anos escondem essa variação.",
        f"**Imprevisibilidade:** mesmo com boas variáveis, o futebol tem grande componente aleatório (média de {num(g['Gols por partida - média'])} gols por jogo e {pct(dist['percentual'].max() / 100)} de vitórias do mandante como referência); é razoável esperar acurácia modesta e comparar o modelo com essa linha de base.",
    ]:
        add(f"- {item}")
    add("")

    add("## 16. Decisões tomadas e suas justificativas\n")
    decisoes = pd.DataFrame([
        ("Manter o CSV original intacto", "Garantir rastreabilidade; toda transformação é reproduzida pelo código."),
        ("Ler tudo como texto", "Evitar que o Pandas converta `No data` ou altere formatos silenciosamente."),
        ("Temporada extraída do link", "O ano da data não identifica a temporada (2020 terminou em 2021)."),
        ("Público ausente mantido como NaN", "`No data` não é zero; imputar criaria informação inexistente."),
        ("Placar como fonte do resultado", "As listas de eventos não devem corrigir o placar; a divergência é documentada, e neste arquivo não houve nenhuma."),
        ("Nenhum outlier removido", "Valores extremos verificados são coerentes com as listas de eventos; podem ser eventos reais."),
        ("Expulsões = vermelhos diretos + segundos amarelos", "Definição solicitada; o segundo amarelo pode aparecer também na lista de amarelos em poucos casos (seção 8)."),
        ("Histórico com `shift(1)` e janela de 5 jogos", "Impede que a partida atual entre em suas próprias médias."),
        ("Histórico ausente com menos de 5 jogos", "Evita preencher com zeros ou dados futuros; as partidas ficam sinalizadas."),
        ("Histórico contínuo entre temporadas", "Preserva mais partidas utilizáveis; a alternativa é reiniciar por temporada (parâmetro `reiniciar_por_temporada`)."),
        ("Rankings de médias com mínimo de 38 jogos", "Uma temporada completa reduz a instabilidade de médias em poucos jogos."),
        ("Colunas JSON brutas fora do arquivo processado", "Mantêm-se no CSV original; na base processada ficam apenas as contagens extraídas."),
    ], columns=["Decisão", "Justificativa"])
    add(df_para_markdown(decisoes))
    add("")

    add("## Validações automáticas\n")
    add(df_para_markdown(ctx["validacoes"].assign(aprovada=lambda d: d["aprovada"].map({True: "sim", False: "não"}))))
    add("")
    add(f"*Semente aleatória fixa: `RANDOM_STATE = {RANDOM_STATE}` (usada apenas no teste de perturbação do futuro).*\n")
    return "\n".join(L)


def main() -> None:
    ctx = executar_analise(salvar=True)
    res = ctx["resumo_final"]
    print("\n" + "=" * 70)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 70)
    print(f"Partidas processadas: {res['linhas']} | colunas: {res['colunas']}")
    print(f"Partidas utilizáveis para ML: {res['utilizaveis']} | sem histórico suficiente: {res['descartadas']}")
    print("Distribuição da variável-alvo:")
    print(ctx["distribuicao"][["classe", "partidas", "percentual"]].round(2).to_string(index=False))
    print(f"Validações aprovadas: {int(ctx['validacoes']['aprovada'].sum())}/{len(ctx['validacoes'])}")


if __name__ == "__main__":
    main()
