"""Testes do servidor MCP.

- Unitários: funções puras (normalização, compatibilidade, carga do corpus).
- Protocolo: sobem `server.py` como SUBPROCESSO e falam com ele pelo cliente oficial do SDK
  via stdio (initialize -> tools/list -> tools/call). Nada aqui chama as tools diretamente.

O índice vetorial é substituído por `fixtures/fixture_retriever.py` até o RAG existir.
"""

import json
import os
import re
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from mcp import Client
from mcp.client.stdio import StdioServerParameters

from conftest import FIXTURES, SERVER_DIR

RECIPES = FIXTURES / "recipes.json"
EMPTY = FIXTURES / "empty_recipes.json"


@asynccontextmanager
async def server(**env):
    base = {
        "RECIPES_JSON": str(RECIPES),
        "RAG_RETRIEVER": "fixture_retriever:retrieve",
        "PYTHONPATH": str(FIXTURES),
        "MCP_LOG_LEVEL": "WARNING",
    }
    base.update({k: str(v) for k, v in env.items()})
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER_DIR / "server.py")], env=base)
    async with Client(params, mode="legacy", read_timeout_seconds=30) as client:
        yield client


async def call(client, name, args=None):
    r = await client.call_tool(name, args or {})
    text = " ".join(getattr(b, "text", "") for b in r.content)
    return r, text


def error_code(text):
    m = re.search(r"\b([A-Z][A-Z_]{3,}):", text)
    return m.group(1) if m else ("VALIDATION" if "validation error" in text else None)


# ============================================================ unitários

from store import RecipeStore, basic_normalize  # noqa: E402
from tools import compute_compatibility  # noqa: E402


def _recipes():
    return RecipeStore(RECIPES).snapshot().recipes


def test_basic_normalize():
    assert basic_normalize("  Ovos ") == "ovo"
    assert basic_normalize("Tomates") == "tomate"
    assert basic_normalize("Chocolate em Pó") == "chocolate em po"
    assert basic_normalize("farinha de trigo") != basic_normalize("farinha de aveia")


def test_store_rejects_invalid_records():
    snap = RecipeStore(RECIPES).snapshot()
    assert set(snap.recipes) == {"fx-001-v1", "fx-002-v1", "fx-003-v1", "fx-003-v2"}
    assert snap.ready and snap.data_version


def test_store_missing_file(tmp_path):
    snap = RecipeStore(tmp_path / "nao.json").snapshot()
    assert not snap.ready and snap.load_error == "FILE_NOT_FOUND"


def test_compatibility_rules():
    r = _recipes()
    omelete, panqueca = r["fx-001-v1"], r["fx-002-v1"]
    c = compute_compatibility(omelete, ["Ovos", "queijo"], basic_normalize)
    assert (c.status, c.missing, c.total_required) == ("COMPLETE", [], 2)  # sal é opcional (RN07)
    c = compute_compatibility(omelete, ["ovo"], basic_normalize)
    assert (c.status, c.available, c.missing) == ("PARTIAL", ["ovos"], ["queijo"])
    c = compute_compatibility(omelete, ["arroz"], basic_normalize)
    assert c.status == "NO_MATCH"
    c = compute_compatibility(omelete, None, basic_normalize)
    assert c.status == "NOT_EVALUATED"
    # Alternativa documentada (água) NÃO equivale a leite (RN03)
    c = compute_compatibility(panqueca, ["farinha de trigo", "água", "ovo"], basic_normalize)
    assert (c.status, c.missing) == ("PARTIAL", ["leite"])
    # farinha genérica não vira farinha de trigo
    c = compute_compatibility(panqueca, ["farinha", "leite", "ovo"], basic_normalize)
    assert c.missing == ["farinha de trigo"]


# ============================================================ protocolo MCP real (stdio)


@pytest.mark.anyio
async def test_initialize_and_discover_three_tools():
    async with server() as client:
        assert client.server_info.name == "receitas-mcp"
        tools = {t.name: t for t in (await client.list_tools()).tools}
        assert set(tools) == {"search_knowledge", "get_document", "list_topics"}
        for t in tools.values():
            assert t.description and len(t.description) > 40
            assert t.input_schema["type"] == "object"
            assert t.output_schema and t.output_schema["type"] == "object"
            assert t.annotations.read_only_hint is True
        sk = tools["search_knowledge"].input_schema
        assert sk["required"] == ["query"]
        assert sk["properties"]["query"]["maxLength"] == 500
        assert sk["properties"]["top_k"]["maximum"] == 10
        assert set(sk["properties"]) == {"query", "available_ingredients", "topic_key", "top_k"}
        assert tools["get_document"].input_schema["required"] == ["recipe_id"]
        assert "include_counts" in tools["list_topics"].input_schema["properties"]
        assert set(tools["search_knowledge"].output_schema["properties"]) >= {
            "query", "evidence_status", "retrieved_count", "results"
        }


