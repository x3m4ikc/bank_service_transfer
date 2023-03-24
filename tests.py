from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_template():
    res = client.get("/api/v1/get-details", params={"template_id": 1})
    assert res == ""
