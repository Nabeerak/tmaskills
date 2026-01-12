"""
Database engine and session configuration.

This template demonstrates:
- Engine setup for different databases (SQLite, PostgreSQL)
- Connection pooling configuration
- Session management with context managers
- Dependency injection pattern for FastAPI
- Database initialization
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os


# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"  # Default to SQLite for development
)

# SQLite-specific connection args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (set to False in production)
    connect_args=connect_args,
    # Connection pool settings (PostgreSQL/MySQL)
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Extra connections when pool is full
    pool_recycle=3600,  # Recycle connections after 1 hour
)


def create_db_and_tables():
    """
    Create all database tables.

    Call this on application startup to ensure tables exist.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Create a database session.

    Use this as a FastAPI dependency:

    @app.get("/users")
    def get_users(session: Session = Depends(get_session)):
        ...

    The session is automatically closed after the request.
    """
    with Session(engine) as session:
        yield session


# Example: Using session directly (not in FastAPI)
def example_usage():
    """Example of using session directly."""
    with Session(engine) as session:
        # Your database operations here
        from models import User

        # Create
        user = User(email="user@example.com", username="user", full_name="User Name")
        session.add(user)
        session.commit()
        session.refresh(user)

        # Read
        from sqlmodel import select

        statement = select(User).where(User.email == "user@example.com")
        user = session.exec(statement).first()

        print(f"Created user: {user}")


# Alternative: PostgreSQL configuration
def create_postgresql_engine():
    """Create engine with PostgreSQL-specific settings."""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/dbname"
    )

    return create_engine(
        database_url,
        echo=False,  # Disable SQL logging in production
        pool_pre_ping=True,
        pool_size=20,  # Larger pool for PostgreSQL
        max_overflow=40,
        pool_recycle=3600,
        # PostgreSQL-specific optimizations
        pool_timeout=30,  # Wait up to 30 seconds for a connection
    )


# Alternative: MySQL configuration
def create_mysql_engine():
    """Create engine with MySQL-specific settings."""
    database_url = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://user:password@localhost:3306/dbname"
    )

    return create_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=15,
        max_overflow=30,
        pool_recycle=3600,
    )


# Testing: In-memory database
def create_test_engine():
    """Create in-memory SQLite engine for testing."""
    return create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False}
    )


if __name__ == "__main__":
    # Initialize database tables
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")

    # Example usage
    example_usage()
