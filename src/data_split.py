"""Divisão de dados temporal e preparação de features para modelagem preditiva.

Este módulo implementa a estratégia experimental descrita em `reports/estrategia_experimental.md`:
- Divisão estritamente temporal em Treino (2020-2021), Validação (2022) e Teste (2023).
- Validação temporal em janela expansiva (Walk-Forward / TimeSeriesSplit).
- Definição rigorosa de features pré-jogo, eliminando qualquer vazamento temporal (data leakage).
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Sequence

# Garante que a raiz do repositório esteja no sys.path
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

import numpy as np
import pandas as pd

logger = logging.getLogger("data_split")

# --------------------------------------------------------------------------- #
# Constantes e Metadados do Problema
# --------------------------------------------------------------------------- #
RANDOM_STATE = 42
CLASSES = ["home_win", "draw", "away_win"]
CODIGO_RESULTADO = {"home_win": 0, "draw": 1, "away_win": 2}
ROTULO_RESULTADO = {
    "home_win": "Vitória do mandante",
    "draw": "Empate",
    "away_win": "Vitória do visitante",
}

CSV_PROCESSADO_PADRAO = RAIZ_PROJETO / "data" / "processed" / "partidas_processadas.csv"

# Colunas proibidas: descrevem eventos que ocorrem durante ou após o apito inicial
COLUNAS_PROIBIDAS = {
    "home_team_score", "away_team_score", "gols_home", "gols_away",
    "yellow_cards_home", "yellow_cards_away", "red_cards_home", "red_cards_away",
    "sec_card_home", "sec_card_away", "total_gols", "total_amarelos",
    "total_expulsoes", "resultado", "resultado_codigo",
    "gols_eventos_mandante", "gols_eventos_visitante",
    "amarelos_mandante", "amarelos_visitante",
    "vermelhos_diretos_mandante", "vermelhos_diretos_visitante",
    "segundos_amarelos_mandante", "segundos_amarelos_visitante",
    "expulsoes_mandante", "expulsoes_visitante",
    "penaltis_convertidos_mandante", "penaltis_convertidos_visitante",
    "gols_contra_mandante", "gols_contra_visitante",
    "saldo_gols_mandante", "teve_expulsao", "teve_penalti_convertido",
    "teve_gol_contra", "publico", "public",
}

# Identificadores e metadados que não devem entrar como features preditivas diretas
COLUNAS_METADADOS = {
    "id_partida", "id_partida_fonte", "link", "game_date", "data_partida",
    "ano_calendario", "utilizavel_ml",
}

# Variáveis numéricas históricas individuais (últimos 5 jogos calculados com shift(1))
FEATURES_HISTORICAS_BASE = [
    "pontos_media_ultimos_5",
    "vitorias_ultimos_5",
    "empates_ultimos_5",
    "derrotas_ultimos_5",
    "gols_marcados_media_ultimos_5",
    "gols_sofridos_media_ultimos_5",
    "saldo_gols_media_ultimos_5",
    "amarelos_media_ultimos_5",
    "expulsoes_media_ultimos_5",
    "aproveitamento_ultimos_5",
]

FEATURES_NUMERICAS_INDIVIDUAIS = (
    [f"{f}_mandante" for f in FEATURES_HISTORICAS_BASE]
    + [f"{f}_visitante" for f in FEATURES_HISTORICAS_BASE]
    + ["aproveitamento_mandante_em_casa", "aproveitamento_visitante_fora"]
)

FEATURES_CATEGORICAS = ["home_team", "away_team", "dia_semana"]
FEATURES_CALENDARIO = ["mes", "hora"]



@dataclass
class ParticoesDados:
    """Estrutura contendo os conjuntos divididos cronologicamente."""
    X_train: pd.DataFrame
    y_train: pd.Series
    X_val: pd.DataFrame
    y_val: pd.Series
    X_test: pd.DataFrame
    y_test: pd.Series
    X_train_val: pd.DataFrame
    y_train_val: pd.Series
    df_train: pd.DataFrame
    df_val: pd.DataFrame
    df_test: pd.DataFrame
    df_train_val: pd.DataFrame
    features_numericas: list[str]
    features_categoricas: list[str]


def criar_features_diferenciais(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Cria variáveis que capturam a diferença de momento e qualidade entre mandante e visitante.
    
    Todas as variáveis derivam unicamente das métricas históricas pré-jogo (sem vazamento).
    """
    df = df.copy()
    diff_cols = []

    # Diferença de pontos médios nos últimos 5 jogos
    df["dif_pontos_media_ultimos_5"] = (
        df["pontos_media_ultimos_5_mandante"] - df["pontos_media_ultimos_5_visitante"]
    )
    diff_cols.append("dif_pontos_media_ultimos_5")

    # Diferença de saldo de gols médio
    df["dif_saldo_gols_media_ultimos_5"] = (
        df["saldo_gols_media_ultimos_5_mandante"] - df["saldo_gols_media_ultimos_5_visitante"]
    )
    diff_cols.append("dif_saldo_gols_media_ultimos_5")

    # Diferença de gols marcados médios
    df["dif_gols_marcados_media_ultimos_5"] = (
        df["gols_marcados_media_ultimos_5_mandante"] - df["gols_marcados_media_ultimos_5_visitante"]
    )
    diff_cols.append("dif_gols_marcados_media_ultimos_5")

    # Diferença de gols sofridos médios (inverso: mandante sofre menos)
    df["dif_gols_sofridos_media_ultimos_5"] = (
        df["gols_sofridos_media_ultimos_5_mandante"] - df["gols_sofridos_media_ultimos_5_visitante"]
    )
    diff_cols.append("dif_gols_sofridos_media_ultimos_5")

    # Diferença de aproveitamento geral
    df["dif_aproveitamento_ultimos_5"] = (
        df["aproveitamento_ultimos_5_mandante"] - df["aproveitamento_ultimos_5_visitante"]
    )
    diff_cols.append("dif_aproveitamento_ultimos_5")

    # Diferença de aproveitamento de mando (mandante em casa vs visitante fora)
    df["dif_aproveitamento_mando"] = (
        df["aproveitamento_mandante_em_casa"] - df["aproveitamento_visitante_fora"]
    )
    diff_cols.append("dif_aproveitamento_mando")

    # Expectativa de gols na partida (soma de gols pró e contra das equipes)
    df["expectativa_total_gols_ultimos_5"] = (
        df["gols_marcados_media_ultimos_5_mandante"] + df["gols_sofridos_media_ultimos_5_visitante"]
    )
    diff_cols.append("expectativa_total_gols_ultimos_5")

    return df, diff_cols


