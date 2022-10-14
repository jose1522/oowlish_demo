from typing import Generator

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    """Fixture for test api client"""
    with TestClient(app) as c:
        yield c
