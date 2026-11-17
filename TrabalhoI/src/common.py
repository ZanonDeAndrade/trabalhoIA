"""Utilitários compartilhados pela API: erros de domínio, catálogo de equipes e carga dos dados."""

from __future__ import annotations

import hashlib
import sys
import unicodedata
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

import pandas as pd

from src.data_analysis import NOME_CURTO
from src.data_split import CSV_PROCESSADO_PADRAO


class ErroApi(Exception):
    """Erro previsto pela aplicação, com código HTTP e mensagem segura para o cliente."""

    def __init__(self, status: int, codigo: str, mensagem: str):
        super().__init__(mensagem)
        self.status = status
        self.codigo = codigo
        self.mensagem = mensagem


def slug(texto: str) -> str:
    """'Atlético-MG' -> 'atletico-mg' (identificador estável e seguro para URLs)."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return "-".join(sem_acento.lower().replace("-", " ").split())


def carregar_partidas(caminho: Path | str = CSV_PROCESSADO_PADRAO) -> pd.DataFrame:
    """Lê a base processada (todas as 1.520 partidas) em ordem cronológica."""
    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(
            f"Base processada não encontrada em {caminho}. Execute `python src/data_analysis.py`."
        )
    df = pd.read_csv(caminho, parse_dates=["data_partida"])
    return df.sort_values(["data_partida", "id_partida"]).reset_index(drop=True)


class CatalogoEquipes:
    """Mapeia identificadores (slug), nomes curtos e nomes oficiais para o nome oficial do dataset."""

    def __init__(self, df: pd.DataFrame):
        oficiais = sorted(set(df["home_team"]) | set(df["away_team"]), key=lambda o: NOME_CURTO.get(o, o))
        self.equipes = [
            {"id": slug(NOME_CURTO.get(o, o)), "name": NOME_CURTO.get(o, o), "official_name": o}
            for o in oficiais
        ]
        self._indice: dict[str, str] = {}
        for e in self.equipes:
            for chave in (e["id"], e["name"].lower(), e["official_name"].lower()):
                self._indice[chave] = e["official_name"]
        self._por_oficial = {e["official_name"]: e for e in self.equipes}

    def resolver(self, identificador: object) -> str:
        """Devolve o nome oficial; levanta 404 se a equipe não existir."""
        if not isinstance(identificador, str) or not identificador.strip():
            raise ErroApi(400, "parametro_invalido", "Informe uma equipe válida.")
        chave = identificador.strip().lower()
        oficial = self._indice.get(chave) or self._indice.get(slug(identificador))
        if oficial is None:
            raise ErroApi(404, "equipe_nao_encontrada", f"Equipe não encontrada: {identificador.strip()[:60]}")
        return oficial

    def info(self, oficial: str) -> dict[str, str]:
        return self._por_oficial[oficial]

    def nome_curto(self, oficial: str) -> str:
        return self._por_oficial[oficial]["name"]


def sha256_texto(caminho: Path | str) -> str:
    """SHA-256 de um arquivo de texto ignorando a diferença de fim de linha (CRLF do Windows x LF)."""
    return hashlib.sha256(Path(caminho).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
