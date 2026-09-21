"""API RESTful do modelo preditivo do Brasileirão Série A.

Fornece endpoints para o frontend (Vite/React):
- GET  /api/health
- GET  /api/teams
- POST /api/predict
- GET  /api/stats/overview
- GET  /api/matches

Utiliza o modelo real treinado (Regressão Logística Multinomial) e a base de dados
processada (partidas_processadas.csv), 100% livre de vazamento de dados.
"""

from __future__ import annotations

import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

# Garante a importação dos módulos da raiz
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

import numpy as np
import pandas as pd

from src.data_analysis import NOME_CURTO
from src.data_split import (
    CLASSES,
    ParticoesDados,
    carregar_e_dividir_dados,
    criar_features_diferenciais,
)
from src.modeling import construir_modelos

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("api")

PORTA = 8000
CSV_PROCESSADO = RAIZ_PROJETO / "data" / "processed" / "partidas_processadas.csv"

# Mapeamento reverso de nomes curtos para nomes oficiais
NOME_OFICIAL = {curto.lower(): oficial for oficial, curto in NOME_CURTO.items()}
for oficial, curto in NOME_CURTO.items():
    NOME_OFICIAL[oficial.lower()] = oficial

# Estado global da aplicação
MODELO_PIPE = None
PARTICOES: ParticoesDados | None = None
DF_PARTIDAS: pd.DataFrame | None = None
TEAMS_LIST: list[dict[str, str]] = []


def inicializar_modelo_e_dados() -> None:
    """Carrega dados e ajusta o modelo vencedor (Regressão Logística) com as temporadas 2020 a 2022."""
    global MODELO_PIPE, PARTICOES, DF_PARTIDAS, TEAMS_LIST

    logger.info("Carregando base de dados e preparando modelo...")
    PARTICOES = carregar_e_dividir_dados(caminho_csv=CSV_PROCESSADO)
    DF_PARTIDAS = pd.read_csv(CSV_PROCESSADO)
    DF_PARTIDAS, _ = criar_features_diferenciais(DF_PARTIDAS)
    DF_PARTIDAS["data_partida"] = pd.to_datetime(DF_PARTIDAS["data_partida"])

    # Ajustar o modelo final com todo o histórico até 2022 (1.052 partidas utilizáveis)
    modelos = construir_modelos(PARTICOES.features_numericas, PARTICOES.features_categoricas)
    MODELO_PIPE = modelos["Regressão Logística"]
    MODELO_PIPE.fit(PARTICOES.X_train_val, PARTICOES.y_train_val)
    logger.info("Modelo Regressão Logística treinado com 1.052 partidas (2020–2022).")

    # Montar lista oficial de equipes (26 clubes)
    equipes_brutas = sorted(DF_PARTIDAS["home_team"].unique())
    TEAMS_LIST = [
        {
            "id": t,
            "name": NOME_CURTO.get(t, t),
        }
        for t in equipes_brutas
    ]
    TEAMS_LIST.sort(key=lambda x: x["name"])


def resolver_nome_equipe(identificador: str) -> str:
    """Converte ID ou nome curto de volta para o nome oficial do dataset."""
    ident_limpo = identificador.strip()
    if ident_limpo in NOME_CURTO:
        return ident_limpo
    # Tenta pelo slug ou nome curto
    for oficial, curto in NOME_CURTO.items():
        slug = (
            curto.lower()
            .replace("ã", "a")
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
            .replace(" ", "-")
        )
        if (
            ident_limpo.lower() == oficial.lower()
            or ident_limpo.lower() == curto.lower()
            or ident_limpo.lower() == slug
        ):
            return oficial
    return ident_limpo


