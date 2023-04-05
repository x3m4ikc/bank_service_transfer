import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from config import TEST_DB_URL
from main import app
from db.database import Base, get_db

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def init_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def get_session():
    with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def test_client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