@pytest.mark.anyio
async def test_search_knowledge_complete_partial_and_not_evaluated():
    async with server() as client:
        r, _ = await call(client, "search_knowledge", {"query": "omelete com ovos e queijo", "available_ingredients": ["Ovos", "queijo"]})
        out = r.structured_content
        assert not r.is_error and out["evidence_status"] == "FOUND"
        top = out["results"][0]
        assert top["recipe_id"] == "fx-001-v1" and top["document_id"] == "fx-001"
        assert top["compatibility"] == "COMPLETE" and top["missing_ingredients"] == []
        assert top["source_url"] == "https://example.org/fixture/omelete"
        assert top["matched_chunks"][0]["chunk_id"] == "fx-001-v1-c0"
        assert out["retrieved_count"] == len(out["results"]) <= 5

        r, _ = await call(client, "search_knowledge", {"query": "panqueca com ovo", "available_ingredients": ["ovo", "leite"]})
        pan = next(x for x in r.structured_content["results"] if x["recipe_id"] == "fx-002-v1")
        assert pan["compatibility"] == "PARTIAL" and pan["missing_ingredients"] == ["farinha de trigo"]

        r, _ = await call(client, "search_knowledge", {"query": "como fazer brigadeiro"})
        res = r.structured_content["results"]
        assert {x["recipe_id"] for x in res} >= {"fx-003-v1", "fx-003-v2"}  # variantes não são amalgamadas
        assert all(x["compatibility"] == "NOT_EVALUATED" for x in res)


@pytest.mark.anyio
async def test_search_knowledge_topic_filter_and_insufficient():
    async with server() as client:
        r, _ = await call(client, "search_knowledge", {"query": "receita com leite", "topic_key": "sobremesas"})
        assert {x["topic_key"] for x in r.structured_content["results"]} == {"sobremesas"}

        r, _ = await call(client, "search_knowledge", {"query": "lagosta flambada ao conhaque"})
        out = r.structured_content
        assert not r.is_error
        assert out["evidence_status"] == "INSUFFICIENT" and out["results"] == [] and out["retrieved_count"] == 0


@pytest.mark.anyio
@pytest.mark.parametrize(
    "args,expected",
    [
        ({"query": "ab"}, "VALIDATION"),
        ({"query": ""}, "VALIDATION"),
        ({}, "VALIDATION"),
        ({"query": "x" * 501}, "VALIDATION"),
        ({"query": "omelete", "top_k": 100000}, "VALIDATION"),  # SEC08
        ({"query": "omelete", "top_k": 0}, "VALIDATION"),
        ({"query": "omelete", "available_ingredients": ["ovo"] * 31}, "VALIDATION"),
        ({"query": "omelete", "available_ingredients": ["x" * 81]}, "VALIDATION"),
        ({"query": "omelete", "topic_key": "Inexistente!"}, "VALIDATION"),
        ({"query": "omelete", "topic_key": "inexistente"}, "INVALID_TOOL_ARGUMENTS"),
        ({"query": "ome\x00lete"}, "INVALID_TOOL_ARGUMENTS"),
        ({"query": "    a    "}, "INVALID_TOOL_ARGUMENTS"),
    ],
)
async def test_search_knowledge_rejects_invalid_arguments(args, expected):
    async with server() as client:
        r, text = await call(client, "search_knowledge", args)
        assert r.is_error and r.structured_content is None
        assert error_code(text) == expected, text


@pytest.mark.anyio
async def test_search_discards_hits_without_corpus_backing():
    async with server(FIXTURE_RETRIEVER_MODE="bogus") as client:
        r, _ = await call(client, "search_knowledge", {"query": "omelete queijo"})
        out = r.structured_content
        ids = {x["recipe_id"] for x in out["results"]}
        assert "nao-existe-v1" not in ids
        assert out["discarded_hits"] == 3  # ID inexistente, document_id trocado, hit malformado
        omelete = next(x for x in out["results"] if x["recipe_id"] == "fx-001-v1")
        assert all(c["chunk_id"] != "y-c0" for c in omelete["matched_chunks"])


@pytest.mark.anyio
async def test_get_document():
    async with server() as client:
        r, _ = await call(client, "get_document", {"recipe_id": "fx-002-v1"})
        out = r.structured_content
        assert out["found"] is True and out["error"] is None
        rec = out["recipe"]
        assert rec["instructions"] == ["Misture (teste).", "Frite (teste)."]
        assert rec["ingredients"][1]["alternatives_documented"] == ["água"]
        assert rec["optional_fields"] == {"portions": "4", "preparation_time": None, "temperature": None}
        assert rec["source_url"] == "https://example.org/fixture/panqueca"

        r, _ = await call(client, "get_document", {"recipe_id": "fx-404-v1"})
        assert not r.is_error
        assert r.structured_content == {
            "found": False, "recipe": None,
            "error": {"code": "DOCUMENT_NOT_FOUND", "message": "Nenhuma receita com este recipe_id."},
        }
        # Documento (página) não é receita: document_id não deve resolver
        r, _ = await call(client, "get_document", {"recipe_id": "fx-003"})
        assert r.structured_content["found"] is False

        for bad in [{"recipe_id": "Omelete de queijo"}, {"recipe_id": ""}, {}, {"recipe_id": "../etc/passwd"}]:
            r, text = await call(client, "get_document", bad)
            assert r.is_error and error_code(text) == "VALIDATION", bad


