from http import HTTPStatus

import pytest
from fastapi import status
from main import app
from models.models import TemplateForPayment
from sqlalchemy import insert
from tests.conftest import TestingSessionLocal


async def test_get_template(ac):
    db = TestingSessionLocal()
    create_template = insert(TemplateForPayment).values(
        id=0,
        name="test1",
        payee_name="test1",
        payee_account_number="test1",
        template_purpose_of_payment="test1",
        BIC="test1",
        INN="test1",
    )
    await db.execute(create_template)
    await db.commit()

    url = app.url_path_for("template_details")
    res = await ac.get(url, params={"template_id": 0})

    assert res.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "currency_from,currency_to,units,expected",
    [
        ("USD", "EUR", 100, status.HTTP_200_OK),
        ("EUR", "USD", 50, status.HTTP_200_OK),
        ("UE", "USD", 100, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("rub", "eur", 20, status.HTTP_200_OK),
    ],
)
async def test_get_rates(ac, currency_from, currency_to, units, expected):
    url = app.url_path_for("exchange_currency")
    res = await ac.get(
        url, params={"currency_from": currency_from, "currency_to": currency_to, "units": units}
    )

    assert res.status_code == expected