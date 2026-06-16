import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.database import Base, get_db
from app.main import app
from httpx import AsyncClient

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost/test_ai_receptionist"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    async with TestSession() as session:
        yield session

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
