"""Rotas, validações, erros, CORS e servidor HTTP real da API."""
from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from src.api import AplicacaoApi, criar_handler


def get(app, caminho, **consulta):
    return app.tratar("GET", caminho, {k: str(v) for k, v in consulta.items()})


def post(app, corpo, caminho="/api/predict"):
    dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo).encode()
    return app.tratar("POST", caminho, {}, dados)


# --------------------------------------------------------------------------- #
def test_health_reporta_modelo_e_base_reais(app):
    status, d = get(app, "/api/health")
    assert status == 200 and d["status"] == "ok" and d["model_loaded"] is True
    assert d["dataset"]["matches"] == 1520 and d["dataset"]["teams"] == 26
    assert d["dataset"]["seasons"] == [2020, 2021, 2022, 2023]
    assert d["model"]["algorithm"] == "Regressão Logística"


def test_docs_lista_os_endpoints(app):
    status, d = get(app, "/api/docs")
    caminhos = {e["path"].split("?")[0] for e in d["endpoints"]}
    assert status == 200 and {"/api/health", "/api/teams", "/api/predict", "/api/stats/charts",
                              "/api/teams/compare", "/api/teams/{team_id}/summary"} <= caminhos


def test_equipes(app):
    status, d = get(app, "/api/teams")
    assert status == 200 and len(d["teams"]) == 26
    assert all({"id", "name", "eligible"} <= set(t) for t in d["teams"])
    assert len({t["id"] for t in d["teams"]}) == 26
    assert d["reference"]["default_date"] == "2023-12-07"
    assert sum(t["eligible"] for t in d["teams"]) == 20


def test_overview_total_e_filtros(app):
    assert get(app, "/api/stats/overview")[1]["total_matches"] == 1520
    _, d23 = get(app, "/api/stats/overview", season=2023)
    assert d23["total_matches"] == 380 and d23["teams"] == 20 and d23["seasons"] == [2023]
    _, fla = get(app, "/api/stats/overview", season=2023, team="flamengo")
    assert fla["total_matches"] == 38
    _, casa = get(app, "/api/stats/overview", season=2023, team="flamengo", venue="home")
    _, fora = get(app, "/api/stats/overview", season=2023, team="flamengo", venue="away")
    assert casa["total_matches"] == 19 and fora["total_matches"] == 19


def test_overview_bate_com_o_csv_original(app, bruto):
    _, d = get(app, "/api/stats/overview")
    assert d["total_goals"] == int(bruto["home_team_score"].sum() + bruto["away_team_score"].sum()) == 3637
    assert d["matches_without_attendance"] == 613
    assert d["home_win_percentage"] + d["draw_percentage"] + d["away_win_percentage"] == pytest.approx(1, abs=1e-3)


def test_graficos_por_temporada_e_rankings(app):
    _, c = get(app, "/api/stats/charts")
    assert [g["season"] for g in c["goals_by_season"]] == ["2020", "2021", "2022", "2023"]
    assert sum(r["count"] for r in c["result_distribution"]) == 1520
    assert len(c["top_winners"]) == 5 and c["rankings_available"] is True
    _, unica = get(app, "/api/stats/charts", team="flamengo")
    assert unica["rankings_available"] is False and unica["top_winners"] == []
    assert len(unica["goals_by_season"]) == 4


def test_filtro_sem_resultado_devolve_estado_vazio_valido(app):
    _, d = get(app, "/api/stats/overview", season=2023, team="sport")
    assert d["total_matches"] == 0 and d["attendance_average"] is None
    _, c = get(app, "/api/stats/charts", season=2023, team="sport")
    assert c["goals_by_season"] == []
    _, m = get(app, "/api/matches", season=2023, team="sport")
    assert m["matches"] == [] and m["total"] == 0 and m["pages"] == 1


def test_partidas_paginacao_e_ordem(app):
    _, p1 = get(app, "/api/matches", page=1, page_size=10)
    _, p2 = get(app, "/api/matches", page=2, page_size=10)
    assert p1["total"] == 1520 and p1["pages"] == 152 and len(p1["matches"]) == 10
    assert p1["matches"][0]["date"] >= p1["matches"][-1]["date"] >= p2["matches"][0]["date"]
    assert p1["matches"][0]["date"] == "2023-12-06"
    assert {"id", "date", "season", "home_team", "away_team", "score", "yellow_cards", "red_cards", "stadium", "attendance"} <= set(p1["matches"][0])
    _, alem = get(app, "/api/matches", page=99999, page_size=10)
    assert alem["page"] == 152


def test_publico_ausente_vira_nulo_e_nao_zero(app):
    _, d = get(app, "/api/matches", season=2020, page_size=50)
    assert any(m["attendance"] is None for m in d["matches"])
    assert all(m["attendance"] is None or m["attendance"] > 0 for m in d["matches"])


