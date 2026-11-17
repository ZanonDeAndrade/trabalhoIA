"""Integração cliente MCP (backend) <-> servidor MCP (subprocesso stdio real).

Sem mocks de protocolo: o cliente inicia mcp-server/server.py, faz initialize, tools/list e
tools/call. Apenas o índice vetorial é o retriever de fixture até o RAG real existir.
Requer o venv do servidor em mcp-server/.venv (ver mcp-server/README.md).
"""

import ast
import os
import signal
import uuid
from pathlib import Path

import anyio
import pytest

from app.integrations.mcp_client import MCPClient, MCPClientError, evidence_set

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "mcp-server" / "tests" / "fixtures"


@pytest.fixture
def mcp_env(monkeypatch):
    marker = uuid.uuid4().hex
    monkeypatch.setenv("RECIPES_JSON", str(FIXTURES / "recipes.json"))
    monkeypatch.setenv("RAG_RETRIEVER", "fixture_retriever:retrieve")
    monkeypatch.setenv("PYTHONPATH", str(FIXTURES))
    monkeypatch.setenv("MCP_LOG_LEVEL", "WARNING")
    monkeypatch.delenv("MCP_COMMAND", raising=False)
    monkeypatch.delenv("MCP_SCRIPT", raising=False)
    return marker


def make_client(marker, **overrides):
    c = MCPClient.from_env(project_root=ROOT)
    c.env["MCP_TEST_MARKER"] = marker
    for k, v in overrides.items():
        if k.isupper():
            c.env[k] = str(v)
        else:
            setattr(c, k, v)
    return c


def server_pids(marker):
    pids = []
    for p in Path("/proc").iterdir():
        if p.name.isdigit():
            try:
                if f"MCP_TEST_MARKER={marker}".encode() in (p / "environ").read_bytes():
                    pids.append(int(p.name))
            except OSError:
                pass
    return pids


@pytest.mark.anyio
async def test_handshake_discovery_and_llm_catalog(mcp_env):
    async with make_client(mcp_env) as mcp:
        assert mcp.connected
        events = [e["event"] for e in mcp.trace]
        assert events[:2] == ["initialize", "list_tools"]
        assert mcp.trace[0]["protocol"]

        catalog = {t["function"]["name"]: t for t in mcp.llm_tools()}
        assert set(catalog) == {"search_knowledge", "get_document", "list_topics"}
        for t in catalog.values():
            assert t["type"] == "function" and t["function"]["description"]
            assert t["function"]["parameters"]["type"] == "object"
        params = catalog["search_knowledge"]["function"]["parameters"]
        # schema repassado sem perder tipos/limites/descrições
        assert params["properties"]["top_k"]["maximum"] == 10
        assert params["properties"]["query"]["description"]
        assert await mcp.ping()


@pytest.mark.anyio
async def test_calls_each_tool_and_builds_evidence(mcp_env):
    async with make_client(mcp_env) as mcp:
        rid = "req-1"
        topics = await mcp.call_tool("list_topics", {}, request_id=rid)
        assert topics.data["corpus_ready"] and topics.data["total_topics"] == 3

        search = await mcp.call_tool(
            "search_knowledge", {"query": "omelete com queijo", "available_ingredients": ["ovos", "queijo"]},
            request_id=rid,
        )
        assert search.data["evidence_status"] == "FOUND"
        top = search.data["results"][0]
        assert top["recipe_id"] == "fx-001-v1" and top["compatibility"] == "COMPLETE"

        doc = await mcp.call_tool("get_document", {"recipe_id": top["recipe_id"]}, request_id=rid)
        assert doc.data["found"] and doc.data["recipe"]["instructions"]
        assert doc.to_llm_content().startswith('{"found": true')

        missing = await mcp.call_tool("get_document", {"recipe_id": "fx-404-v1"}, request_id=rid)
        assert missing.error_code == "DOCUMENT_NOT_FOUND" and missing.evidence == []

        ev = evidence_set([topics, search, doc, missing])
        assert ev["fx-001-v1"] == {
            "recipe_id": "fx-001-v1", "document_id": "fx-001",
            "title": "[FIXTURE] Omelete de queijo", "source_url": "https://example.org/fixture/omelete",
        }
        calls = [e for e in mcp.trace_for(rid) if e["event"] == "call_tool"]
        assert [c["tool"] for c in calls] == ["list_topics", "search_knowledge", "get_document", "get_document"]
        assert all(c["ok"] and c["duration_ms"] >= 0 for c in calls)
        assert calls[1]["ids"][0] == "fx-001-v1"
        assert "arguments" not in calls[1] and "query" not in calls[1]  # trace não guarda texto do usuário


@pytest.mark.anyio
@pytest.mark.parametrize(
    "name,args",
    [
        ("delete_everything", {}),
        ("search_knowledge", {"query": "omelete", "top_k": 100000}),
        ("search_knowledge", {"top_k": 3}),
        ("search_knowledge", "não é json"),
        ("search_knowledge", ["lista"]),
        ("get_document", {"recipe_id": "Nome Com Espaço"}),
    ],
)
async def test_rejects_disallowed_tools_and_invalid_args_locally(mcp_env, name, args):
    async with make_client(mcp_env) as mcp:
        with pytest.raises(MCPClientError) as exc:
            await mcp.call_tool(name, args)
        assert exc.value.code == "INVALID_TOOL_ARGUMENTS"
        assert mcp.trace[-1]["error_code"] == "INVALID_TOOL_ARGUMENTS"


