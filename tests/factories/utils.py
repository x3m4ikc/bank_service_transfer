import factory
from tests.conftest import TestingSessionLocal


class AsyncFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestingSessionLocal
        abstract = True

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        obj = model_class(*args, **kwargs)
        async with session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj
