"""
Shared pytest fixtures for all tests.

This conftest.py file is located at the root of the tests directory,
making fixtures available to all test modules.
"""

import pytest
from typing import Generator


# ==================== Application Fixtures ====================

@pytest.fixture(scope="session")
def app():
    """
    Create application instance for testing.

    Scope: session (created once for entire test session)
    """
    from myapp import create_app

    app = create_app(testing=True)
    return app


@pytest.fixture(scope="function")
def client(app):
    """
    Create test client for API testing.

    Scope: function (new client for each test)
    """
    return app.test_client()


# ==================== Database Fixtures ====================

@pytest.fixture(scope="session")
def db_engine():
    """
    Create database engine for testing.

    Scope: session (one engine for all tests)
    """
    from sqlmodel import create_engine

    # Use in-memory SQLite for fast tests
    engine = create_engine("sqlite:///:memory:")
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator:
    """
    Provide database session with automatic rollback.

    Each test gets a fresh session with all changes rolled back afterwards.

    Scope: function (new session per test)
    """
    from sqlmodel import Session, SQLModel

    # Create tables
    SQLModel.metadata.create_all(db_engine)

    with Session(db_engine) as session:
        yield session
        # Rollback all changes after test
        session.rollback()

    # Drop all tables after test
    SQLModel.metadata.drop_all(db_engine)


# ==================== Test Data Fixtures ====================

@pytest.fixture
def sample_user_data():
    """
    Provide sample user data for tests.

    Returns a dictionary with valid user fields.
    """
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 30,
    }


@pytest.fixture
def sample_users_list():
    """
    Provide a list of sample users for bulk testing.
    """
    return [
        {"name": "Alice", "email": "alice@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 35},
    ]


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_external_api(mocker):
    """
    Mock external API calls.

    Returns a mock that can be configured in individual tests.
    """
    return mocker.patch("myapp.external_api.make_request")


@pytest.fixture
def mock_email_service(mocker):
    """
    Mock email sending service.
    """
    return mocker.patch("myapp.email.send_email")


# ==================== Authentication Fixtures ====================

@pytest.fixture
def auth_token(db_session, sample_user_data):
    """
    Create authentication token for testing protected endpoints.
    """
    from myapp.models import User
    from myapp.auth import create_access_token

    # Create test user
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Generate token
    token = create_access_token(user.id)
    return token


@pytest.fixture
def authenticated_client(client, auth_token):
    """
    Provide test client with authentication headers.
    """
    client.headers = {"Authorization": f"Bearer {auth_token}"}
    return client


# ==================== Pytest Hooks ====================

def pytest_configure(config):
    """
    Configure pytest with custom settings.
    """
    # Add custom markers
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection.

    This hook runs after test collection and can be used to
    automatically add markers based on test location.
    """
    for item in items:
        # Auto-mark tests based on directory
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "functional" in str(item.fspath):
            item.add_marker(pytest.mark.functional)
