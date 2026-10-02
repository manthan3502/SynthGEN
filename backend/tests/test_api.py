import pytest
from werkzeug.security import check_password_hash

from app import create_app
from database import Generation, User, db


def test_registration_and_login(client, app):
    credentials = {"name": " Alice ", "email": " Alice@Example.test ", "password": "test-only-password"}
    response = client.post("/api/register", json=credentials)
    assert response.status_code == 201
    with app.app_context():
        user = User.query.one()
        assert user.name == "Alice"
        assert user.email == "alice@example.test"
        assert user.password != credentials["password"]
        assert check_password_hash(user.password, credentials["password"])
    response = client.post("/api/login", json=credentials)
    assert response.status_code == 200
    assert set(response.json) == {"token", "name", "email"}
    headers = {"Authorization": "Bearer " + response.json["token"]}
    assert client.get("/api/settings", headers=headers).json == {"name": "Alice", "email": "alice@example.test"}


def test_duplicate_registration(client, headers):
    response = client.post("/api/register", json={"name": "Other", "email": "ALICE@example.test", "password": "test-only-password"})
    assert response.status_code == 400


@pytest.mark.parametrize("body", [None, [], {}, {"name": " ", "email": "a@example.test", "password": "x"},
    {"name": "A", "email": "invalid", "password": "x"},
    {"name": "A", "email": "a@example.test", "password": 12},
    {"name": "A", "email": "a@example.test", "password": ""}])
def test_invalid_registration(client, body):
    assert client.post("/api/register", json=body).status_code == 400


@pytest.mark.parametrize("body", [{}, {"email": "alice@example.test", "password": "wrong"},
    {"email": "absent@example.test", "password": "test-only-password"},
    {"email": "alice@example.test", "password": None}])
def test_invalid_login(client, headers, body):
    assert client.post("/api/login", json=body).status_code == 401


@pytest.mark.parametrize("method,path", [("GET", "/api/history"), ("POST", "/api/generate"),
    ("POST", "/api/download"), ("DELETE", "/api/history/1"), ("GET", "/api/settings"), ("PUT", "/api/settings")])
def test_protected_routes(client, method, path):
    assert client.open(path, method=method, json={}).status_code == 401


def test_generation_and_history(client, headers, schema_mock, app):
    response = client.post("/api/generate", headers=headers, json={"prompt": "People and ages", "rows": 25})
    assert response.status_code == 200
    schema_mock.assert_called_once_with("People and ages")
    result = response.json
    assert result["rows"] == 25
    assert result["columns"] == ["person", "age"]
    assert len(result["data"]) == 20
    assert all(18 <= row[1] <= 80 for row in result["data"])
    history = client.get("/api/history", headers=headers).json
    assert len(history) == 1
    assert history[0]["id"] == result["gen_id"]
    assert history[0]["prompt"] == "People and ages"
    with app.app_context():
        assert Generation.query.one().rows == 25


@pytest.mark.parametrize("body", [{}, {"prompt": ""}, {"prompt": "   "}, {"prompt": 7},
    {"prompt": "People", "rows": 0}, {"prompt": "People", "rows": -1},
    {"prompt": "People", "rows": "bad"}, {"prompt": "People", "rows": True},
    {"prompt": "People", "rows": 1.5}, [], None])
@pytest.mark.parametrize("path", ["/api/generate", "/api/download"])
def test_invalid_generation(client, headers, schema_mock, body, path):
    assert client.post(path, headers=headers, json=body).status_code == 400
    schema_mock.assert_not_called()
    assert client.get("/api/history", headers=headers).json == []


def test_row_limit(client, headers, schema_mock):
    response = client.post("/api/generate", headers=headers, json={"prompt": "People", "rows": 6000})
    assert response.status_code == 200
    assert response.json["rows"] == 5000


def test_download_csv(client, headers, schema_mock):
    response = client.post("/api/download", headers=headers, json={"prompt": "People", "rows": 3})
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert "dataset_3rows.csv" in response.headers["Content-Disposition"]
    assert response.data.decode().splitlines()[0] == "person,age"
    assert len(response.data.decode().splitlines()) == 4
    assert client.get("/api/history", headers=headers).json == []


def test_delete_and_ownership(client, headers, account, schema_mock):
    gen_id = client.post("/api/generate", headers=headers, json={"prompt": "People", "rows": 2}).json["gen_id"]
    other = account("bob@example.test")
    assert client.get("/api/history", headers=other).json == []
    assert client.delete(f"/api/history/{gen_id}", headers=other).status_code == 404
    assert len(client.get("/api/history", headers=headers).json) == 1
    assert client.delete(f"/api/history/{gen_id}", headers=headers).status_code == 200
    assert client.get("/api/history", headers=headers).json == []
    assert client.delete(f"/api/history/{gen_id}", headers=headers).status_code == 404
    assert client.delete("/api/history/99999", headers=headers).status_code == 404


@pytest.mark.parametrize("path", ["/api/generate", "/api/download"])
def test_provider_errors_are_private(client, headers, monkeypatch, caplog, path):
    import generator

    def failure(prompt):
        raise RuntimeError("SYNTHETIC_PRIVATE_ERROR_MARKER")

    monkeypatch.setattr(generator, "get_schema", failure)
    response = client.post(path, headers=headers, json={"prompt": "People", "rows": 2})
    assert response.status_code == 500
    assert "SYNTHETIC_PRIVATE_ERROR_MARKER" not in response.get_data(as_text=True)
    assert "SYNTHETIC_PRIVATE_ERROR_MARKER" not in caplog.text
    assert client.get("/api/history", headers=headers).json == []


def test_missing_api_configuration(client, headers):
    assert client.post("/api/generate", headers=headers, json={"prompt": "People"}).status_code == 500


def test_secret_configuration(monkeypatch, tmp_path):
    # Patch dotenv as an additional guard against reading any real environment file.
    monkeypatch.setattr("app.load_dotenv", lambda *args: None)
    with pytest.raises(RuntimeError, match="Set SECRET_KEY"):
        create_app()
    with pytest.raises(RuntimeError, match="Set SECRET_KEY"):
        create_app({"TESTING": True, "SECRET_KEY": "short"})
    with pytest.raises(RuntimeError, match="CORS_ORIGINS"):
        create_app({"TESTING": True, "SECRET_KEY": "test-only-signing-value-never-use-in-deployment", "CORS_ORIGINS": "*"})


def test_cors(client):
    allowed = client.get("/api/history", headers={"Origin": "http://localhost:5173"})
    assert allowed.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"
    denied = client.get("/api/history", headers={"Origin": "https://untrusted.example"})
    assert "Access-Control-Allow-Origin" not in denied.headers


def test_settings_validation(client, headers, account):
    account("bob@example.test")
    assert client.put("/api/settings", headers=headers, json={"email": "bob@example.test"}).status_code == 400
    assert client.put("/api/settings", headers=headers, json={"email": "bad"}).status_code == 400
    assert client.put("/api/settings", headers=headers, json={"name": " "}).status_code == 400
    assert client.put("/api/settings", headers=headers, json={"name": "Updated"}).status_code == 200
    assert client.get("/api/settings", headers=headers).json["name"] == "Updated"
