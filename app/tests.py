import sqlite3
import pytest
from api.schemas import Result
from main import app
from fastapi.testclient import TestClient


def test_create_question():
    client = TestClient(app)

    response = client.post("/questions/", json={"questions_num": 5})

    assert response.status_code == 200

    result = Result(**response.json())
    assert result.questions is not None
    assert len(result.questions) == 5
