import pandas as pd
import pytest

from generator import generate_dataset, validate_schema


def test_faker_generation(schema_mock):
    frame, columns = generate_dataset("People", 5)
    assert isinstance(frame, pd.DataFrame)
    assert frame.shape == (5, 2)
    assert columns == schema_mock.return_value["columns"]
    assert all(isinstance(value, str) and value for value in frame["person"])


@pytest.mark.parametrize("schema", [None, {}, {"columns": []}, {"columns": [None]},
    {"columns": [{"name": "=formula", "type": "name"}]},
    {"columns": [{"name": "x", "type": "unknown"}]},
    {"columns": [{"name": "x", "type": "integer", "min": 5, "max": 1}]},
    {"columns": [{"name": "x", "type": "integer", "min": 1.5}]},
    {"columns": [{"name": "x", "type": "float", "min": float("nan")}]},
    {"columns": [{"name": "x", "type": "choice", "values": []}]},
    {"columns": [{"name": "x", "type": "name"}, {"name": "x", "type": "email"}]}])
def test_untrusted_schema(schema):
    with pytest.raises(ValueError):
        validate_schema(schema)


def test_csv_formula_protection(client, headers, monkeypatch):
    monkeypatch.setattr("app.generate_dataset", lambda *args: (
        pd.DataFrame({"=header": ["=1+1", "@SUM(1)", "normal"]}), []
    ))
    response = client.post("/api/download", headers=headers, json={"prompt": "Example", "rows": 3})
    assert response.status_code == 200
    assert response.data.decode().splitlines() == ["'=header", "'=1+1", "'@SUM(1)", "normal"]
