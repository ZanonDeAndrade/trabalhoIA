"""Serviço de previsão: carrega o modelo salvo e calcula os atributos pré-jogo de um confronto.

Os atributos de histórico são calculados com **o mesmo código do treinamento**
(``src.data_analysis.adicionar_historico``) sobre as partidas anteriores à data de referência:
o confronto consultado entra na tabela como uma linha sem placar, cuja própria informação nunca
participa das médias móveis (``shift(1)``). Assim, o modelo recebe na API exatamente o mesmo tipo
de entrada que recebeu no treino.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import sklearn

from src.common import CatalogoEquipes, ErroApi
from src.data_analysis import DIAS_SEMANA, JANELA, adicionar_historico
from src.data_split import CLASSES, ROTULO_RESULTADO, criar_features_diferenciais
from src.evaluation import rotulo_atributo

logger = logging.getLogger("predictor")

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO_MODELO = RAIZ / "models" / "model.joblib"
ARQUIVO_METADADOS = RAIZ / "models" / "metadata.json"

HORA_PADRAO = 16
JANELA_FUTURO_DIAS = 60  # datas de referência aceitas depois do último jogo da base
MAX_DIAS_SEM_JOGO = 200  # maior intervalo aceito desde o último jogo (a entressafra tem ~155 dias)
ID_HIPOTETICO = 10**9

METRICAS_GERAIS = [
    "pontos_media_ultimos_5", "vitorias_ultimos_5", "empates_ultimos_5", "derrotas_ultimos_5",
    "gols_marcados_media_ultimos_5", "gols_sofridos_media_ultimos_5", "saldo_gols_media_ultimos_5",
    "amarelos_media_ultimos_5", "expulsoes_media_ultimos_5", "aproveitamento_ultimos_5",
]


class ServicoPrevisao:
    def __init__(
        self,
        partidas: pd.DataFrame,
        catalogo: CatalogoEquipes,
        caminho_modelo: Path = ARQUIVO_MODELO,
        caminho_metadados: Path = ARQUIVO_METADADOS,
    ):
        self.df = partidas
        self.catalogo = catalogo
        self.modelo = None
        self.metadados: dict[str, Any] | None = None
        self.avisos: list[str] = []
        self.primeira_data = partidas["data_partida"].min()
        self.ultima_data = partidas["data_partida"].max()
        self._carregar_modelo(Path(caminho_modelo), Path(caminho_metadados))

    # ------------------------------------------------------------------ #
    def _carregar_modelo(self, caminho_modelo: Path, caminho_metadados: Path) -> None:
        if not caminho_modelo.exists() or not caminho_metadados.exists():
            self.avisos.append("Modelo não encontrado. Execute `python src/modeling.py`.")
            logger.warning(self.avisos[-1])
            return
        self.metadados = json.loads(caminho_metadados.read_text(encoding="utf-8"))
        self.modelo = joblib.load(caminho_modelo)
        versao_treino = self.metadados.get("dependencias", {}).get("scikit_learn")
        if versao_treino and versao_treino != sklearn.__version__:
            aviso = f"scikit-learn {sklearn.__version__} difere da versão do treino ({versao_treino})."
            self.avisos.append(aviso)
            logger.warning(aviso)
        self.colunas_entrada: list[str] = self.metadados["colunas_entrada"]

    @property
    def modelo_carregado(self) -> bool:
        return self.modelo is not None

    # ------------------------------------------------------------------ #
    # Datas de referência e elegibilidade
    # ------------------------------------------------------------------ #
    @property
    def referencia_padrao(self) -> datetime:
        return (self.ultima_data.normalize() + timedelta(days=1)).to_pydatetime().replace(hour=HORA_PADRAO)

    @property
    def limites_referencia(self) -> tuple[date, date]:
        return self.primeira_data.date(), (self.ultima_data + timedelta(days=JANELA_FUTURO_DIAS)).date()

    def resolver_referencia(self, data: object = None, hora: object = None) -> tuple[datetime, str]:
        """Valida data (AAAA-MM-DD) e hora (0-23) opcionais; devolve o instante e a origem."""
        origem = "padrao"
        if data is None and hora is None:
            return self.referencia_padrao, origem
        try:
            dia = datetime.strptime(str(data), "%Y-%m-%d").date() if data is not None else self.referencia_padrao.date()
        except ValueError:
            raise ErroApi(400, "data_invalida", "Data inválida. Use o formato AAAA-MM-DD.") from None
        try:
            h = HORA_PADRAO if hora is None else int(hora)
            if isinstance(hora, bool) or not 0 <= h <= 23:
                raise ValueError
        except (TypeError, ValueError):
            raise ErroApi(400, "hora_invalida", "Hora inválida. Informe um inteiro de 0 a 23.") from None
        minimo, maximo = self.limites_referencia
        if not minimo < dia <= maximo:
            raise ErroApi(
                422,
                "data_fora_da_base",
                f"A data de referência deve estar entre {minimo.strftime('%d/%m/%Y')} (exclusive) e "
                f"{maximo.strftime('%d/%m/%Y')}: a base cobre partidas de {minimo.strftime('%d/%m/%Y')} "
                f"a {self.ultima_data.strftime('%d/%m/%Y')}.",
            )
        return datetime(dia.year, dia.month, dia.day, h), "usuario"

    def _anteriores(self, referencia: datetime) -> pd.DataFrame:
        return self.df[self.df["data_partida"] < pd.Timestamp(referencia)]

    def elegibilidade(self, oficial: str, referencia: datetime) -> dict[str, Any]:
        """Equipe prevista com ao menos ``JANELA`` jogos e sem longo afastamento antes da data de referência."""
        anteriores = self._anteriores(referencia)
        jogos = anteriores[(anteriores["home_team"] == oficial) | (anteriores["away_team"] == oficial)]
        n = len(jogos)
        if n < JANELA:
            return {"eligible": False, "matches_before": n,
                    "reason": f"Apenas {n} jogo(s) anterior(es) na base; são necessários {JANELA}."}
        dias = (pd.Timestamp(referencia) - jogos["data_partida"].max()).days
        if dias > MAX_DIAS_SEM_JOGO:
            return {"eligible": False, "matches_before": n,
                    "reason": f"Sem jogos há {dias} dias na base; o histórico está desatualizado."}
        return {"eligible": True, "matches_before": n, "reason": None}

    def equipes(self) -> list[dict[str, Any]]:
        ref = self.referencia_padrao
        saida = []
        for e in self.catalogo.equipes:
            saida.append({**e, **self.elegibilidade(e["official_name"], ref)})
        return saida

    # ------------------------------------------------------------------ #
    # Atributos pré-jogo
    # ------------------------------------------------------------------ #
    def atributos_confronto(self, mandante: str, visitante: str, referencia: datetime) -> pd.DataFrame:
        """Uma linha com todas as colunas de entrada do modelo, usando só jogos anteriores a ``referencia``."""
        anteriores = self._anteriores(referencia)
        if anteriores.empty:
            raise ErroApi(422, "sem_historico", "Não há partidas anteriores à data escolhida.")
        temporada = int(anteriores["temporada"].max())
        for oficial in (mandante, visitante):
            el = self.elegibilidade(oficial, referencia)
            if not el["eligible"]:
                raise ErroApi(422, "historico_insuficiente", f"{self.catalogo.nome_curto(oficial)}: {el['reason']}")

        recorte = anteriores[
            anteriores["home_team"].isin([mandante, visitante]) | anteriores["away_team"].isin([mandante, visitante])
        ].copy()
        hipotetica = {c: np.nan for c in recorte.columns}
        hipotetica.update(
            id_partida=ID_HIPOTETICO, temporada=temporada, data_partida=pd.Timestamp(referencia),
            home_team=mandante, away_team=visitante,
        )
        tabela = pd.concat([recorte, pd.DataFrame([hipotetica])], ignore_index=True)
        tabela["data_partida"] = pd.to_datetime(tabela["data_partida"])
        com_historico = adicionar_historico(tabela)
        linha = com_historico[com_historico["id_partida"] == ID_HIPOTETICO].copy()

        for lado, oficial in (("mandante", mandante), ("visitante", visitante)):
            gerais = [f"{m}_{lado}" for m in METRICAS_GERAIS]
            if linha[gerais].isna().any(axis=1).iloc[0]:
                fase = int(linha[f"jogos_anteriores_{lado}"].iloc[0])
                raise ErroApi(
                    422, "historico_insuficiente",
                    f"{self.catalogo.nome_curto(oficial)}: apenas {fase} jogo(s) na fase atual da base "
                    f"(o histórico reinicia após uma temporada inteira sem jogos); são necessários {JANELA}.",
                )

        linha["mes"] = referencia.month
        linha["hora"] = referencia.hour
        linha["dia_semana"] = DIAS_SEMANA[referencia.weekday()]
        linha, _ = criar_features_diferenciais(linha)
        return linha[self.colunas_entrada].reset_index(drop=True)

    # ------------------------------------------------------------------ #
    # Componentes da resposta
    # ------------------------------------------------------------------ #
    def _sequencia(self, oficial: str, referencia: datetime) -> list[str]:
        anteriores = self._anteriores(referencia)
        jogos = anteriores[(anteriores["home_team"] == oficial) | (anteriores["away_team"] == oficial)].tail(JANELA)
        sequencia = []
        for _, j in jogos.iterrows():
            gp, gc = (j["home_team_score"], j["away_team_score"]) if j["home_team"] == oficial else (j["away_team_score"], j["home_team_score"])
            sequencia.append("V" if gp > gc else "E" if gp == gc else "D")
        return sequencia

    def _forma(self, oficial: str, lado: str, atributos: pd.Series, referencia: datetime) -> dict[str, Any]:
        return {
            "last_five": self._sequencia(oficial, referencia),
            "points_average": round(float(atributos[f"pontos_media_ultimos_5_{lado}"]), 2),
            "goals_scored_average": round(float(atributos[f"gols_marcados_media_ultimos_5_{lado}"]), 2),
            "goals_conceded_average": round(float(atributos[f"gols_sofridos_media_ultimos_5_{lado}"]), 2),
            "yellow_cards_average": round(float(atributos[f"amarelos_media_ultimos_5_{lado}"]), 2),
            "red_cards_average": round(float(atributos[f"expulsoes_media_ultimos_5_{lado}"]), 2),
            "matches_considered": JANELA,
        }

    def confronto_direto(self, mandante: str, visitante: str, referencia: datetime) -> dict[str, Any]:
        anteriores = self._anteriores(referencia)
        jogos = anteriores[
            ((anteriores["home_team"] == mandante) & (anteriores["away_team"] == visitante))
            | ((anteriores["home_team"] == visitante) & (anteriores["away_team"] == mandante))
        ]
        vit_m = vit_v = emp = 0
        for _, j in jogos.iterrows():
            gm, gv = (j["home_team_score"], j["away_team_score"]) if j["home_team"] == mandante else (j["away_team_score"], j["home_team_score"])
            vit_m += gm > gv
            vit_v += gm < gv
            emp += gm == gv
        ultimos = [
            {
                "date": str(j["data_partida"])[:10],
                "home_team": self.catalogo.nome_curto(j["home_team"]),
                "away_team": self.catalogo.nome_curto(j["away_team"]),
                "score": f"{int(j['home_team_score'])} x {int(j['away_team_score'])}",
            }
            for _, j in jogos.tail(5).iloc[::-1].iterrows()
        ]
        return {"matches": int(len(jogos)), "home_team_wins": int(vit_m), "draws": int(emp),
                "away_team_wins": int(vit_v), "last_matches": ultimos}

    def fatores(self, X: pd.DataFrame, probabilidades: np.ndarray, top: int = 3) -> list[dict[str, Any]]:
        """Atributos que mais pesam na diferença entre as duas classes mais prováveis.

        Só se aplica a modelos lineares: contribuição = (coef[1ª] − coef[2ª]) × valor padronizado.
        É uma associação aprendida pelo modelo, não uma relação causal.
        """
        clf = self.modelo.named_steps.get("clf")
        if not hasattr(clf, "coef_"):
            return []
        prep = self.modelo.named_steps["prep"]
        nomes = [n.split("__", 1)[1] for n in prep.get_feature_names_out()]
        valores = prep.transform(X)[0]
        ordem = np.argsort(-probabilidades)
        a, b = int(ordem[0]), int(ordem[1])
        contrib = (clf.coef_[a] - clf.coef_[b]) * valores
        saida = []
        for j in np.argsort(-np.abs(contrib))[:top]:
            nome = nomes[j]
            if nome in X.columns:
                rotulo, valor = rotulo_atributo(nome), float(X.iloc[0][nome])
                descricao = f"{rotulo}: {valor:.2f}".replace(".", ",")
            else:  # indicador de equipe / dia da semana
                coluna = next(c for c in X.columns if nome.startswith(f"{c}_"))
                categoria = nome[len(coluna) + 1:]
                if coluna in ("home_team", "away_team"):
                    categoria = self.catalogo.nome_curto(categoria) if categoria in self.catalogo._por_oficial else categoria
                rotulo, valor = rotulo_atributo(coluna), categoria
                descricao = f"{rotulo}: {categoria}"
            favorece = CLASSES[a] if contrib[j] > 0 else CLASSES[b]
            saida.append({"feature": nome, "label": rotulo, "value": valor, "description": descricao,
                          "favors": favorece, "weight": round(float(abs(contrib[j])), 4)})
        return saida

    # ------------------------------------------------------------------ #
    def prever(
        self,
        mandante_id: object,
        visitante_id: object,
        data: object = None,
        hora: object = None,
        id_partida: object = None,
    ) -> dict[str, Any]:
        if not self.modelo_carregado:
            raise ErroApi(503, "modelo_indisponivel", "Modelo não encontrado. Execute `python src/modeling.py` e reinicie a API.")

        real = None
        if id_partida is not None:
            try:
                id_int = int(id_partida)
            except (TypeError, ValueError):
                raise ErroApi(400, "id_invalido", "match_id deve ser um número inteiro.") from None
            achadas = self.df[self.df["id_partida"] == id_int]
            if achadas.empty:
                raise ErroApi(404, "partida_nao_encontrada", "Partida não encontrada na base.")
            real = achadas.iloc[0]
            mandante, visitante = real["home_team"], real["away_team"]
            referencia, origem = real["data_partida"].to_pydatetime(), "partida"
        else:
            mandante = self.catalogo.resolver(mandante_id)
            visitante = self.catalogo.resolver(visitante_id)
            if mandante == visitante:
                raise ErroApi(422, "equipes_iguais", "Mandante e visitante devem ser equipes diferentes.")
            referencia, origem = self.resolver_referencia(data, hora)

        X = self.atributos_confronto(mandante, visitante, referencia)
        probs = self.modelo.predict_proba(X)[0]
        indice = int(np.argmax(probs))
        classe = CLASSES[indice]
        atributos = X.iloc[0]
        h, v = self.catalogo.nome_curto(mandante), self.catalogo.nome_curto(visitante)
        rotulos = {"home_win": f"Vitória do {h}", "draw": "Empate", "away_win": f"Vitória do {v}"}
        fatores = self.fatores(X, probs)
        anteriores = self._anteriores(referencia)

        resposta: dict[str, Any] = {
            "prediction": classe,
            "label": rotulos[classe],
            "confidence": round(float(probs[indice]), 4),
            "probabilities": {c: round(float(probs[i]), 4) for i, c in enumerate(CLASSES)},
            "home_team_form": self._forma(mandante, "mandante", atributos, referencia),
            "away_team_form": self._forma(visitante, "visitante", atributos, referencia),
            "head_to_head": self.confronto_direto(mandante, visitante, referencia),
            "factors": fatores,
            "explanations": [
                f"{f['description']} pesa a favor de: {ROTULO_RESULTADO[f['favors']].lower()}." for f in fatores
            ],
            "reference": {
                "date": referencia.strftime("%Y-%m-%d"),
                "hour": referencia.hour,
                "weekday": DIAS_SEMANA[referencia.weekday()],
                "source": origem,
                "history_until": str(anteriores["data_partida"].max())[:10],
                "hypothetical": origem != "partida",
            },
            "model": {
                "algorithm": self.metadados["algoritmo"],
                "version": self.metadados["versao"],
                "trained_at": self.metadados["data_treinamento"],
            },
        }
        if real is not None:
            resposta["actual"] = {
                "result": real["resultado"],
                "label": ROTULO_RESULTADO[real["resultado"]],
                "score": f"{int(real['home_team_score'])} x {int(real['away_team_score'])}",
                "used_in_training": int(real["temporada"]) <= 2022,
            }
        return resposta
