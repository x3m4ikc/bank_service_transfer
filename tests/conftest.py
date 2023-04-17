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


@pytest.fixture(autouse=True, scope="function")
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
