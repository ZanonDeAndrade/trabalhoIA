# Servidor e cliente MCP — Assistente Inteligente de Receitas

Implementa o **RF02** (prompts 13 a 18 da documentação): um servidor MCP real, com SDK oficial
Python **v2 (`mcp==2.3.0`, classe `MCPServer`)** e transporte **stdio**, que expõe três tools
tipadas, e o **cliente MCP do backend** que inicia o servidor, faz o handshake e chama as tools
pelo protocolo.

```
backend (FastAPI)                         mcp-server (subprocesso)
app/integrations/mcp_client.py  ──stdio──▶ server.py ─▶ tools.py ─▶ store.py ─▶ rag/retrieve.py  (equipe RAG)
  initialize / tools/list / tools/call                                  └──▶ data/normalized/recipes.json
```

O backend **não importa** `rag/` nem as tools. Um teste (`test_backend_does_not_import_tools_or_rag_directly`)
garante isso.

## Situação

| Item | Situação |
|---|---|
| Servidor MCP stdio + 3 tools | **Implementado e testado** (29 testes, todos via subprocesso stdio real) |
| Cliente MCP no backend | **Implementado e testado** (18 testes de integração com o servidor real) |
| Busca vetorial real (Chroma + embeddings) | **Pendente, responsabilidade da equipe RAG.** Nos testes, o índice é substituído por `tests/fixtures/fixture_retriever.py`. O protocolo MCP continua real. |
| Evidência com o corpus real | **Pendente.** Rodar `scripts/mcp_smoke.py` depois da ingestão |

Os dados de `tests/fixtures/` são **sintéticos** (títulos `[FIXTURE]`, URLs `example.org`). Não são receitas do corpus.

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `server.py` | entrypoint stdio, registro das tools (descrições, tipos e limites), logs em stderr, conversão de falhas em erro MCP |
| `tools.py` | lógica das 3 tools e cálculo de compatibilidade de ingredientes (função pura) |
| `models.py` | contratos de saída (viram o `outputSchema` das tools) |
| `store.py` | leitura e validação do `recipes.json` (recarrega quando o arquivo muda) e adaptador do retriever RAG; **único** ponto que conhece `rag/` |
| `tests/test_tools.py` | testes unitários e de protocolo |
| `../backend/app/integrations/mcp_client.py` | cliente MCP do backend |
| `../backend/tests/test_mcp_integration.py` | integração cliente ↔ servidor |
| `../scripts/mcp_smoke.py` | smoke test que salva a evidência em `tests/evidence/` |

## Instalação (Ubuntu)

Testado com Python 3.12 e `uv`. O `pip` também funciona.

```bash
# servidor MCP (no mesmo venv entram as dependências do RAG, porque o servidor importa rag.retrieve)
cd mcp-server
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[test]"
# depois que o RAG existir:  uv pip install --python .venv/bin/python -r ../rag/requirements.txt  (ou -e ../rag)

# cliente (venv do backend)
cd ../backend
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -e ".[test]"
```

## Execução e testes

```bash
cd mcp-server && .venv/bin/python -m pytest -q        # 29 passed
cd backend    && .venv/bin/python -m pytest -q        # 18 passed (sobe o servidor de mcp-server/.venv)

# evidência do protocolo (initialize -> tools/list -> tools/call)
backend/.venv/bin/python scripts/mcp_smoke.py --fixtures   # com dados sintéticos
backend/.venv/bin/python scripts/mcp_smoke.py              # com o corpus real (após a ingestão)
```

O servidor não precisa ser iniciado à mão: o backend o inicia. Para inspecionar manualmente:
`npx @modelcontextprotocol/inspector mcp-server/.venv/bin/python mcp-server/server.py`.

## Variáveis de ambiente

