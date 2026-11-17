"""API HTTP do preditor do Brasileirão Série A (somente biblioteca padrão + pacotes do projeto).

Execução (a partir da raiz do repositório)::

    python src/api.py              # http://127.0.0.1:8000/api

Variáveis de ambiente opcionais: ``API_HOST`` (127.0.0.1), ``API_PORT`` (8000) e ``CORS_ORIGINS``
(lista separada por vírgulas; padrão: http://localhost:5173,http://127.0.0.1:5173).

O modelo é carregado de ``models/model.joblib`` (gerado por ``python src/modeling.py``) e as
estatísticas vêm de ``data/processed/partidas_processadas.csv``. Nada é simulado: sem modelo,
``POST /api/predict`` responde 503.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, unquote, urlparse

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from src.analytics import Analises
from src.common import CatalogoEquipes, ErroApi, carregar_partidas
from src.data_split import CSV_PROCESSADO_PADRAO
from src.predictor import ARQUIVO_METADADOS, ServicoPrevisao

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("api")

VERSAO_API = "1.0.0"
ARQUIVO_METRICAS = RAIZ_PROJETO / "reports" / "evidencias" / "metricas_execucao.json"
ORIGENS_PADRAO = "http://localhost:5173,http://127.0.0.1:5173"
TAMANHO_MAXIMO_CORPO = 10_000

ENDPOINTS = [
    {"method": "GET", "path": "/api/health", "description": "Estado da API, do modelo e da base de dados."},
    {"method": "GET", "path": "/api/docs", "description": "Lista os endpoints disponíveis."},
    {"method": "GET", "path": "/api/model", "description": "Metadados, métricas reais e limitações do modelo."},
    {"method": "GET", "path": "/api/teams", "description": "Equipes da base, com elegibilidade para previsão."},
    {"method": "GET", "path": "/api/teams/{team_id}/summary", "description": "Resumo de desempenho de uma equipe."},
    {"method": "GET", "path": "/api/teams/compare?team_a=&team_b=", "description": "Comparação e confronto direto entre duas equipes."},
    {"method": "GET", "path": "/api/stats/overview?season=&team=&venue=", "description": "Indicadores do recorte filtrado."},
    {"method": "GET", "path": "/api/stats/charts?season=&team=&venue=", "description": "Séries para os gráficos do recorte filtrado."},
    {"method": "GET", "path": "/api/matches?season=&team=&venue=&page=&page_size=", "description": "Partidas paginadas (mais recentes primeiro)."},
    {"method": "POST", "path": "/api/predict", "description": "Corpo JSON: home_team, away_team e, opcionalmente, date (AAAA-MM-DD), hour (0-23) ou match_id."},
]


def _inteiro(params: dict[str, str], nome: str, padrao: int) -> int:
    try:
        return int(params.get(nome, padrao))
    except (TypeError, ValueError):
        raise ErroApi(400, "parametro_invalido", f"{nome} deve ser um número inteiro.") from None


class AplicacaoApi:
    """Rotas e regras da API, independentes do servidor HTTP (facilita os testes)."""

    def __init__(
        self,
        caminho_csv: Path | str = CSV_PROCESSADO_PADRAO,
        caminho_modelo: Path | None = None,
        caminho_metadados: Path = ARQUIVO_METADADOS,
        caminho_metricas: Path = ARQUIVO_METRICAS,
    ):
        self.partidas = carregar_partidas(caminho_csv)
        self.catalogo = CatalogoEquipes(self.partidas)
        self.analises = Analises(self.partidas, self.catalogo)
        argumentos = {"caminho_metadados": caminho_metadados}
        if caminho_modelo is not None:
            argumentos["caminho_modelo"] = caminho_modelo
        self.previsao = ServicoPrevisao(self.partidas, self.catalogo, **argumentos)
        self.caminho_metricas = caminho_metricas
        self._prever_cache = lru_cache(maxsize=512)(self._prever)
        self.rotas: list[tuple[str, re.Pattern[str], Callable[..., Any]]] = [
            ("GET", re.compile(r"^/api/health$"), self.health),
            ("GET", re.compile(r"^/api/docs$"), self.docs),
            ("GET", re.compile(r"^/api/model$"), self.modelo),
            ("GET", re.compile(r"^/api/teams$"), self.equipes),
            ("GET", re.compile(r"^/api/teams/compare$"), self.comparar),
            ("GET", re.compile(r"^/api/teams/(?P<team_id>[^/]+)/summary$"), self.resumo_equipe),
            ("GET", re.compile(r"^/api/stats/overview$"), self.visao_geral),
            ("GET", re.compile(r"^/api/stats/charts$"), self.graficos),
            ("GET", re.compile(r"^/api/matches$"), self.partidas_paginadas),
            ("POST", re.compile(r"^/api/predict$"), self.prever),
        ]

    # ------------------------------------------------------------------ #
    def tratar(self, metodo: str, caminho: str, consulta: dict[str, str], corpo: bytes = b"") -> tuple[int, dict[str, Any]]:
        """Executa a rota e devolve (status HTTP, JSON). Nunca expõe detalhes internos de exceções."""
        try:
            caminho = caminho.rstrip("/") or "/"
            metodos_do_caminho = set()
            for m, padrao, funcao in self.rotas:
                achou = padrao.match(caminho)
                if not achou:
                    continue
                metodos_do_caminho.add(m)
                if m == metodo:
                    argumentos = {k: unquote(v) for k, v in achou.groupdict().items()}
                    if metodo == "POST":
                        return 200, funcao(self._corpo_json(corpo), **argumentos)
                    return 200, funcao(consulta, **argumentos)
            if metodos_do_caminho:
                raise ErroApi(405, "metodo_nao_permitido", f"Use {', '.join(sorted(metodos_do_caminho))} nesta rota.")
            raise ErroApi(404, "rota_nao_encontrada", "Rota não encontrada. Consulte /api/docs.")
        except ErroApi as erro:
            return erro.status, {"error": erro.mensagem, "code": erro.codigo}
        except Exception:  # noqa: BLE001 - falha inesperada: registra e responde sem detalhes internos
            logger.exception("Erro inesperado em %s %s", metodo, caminho)
            return 500, {"error": "Erro interno ao processar a solicitação.", "code": "erro_interno"}

    @staticmethod
    def _corpo_json(corpo: bytes) -> dict[str, Any]:
        if len(corpo) > TAMANHO_MAXIMO_CORPO:
            raise ErroApi(413, "corpo_grande", "Corpo da requisição grande demais.")
        try:
            dados = json.loads(corpo.decode("utf-8") or "null")
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ErroApi(400, "json_invalido", "O corpo da requisição deve ser um JSON válido.") from None
        if not isinstance(dados, dict):
            raise ErroApi(400, "json_invalido", "O corpo da requisição deve ser um objeto JSON.")
        return dados

    # ------------------------------------------------------------------ #
    # Rotas
    # ------------------------------------------------------------------ #
    def health(self, _: dict[str, str]) -> dict[str, Any]:
        meta = self.previsao.metadados
        return {
            "status": "ok" if self.previsao.modelo_carregado else "degraded",
            "api_version": VERSAO_API,
            "model_loaded": self.previsao.modelo_carregado,
            "model": None if meta is None else {
                "algorithm": meta["algoritmo"], "version": meta["versao"], "trained_at": meta["data_treinamento"],
            },
            "dataset": {
                "matches": int(len(self.partidas)),
                "seasons": self.analises.temporadas,
                "teams": len(self.catalogo.equipes),
                "goals": int(self.partidas["total_gols"].sum()),
                "goals_average": round(float(self.partidas["total_gols"].mean()), 2),
                "first_date": str(self.previsao.primeira_data)[:10],
                "last_date": str(self.previsao.ultima_data)[:10],
            },
            "warnings": self.previsao.avisos,
        }

    def docs(self, _: dict[str, str]) -> dict[str, Any]:
        return {"api_version": VERSAO_API, "endpoints": ENDPOINTS}

    def modelo(self, _: dict[str, str]) -> dict[str, Any]:
        meta = self.previsao.metadados
        if meta is None:
            raise ErroApi(503, "modelo_indisponivel", "Modelo não encontrado. Execute `python src/modeling.py`.")
        metricas = meta["metricas"]
        teste = metricas["teste"]
        extras: dict[str, Any] = {}
        if self.caminho_metricas.exists():
            completo = json.loads(self.caminho_metricas.read_text(encoding="utf-8"))
            extras = {
                "permutation_importance": completo["importancia_permutacao"][:10],
                "candidates": {
                    nome: {"validation": m["validacao"], "train": m["treino"], "fit_seconds": m["tempo_treino_s"]}
                    for nome, m in completo["modelos"].items()
                },
                "error_analysis": completo["analise_erros"],
                "calibration": completo["calibracao"],
                "selection_criterion": completo["criterio_selecao"],
            }
        return {
            "algorithm": meta["algoritmo"],
            "version": meta["versao"],
            "trained_at": meta["data_treinamento"],
            "trained_with": meta["treinado_com"],
            "hyperparameters": meta["hiperparametros"],
            "random_state": meta["semente_aleatoria"],
            "classes": meta["classes"],
            "class_labels": meta["rotulos_classes"],
            "features": {"numeric": meta["atributos_numericos"], "categorical": meta["atributos_categoricos"]},
            "data_period": meta["periodo_dados"],
            "splits": meta["particoes"],
            "metrics": {
                "test": teste,
                "validation": metricas["validacao"],
                "train_final": metricas["treino_final"],
                "baseline_majority_test": metricas["baselines_teste"]["majoritaria"],
                "baseline_frequency_test": metricas["baselines_teste"]["frequencias"],
            },
            "dependencies": meta["dependencias"],
            "limitations": [
                "Somente quatro temporadas de uma competição; não há escalações, lesões, elenco ou mercado.",
                "Histórico dos últimos 5 jogos; não há intervalo de confiança nem avaliação em várias janelas.",
                "O modelo não supera a referência de frequências históricas em Log-Loss e Brier no teste.",
                "Empates são raramente previstos; importâncias e coeficientes são associações, não causas.",
            ],
            **extras,
        }

    def equipes(self, _: dict[str, str]) -> dict[str, Any]:
        minimo, maximo = self.previsao.limites_referencia
        referencia = self.previsao.referencia_padrao
        return {
            "teams": self.previsao.equipes(),
            "reference": {
                "default_date": referencia.strftime("%Y-%m-%d"),
                "default_hour": referencia.hour,
                "min_date": minimo.isoformat(),
                "max_date": maximo.isoformat(),
                "last_match_date": str(self.previsao.ultima_data)[:10],
            },
        }

    def resumo_equipe(self, _: dict[str, str], team_id: str) -> dict[str, Any]:
        return self.analises.resumo_equipe(team_id)

    def comparar(self, params: dict[str, str]) -> dict[str, Any]:
        if "team_a" not in params or "team_b" not in params:
            raise ErroApi(400, "parametro_obrigatorio", "Informe team_a e team_b.")
        return self.analises.comparar(params["team_a"], params["team_b"])

    @staticmethod
    def _filtros(params: dict[str, str]) -> tuple[str, str, str]:
        return params.get("season", "all"), params.get("team", "all"), params.get("venue", "all")

    def visao_geral(self, params: dict[str, str]) -> dict[str, Any]:
        return self.analises.visao_geral(*self._filtros(params))

    def graficos(self, params: dict[str, str]) -> dict[str, Any]:
        return self.analises.graficos(*self._filtros(params))

    def partidas_paginadas(self, params: dict[str, str]) -> dict[str, Any]:
        return self.analises.partidas(
            *self._filtros(params), pagina=_inteiro(params, "page", 1), tamanho=_inteiro(params, "page_size", 5)
        )

    def _prever(self, mandante: Any, visitante: Any, data: Any, hora: Any, id_partida: Any) -> dict[str, Any]:
        return self.previsao.prever(mandante, visitante, data, hora, id_partida)

    def prever(self, corpo: dict[str, Any]) -> dict[str, Any]:
        id_partida = corpo.get("match_id")
        if id_partida is None:
            for campo in ("home_team", "away_team"):
                if not isinstance(corpo.get(campo), str) or not corpo[campo].strip():
                    raise ErroApi(400, "parametro_obrigatorio", "home_team e away_team são obrigatórios.")
        for campo in ("date", "hour", "match_id"):
            if isinstance(corpo.get(campo), (dict, list)):
                raise ErroApi(400, "parametro_invalido", f"{campo} inválido.")
        return self._prever_cache(
            corpo.get("home_team"), corpo.get("away_team"), corpo.get("date"), corpo.get("hour"), id_partida
        )


def _origens_permitidas() -> set[str]:
    return {o.strip() for o in os.environ.get("CORS_ORIGINS", ORIGENS_PADRAO).split(",") if o.strip()}


def criar_handler(app: AplicacaoApi, origens: set[str] | None = None) -> type[BaseHTTPRequestHandler]:
    permitidas = origens if origens is not None else _origens_permitidas()

    class Handler(BaseHTTPRequestHandler):
        def _cabecalhos_cors(self) -> None:
            origem = self.headers.get("Origin")
            if origem and ("*" in permitidas or origem in permitidas):
                self.send_header("Access-Control-Allow-Origin", origem if "*" not in permitidas else "*")
                self.send_header("Vary", "Origin")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def _responder(self, status: int, dados: dict[str, Any]) -> None:
            payload = json.dumps(dados, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self._cabecalhos_cors()
            self.end_headers()
            self.wfile.write(payload)

        def _despachar(self, metodo: str) -> None:
            url = urlparse(self.path)
            consulta = {k: v[0] for k, v in parse_qs(url.query).items()}
            corpo = b""
            if metodo == "POST":
                try:
                    tamanho = int(self.headers.get("Content-Length", 0))
                except ValueError:
                    tamanho = -1
                if tamanho < 0 or tamanho > TAMANHO_MAXIMO_CORPO:
                    self._responder(413, {"error": "Corpo da requisição inválido ou grande demais.", "code": "corpo_grande"})
                    return
                corpo = self.rfile.read(tamanho)
            status, dados = app.tratar(metodo, url.path, consulta, corpo)
            self._responder(status, dados)

        def do_GET(self) -> None:  # noqa: N802
            self._despachar("GET")

        def do_POST(self) -> None:  # noqa: N802
            self._despachar("POST")

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self._cabecalhos_cors()
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            logger.info("%s %s", self.command, self.path)

    return Handler


def rodar_servidor(host: str | None = None, porta: int | None = None) -> None:
    host = host or os.environ.get("API_HOST", "127.0.0.1")
    porta = porta or int(os.environ.get("API_PORT", "8000"))
    logger.info("Carregando base de dados e modelo...")
    app = AplicacaoApi()
    if not app.previsao.modelo_carregado:
        logger.warning("Modelo ausente: /api/predict responderá 503 até executar `python src/modeling.py`.")
    servidor = ThreadingHTTPServer((host, porta), criar_handler(app))
    logger.info("API ativa em http://%s:%d/api (Ctrl+C para encerrar)", host, porta)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor encerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    rodar_servidor()