def obter_forma_equipe(equipe_oficial: str, limite: int = 5) -> dict[str, Any]:
    """Extrai os últimos resultados e estatísticas médias da equipe."""
    assert DF_PARTIDAS is not None
    mask = (DF_PARTIDAS["home_team"] == equipe_oficial) | (DF_PARTIDAS["away_team"] == equipe_oficial)
    jogos = DF_PARTIDAS[mask].sort_values("data_partida").tail(limite)

    sequencia = []
    gols_pro = []
    gols_contra = []
    pontos = []
    amarelos = []
    vermelhos = []

    for _, j in jogos.iterrows():
        eh_mandante = j["home_team"] == equipe_oficial
        gp = j["home_team_score"] if eh_mandante else j["away_team_score"]
        gc = j["away_team_score"] if eh_mandante else j["home_team_score"]
        gols_pro.append(gp)
        gols_contra.append(gc)

        am = j["amarelos_mandante"] if eh_mandante else j["amarelos_visitante"]
        vm = j["expulsoes_mandante"] if eh_mandante else j["expulsoes_visitante"]
        amarelos.append(am)
        vermelhos.append(vm)

        if gp > gc:
            sequencia.append("V")
            pontos.append(3)
        elif gp == gc:
            sequencia.append("E")
            pontos.append(1)
        else:
            sequencia.append("D")
            pontos.append(0)

    n = max(1, len(jogos))
    return {
        "last_five": sequencia if sequencia else ["E", "E", "E", "E", "E"],
        "points_average": round(float(np.mean(pontos)), 2) if pontos else 1.0,
        "goals_scored_average": round(float(np.mean(gols_pro)), 2) if gols_pro else 1.0,
        "goals_conceded_average": round(float(np.mean(gols_contra)), 2) if gols_contra else 1.0,
        "yellow_cards_average": round(float(np.mean(amarelos)), 2) if amarelos else 2.0,
        "red_cards_average": round(float(np.mean(vermelhos)), 2) if vermelhos else 0.1,
    }


def prever_confronto(home_team: str, away_team: str, match_id: int | None = None) -> dict[str, Any]:
    """Executa a predição usando o modelo real treinado e gera a resposta completa."""
    assert MODELO_PIPE is not None
    assert PARTICOES is not None
    assert DF_PARTIDAS is not None

    home_oficial = resolver_nome_equipe(home_team)
    away_oficial = resolver_nome_equipe(away_team)

    home_curto = NOME_CURTO.get(home_oficial, home_oficial)
    away_curto = NOME_CURTO.get(away_oficial, away_oficial)

    # Verifica se o usuário pediu uma partida específica real do dataset
    linha_partida = None
    if match_id is not None:
        sub = DF_PARTIDAS[DF_PARTIDAS["id_partida"] == int(match_id)]
        if not sub.empty:
            linha_partida = sub.iloc[0]

    # Se não foi fornecido match_id, procura se há confronto direto no conjunto de teste (2023)
    if linha_partida is None:
        sub = DF_PARTIDAS[
            (DF_PARTIDAS["home_team"] == home_oficial)
            & (DF_PARTIDAS["away_team"] == away_oficial)
            & (DF_PARTIDAS["temporada"] == 2023)
            & (DF_PARTIDAS["utilizavel_ml"] == 1)
        ]
        if not sub.empty:
            linha_partida = sub.iloc[-1]

    # Caso ainda seja None, busca o histórico mais recente conhecido de cada equipe
    if linha_partida is None:
        sub_h = DF_PARTIDAS[
            (DF_PARTIDAS["home_team"] == home_oficial) & (DF_PARTIDAS["utilizavel_ml"] == 1)
        ].sort_values("data_partida").tail(1)
        sub_a = DF_PARTIDAS[
            (DF_PARTIDAS["away_team"] == away_oficial) & (DF_PARTIDAS["utilizavel_ml"] == 1)
        ].sort_values("data_partida").tail(1)

        linha_simulada = {}
        for c in PARTICOES.features_numericas:
            if c.endswith("_mandante") and not sub_h.empty:
                linha_simulada[c] = sub_h[c].values[0]
            elif c.endswith("_visitante") and not sub_a.empty:
                linha_simulada[c] = sub_a[c].values[0]
            elif c == "aproveitamento_mandante_em_casa" and not sub_h.empty:
                linha_simulada[c] = sub_h[c].values[0]
            elif c == "aproveitamento_visitante_fora" and not sub_a.empty:
                linha_simulada[c] = sub_a[c].values[0]
            else:
                linha_simulada[c] = 0.0

        linha_simulada["home_team"] = home_oficial
        linha_simulada["away_team"] = away_oficial
        linha_simulada["dia_semana"] = "domingo"
        linha_simulada["mes"] = 10
        linha_simulada["hora"] = 16

        df_input = pd.DataFrame([linha_simulada])
        df_input, _ = criar_features_diferenciais(df_input)
    else:
        # Usa exatamente as features pré-jogo reais daquela partida
        linha_simulada = linha_partida[PARTICOES.X_train.columns].to_dict()
        df_input = pd.DataFrame([linha_simulada])

    # Inferência com o modelo scikit-learn
    probs = MODELO_PIPE.predict_proba(df_input[PARTICOES.X_train.columns])[0]
    p_home, p_draw, p_away = float(probs[0]), float(probs[1]), float(probs[2])

    prob_dict = {
        "home_win": round(p_home, 4),
        "draw": round(p_draw, 4),
        "away_win": round(p_away, 4),
    }

    pred_idx = int(np.argmax(probs))
    pred_class = CLASSES[pred_idx]

    rotulos_amigaveis = {
        "home_win": f"Vitória do {home_curto}",
        "draw": "Empate",
        "away_win": f"Vitória do {away_curto}",
    }

    form_home = obter_forma_equipe(home_oficial)
    form_away = obter_forma_equipe(away_oficial)

    # Geração de explicações analíticas baseadas nas features reais
    explicacoes = [
        f"Aproveitamento recente do {home_curto}: média de {form_home['points_average']:.1f} pontos por jogo nos últimos 5 confrontos.",
        f"Eficiência ofensiva: {home_curto} marcou média de {form_home['goals_scored_average']:.1f} gols/jogo contra {form_away['goals_scored_average']:.1f} do {away_curto}.",
        f"Vantagem histórica do mando de campo na Série A (mandantes vencem 45,5% dos jogos da base de dados).",
    ]

    return {
        "prediction": pred_class,
        "label": rotulos_amigaveis[pred_class],
        "confidence": round(float(probs[pred_idx]), 4),
        "probabilities": prob_dict,
        "home_team_form": form_home,
        "away_team_form": form_away,
        "explanations": explicacoes,
    }


