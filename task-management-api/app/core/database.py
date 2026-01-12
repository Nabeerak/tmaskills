"""
Database configuration and session management for SQLModel with async support.
"""
from typing import AsyncGenerator
import ssl
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Convert PostgreSQL URL to async format for Neon
# Neon requires asyncpg driver: postgresql+asyncpg://...
database_url = settings.DATABASE_URL

# Remove URL parameters that asyncpg doesn't support
# (sslmode, channel_binding) - we'll configure SSL via connect_args
if "?" in database_url:
    base_url = database_url.split("?")[0]
    database_url = base_url

# Convert to asyncpg format
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Configure SSL for Neon PostgreSQL
# Neon requires SSL connections
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create async engine with SSL configuration
engine = create_async_engine(
    database_url,
    echo=True,  # Set to False in production
    future=True,
    pool_pre_ping=True,  # Verify connections before using
    connect_args={
        "ssl": ssl_context,  # SSL context for Neon
        "server_settings": {
            "jit": "off"  # Recommended for Neon
        }
    }
)

# Async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Create database tables. Call this on application startup."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    Automatically handles session lifecycle and cleanup.

    Usage:
        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