@pytest.mark.anyio
async def test_string_json_arguments_are_accepted(mcp_env):
    async with make_client(mcp_env) as mcp:
        r = await mcp.call_tool("search_knowledge", '{"query": "brigadeiro"}')
        assert r.data["evidence_status"] == "FOUND"


@pytest.mark.anyio
async def test_server_side_errors_are_mapped(mcp_env):
    async with make_client(mcp_env) as mcp:
        with pytest.raises(MCPClientError) as exc:
            await mcp.call_tool("search_knowledge", {"query": "omelete", "topic_key": "inexistente"})
        assert exc.value.code == "INVALID_TOOL_ARGUMENTS" and "Valores válidos" in exc.value.message

    async with make_client(mcp_env, FIXTURE_RETRIEVER_MODE="broken") as mcp:
        with pytest.raises(MCPClientError) as exc:
            await mcp.call_tool("search_knowledge", {"query": "omelete"})
        assert (exc.value.code, exc.value.detail_code) == ("MCP_TOOL_ERROR", "RAG_ERROR")
        assert mcp.connected  # erro de tool não derruba a sessão


@pytest.mark.anyio
async def test_empty_corpus_is_structured_not_exception(mcp_env):
    async with make_client(mcp_env, RECIPES_JSON=FIXTURES / "empty_recipes.json") as mcp:
        r = await mcp.call_tool("search_knowledge", {"query": "omelete"})
        assert r.error_code == "CORPUS_EMPTY" and r.data["evidence_status"] == "INSUFFICIENT"
        assert (await mcp.call_tool("list_topics")).data["corpus_ready"] is False


@pytest.mark.anyio
async def test_timeout_then_session_still_usable(mcp_env):
    client = make_client(mcp_env, FIXTURE_RETRIEVER_MODE="slow", FIXTURE_RETRIEVER_SLEEP=3, call_timeout=1.0)
    async with client as mcp:
        with anyio.fail_after(10):
            with pytest.raises(MCPClientError) as exc:
                await mcp.call_tool("search_knowledge", {"query": "omelete"})
        assert exc.value.code == "UPSTREAM_TIMEOUT"
        assert (await mcp.call_tool("list_topics")).data["corpus_ready"] is True


@pytest.mark.anyio
async def test_concurrent_calls_share_one_session(mcp_env):
    async with make_client(mcp_env) as mcp:
        results = {}

        async def one(i):
            results[i] = await mcp.call_tool("search_knowledge", {"query": "omelete queijo"}, request_id=f"r{i}")

        async with anyio.create_task_group() as tg:
            for i in range(6):
                tg.start_soon(one, i)
        assert all(r.data["evidence_status"] == "FOUND" for r in results.values())
        assert len(server_pids(mcp_env)) == 1


@pytest.mark.anyio
async def test_server_crash_yields_mcp_unavailable(mcp_env):
    async with make_client(mcp_env) as mcp:
        await mcp.call_tool("list_topics")
        for pid in server_pids(mcp_env):
            os.kill(pid, signal.SIGKILL)
        await anyio.sleep(0.3)
        with anyio.fail_after(10):
            with pytest.raises(MCPClientError) as exc:
                await mcp.call_tool("list_topics")
        assert exc.value.code == "MCP_UNAVAILABLE"
        assert not mcp.connected and not await mcp.ping()
        with pytest.raises(MCPClientError) as exc:  # chamadas seguintes falham rápido
            await mcp.call_tool("list_topics")
        assert exc.value.code == "MCP_UNAVAILABLE"


@pytest.mark.anyio
@pytest.mark.parametrize("override", [{"args": ["/nao/existe/server.py"]}, {"command": "/nao/existe/python"}])
async def test_unstartable_server(mcp_env, override):
    client = make_client(mcp_env, startup_timeout=10, **override)
    with pytest.raises(MCPClientError) as exc:
        await client.start()
    assert exc.value.code == "MCP_UNAVAILABLE" and not client.connected
    with pytest.raises(MCPClientError):
        await client.call_tool("list_topics")


@pytest.mark.anyio
async def test_close_terminates_subprocess(mcp_env):
    mcp = make_client(mcp_env)
    await mcp.start()
    assert len(server_pids(mcp_env)) == 1
    await mcp.close()
    await anyio.sleep(0.2)
    assert server_pids(mcp_env) == [] and not mcp.connected


def test_backend_does_not_import_tools_or_rag_directly():
    """RF02: o backend só acessa as tools pelo protocolo MCP."""
    forbidden = {"rag", "tools", "store", "models", "server"}
    for path in (ROOT / "backend" / "app").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                names = [node.module]
            for n in names:
                assert n.split(".")[0] not in forbidden, f"{path}: import proibido {n}"
