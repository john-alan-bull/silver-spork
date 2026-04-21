import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import create_app, DEFAULT_ACTIVITIES


@pytest.fixture
def activities_db():
    """Fixture providing an isolated copy of the activities database for each test"""
    return deepcopy(DEFAULT_ACTIVITIES)


@pytest.fixture
def client(activities_db):
    """Fixture providing a TestClient with an isolated app instance"""
    app = create_app(activities_db)
    return TestClient(app)
