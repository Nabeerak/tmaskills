"""
Database configuration and session management with SQLModel.

Usage:
    from app.core.database import engine, get_session

    # In endpoints
    @router.get("/items")
    def get_items(session: Session = Depends(get_session)):
        items = session.exec(select(Item)).all()
        return items
"""

from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=not settings.is_production,  # Log SQL in development
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)


def create_db_and_tables():
    """
    Create all database tables.

    Call this on application startup to ensure tables exist.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency that provides a database session.

    Yields a session that is automatically closed after use.
    Use with FastAPI's Depends():

    Example:
        @router.get("/items")
        def get_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session


# Advanced: Session with automatic transaction handling
def get_session_with_commit():
    """
    Dependency that provides a session with automatic commit/rollback.

    Commits on success, rolls back on exception.

    Example:
        @router.post("/items")
        def create_item(
            item_in: ItemCreate,
            session: Session = Depends(get_session_with_commit)
        ):
            item = Item(**item_in.model_dump())
            session.add(item)
            # Automatically committed by dependency
            return item
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


# For testing: Create test database
def get_test_session():
    """
    Create a test database session.

    Used in tests to override the main get_session dependency.

    Example:
        from app.core.database import get_test_session, get_session

        app.dependency_overrides[get_session] = get_test_session

        def test_create_item():
            response = client.post("/api/v1/items", json={"name": "Test"})
            assert response.status_code == 201
    """
    from sqlmodel import create_engine

    # Create in-memory SQLite database for tests
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session


# Advanced: Async database support
"""
For async database operations, use AsyncSession:

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

# Create async engine
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=not settings.is_production,
)

async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

# Usage
@router.get("/items")
async def get_items(session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Item))
    items = result.all()
    return items
"""
