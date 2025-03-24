import os
import sys
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# including app root in sys.path so it can be used for imports
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/starneighbours"
)


from starneighbours.main import create_app
from starneighbours.settings import Settings

app_settings = Settings()


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    yield create_app()


@pytest.fixture(scope="function")
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def auth_headers():
    return {"Authorization": f"Bearer sometoken"}
