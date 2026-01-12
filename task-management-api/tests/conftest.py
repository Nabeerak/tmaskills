"""
Shared pytest fixtures for Task Management API tests.
Provides database sessions, FastAPI test client, and test data.
"""
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_session
from app.models.task import Task


# Test database URL (using SQLite for fast testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Provide database session for tests with automatic rollback.
    Each test gets a fresh session and database state.
    """
    async_session_maker = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide async HTTP client for FastAPI testing.
    Overrides database dependency to use test session.
    """
    # Override get_session dependency
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    # Clean up dependency override
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data():
    """Provide sample task data for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task description",
        "status": "pending",
        "priority": "medium"
    }


@pytest.fixture
def sample_task_update_data():
    """Provide sample task update data for testing."""
    return {
        "title": "Updated Task",
        "status": "in_progress",
        "priority": "high"
    }


@pytest_asyncio.fixture
async def created_task(client: AsyncClient, sample_task_data: dict):
    """
    Create a task for tests that need an existing task.
    Automatically created and cleaned up per test.
    """
    response = await client.post("/api/v1/tasks/", json=sample_task_data)
    assert response.status_code == 201
    return response.json()


@pytest_asyncio.fixture
async def multiple_tasks(client: AsyncClient):
    """Create multiple tasks for pagination and filtering tests."""
    tasks_data = [
        {"title": "Task 1", "description": "First task", "status": "pending", "priority": "low"},
        {"title": "Task 2", "description": "Second task", "status": "in_progress", "priority": "medium"},
        {"title": "Task 3", "description": "Third task", "status": "completed", "priority": "high"},
        {"title": "Task 4", "description": "Fourth task", "status": "pending", "priority": "high"},
        {"title": "Task 5", "description": "Fifth task", "status": "in_progress", "priority": "low"},
    ]

    created_tasks = []
    for task_data in tasks_data:
        response = await client.post("/api/v1/tasks/", json=task_data)
        assert response.status_code == 201
        created_tasks.append(response.json())

    return created_tasks
