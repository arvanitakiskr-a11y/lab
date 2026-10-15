import pytest
from fastapi.testclient import TestClient
from app import app
@pytest.fixture
def client():
    with TestClient(app) as c:
        c.post('/reset')
        yield c
        c.post('/reset')