@pytest.mark.anyio
async def test_list_topics_matches_normalized_json():
    valid = _recipes()
    expected = {}
    for rec in valid.values():
        expected[rec.topic_key] = expected.get(rec.topic_key, 0) + 1
    async with server() as client:
        r, _ = await call(client, "list_topics")
        out = r.structured_content
        assert out["corpus_ready"] is True
        assert {t["topic_key"]: t["recipe_count"] for t in out["topics"]} == expected
        assert [t["topic_key"] for t in out["topics"]] == sorted(expected)
        assert out["total_topics"] == len(expected) and out["total_recipes"] == len(valid)
        assert next(t for t in out["topics"] if t["topic_key"] == "massas")["label"] == "Massas"

        r, _ = await call(client, "list_topics", {"include_counts": False})
        assert all(t["recipe_count"] is None for t in r.structured_content["topics"])


@pytest.mark.anyio
@pytest.mark.parametrize("recipes_path", [EMPTY, FIXTURES / "nao_existe.json"])
async def test_empty_corpus(recipes_path):
    async with server(RECIPES_JSON=recipes_path) as client:
        assert len((await client.list_tools()).tools) == 3  # servidor sobe mesmo sem corpus
        r, _ = await call(client, "list_topics")
        assert r.structured_content["corpus_ready"] is False and r.structured_content["topics"] == []
        r, _ = await call(client, "search_knowledge", {"query": "omelete"})
        out = r.structured_content
        assert out["evidence_status"] == "INSUFFICIENT" and out["error"]["code"] == "CORPUS_EMPTY"
        r, _ = await call(client, "get_document", {"recipe_id": "fx-001-v1"})
        assert r.structured_content["error"]["code"] == "CORPUS_EMPTY"


@pytest.mark.anyio
async def test_stdout_noise_does_not_corrupt_protocol():
    async with server(FIXTURE_RETRIEVER_MODE="noisy") as client:
        for _ in range(3):
            r, _ = await call(client, "search_knowledge", {"query": "omelete queijo"})
            assert r.structured_content["evidence_status"] == "FOUND"


@pytest.mark.anyio
async def test_retriever_failure_is_sanitized():
    async with server(FIXTURE_RETRIEVER_MODE="broken") as client:
        r, text = await call(client, "search_knowledge", {"query": "omelete"})
        assert r.is_error and error_code(text) == "RAG_ERROR"
        assert "secreto" not in text and "Traceback" not in text
        r, _ = await call(client, "list_topics")  # demais tools continuam funcionando
        assert r.structured_content["corpus_ready"] is True


@pytest.mark.anyio
async def test_rag_module_missing():
    async with server(RAG_RETRIEVER="rag_que_nao_existe.retrieve:retrieve") as client:
        r, text = await call(client, "search_knowledge", {"query": "omelete"})
        assert r.is_error and error_code(text) == "RAG_UNAVAILABLE"
        r, _ = await call(client, "get_document", {"recipe_id": "fx-001-v1"})
        assert r.structured_content["found"] is True


def _pids_with_marker(marker):
    pids = []
    for p in Path("/proc").iterdir():
        if p.name.isdigit():
            try:
                if marker.encode() in (p / "environ").read_bytes():
                    pids.append(int(p.name))
            except OSError:
                pass
    return pids


@pytest.mark.anyio
@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="usa /proc")
async def test_shutdown_leaves_no_process():
    marker = f"MCP_TEST_MARKER={uuid.uuid4().hex}"
    async with server(MCP_TEST_MARKER=marker.split("=")[1]) as client:
        await call(client, "list_topics")
        assert _pids_with_marker(marker), "servidor deveria estar rodando"
    assert _pids_with_marker(marker) == []


@pytest.mark.anyio
async def test_corpus_reload_after_reingestion(tmp_path):
    path = tmp_path / "recipes.json"
    data = json.loads(RECIPES.read_text())
    path.write_text(json.dumps({"recipes": data["recipes"][:1]}))
    async with server(RECIPES_JSON=path) as client:
        r, _ = await call(client, "list_topics")
        assert r.structured_content["total_recipes"] == 1
        path.write_text(json.dumps({"recipes": data["recipes"][:3]}))
        os.utime(path, (1e9, 2e9))
        r, _ = await call(client, "list_topics")
        assert r.structured_content["total_recipes"] == 3
