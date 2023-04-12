import asyncio
from typing import AsyncGenerator

import pytest
from config import TEST_DB_URL
from db.database import Base, get_db
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

test_engine = create_async_engine(TEST_DB_URL)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, class_=AsyncSession, autoflush=False, bind=test_engine
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        yield ac


# @pytest.fixture
# async def create_transfer_order():
# class TransferOrder(Base):
#     __tablename__ = "transfer_order"
#     __metadata__ = metadata
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
#     transfer_type_id = mapped_column(ForeignKey("transfer_type.id"))
#     purpose = Column(String)
#     remitter_card_number = Column(String(length=16), nullable=False)
#     payee_id = mapped_column(ForeignKey("payee.id"))
#     sum = Column(DECIMAL, nullable=False)
#     sum_commission = Column(DECIMAL, nullable=False)
#     completed_at = Column(TIMESTAMP(timezone=True), nullable=False, onupdate=func.now())
#     status = Column(Enum(TransferStatus), nullable=False)
#     authorization_code = Column(String(length=255), nullable=False)
#     currency_exchange = Column(DECIMAL, nullable=False)
#     is_favorite = Column(Boolean, nullable=False)
#     start_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
#     periodicity = Column(Enum(TransferPeriod), nullable=True)
#     client_id = Column(UUID, nullable=False)
#
#     payee = relationship("Payee")
#     transfer_type = relationship("TransferType")
# db = TestingSessionLocal()
#
# transfer_type = insert(TransferType).values(
#     id=0,
#     type_name="test",
#     currency_code="test",
#     min_commission=1,
#     max_commission=1,
#     percent_commission=1,
#     commission_fix=1,
#     min_sum=1,
# )
#
# payee = insert(Payee).values(
#     id=0,
#     type="INDIVIDUALS",
#     name="test",
#     INN="test",
#     BIC="test",
#     payee_account_number="test",
#     payee_card_number="test"
# )
#
# transfer_order = insert(TransferOrder).values(
#     id=0,
#     created_at=func.now(),
#     transfer_type_id=0,
#     purpose="test",
#     remitter_card_number="test",
#     payee_id=0,
#     sum=100,
#     sum_commission=1,
#     completed_at=func.now(),
#     status="DRAFT",
#     authorization_code="test",
#     currency_exchange=1000,
#     is_favorite=False,
#     start_date=func.now(),
#     periodicity="WEEKLY",
#     client_id=0
# )
# await db.execute(transfer_type)
# await db.execute(payee)
# await db.execute(transfer_order)
# await db.commit()
