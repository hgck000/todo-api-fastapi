import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]  # repo root
sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402
from app.db.in_memory import store  # noqa: E402


@pytest.fixture(autouse=True)
def reset_store():
    store.items.clear()
    yield
    store.items.clear()


@pytest.fixture
def client():
    return TestClient(app)
