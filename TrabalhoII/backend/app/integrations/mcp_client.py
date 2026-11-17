"""Cliente MCP real do backend (SDK oficial Python v2, transporte stdio).

O backend inicia `mcp-server/server.py` como subprocesso, faz o handshake `initialize`,
descobre as tools por `tools/list` e executa `tools/call` pela sessão. O backend NUNCA
importa as tools nem o RAG diretamente: a única fronteira é o protocolo MCP.

Uso típico no lifespan do FastAPI (entrada e saída na mesma task):

    from contextlib import asynccontextmanager
    from app.integrations.mcp_client import MCPClient

    @asynccontextmanager
    async def lifespan(app):
        async with MCPClient.from_env() as mcp:
            app.state.mcp = mcp
            yield

    # no orquestrador:
    tools = app.state.mcp.llm_tools()                 # -> enviar ao Ollama em `tools=`
    result = await app.state.mcp.call_tool(name, args, request_id=rid)
    tool_message = {"role": "tool", "tool_name": name, "content": result.to_llm_content()}
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import time
from collections import deque
from collections.abc import Iterable, Mapping
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anyio
from mcp import Client, Implementation, MCPError, StdioServerParameters, Tool
from mcp.types import CONNECTION_CLOSED, REQUEST_TIMEOUT

logger = logging.getLogger("app.mcp_client")

ALLOWED_TOOLS: frozenset[str] = frozenset({"search_knowledge", "get_document", "list_topics"})

# Variáveis repassadas ao subprocesso (além do ambiente mínimo seguro do SDK: HOME, PATH...).
# Nenhuma credencial do backend (ex.: chaves de API) é herdada pelo servidor MCP.
FORWARDED_ENV = (
    "PROJECT_ROOT",
    "RECIPES_JSON",
    "CHROMA_PATH",
    "EMBEDDING_MODEL",
    "RAG_TOP_K",
    "RAG_RETRIEVER",
    "RAG_NORMALIZER",
    "MCP_LOG_LEVEL",
    "HF_HOME",
    "HF_HUB_OFFLINE",
    "TRANSFORMERS_OFFLINE",
    "SENTENCE_TRANSFORMERS_HOME",
    "PYTHONPATH",
)

_SERVER_CODE_RE = re.compile(r"\b([A-Z][A-Z_]{3,}):")


class MCPClientError(Exception):
    """Erro estável para o backend converter em resposta HTTP.

    code: MCP_UNAVAILABLE | MCP_TOOL_ERROR | INVALID_TOOL_ARGUMENTS | UPSTREAM_TIMEOUT
    detail_code: código mais específico vindo do servidor (ex.: RAG_UNAVAILABLE), se houver.
    """

    def __init__(self, code: str, message: str, *, tool: str | None = None, detail_code: str | None = None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.tool = tool
        self.detail_code = detail_code


@dataclass(frozen=True)
class ToolCallResult:
    name: str
    data: dict[str, Any]
    duration_ms: float
    request_id: str | None = None

    @property
    def error_code(self) -> str | None:
        """Erro de negócio estruturado (CORPUS_EMPTY, DOCUMENT_NOT_FOUND...), ou None."""
        err = self.data.get("error")
        return err.get("code") if isinstance(err, Mapping) else None

    @property
    def evidence(self) -> list[dict[str, str]]:
        """Fontes efetivamente retornadas nesta chamada, para montar o evidence_set do turno."""
        items: list[Mapping[str, Any]] = []
        if self.name == "search_knowledge":
            items = self.data.get("results") or []
        elif self.name == "get_document" and self.data.get("found"):
            items = [self.data["recipe"]]
        return [
            {k: str(it[k]) for k in ("recipe_id", "document_id", "title", "source_url") if it.get(k) is not None}
            for it in items
        ]

    def to_llm_content(self) -> str:
        """Conteúdo da mensagem `role=tool` enviada de volta ao LLM (JSON estruturado)."""
        return json.dumps(self.data, ensure_ascii=False)


@dataclass
class MCPClient:
    command: str
    args: list[str]
    cwd: str | Path | None = None
    env: dict[str, str] = field(default_factory=dict)
    startup_timeout: float = 30.0
    call_timeout: float = 60.0
    allowed_tools: frozenset[str] = ALLOWED_TOOLS
    trace_size: int = 200

    _client: Client | None = field(init=False, default=None, repr=False)
    _stack: AsyncExitStack | None = field(init=False, default=None, repr=False)
    _tools: dict[str, Tool] = field(init=False, default_factory=dict, repr=False)
    _validators: dict[str, Any] = field(init=False, default_factory=dict, repr=False)
    _connected: bool = field(init=False, default=False)
    trace: deque[dict[str, Any]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.trace = deque(maxlen=self.trace_size)

    # ------------------------------------------------------------ construção

    @classmethod
    def from_env(cls, project_root: str | Path | None = None) -> MCPClient:
        """Configuração por ambiente (.env do backend).

        PROJECT_ROOT       raiz do repositório (padrão: dois níveis acima de backend/app)
        MCP_COMMAND        interpretador do servidor (padrão: mcp-server/.venv/bin/python, se existir)
        MCP_SCRIPT         script do servidor (padrão: mcp-server/server.py)
        MCP_STARTUP_TIMEOUT, MCP_CALL_TIMEOUT  em segundos
        """
        root = Path(project_root or os.environ.get("PROJECT_ROOT") or Path(__file__).resolve().parents[3]).resolve()
        venv_python = root / "mcp-server" / ".venv" / "bin" / "python"
        command = os.environ.get("MCP_COMMAND") or (str(venv_python) if venv_python.exists() else sys.executable)
        script = Path(os.environ.get("MCP_SCRIPT", "mcp-server/server.py"))
        if not script.is_absolute():
            script = root / script
        env = {k: os.environ[k] for k in FORWARDED_ENV if k in os.environ}
        env.setdefault("PROJECT_ROOT", str(root))
        return cls(
            command=command,
            args=[str(script)],
            cwd=root,
            env=env,
            startup_timeout=float(os.environ.get("MCP_STARTUP_TIMEOUT", "30")),
            call_timeout=float(os.environ.get("MCP_CALL_TIMEOUT", "60")),
        )

    # ------------------------------------------------------------ ciclo de vida

    async def __aenter__(self) -> MCPClient:
        await self.start()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def start(self) -> None:
        """Inicia o subprocesso, faz `initialize` e `tools/list`. Levanta MCP_UNAVAILABLE em falha."""
        if self._stack is not None:
            raise RuntimeError("MCPClient já iniciado")
        params = StdioServerParameters(command=self.command, args=self.args, cwd=self.cwd, env=self.env)
        client = Client(
            params,
            mode="legacy",  # handshake explícito `initialize` (protocolo 2025-11-25)
            # Timeout padrão da sessão = startup (initialize/tools/list); cada call_tool passa o seu.
            read_timeout_seconds=self.startup_timeout,
            client_info=Implementation(name="receitas-backend", version="0.1.0"),
        )
        stack = AsyncExitStack()
        started = time.perf_counter()
        try:
            # Sem anyio.fail_after aqui: o Client abre um task group próprio, que não pode ficar
            # aninhado num cancel scope que termina antes dele. O limite vem de read_timeout_seconds.
            await stack.enter_async_context(client)
            self._record("initialize", started, ok=True, protocol=client.protocol_version)
            await self._discover(client)
        except BaseException as exc:
            await self._safe_close(stack)
            self._record("start_failed", started, ok=False, error_code="MCP_UNAVAILABLE")
            if isinstance(exc, MCPClientError) or not isinstance(exc, Exception):
                raise  # erro já classificado, ou cancelamento/KeyboardInterrupt
            logger.error("falha ao iniciar servidor MCP: %r", exc)
            raise MCPClientError("MCP_UNAVAILABLE", "Não foi possível iniciar o servidor MCP.") from exc
        self._client, self._stack, self._connected = client, stack, True
        logger.info(
            "MCP conectado: servidor=%s protocolo=%s tools=%s",
            client.server_info.name if client.server_info else "?",
            client.protocol_version,
            sorted(self._tools),
        )

    async def close(self) -> None:
        """Encerra sessão e subprocesso (o SDK termina a árvore de processos)."""
        stack, self._stack, self._client, self._connected = self._stack, None, None, False
        if stack is not None:
            await self._safe_close(stack)

    @staticmethod
    async def _safe_close(stack: AsyncExitStack) -> None:
        try:
            await stack.aclose()
        except Exception:  # noqa: BLE001 - encerramento deve ser best-effort
            logger.warning("erro ao encerrar sessão MCP", exc_info=True)

    @property
    def connected(self) -> bool:
        return self._connected

    async def _discover(self, client: Client) -> None:
        started = time.perf_counter()
        listed = await client.list_tools()
        tools = {t.name: t for t in listed.tools if t.name in self.allowed_tools}
        missing = self.allowed_tools - tools.keys()
        self._record("list_tools", started, ok=not missing, tools=sorted(t.name for t in listed.tools))
        if missing:
            raise MCPClientError("MCP_UNAVAILABLE", f"Servidor MCP não expõe as tools: {sorted(missing)}")
        from jsonschema import Draft202012Validator  # dependência do próprio SDK MCP

        self._tools = tools
        self._validators = {name: Draft202012Validator(t.input_schema) for name, t in tools.items()}

    # ------------------------------------------------------------ catálogo para o LLM

    @property
    def tools(self) -> list[Tool]:
        return list(self._tools.values())

    def llm_tools(self) -> list[dict[str, Any]]:
        """Tools descobertas via MCP no formato de function calling do Ollama/OpenAI.

        Os JSON Schemas são repassados sem remover tipos, limites e descrições.
        """
        return [
            {
                "type": "function",
                "function": {"name": t.name, "description": t.description or "", "parameters": t.input_schema},
            }
            for t in self._tools.values()
        ]

    # ------------------------------------------------------------ chamadas

    def validate_arguments(self, name: str, arguments: Any) -> dict[str, Any]:
        """Allowlist + validação local contra o inputSchema anunciado (antes de ir ao servidor)."""
        if name not in self.allowed_tools or name not in self._tools:
            raise MCPClientError("INVALID_TOOL_ARGUMENTS", f"Tool não permitida: {name!r}", tool=name)
        if isinstance(arguments, str):  # alguns modelos devolvem argumentos como string JSON
            try:
                arguments = json.loads(arguments) if arguments.strip() else {}
            except json.JSONDecodeError:
                raise MCPClientError("INVALID_TOOL_ARGUMENTS", "Argumentos não são JSON válido.", tool=name) from None
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, Mapping):
            raise MCPClientError("INVALID_TOOL_ARGUMENTS", "Argumentos devem ser um objeto.", tool=name)
        arguments = dict(arguments)
        errors = sorted(self._validators[name].iter_errors(arguments), key=lambda e: list(e.path))
        if errors:
            first = errors[0]
            where = ".".join(str(p) for p in first.path) or "(raiz)"
            raise MCPClientError("INVALID_TOOL_ARGUMENTS", f"{where}: {first.message[:200]}", tool=name)
        return arguments

    async def call_tool(self, name: str, arguments: Any = None, *, request_id: str | None = None) -> ToolCallResult:
        started = time.perf_counter()
        try:
            result = await self._call(name, arguments, request_id)
        except MCPClientError as exc:
            self._record("call_tool", started, ok=False, tool=name, request_id=request_id, error_code=exc.code,
                         detail_code=exc.detail_code)
            logger.warning("request_id=%s tool=%s erro=%s", request_id, name, exc.code)
            raise
        self._record("call_tool", started, ok=True, tool=name, request_id=request_id,
                     business_error=result.error_code, ids=[e.get("recipe_id") for e in result.evidence])
        return result

    async def _call(self, name: str, arguments: Any, request_id: str | None) -> ToolCallResult:
        client = self._client
        if client is None or not self._connected:
            raise MCPClientError("MCP_UNAVAILABLE", "Sessão MCP não está ativa.", tool=name)
        args = self.validate_arguments(name, arguments)
        started = time.perf_counter()
        try:
            with anyio.fail_after(self.call_timeout + 5):  # rede de segurança além do timeout do SDK
                result = await client.call_tool(name, args, read_timeout_seconds=self.call_timeout)
        except TimeoutError:
            raise MCPClientError("UPSTREAM_TIMEOUT", "Tempo esgotado aguardando a ferramenta.", tool=name) from None
        except MCPError as exc:
            if exc.code == REQUEST_TIMEOUT:
                raise MCPClientError("UPSTREAM_TIMEOUT", "Tempo esgotado aguardando a ferramenta.", tool=name) from None
            if exc.code == CONNECTION_CLOSED:
                self._connected = False
                raise MCPClientError("MCP_UNAVAILABLE", "Conexão com o servidor MCP encerrada.", tool=name) from None
            raise MCPClientError("MCP_TOOL_ERROR", "Erro de protocolo ao chamar a ferramenta.", tool=name) from exc
        except (anyio.ClosedResourceError, anyio.BrokenResourceError, anyio.EndOfStream, OSError) as exc:
            self._connected = False
            raise MCPClientError("MCP_UNAVAILABLE", "Conexão com o servidor MCP encerrada.", tool=name) from exc
        except Exception as exc:  # ex.: structuredContent fora do outputSchema (validado pelo SDK)
            logger.error("resposta inválida da tool %s: %r", name, exc)
            raise MCPClientError("MCP_TOOL_ERROR", "Resposta inválida da ferramenta.", tool=name) from exc

        duration_ms = (time.perf_counter() - started) * 1000
        if result.is_error:
            text = " ".join(getattr(b, "text", "") for b in result.content)
            match = _SERVER_CODE_RE.search(text)
            server_code = match.group(1) if match else None
            if server_code == "INVALID_TOOL_ARGUMENTS" or (server_code is None and "validation error" in text):
                msg = text.split(":", 2)[-1].strip()[:200] if server_code else "Argumentos rejeitados pelo servidor."
                raise MCPClientError("INVALID_TOOL_ARGUMENTS", msg, tool=name, detail_code=server_code)
            raise MCPClientError("MCP_TOOL_ERROR", "A ferramenta retornou erro.", tool=name, detail_code=server_code)
        if not isinstance(result.structured_content, dict):
            raise MCPClientError("MCP_TOOL_ERROR", "A ferramenta não retornou conteúdo estruturado.", tool=name)
        return ToolCallResult(name=name, data=result.structured_content, duration_ms=duration_ms, request_id=request_id)

    async def ping(self) -> bool:
        """Verificação leve para /ready: um `tools/list` real, sem cache (ping saiu do protocolo 2026-07-28)."""
        if self._client is None or not self._connected:
            return False
        try:
            with anyio.fail_after(5):
                listed = await self._client.list_tools(cache_mode="bypass")
            return self.allowed_tools <= {t.name for t in listed.tools}
        except Exception:  # noqa: BLE001
            self._connected = False
            return False

    # ------------------------------------------------------------ rastreio sanitizado

    def _record(self, event: str, started: float, **fields: Any) -> None:
        entry = {"ts": time.time(), "event": event, "duration_ms": round((time.perf_counter() - started) * 1000, 1)}
        entry.update({k: v for k, v in fields.items() if v is not None})
        self.trace.append(entry)

    def trace_for(self, request_id: str) -> list[dict[str, Any]]:
        return [e for e in self.trace if e.get("request_id") == request_id]


def evidence_set(results: Iterable[ToolCallResult]) -> dict[str, dict[str, str]]:
    """recipe_id -> fonte, a partir das chamadas MCP do turno (base do guardrail de saída)."""
    out: dict[str, dict[str, str]] = {}
    for r in results:
        for e in r.evidence:
            out.setdefault(e["recipe_id"], e)
    return out