def validar_sem_vazamento(colunas_features: Sequence[str]) -> None:
    """Verifica se nenhuma coluna proibida ou pós-jogo vazou para o conjunto de features."""
    intersecao = set(colunas_features).intersection(COLUNAS_PROIBIDAS)
    if intersecao:
        raise ValueError(
            f"Vazamento de dados detectado! As seguintes colunas proibidas estão nas features: {sorted(intersecao)}"
        )


def carregar_e_dividir_dados(
    caminho_csv: Path | str = CSV_PROCESSADO_PADRAO,
    apenas_utilizaveis: bool = True,
    incluir_diferenciais: bool = True,
) -> ParticoesDados:
    """Carrega a base processada e executa a partição estritamente cronológica.
    
    Partições:
    - Treino: Temporadas 2020 e 2021
    - Validação: Temporada 2022
    - Teste: Temporada 2023
    """
    df = pd.read_csv(caminho_csv)

    # Filtrar apenas partidas elegíveis para modelagem confiável (histórico >= 5)
    if apenas_utilizaveis:
        df = df[df["utilizavel_ml"] == 1].copy()

    # Garantir ordenação cronológica
    if "data_partida" in df.columns:
        df = df.sort_values("data_partida").reset_index(drop=True)

    features_numericas = list(FEATURES_NUMERICAS_INDIVIDUAIS) + list(FEATURES_CALENDARIO)
    if incluir_diferenciais:
        df, diff_cols = criar_features_diferenciais(df)
        features_numericas.extend(diff_cols)

    features_categoricas = list(FEATURES_CATEGORICAS)
    todas_features = features_numericas + features_categoricas

    # Auditoria de segurança contra vazamento
    validar_sem_vazamento(todas_features)

    # Partições temporais
    mask_train = df["temporada"].isin([2020, 2021])
    mask_val = df["temporada"] == 2022
    mask_test = df["temporada"] == 2023

    df_train = df[mask_train].copy().reset_index(drop=True)
    df_val = df[mask_val].copy().reset_index(drop=True)
    df_test = df[mask_test].copy().reset_index(drop=True)
    df_train_val = df[mask_train | mask_val].copy().reset_index(drop=True)

    X_train = df_train[todas_features].copy()
    y_train = df_train["resultado_codigo"].astype(int).copy()

    X_val = df_val[todas_features].copy()
    y_val = df_val["resultado_codigo"].astype(int).copy()

    X_test = df_test[todas_features].copy()
    y_test = df_test["resultado_codigo"].astype(int).copy()

    X_train_val = df_train_val[todas_features].copy()
    y_train_val = df_train_val["resultado_codigo"].astype(int).copy()

    return ParticoesDados(
        X_train=X_train,
        y_train=y_train,
        X_val=X_val,
        y_val=y_val,
        X_test=X_test,
        y_test=y_test,
        X_train_val=X_train_val,
        y_train_val=y_train_val,
        df_train=df_train,
        df_val=df_val,
        df_test=df_test,
        df_train_val=df_train_val,
        features_numericas=features_numericas,
        features_categoricas=features_categoricas,
    )


