from http import HTTPStatus

from main import app
from models.models import TemplateForPayment, TransferOrder
from sqlalchemy import func, insert
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


async def test_add_transfer_order_to_favorites(ac):
    db = TestingSessionLocal()
    create_transfer_order = insert(TransferOrder).values(
        id=0,
        created_at=func.now(),
        transfer_type_id=0,
        purpose="test",
        remitter_card_number="test",
        payee_id=0,
        sum=100,
        sum_commission=1,
        completed_at=func.now(),
        status="DRAFT",
        authorization_code="test",
        currency_exchange=1000,
        is_favorite=False,
        start_date=func.now(),
        periodicity="WEEKLY",
        client_id=0,
    )
    await db.execute(create_transfer_order)
    await db.commit()

    url = app.url_path_for("add_transfer_order_to_favorites")
    res = await ac.patch(url, data={"transfer_order_id": 0})

    assert res.status_code == HTTPStatus.OK
