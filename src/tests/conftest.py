from datetime import datetime
from typing import AsyncGenerator, List

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.app import app
from src.config.config import DATABASE_URL
from src.database.func import get_db_session
from src.database.models import Base, Task

engine_test = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session_maker: async_sessionmaker = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
)


async def override_get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_async_session

tasks: List[dict] = [
    {
        "task_name": f"test task{i}",
        "task_type": f"test{i}",
        "time_add": datetime.fromisoformat(f"2025-08-20T12:0{i}:00"),
    }
    for i in range(3)
]


@pytest.fixture(scope="session")
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        async with session.begin():
            session.add_all([Task(**task) for task in tasks])
        await session.commit()

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для работы эндпоинтов на тестовом адресе"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        trust_env=False,
    ) as ac:
        yield ac