@pytest.mark.parametrize(
    "caminho,consulta",
    [
        ("/api/matches", {"page": "abc"}),
        ("/api/matches", {"page": "0"}),
        ("/api/matches", {"page_size": "1000"}),
        ("/api/matches", {"season": "1999"}),
        ("/api/stats/overview", {"venue": "meio"}),
        ("/api/stats/charts", {"season": "abc"}),
        ("/api/teams/compare", {"team_a": "flamengo"}),
    ],
)
def test_parametros_invalidos_retornam_400(app, caminho, consulta):
    status, d = get(app, caminho, **consulta)
    assert status == 400 and d["error"] and d["code"]


def test_equipe_inexistente_retorna_404(app):
    assert get(app, "/api/teams/xyz/summary")[0] == 404
    assert get(app, "/api/matches", team="xyz")[0] == 404


def test_resumo_da_equipe(app):
    status, d = get(app, "/api/teams/flamengo/summary")
    o = d["overall"]
    assert status == 200 and o["matches"] == 152 and o["wins"] + o["draws"] + o["losses"] == 152
    assert d["home"]["matches"] == d["away"]["matches"] == 76
    assert o["points"] == 3 * o["wins"] + o["draws"]
    assert len(d["by_season"]) == 4 and len(d["last_five"]) == 5


def test_comparacao_entre_equipes(app):
    status, d = get(app, "/api/teams/compare", team_a="flamengo", team_b="palmeiras")
    h = d["head_to_head"]
    assert status == 200 and h["matches"] == h["team_a_wins"] + h["draws"] + h["team_b_wins"] == 8
    assert get(app, "/api/teams/compare", team_a="flamengo", team_b="flamengo")[0] == 422


# --------------------------------------------------------------------------- #
def test_previsao_valida(app):
    status, d = post(app, {"home_team": "flamengo", "away_team": "palmeiras"})
    p = d["probabilities"]
    assert status == 200
    assert set(p) == {"home_win", "draw", "away_win"}
    assert all(0 <= v <= 1 for v in p.values())
    assert sum(p.values()) == pytest.approx(1, abs=1e-3)
    assert d["prediction"] == max(p, key=p.get) and d["confidence"] == max(p.values())
    assert d["label"].startswith("Vitória do") or d["label"] == "Empate"
    assert len(d["home_team_form"]["last_five"]) == 5 and d["head_to_head"]["matches"] == 8
    assert d["reference"]["history_until"] == "2023-12-06" and d["model"]["version"]


def test_previsao_aceita_nome_curto_e_oficial(app):
    a = post(app, {"home_team": "flamengo", "away_team": "palmeiras"})[1]["probabilities"]
    b = post(app, {"home_team": "Flamengo", "away_team": "SE Palmeiras"})[1]["probabilities"]
    assert a == b


def test_previsao_e_deterministica(app):
    corpo = {"home_team": "fluminense", "away_team": "gremio"}
    assert post(app, corpo)[1] == post(app, corpo)[1]


def test_previsao_muda_com_as_equipes(app):
    a = post(app, {"home_team": "flamengo", "away_team": "palmeiras"})[1]["probabilities"]
    b = post(app, {"home_team": "palmeiras", "away_team": "flamengo"})[1]["probabilities"]
    assert a != b  # mando de campo importa


def test_previsao_equipes_iguais_retorna_422(app):
    status, d = post(app, {"home_team": "flamengo", "away_team": "flamengo"})
    assert status == 422 and d["code"] == "equipes_iguais"


def test_previsao_equipe_sem_historico_recente_retorna_422(app):
    status, d = post(app, {"home_team": "sport", "away_team": "flamengo"})
    assert status == 422 and d["code"] == "historico_insuficiente"


@pytest.mark.parametrize(
    "corpo,status_esperado",
    [
        ({}, 400),
        ({"home_team": "flamengo"}, 400),
        ({"home_team": "", "away_team": "flamengo"}, 400),
        ({"home_team": 1, "away_team": "flamengo"}, 400),
        ({"home_team": "xyz", "away_team": "flamengo"}, 404),
        ({"home_team": "flamengo", "away_team": "palmeiras", "date": "ontem"}, 400),
        ({"home_team": "flamengo", "away_team": "palmeiras", "date": "2035-01-01"}, 422),
        ({"home_team": "flamengo", "away_team": "palmeiras", "hour": 99, "date": "2023-05-01"}, 400),
        ({"match_id": 999999}, 404),
        ({"match_id": "abc"}, 400),
        ({"home_team": ["a"], "away_team": "b"}, 400),
    ],
)
def test_previsao_validacoes(app, corpo, status_esperado):
    assert post(app, corpo)[0] == status_esperado