| Variável | Padrão | Quem usa |
|---|---|---|
| `PROJECT_ROOT` | raiz do repositório | cliente e servidor (resolução de caminhos relativos) |
| `MCP_COMMAND` | `mcp-server/.venv/bin/python` (se existir) | cliente |
| `MCP_SCRIPT` | `mcp-server/server.py` | cliente |
| `MCP_STARTUP_TIMEOUT` / `MCP_CALL_TIMEOUT` | `30` / `60` s | cliente |
| `RECIPES_JSON` | `data/normalized/recipes.json` | servidor |
| `RAG_RETRIEVER` | `rag.retrieve:retrieve` | servidor |
| `RAG_NORMALIZER` | `rag.ingredients:normalize_ingredient` | servidor (opcional) |
| `RAG_TOP_K` | `8` | servidor (padrão do `top_k`) |
| `CHROMA_PATH`, `EMBEDDING_MODEL`, `HF_*` | — | repassadas ao subprocesso para o RAG |
| `MCP_LOG_LEVEL` | `INFO` | servidor (logs em stderr) |

O subprocesso recebe só o ambiente mínimo do SDK (PATH, HOME...) mais as variáveis acima.
Nenhuma chave do backend é herdada.

> Diferença em relação a `docs/10-development/setup.md`: o `.env.example` de lá cita
> `MCP_SCRIPT=mcp-server/src/server.py`, mas a árvore oficial (`project-structure.md`) usa
> `mcp-server/server.py`. Segui a árvore.

## Tools

Todas são somente leitura (`readOnlyHint=true`). Os argumentos são validados por JSON Schema
no servidor e, antes de sair do backend, também no cliente.

### `search_knowledge(query, available_ingredients?, topic_key?, top_k=8)`
- `query` com 3 a 500 caracteres (caracteres de controle são rejeitados); `available_ingredients` com até 30 itens de 1 a 80 caracteres;
  `topic_key` precisa existir no corpus; `top_k` de 1 a 10.
- Faz o top-k no índice, descarta hits cujo `recipe_id`/`document_id` não batem com o `recipes.json`,
  deduplica por `recipe_id`, calcula a compatibilidade e ordena por (proporção de obrigatórios presentes,
  distância, ordem do índice). Retorna no máximo 5 receitas.
- Saída: `{query, evidence_status: FOUND|INSUFFICIENT, retrieved_count, chunks_retrieved, discarded_hits,
  results: [{recipe_id, document_id, title, topic_key, source_url, source_excerpt, available_ingredients,
  missing_ingredients, matched_required, total_required, compatibility, distance, matched_chunks[]}], error?}`.
- `compatibility`:
  - `COMPLETE`: todos os obrigatórios foram informados.
  - `PARTIAL`: alguns foram informados.
  - `NO_MATCH`: ingredientes foram informados, mas nenhum obrigatório coincide.
  - `NOT_EVALUATED`: o usuário não informou ingredientes.

  Os dois últimos valores **foram acrescentados ao contrato** para nunca dizer `COMPLETE` sem base.
  Opcionais não contam (RN07). Alternativas documentadas não equivalem ao ingrediente (RN03).
  "farinha" não casa com "farinha de trigo".

### `get_document(recipe_id)`
- Aceita só `recipe_id` (padrão `[a-z0-9][a-z0-9_.-]*`). Um `document_id` (página) não resolve.
- Saída: `{found, recipe?: {recipe_id, document_id, variant_index, title, topic_key, ingredients[], instructions[],
  source_url, license, revision_url, retrieved_at, optional_fields{portions, preparation_time, temperature}}, error?}`.
- ID inexistente: `found=false`, `error.code=DOCUMENT_NOT_FOUND`. Nunca devolve outra receita.

### `list_topics(include_counts=true)`
- Os tópicos são derivados das receitas válidas do `recipes.json`, ordenados por `topic_key`.
- Saída: `{topics: [{topic_key, label, recipe_count}], total_topics, total_recipes, corpus_ready, data_version, error?}`.

### Erros

