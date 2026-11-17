# Trabalho II — Assistente Inteligente de Receitas

Especificação completa e os 45 prompts de implementação: [`docs/`](docs/).

| Componente | Pasta | Situação |
|---|---|---|
| Servidor MCP (stdio, 3 tools) | [`mcp-server/`](mcp-server/) | implementado e testado — ver [README](mcp-server/README.md) |
| Cliente MCP do backend | [`backend/app/integrations/`](backend/app/integrations/) | implementado e testado |
| RAG (ingestão, embeddings, Chroma) | `rag/` | pendente (equipe RAG) — contrato em [`mcp-server/README.md`](mcp-server/README.md#contrato-com-o-rag-equipe-rag) |
| Backend FastAPI / LLM / guardrails | `backend/` | pendente |
| Frontend React | `frontend/` | pendente (equipe front) |

Os comandos abaixo devem ser executados a partir desta pasta (`TrabalhoII/`):

```bash
cd mcp-server && uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -e ".[test]" && .venv/bin/python -m pytest -q
cd ../backend && uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -e ".[test]" && .venv/bin/python -m pytest -q
cd .. && backend/.venv/bin/python scripts/mcp_smoke.py --fixtures
```
