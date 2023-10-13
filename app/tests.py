import sqlite3
import pytest
from api.schemas import Result
from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_session():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE question (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        value INTEGER,
        created_at DATETIME
    )''')

    connection.commit()
    yield connection
    connection.close()


def test_create_question():
    client = TestClient(app)

    response = client.post("/questions/", json={"questions_num": 5})

    assert response.status_code == 200

    result = Result(**response.json())
    assert result.questions is not None
    assert len(result.questions) == 5