| Onde | Código | Significado |
|---|---|---|
| saída estruturada (`error.code`) | `CORPUS_EMPTY` | `recipes.json` ausente, vazio ou inválido |
| saída estruturada | `DOCUMENT_NOT_FOUND` | `recipe_id` inexistente |
| `isError` do MCP | `INVALID_TOOL_ARGUMENTS` | argumento fora do schema, `topic_key` desconhecido, caracteres de controle |
| `isError` do MCP | `RAG_UNAVAILABLE` / `RAG_ERROR` | módulo RAG ausente / exceção no retriever (mensagem sanitizada; o detalhe só vai para o stderr) |

No cliente, tudo isso vira `MCPClientError.code`, com um destes valores: `MCP_UNAVAILABLE`, `MCP_TOOL_ERROR`,
`INVALID_TOOL_ARGUMENTS` ou `UPSTREAM_TIMEOUT`. Quando existir, o código do servidor fica em `detail_code`.

## Contrato com o RAG (equipe RAG)

O servidor só precisa de **uma função** e do JSON normalizado:

```python
# rag/retrieve.py
def retrieve(query: str, top_k: int = 8, topic_key: str | None = None) -> list[dict]:
    """Hits do Chroma em ordem de relevância. Cada dict precisa ter:
       chunk_id: str, recipe_id: str, document_id: str, text: str (o "document" do Chroma),
       distance: float | None
    Opcional: section, ou um dict "metadata" com esses campos (metadados achatados do Chroma)."""
```

- Carregar o modelo de embeddings e o `PersistentClient` **uma vez** (cache no módulo). O servidor é um
  processo persistente e chama `retrieve` em uma thread.
- Não use `print` para logs. O SDK desvia o stdout durante o serviço (há teste para isso), mas use `logging`/stderr.
- Opcional: `rag/ingredients.py: normalize_ingredient(name: str) -> str`, a mesma regra usada para gerar
  `name_normalized`. Se não existir, o servidor usa uma normalização básica (minúsculas, sem acentos, plural simples).
- `data/normalized/recipes.json`: uma lista de receitas ou `{"recipes": [...]}`, no formato de
  `docs/08-application/contracts.md`. Campos obrigatórios: `recipe_id`, `document_id`, `title`, `topic_key`,
  `ingredients[{name_original, name_normalized?, quantity_text?, required=true, notes?, alternatives_documented[]}]`,
  `instructions` (não vazio) e `source_url` (http/https). Opcionais: `variant_index`, `topic_label`, `license`,
  `revision_url`, `retrieved_at`, `portions`, `preparation_time`, `temperature`. Registros inválidos ou com
  `recipe_id` duplicado **não são servidos** e aparecem no log.
- O `recipe_id` e o `document_id` dos metadados do Chroma devem ser iguais aos do JSON. Hits divergentes são descartados.

## Uso no backend (equipe backend/LLM)

```python
from contextlib import asynccontextmanager
from app.integrations.mcp_client import MCPClient, MCPClientError, evidence_set

@asynccontextmanager
async def lifespan(app):
    async with MCPClient.from_env() as mcp:        # inicia o subprocesso + initialize + tools/list
        app.state.mcp = mcp
        yield                                       # no shutdown, encerra a sessão e o processo

# orquestrador
tools = mcp.llm_tools()                             # schemas descobertos via MCP, no formato do Ollama
result = await mcp.call_tool(call.function.name, call.function.arguments, request_id=rid)
messages.append({"role": "tool", "tool_name": result.name, "content": result.to_llm_content()})
evid = evidence_set(all_results_of_turn)            # recipe_id -> {document_id, title, source_url}
await mcp.ping()                                    # para o /ready
mcp.trace_for(rid)                                  # trace sanitizado (sem texto do usuário)
```

- O limite de chamadas por turno é do orquestrador. A documentação diverge: 4 em `architecture.md`,
  6 em `mcp-server.md` e no `.env`.
- Não há reconexão automática. Se o servidor cair, as chamadas levantam `MCP_UNAVAILABLE`, `connected` fica falso
  e o `/ready` deve refletir isso. Reiniciar o backend reconecta.
- O handshake usa `mode="legacy"` (`initialize` explícito, protocolo 2025-11-25), que é o que a documentação pede como evidência.
