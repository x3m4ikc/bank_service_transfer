from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_payment_type():
    res = client.get("/api/v1/payments/paymentType")
    assert 'FAVORITES' in res.json()
    assert len(res.json()) == 11
    assert res.status_code == status.HTTP_200_OK
