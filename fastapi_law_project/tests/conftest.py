import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.core.security import generate_api_key, hash_api_key
from app.db.session import Base, get_db
from app.main import app
from app.models.api_key import ApiKey


@pytest.fixture
async def db_session_factory():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


@pytest.fixture
async def client(db_session_factory):
    async def override_get_db():
        async with db_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def make_api_key(db_session_factory):
    async def _make(user_id: str) -> str:
        key = generate_api_key()
        async with db_session_factory() as session:
            session.add(ApiKey(key_hash=hash_api_key(key), user_id=user_id))
            await session.commit()
        return key

    return _make