from http import HTTPStatus

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