@pytest.mark.parametrize("corpo", [b"xx", b"[1, 2]", b"null", b"\xff\xfe"])
def test_previsao_json_invalido(app, corpo):
    status, d = post(app, corpo)
    assert status == 400 and d["code"] == "json_invalido"


def test_previsao_retrospectiva_por_match_id(app):
    status, d = post(app, {"match_id": 1461})
    assert status == 200 and d["actual"]["score"] == "3 x 0" and d["reference"]["hypothetical"] is False


def test_sem_modelo_a_previsao_responde_503_e_nao_inventa_resultado(tmp_path):
    sem_modelo = AplicacaoApi(caminho_modelo=tmp_path / "nao_existe.joblib", caminho_metadados=tmp_path / "nao_existe.json")
    assert get(sem_modelo, "/api/health")[1]["status"] == "degraded"
    status, d = post(sem_modelo, {"home_team": "flamengo", "away_team": "palmeiras"})
    assert status == 503 and d["code"] == "modelo_indisponivel" and "probabilities" not in d
    assert get(sem_modelo, "/api/model")[0] == 503
    assert get(sem_modelo, "/api/stats/overview")[0] == 200  # estatísticas continuam disponíveis


def test_modelo_expoe_metricas_reais(app):
    status, d = get(app, "/api/model")
    t = d["metrics"]["test"]
    assert status == 200 and d["algorithm"] == "Regressão Logística" and d["version"]
    assert 0 < t["acuracia"] < 1 and len(t["matriz_confusao"]) == 3 and t["n"] == 362
    assert d["splits"]["teste"]["n"] == 362 and d["limitations"]


def test_rota_inexistente_e_metodo_errado(app):
    assert get(app, "/api/nada")[0] == 404
    assert app.tratar("POST", "/api/teams", {}, b"{}")[0] == 405
    assert app.tratar("GET", "/api/predict", {})[0] == 405


def test_erro_interno_nao_vaza_detalhes(app, monkeypatch):
    def quebrar(*_a, **_k):
        raise RuntimeError("segredo-interno /home/usuario/chave")

    monkeypatch.setattr(app.previsao, "prever", quebrar)
    app._prever_cache.cache_clear()
    status, d = post(app, {"home_team": "botafogo", "away_team": "santos"})
    assert status == 500 and "segredo" not in json.dumps(d) and d["code"] == "erro_interno"
    app._prever_cache.cache_clear()


def test_previsao_e_tratamento_de_erros_nao_expoem_caminhos_nem_credenciais(app):
    texto = json.dumps([get(app, "/api/health")[1], get(app, "/api/model")[1]])
    assert "/home/" not in texto and "password" not in texto.lower() and "token" not in texto.lower()


# --------------------------------------------------------------------------- #
# Servidor HTTP real (porta efêmera) + CORS
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def servidor(app):
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), criar_handler(app, {"http://localhost:5173"}))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()


def chamar(url, dados=None, cabecalhos=None, metodo=None):
    req = urllib.request.Request(url, data=dados, headers=cabecalhos or {}, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, dict(r.headers), json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), json.loads(e.read() or b"null")


def test_http_health_e_previsao(servidor):
    status, cab, corpo = chamar(f"{servidor}/api/health")
    assert status == 200 and cab["Content-Type"].startswith("application/json") and corpo["model_loaded"]
    status, _, corpo = chamar(
        f"{servidor}/api/predict", json.dumps({"home_team": "flamengo", "away_team": "palmeiras"}).encode(),
        {"Content-Type": "application/json"},
    )
    assert status == 200 and sum(corpo["probabilities"].values()) == pytest.approx(1, abs=1e-3)


def test_http_cors_somente_para_origem_permitida(servidor):
    _, cab, _ = chamar(f"{servidor}/api/health", cabecalhos={"Origin": "http://localhost:5173"})
    assert cab["Access-Control-Allow-Origin"] == "http://localhost:5173"
    _, cab, _ = chamar(f"{servidor}/api/health", cabecalhos={"Origin": "http://malicioso.example"})
    assert "Access-Control-Allow-Origin" not in cab
    status, cab, _ = chamar(f"{servidor}/api/predict", cabecalhos={"Origin": "http://localhost:5173"}, metodo="OPTIONS")
    assert status == 204 and "POST" in cab["Access-Control-Allow-Methods"]


def test_http_erros_sao_json(servidor):
    status, _, corpo = chamar(f"{servidor}/api/matches?page=abc")
    assert status == 400 and corpo["code"] == "parametro_invalido"
    status, _, corpo = chamar(f"{servidor}/api/inexistente")
    assert status == 404 and "error" in corpo
    status, _, corpo = chamar(f"{servidor}/api/predict", b"{", {"Content-Type": "application/json"})
    assert status == 400