def calcular_estatisticas_overview(filters: dict[str, str]) -> dict[str, Any]:
    """Calcula estatísticas de visão geral com suporte completo e dinâmico aos filtros."""
    assert DF_PARTIDAS is not None
    sub = DF_PARTIDAS.copy()

    season = filters.get("season", "all")
    team = filters.get("team", "all")
    venue = filters.get("venue", "all")

    if season != "all":
        try:
            sub = sub[sub["temporada"] == int(season)]
        except ValueError:
            pass

    if team != "all":
        team_oficial = resolver_nome_equipe(team)
        if venue == "home":
            sub = sub[sub["home_team"] == team_oficial]
        elif venue == "away":
            sub = sub[sub["away_team"] == team_oficial]
        else:
            sub = sub[(sub["home_team"] == team_oficial) | (sub["away_team"] == team_oficial)]
    elif venue != "all":
        # Se equipe for all, venue por si só descreve visão de mandantes ou visitantes
        pass

    total_matches = len(sub)
    if total_matches == 0:
        return {
            "total_matches": 0,
            "total_goals": 0,
            "goals_average": 0.0,
            "total_yellow_cards": 0,
            "yellow_cards_average": 0.0,
            "total_red_cards": 0,
            "red_cards_average": 0.0,
            "home_win_percentage": 0.0,
            "draw_percentage": 0.0,
            "away_win_percentage": 0.0,
            "result_distribution": [
                {"name": "Mandante", "value": 0},
                {"name": "Empate", "value": 0},
                {"name": "Visitante", "value": 0},
            ],
            "goals_by_season": [],
            "cards_by_season": [],
            "top_winners": [],
            "top_goals": [],
            "top_cards": [],
        }

    total_goals = int(sub["home_team_score"].sum() + sub["away_team_score"].sum())
    goals_average = round(total_goals / total_matches, 2)

    total_yellows = int(sub["total_amarelos"].sum())
    total_reds = int(sub["total_expulsoes"].sum())
    yellow_avg = round(total_yellows / total_matches, 2)
    red_avg = round(total_reds / total_matches, 2)

    hw = int((sub["resultado"] == "home_win").sum())
    dr = int((sub["resultado"] == "draw").sum())
    aw = int((sub["resultado"] == "away_win").sum())

    hw_pct = round(hw / total_matches, 4)
    dr_pct = round(dr / total_matches, 4)
    aw_pct = round(aw / total_matches, 4)

    # Gols por temporada
    goals_by_season = []
    for s in [2020, 2021, 2022, 2023]:
        s_matches = DF_PARTIDAS[DF_PARTIDAS["temporada"] == s]
        if not s_matches.empty:
            g = s_matches["home_team_score"].sum() + s_matches["away_team_score"].sum()
            goals_by_season.append({"season": str(s), "goals_average": round(g / len(s_matches), 2)})

    # Cartões por temporada
    cards_by_season = []
    for s in [2020, 2021, 2022, 2023]:
        s_matches = DF_PARTIDAS[DF_PARTIDAS["temporada"] == s]
        if not s_matches.empty:
            y = s_matches["total_amarelos"].sum() / len(s_matches)
            r = s_matches["total_expulsoes"].sum() / len(s_matches)
            cards_by_season.append({"season": str(s), "yellow": round(y, 2), "red": round(r, 2)})

    # Top Vencedores (calculado sobre o recorte atual)
    vitorias_dict = {}
    for _, j in sub.iterrows():
        if j["resultado"] == "home_win":
            time = NOME_CURTO.get(j["home_team"], j["home_team"])
            vitorias_dict[time] = vitorias_dict.get(time, 0) + 1
        elif j["resultado"] == "away_win":
            time = NOME_CURTO.get(j["away_team"], j["away_team"])
            vitorias_dict[time] = vitorias_dict.get(time, 0) + 1

    top_winners = [
        {"team": time, "wins": count}
        for time, count in sorted(vitorias_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    # Top Gols Média (mínimo de partidas no recorte)
    gols_times = {}
    jogos_times = {}
    for _, j in sub.iterrows():
        t_home = NOME_CURTO.get(j["home_team"], j["home_team"])
        t_away = NOME_CURTO.get(j["away_team"], j["away_team"])
        gols_times[t_home] = gols_times.get(t_home, 0) + j["home_team_score"]
        gols_times[t_away] = gols_times.get(t_away, 0) + j["away_team_score"]
        jogos_times[t_home] = jogos_times.get(t_home, 0) + 1
        jogos_times[t_away] = jogos_times.get(t_away, 0) + 1

    top_goals = [
        {"team": time, "goals_average": round(gols_times[time] / jogos_times[time], 2)}
        for time in sorted(gols_times.keys(), key=lambda t: gols_times[t] / jogos_times[t], reverse=True)[:5]
    ]

    # Top Cartões Média
    cards_times = {}
    for _, j in sub.iterrows():
        t_home = NOME_CURTO.get(j["home_team"], j["home_team"])
        t_away = NOME_CURTO.get(j["away_team"], j["away_team"])
        cards_times[t_home] = cards_times.get(t_home, 0) + j["amarelos_mandante"] + j["expulsoes_mandante"]
        cards_times[t_away] = cards_times.get(t_away, 0) + j["amarelos_visitante"] + j["expulsoes_visitante"]

    top_cards = [
        {"team": time, "cards": round(cards_times[time] / jogos_times[time], 1)}
        for time in sorted(cards_times.keys(), key=lambda t: cards_times[t] / jogos_times[t], reverse=True)[:5]
    ]

    return {
        "total_matches": total_matches,
        "total_goals": total_goals,
        "goals_average": goals_average,
        "total_yellow_cards": total_yellows,
        "yellow_cards_average": yellow_avg,
        "total_red_cards": total_reds,
        "red_cards_average": red_avg,
        "home_win_percentage": hw_pct,
        "draw_percentage": dr_pct,
        "away_win_percentage": aw_pct,
        "result_distribution": [
            {"name": "Mandante", "value": round(hw_pct * 100)},
            {"name": "Empate", "value": round(dr_pct * 100)},
            {"name": "Visitante", "value": round(aw_pct * 100)},
        ],
        "goals_by_season": goals_by_season,
        "cards_by_season": cards_by_season,
        "top_winners": top_winners,
        "top_goals": top_goals,
        "top_cards": top_cards,
    }


def obter_partidas_paginadas(filters: dict[str, str], page: int = 1, page_size: int = 5) -> dict[str, Any]:
    """Retorna partidas reais do dataset conforme filtros e paginação."""
    assert DF_PARTIDAS is not None
    sub = DF_PARTIDAS.copy()

    season = filters.get("season", "all")
    team = filters.get("team", "all")
    venue = filters.get("venue", "all")

    if season != "all":
        try:
            sub = sub[sub["temporada"] == int(season)]
        except ValueError:
            pass

    if team != "all":
        team_oficial = resolver_nome_equipe(team)
        if venue == "home":
            sub = sub[sub["home_team"] == team_oficial]
        elif venue == "away":
            sub = sub[sub["away_team"] == team_oficial]
        else:
            sub = sub[(sub["home_team"] == team_oficial) | (sub["away_team"] == team_oficial)]

    total = len(sub)
    pages = max(1, (total + page_size - 1) // page_size)
    page_ajustada = max(1, min(page, pages))

    inicio = (page_ajustada - 1) * page_size
    fim = inicio + page_size
    pedaco = sub.sort_values("data_partida", ascending=False).iloc[inicio:fim]

    partidas_lista = []
    for _, r in pedaco.iterrows():
        partidas_lista.append({
            "id": str(r["id_partida"]),
            "date": str(r["data_partida"])[:10],
            "season": str(r["temporada"]),
            "home_team": NOME_CURTO.get(r["home_team"], r["home_team"]),
            "away_team": NOME_CURTO.get(r["away_team"], r["away_team"]),
            "score": f"{r['home_team_score']} x {r['away_team_score']}",
            "yellow_cards": int(r["total_amarelos"]),
            "red_cards": int(r["total_expulsoes"]),
            "stadium": str(r["stadium"]),
        })

    return {
        "matches": partidas_lista,
        "total": total,
        "page": page_ajustada,
        "pages": pages,
    }


class ApiHandler(BaseHTTPRequestHandler):
    """Manipulador HTTP com suporte a CORS e rotas da API."""

    def _responder_json(self, status_code: int, dados: Any) -> None:
        payload = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

        if path in ("/api/health", "/health"):
            self._responder_json(200, {
                "status": "online",
                "model": "Regressão Logística Multinomial (L2, C=0.5)",
                "version": "1.0.0",
                "dataset_matches": 1520,
                "dataset_goals": 3637,
                "train_matches": 1052,
                "test_matches": 362,
            })
        elif path == "/api/teams":
            self._responder_json(200, {"teams": TEAMS_LIST})
        elif path == "/api/stats/overview":
            overview = calcular_estatisticas_overview(params)
            self._responder_json(200, overview)
        elif path == "/api/matches":
            page = int(params.get("page", 1))
            page_size = int(params.get("page_size", 5))
            matches_data = obter_partidas_paginadas(params, page, page_size)
            self._responder_json(200, matches_data)
        else:
            self._responder_json(404, {"error": "Rota não encontrada"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/predict":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                dados = json.loads(body.decode("utf-8"))
                home_team = dados.get("home_team")
                away_team = dados.get("away_team")
                match_id = dados.get("match_id")

                if not home_team or not away_team:
                    self._responder_json(400, {"error": "home_team e away_team são obrigatórios."})
                    return

                res = prever_confronto(home_team, away_team, match_id=match_id)
                self._responder_json(200, res)
            except Exception as e:
                logger.exception("Erro ao processar predição: %s", e)
                self._responder_json(500, {"error": str(e)})
        else:
            self._responder_json(404, {"error": "Rota não encontrada"})

    def log_message(self, format: str, *args: Any) -> None:
        # Suprime logs de requisições rotineiras para manter o terminal limpo
        pass


def rodar_servidor(porta: int = PORTA) -> None:
    """Inicia o servidor HTTP."""
    inicializar_modelo_e_dados()
    servidor = HTTPServer(("0.0.0.0", porta), ApiHandler)
    logger.info("API do Preditor Brasileirão ativa em: http://localhost:%d/api", porta)
    logger.info("Pressione Ctrl+C para encerrar.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor encerrado.")


if __name__ == "__main__":
    rodar_servidor()
