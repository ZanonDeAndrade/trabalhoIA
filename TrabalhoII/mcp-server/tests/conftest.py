import sys
from pathlib import Path

import pytest

SERVER_DIR = Path(__file__).resolve().parents[1]
FIXTURES = SERVER_DIR / "tests" / "fixtures"
sys.path.insert(0, str(SERVER_DIR))  # permite importar tools/store/models nos testes unitários


@pytest.fixture
def anyio_backend():
    return "asyncio"
