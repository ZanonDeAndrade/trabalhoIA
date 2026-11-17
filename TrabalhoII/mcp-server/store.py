"""Acesso a dados do servidor MCP: receitas normalizadas (JSON) e adaptador do retriever RAG.

Este é o ÚNICO módulo do servidor que conhece o pacote `rag/`. O contrato esperado está
documentado em `mcp-server/README.md` (seção "Contrato com o RAG").
"""

from __future__ import annotations

import hashlib
import importlib
import json
import logging
import os
import re
import threading
import unicodedata
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

logger = logging.getLogger("mcp_server.store")

SERVER_DIR = Path(__file__).resolve().parent
DEFAULT_PROJECT_ROOT = SERVER_DIR.parent


# ---------------------------------------------------------------- configuração


@dataclass(frozen=True)
class Settings:
    project_root: Path
    recipes_json: Path
    retriever_ref: str
    normalizer_ref: str
    default_top_k: int

    @classmethod
    def from_env(cls) -> Settings:
        root = Path(os.environ.get("PROJECT_ROOT") or DEFAULT_PROJECT_ROOT).resolve()

        def resolve(value: str) -> Path:
            p = Path(value)
            return p if p.is_absolute() else (root / p).resolve()

        top_k = int(os.environ.get("RAG_TOP_K", "8"))
        return cls(
            project_root=root,
            recipes_json=resolve(os.environ.get("RECIPES_JSON", "data/normalized/recipes.json")),
            retriever_ref=os.environ.get("RAG_RETRIEVER", "rag.retrieve:retrieve"),
            normalizer_ref=os.environ.get("RAG_NORMALIZER", "rag.ingredients:normalize_ingredient"),
            default_top_k=min(max(top_k, 1), 10),
        )


def load_callable(ref: str) -> Callable[..., Any]:
    """Importa `pacote.modulo:funcao`. Levanta ImportError/AttributeError se não existir."""
    module_name, _, attr = ref.partition(":")
    if not module_name or not attr:
        raise ImportError(f"referência inválida {ref!r}; use 'modulo:funcao'")
    fn = getattr(importlib.import_module(module_name), attr)
    if not callable(fn):
        raise ImportError(f"{ref!r} não é chamável")
    return fn


# ---------------------------------------------------------------- normalização de ingredientes


def basic_normalize(name: str) -> str:
    """Normalização mínima usada quando `rag.ingredients` não está disponível.

    minúsculas, sem acentos, espaços colapsados e plural simples por palavra (ovos -> ovo).
    Não cria equivalências entre ingredientes diferentes (RN03).
    """
    text = unicodedata.normalize("NFKD", name.strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    words = []
    for w in text.split():
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        words.append(w)
    return " ".join(words)


class IngredientNormalizer:
    """Usa `rag.ingredients.normalize_ingredient` quando existir (mesma regra da ingestão)."""

    def __init__(self, ref: str) -> None:
        self._ref = ref
        self._fn: Callable[[str], str] | None = None
        self._resolved = False
        self._lock = threading.Lock()

    def _resolve(self) -> None:
        with self._lock:
            if self._resolved:
                return
            try:
                self._fn = load_callable(self._ref)
                logger.info("normalizador de ingredientes: %s", self._ref)
            except Exception as exc:  # noqa: BLE001 - qualquer falha cai no fallback documentado
                logger.warning("normalizador %s indisponível (%s); usando normalização básica", self._ref, exc)
                self._fn = None
            self._resolved = True

    def __call__(self, name: str) -> str:
        if not self._resolved:
            self._resolve()
        if self._fn is not None:
            try:
                value = self._fn(name)
                if isinstance(value, str) and value.strip():
                    return value.strip()
            except Exception:  # noqa: BLE001
                logger.exception("normalizador do RAG falhou para um ingrediente; usando básico")
        return basic_normalize(name)


# ---------------------------------------------------------------- receitas normalizadas

_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,127}$")


class IngredientRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name_original: str = Field(min_length=1)
    name_normalized: str | None = None
    quantity_text: str | None = None
    # Se a fonte não distingue opcionais, o ingrediente é tratado como obrigatório.
    required: bool = True
    notes: str | None = None
    alternatives_documented: list[str] = Field(default_factory=list)


class RecipeRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")

    recipe_id: str
    document_id: str
    variant_index: int | None = None
    title: str = Field(min_length=1)
    topic_key: str
    topic_label: str | None = None
    ingredients: list[IngredientRecord]
    instructions: list[str] = Field(min_length=1)
    source_url: str
    license: str | None = None
    revision_url: str | None = None
    retrieved_at: str | None = None
    portions: str | None = None
    preparation_time: str | None = None
    temperature: str | None = None

    @field_validator("recipe_id", "document_id", "topic_key")
    @classmethod
    def _stable_id(cls, v: str) -> str:
        if not _ID_RE.match(v):
            raise ValueError("ID deve ser ASCII minúsculo estável ([a-z0-9_.-])")
        return v

    @field_validator("source_url")
    @classmethod
    def _absolute_url(cls, v: str) -> str:
        if not re.match(r"^https?://", v):
            raise ValueError("source_url deve ser URL absoluta http(s)")
        return v

    @field_validator("portions", "preparation_time", "temperature", mode="before")
    @classmethod
    def _optional_as_text(cls, v: Any) -> Any:
        return None if v is None else str(v)


