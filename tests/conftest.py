import pytest
import joblib
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        # using yield instead of return allows for teardown code after. Anything written after yield runs after the test finished
        yield c 

@pytest.fixture(scope="session")
def model():
   yield joblib.load(settings.MODEL_PATH)
