import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from catalog.database.connection import Base, get_db
from catalog.app import app
from httpx import AsyncClient, ASGITransport

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def test_session_factory(test_engine):
    return async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session(test_session_factory):
    async with test_session_factory() as session:
        yield session

@pytest_asyncio.fixture
async def client(test_session_factory):
    # Override the dependency
    async def override_get_db():
        async with test_session_factory() as session:
            yield session
            
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