@dataclass(frozen=True)
class CorpusSnapshot:
    recipes: dict[str, RecipeRecord]
    data_version: str | None
    load_error: str | None = None

    @property
    def ready(self) -> bool:
        return bool(self.recipes)


class RecipeStore:
    """Carrega `recipes.json` e recarrega automaticamente quando o arquivo muda (reingestão)."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._mtime: float | None = None
        self._snapshot = CorpusSnapshot(recipes={}, data_version=None, load_error="NOT_LOADED")

    def snapshot(self) -> CorpusSnapshot:
        with self._lock:
            try:
                mtime = self.path.stat().st_mtime
            except FileNotFoundError:
                if self._mtime is not None or self._snapshot.load_error != "FILE_NOT_FOUND":
                    logger.warning("recipes.json não encontrado em %s", self.path)
                self._mtime = None
                self._snapshot = CorpusSnapshot(recipes={}, data_version=None, load_error="FILE_NOT_FOUND")
                return self._snapshot
            if mtime != self._mtime:
                self._snapshot = self._load()
                self._mtime = mtime
            return self._snapshot

    def _load(self) -> CorpusSnapshot:
        try:
            raw = self.path.read_bytes()
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            logger.error("falha ao ler %s: %s", self.path, exc)
            return CorpusSnapshot(recipes={}, data_version=None, load_error="INVALID_JSON")

        items = data.get("recipes") if isinstance(data, Mapping) else data
        if not isinstance(items, list):
            logger.error("%s deve conter uma lista de receitas ou {'recipes': [...]}", self.path)
            return CorpusSnapshot(recipes={}, data_version=None, load_error="INVALID_FORMAT")

        recipes: dict[str, RecipeRecord] = {}
        rejected = 0
        for i, item in enumerate(items):
            try:
                rec = RecipeRecord.model_validate(item)
            except ValidationError as exc:
                rejected += 1
                logger.error("receita #%d rejeitada (não será servida): %s", i, exc.errors()[:3])
                continue
            if rec.recipe_id in recipes:
                rejected += 1
                logger.error("recipe_id duplicado %s; mantendo a primeira ocorrência", rec.recipe_id)
                continue
            recipes[rec.recipe_id] = rec

        version = hashlib.sha256(raw).hexdigest()[:12]
        logger.info("corpus carregado: %d receitas válidas, %d rejeitadas, versão %s", len(recipes), rejected, version)
        return CorpusSnapshot(recipes=recipes, data_version=version)


# ---------------------------------------------------------------- retriever RAG


class RetrieverUnavailable(RuntimeError):
    """O módulo RAG não pôde ser importado/inicializado."""


@dataclass(frozen=True)
class Hit:
    chunk_id: str
    recipe_id: str
    document_id: str
    text: str
    distance: float | None
    section: str | None


class RetrieverAdapter:
    """Chama `rag.retrieve.retrieve(query, top_k=..., topic_key=...)` e valida o formato dos hits."""

    def __init__(self, ref: str) -> None:
        self._ref = ref
        self._fn: Callable[..., Any] | None = None
        self._lock = threading.Lock()

    def _get(self) -> Callable[..., Any]:
        with self._lock:
            if self._fn is None:
                try:
                    self._fn = load_callable(self._ref)
                except Exception as exc:  # noqa: BLE001
                    logger.error("retriever %s indisponível: %r", self._ref, exc)
                    raise RetrieverUnavailable(str(exc)) from exc
                logger.info("retriever carregado: %s", self._ref)
            return self._fn

    def search(self, query: str, top_k: int, topic_key: str | None) -> tuple[list[Hit], int]:
        """Retorna (hits válidos, quantidade de hits malformados descartados)."""
        raw_hits = self._get()(query, top_k=top_k, topic_key=topic_key)
        hits: list[Hit] = []
        malformed = 0
        for h in raw_hits or []:
            if not isinstance(h, Mapping):
                malformed += 1
                continue
            meta = h.get("metadata") if isinstance(h.get("metadata"), Mapping) else {}

            def pick(key: str, h: Mapping[str, Any] = h, meta: Mapping[str, Any] = meta) -> Any:
                return h.get(key) if h.get(key) is not None else meta.get(key)

            chunk_id, recipe_id, document_id = pick("chunk_id"), pick("recipe_id"), pick("document_id")
            text = h.get("text") if h.get("text") is not None else h.get("document")
            if not all(isinstance(v, str) and v for v in (chunk_id, recipe_id, document_id)) or not isinstance(
                text, str
            ):
                malformed += 1
                continue
            distance = h.get("distance")
            section = pick("section")
            hits.append(
                Hit(
                    chunk_id=chunk_id,
                    recipe_id=recipe_id,
                    document_id=document_id,
                    text=text,
                    distance=float(distance) if isinstance(distance, int | float) else None,
                    section=section if isinstance(section, str) else None,
                )
            )
        return hits[:top_k], malformed
