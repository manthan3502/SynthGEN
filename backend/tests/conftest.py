import socket

import pytest

from app import create_app
from database import db


@pytest.fixture(autouse=True)
def no_credentials_or_network(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)

    def blocked(*args, **kwargs):
        raise AssertionError("Tests must not use network connections")

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)


@pytest.fixture
def app(tmp_path):
    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-signing-value-never-use-in-deployment",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + (tmp_path / "test.sqlite").as_posix(),
    })
    yield application
    with application.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def account(client):
    def create(email="alice@example.test"):
        credentials = {"name": "Alice", "email": email, "password": "test-only-password"}
        assert client.post("/api/register", json=credentials).status_code == 201
        response = client.post("/api/login", json=credentials)
        assert response.status_code == 200
        return {"Authorization": "Bearer " + response.json["token"]}
    return create


@pytest.fixture
def headers(account):
    return account()


@pytest.fixture
def schema_mock(monkeypatch):
    from unittest.mock import Mock
    import generator

    schema = {"columns": [
        {"name": "person", "type": "name"},
        {"name": "age", "type": "integer", "min": 18, "max": 80},
    ]}
    mocked = Mock(return_value=schema)
    monkeypatch.setattr(generator, "get_schema", mocked)
    return mocked
