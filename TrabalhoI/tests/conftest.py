"""Fixtures compartilhadas. Os testes usam a base e o modelo reais do repositório."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src import data_analysis as da  # noqa: E402
from src.api import AplicacaoApi  # noqa: E402


@pytest.fixture(scope="session")
def bruto() -> pd.DataFrame:
    return da.carregar_dados_brutos()


@pytest.fixture(scope="session")
def bruto_texto() -> pd.DataFrame:
    return da.carregar_dados_brutos(como_texto=True)


@pytest.fixture(scope="session")
def processado(bruto_texto):
    """Base processada em memória a partir do CSV original (mesmo código do pipeline)."""
    df, auxiliares = da.processar_partidas(bruto_texto)
    return df, auxiliares


@pytest.fixture(scope="session")
def app() -> AplicacaoApi:
    return AplicacaoApi()
