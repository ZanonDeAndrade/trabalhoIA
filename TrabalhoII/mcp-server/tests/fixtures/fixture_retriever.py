"""Retriever SUBSTITUTO para testes do MCP enquanto o RAG real (rag/retrieve.py) não existe.

Segue exatamente o contrato `retrieve(query, top_k, topic_key) -> list[dict]` descrito no
README do mcp-server. Faz sobreposição lexical simples sobre o recipes.json de fixture.
O protocolo MCP nos testes continua real; só a busca vetorial é substituída.

Modos (env FIXTURE_RETRIEVER_MODE): normal | noisy | broken | slow | bogus
"""

import json
import os
import sys
import time
import unicodedata


_STOP = {"a", "o", "e", "de", "da", "do", "com", "ao", "em", "para", "que", "receita", "posso", "fazer", "como"}


def _words(text):
    return {w for w in _norm(text).replace(",", " ").replace(".", " ").replace("?", " ").split() if w not in _STOP}


def _norm(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def _chunks():
    with open(os.environ["RECIPES_JSON"], encoding="utf-8") as fh:
        data = json.load(fh)
    for r in data["recipes"] if isinstance(data, dict) else data:
        names = ", ".join(i["name_original"] for i in r.get("ingredients", []))
        yield {
            "chunk_id": f"{r['recipe_id']}-c0",
            "recipe_id": r["recipe_id"],
            "document_id": r["document_id"],
            "text": f"{r['title']}. Ingredientes: {names}",
            "metadata": {"section": "synopsis", "topic_key": r.get("topic_key")},
        }


def retrieve(query, top_k=8, topic_key=None):
    mode = os.environ.get("FIXTURE_RETRIEVER_MODE", "normal")
    if mode == "broken":
        raise RuntimeError("falha simulada do índice com /caminho/secreto")
    if mode == "slow":
        time.sleep(float(os.environ.get("FIXTURE_RETRIEVER_SLEEP", "5")))
    if mode == "noisy":
        print("ruido em stdout vindo de uma biblioteca")  # não pode corromper o protocolo
        os.write(1, b"ruido direto no fd 1\n")
        sys.stdout.flush()

    q = _words(query)
    scored = []
    for c in _chunks():
        if topic_key and c["metadata"]["topic_key"] != topic_key:
            continue
        words = _words(c["text"])
        overlap = len(q & words)
        if overlap:
            scored.append((1.0 - overlap / max(len(q), 1), c))
    scored.sort(key=lambda x: x[0])
    hits = [dict(c, distance=round(d, 4)) for d, c in scored[:top_k]]
    if mode == "bogus":
        hits = [
            {"chunk_id": "x-c0", "recipe_id": "nao-existe-v1", "document_id": "nao-existe", "text": "inventado", "distance": 0.0},
            {"chunk_id": "y-c0", "recipe_id": "fx-001-v1", "document_id": "fx-002", "text": "doc errado", "distance": 0.0},
            {"sem": "campos"},
        ] + hits
    return hits
