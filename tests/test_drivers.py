import os
import sys

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.database import Base
from app.main import app


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    session_factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    from app.database import async_session_factory
    original = async_session_factory
    engine = db_session.bind
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    import app.database as db_mod
    db_mod.async_session_factory = factory
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    db_mod.async_session_factory = original


@pytest.mark.asyncio
async def test_get_driver_not_found(client: AsyncClient):
    resp = await client.get("/drivers/999999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_driver_telemetry(client: AsyncClient):
    resp = await client.get("/drivers/1/telemetry")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
