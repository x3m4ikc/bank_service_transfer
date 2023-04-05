from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_template():
    res = client.get("/api/v1/get-details", params={"template_id": 0})

    assert res.status_code == status.HTTP_200_OK
