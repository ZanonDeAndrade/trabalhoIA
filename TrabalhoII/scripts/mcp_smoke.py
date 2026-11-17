"""Smoke test / evidência do MCP real: initialize -> tools/list -> tools/call das 3 tools.

Executar com o venv do BACKEND (o servidor sobe com o venv de mcp-server/):

    backend/.venv/bin/python scripts/mcp_smoke.py              # corpus real (data/normalized + rag/)
    backend/.venv/bin/python scripts/mcp_smoke.py --fixtures   # dados sintéticos de teste

Salva um trace sanitizado em tests/evidence/mcp_smoke_<data>.json (sem texto do usuário além
das consultas de exemplo deste script).
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import anyio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.integrations.mcp_client import MCPClient, MCPClientError  # noqa: E402


async def main(args: argparse.Namespace) -> int:
    if args.fixtures:
        fx = ROOT / "mcp-server" / "tests" / "fixtures"
        os.environ.update(
            RECIPES_JSON=str(fx / "recipes.json"), RAG_RETRIEVER="fixture_retriever:retrieve", PYTHONPATH=str(fx)
        )
    report: dict = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "fixtures": args.fixtures, "calls": []}
    async with MCPClient.from_env(project_root=ROOT) as mcp:
        report["tools"] = [
            {"name": t.name, "description": t.description, "input_schema": t.input_schema} for t in mcp.tools
        ]
        print(f"[ok] initialize + tools/list: {[t.name for t in mcp.tools]}")
        plan = [
            ("list_topics", {"include_counts": True}),
            ("search_knowledge", {"query": args.query, "available_ingredients": args.ingredients}),
            ("search_knowledge", {"query": "receita de lagosta ao molho de champanhe"}),
            ("get_document", {"recipe_id": "id-inexistente-v9"}),
        ]
        for i, (name, call_args) in enumerate(plan):
            try:
                r = await mcp.call_tool(name, call_args, request_id=f"smoke-{i}")
                report["calls"].append({"tool": name, "arguments": call_args, "ok": True, "result": r.data})
                print(f"[ok] {name} ({r.duration_ms:.0f} ms) erro_negocio={r.error_code} fontes={r.evidence}")
                if name == "search_knowledge" and r.data.get("results"):
                    rid = r.data["results"][0]["recipe_id"]
                    d = await mcp.call_tool("get_document", {"recipe_id": rid}, request_id=f"smoke-{i}-doc")
                    report["calls"].append({"tool": "get_document", "arguments": {"recipe_id": rid}, "ok": True,
                                            "result": d.data})
                    print(f"[ok] get_document({rid}) found={d.data['found']}")
            except MCPClientError as exc:
                report["calls"].append({"tool": name, "arguments": call_args, "ok": False,
                                        "error": {"code": exc.code, "detail_code": exc.detail_code}})
                print(f"[erro] {name}: {exc.code} {exc.detail_code or ''}")
        report["trace"] = list(mcp.trace)

    out = ROOT / "tests" / "evidence" / f"mcp_smoke_{time.strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"evidência salva em {out.relative_to(ROOT)}")
    if not report["calls"][0].get("result", {}).get("corpus_ready"):
        print("[aviso] corpus não preparado (CORPUS_EMPTY): rode a ingestão do RAG antes da evidência final")
        return 2
    return 0 if all(c["ok"] for c in report["calls"]) else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--fixtures", action="store_true", help="usar dados sintéticos de teste")
    p.add_argument("--query", default="o que posso fazer com ovos e queijo?")
    p.add_argument("--ingredients", nargs="*", default=["ovos", "queijo"])
    sys.exit(anyio.run(main, p.parse_args()))