def obter_folds_walk_forward(df_train_val: pd.DataFrame) -> Generator[tuple[np.ndarray, np.ndarray], None, None]:
    """Gera índices para validação cruzada temporal progressiva (Walk-Forward / Expanding Window).
    
    Fold 1: Treino em 2020 -> Validação em 2021
    Fold 2: Treino em 2020 e 2021 -> Validação em 2022
    """
    temporadas = df_train_val["temporada"].to_numpy()

    # Fold 1
    idx_train_1 = np.where(temporadas == 2020)[0]
    idx_val_1 = np.where(temporadas == 2021)[0]
    yield idx_train_1, idx_val_1

    # Fold 2
    idx_train_2 = np.where(np.isin(temporadas, [2020, 2021]))[0]
    idx_val_2 = np.where(temporadas == 2022)[0]
    yield idx_train_2, idx_val_2


def relatorio_particoes(particoes: ParticoesDados) -> str:
    """Gera um resumo detalhado em texto das partições."""
    linhas = [
        "============================================================",
        "          AUDITORIA DE DIVISÃO TEMPORAL DOS DADOS           ",
        "============================================================",
        f"Features Totais: {len(particoes.features_numericas) + len(particoes.features_categoricas)}",
        f"  - Numéricas:   {len(particoes.features_numericas)}",
        f"  - Categóricas: {len(particoes.features_categoricas)}",
        "------------------------------------------------------------",
        f"Treino (2020-2021):     {len(particoes.X_train):>5} partidas",
        f"Validação (2022):       {len(particoes.X_val):>5} partidas",
        f"Teste (2023):           {len(particoes.X_test):>5} partidas",
        f"Total Utilizável:       {len(particoes.X_train) + len(particoes.X_val) + len(particoes.X_test):>5} partidas",
        "------------------------------------------------------------",
        "Distribuição de Classes nas Partições:",
    ]

    for nome, y in [("Treino", particoes.y_train), ("Validação", particoes.y_val), ("Teste", particoes.y_test)]:
        vc = y.value_counts().sort_index()
        total = len(y)
        hw = vc.get(0, 0)
        dr = vc.get(1, 0)
        aw = vc.get(2, 0)
        linhas.append(
            f"  {nome:<10}: Home Win: {hw:>3} ({hw/total*100:5.2f}%) | "
            f"Draw: {dr:>3} ({dr/total*100:5.2f}%) | "
            f"Away Win: {aw:>3} ({aw/total*100:5.2f}%)"
        )
    linhas.append("============================================================")
    return "\n".join(linhas)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    particoes = carregar_e_dividir_dados()
    print(relatorio_particoes(particoes))
    print("\n[OK] Validação de features concluída: 0 colunas proibidas encontradas.")
