"""
Example async tests for FastAPI and async code.

This file demonstrates:
- Testing async functions with pytest-asyncio
- Testing FastAPI endpoints with TestClient and AsyncClient
- Async fixtures
- Mocking async functions
"""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient


# ==================== Synchronous FastAPI Tests ====================

def test_read_root_endpoint():
    """Test root endpoint returns welcome message."""
    from myapp.main import app

    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}


def test_create_user_endpoint(client, sample_user_data):
    """Test user creation endpoint."""
    # Arrange - done by fixtures

    # Act
    response = client.post("/api/v1/users", json=sample_user_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_user_data["name"]
    assert data["email"] == sample_user_data["email"]
    assert "id" in data


def test_get_user_endpoint(client, auth_token):
    """Test getting user by ID (authenticated)."""
    # Arrange
    # First create a user
    user_data = {"name": "Alice", "email": "alice@example.com"}
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]

    # Add authentication
    client.headers = {"Authorization": f"Bearer {auth_token}"}

    # Act
    response = client.get(f"/api/v1/users/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user_endpoint_requires_authentication(client):
    """Test that updating user requires authentication."""
    # Arrange
    user_id = 1
    update_data = {"name": "Updated Name"}

    # Act
    response = client.patch(f"/api/v1/users/{user_id}", json=update_data)

    # Assert
    assert response.status_code == 401
    assert "Unauthorized" in response.json()["detail"]


# ==================== Async Function Tests ====================

@pytest.mark.asyncio
async def test_async_fetch_data():
    """Test async function that fetches data."""
    from myapp.services import async_fetch_data

    # Arrange
    user_id = 123

    # Act
    result = await async_fetch_data(user_id)

    # Assert
    assert result is not None
    assert result["user_id"] == user_id


@pytest.mark.asyncio
async def test_async_database_query(db_session):
    """Test async database query."""
    from myapp.models import User
    from sqlmodel import select

    # Arrange
    user = User(name="Alice", email="alice@example.com")
    db_session.add(user)
    await db_session.commit()

    # Act
    statement = select(User).where(User.email == "alice@example.com")
    result = await db_session.exec(statement)
    found_user = result.first()

    # Assert
    assert found_user is not None
    assert found_user.name == "Alice"


# ==================== Async Fixtures ====================

@pytest.fixture
async def async_client():
    """Provide async HTTP client for testing."""
    from myapp.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def async_db_session():
    """Provide async database session."""
    from sqlmodel.ext.asyncio.session import AsyncSession
    from sqlmodel import create_engine
    from myapp.core.database import get_async_engine

    engine = get_async_engine()

    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
        await session.close()


# ==================== Async Client Tests ====================

@pytest.mark.asyncio
async def test_async_get_users(async_client):
    """Test getting users list with async client."""
    # Act
    response = await async_client.get("/api/v1/users")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_async_create_user(async_client):
    """Test creating user with async client."""
    # Arrange
    user_data = {
        "name": "Async User",
        "email": "async@example.com"
    }

    # Act
    response = await async_client.post("/api/v1/users", json=user_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Async User"
    assert "id" in data


@pytest.mark.asyncio
async def test_async_endpoint_with_auth(async_client, auth_token):
    """Test authenticated async endpoint."""
    # Arrange
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Act
    response = await async_client.get("/api/v1/me", headers=headers)

    # Assert
    assert response.status_code == 200
    assert "email" in response.json()


# ==================== Mocking Async Functions ====================

@pytest.mark.asyncio
async def test_async_external_api_call(mocker):
    """Test async function that calls external API."""
    from myapp.services import fetch_external_data

    # Arrange
    mock_response = {"data": "mocked"}
    mock_get = mocker.patch(
        "myapp.services.httpx.AsyncClient.get",
        return_value=mocker.Mock(json=lambda: mock_response)
    )

    # Act
    result = await fetch_external_data()

    # Assert
    assert result == mock_response
    mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_async_email_sending(mocker):
    """Test async email sending function."""
    from myapp.email import send_async_email

    # Arrange
    mock_send = mocker.patch("myapp.email.async_smtp_send")
    recipient = "user@example.com"
    subject = "Test Email"

    # Act
    await send_async_email(recipient, subject, "Body")

    # Assert
    mock_send.assert_called_once_with(
        to=recipient,
        subject=subject,
        body="Body"
    )


# ==================== Testing Background Tasks ====================

@pytest.mark.asyncio
async def test_background_task_execution(async_client, mocker):
    """Test that background task is triggered."""
    from myapp.tasks import process_in_background

    # Arrange
    mock_task = mocker.patch("myapp.tasks.process_in_background")

    # Act
    response = await async_client.post("/api/v1/trigger-task")

    # Assert
    assert response.status_code == 202  # Accepted
    mock_task.assert_called_once()


# ==================== Testing WebSocket Connections ====================

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection."""
    from fastapi.testclient import TestClient
    from myapp.main import app

    client = TestClient(app)

    # Act & Assert
    with client.websocket_connect("/ws") as websocket:
        # Send data
        websocket.send_text("Hello")

        # Receive response
        data = websocket.receive_text()
        assert data == "Echo: Hello"


# ==================== Parametrized Async Tests ====================

@pytest.mark.asyncio
@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200),    # Existing user
    (999, 404),  # Non-existent user
    (-1, 422),   # Invalid ID
])
async def test_get_user_various_ids(async_client, user_id, expected_status):
    """Test getting user with various IDs."""
    # Act
    response = await async_client.get(f"/api/v1/users/{user_id}")

    # Assert
    assert response.status_code == expected_status


# ==================== Testing Async Generators ====================

@pytest.mark.asyncio
async def test_async_generator():
    """Test async generator function."""
    from myapp.services import fetch_paginated_data

    # Arrange
    expected_pages = 3
    collected_data = []

    # Act
    async for page in fetch_paginated_data(page_size=10):
        collected_data.append(page)
        if len(collected_data) >= expected_pages:
            break

    # Assert
    assert len(collected_data) == expected_pages
    assert all(len(page) == 10 for page in collected_data)


# ==================== Testing Async Context Managers ====================

@pytest.mark.asyncio
async def test_async_context_manager():
    """Test async context manager."""
    from myapp.database import async_transaction

    # Arrange
    async with async_transaction() as session:
        # Act
        user = User(name="Test", email="test@example.com")
        session.add(user)
        await session.commit()

        # Assert
        assert user.id is not None


# ==================== Testing Concurrent Operations ====================

@pytest.mark.asyncio
async def test_concurrent_requests(async_client):
    """Test multiple concurrent API requests."""
    import asyncio

    # Arrange
    endpoints = [
        "/api/v1/users/1",
        "/api/v1/users/2",
        "/api/v1/users/3",
    ]

    # Act
    tasks = [async_client.get(endpoint) for endpoint in endpoints]
    responses = await asyncio.gather(*tasks)

    # Assert
    assert all(r.status_code in [200, 404] for r in responses)


# ==================== Testing Timeouts ====================

@pytest.mark.asyncio
async def test_async_function_timeout():
    """Test that async function times out appropriately."""
    from myapp.services import slow_async_operation

    # Act & Assert
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_async_operation(), timeout=1.0)


# ==================== Testing Retries ====================

@pytest.mark.asyncio
async def test_async_retry_mechanism(mocker):
    """Test async function with retry logic."""
    from myapp.services import fetch_with_retry

    # Arrange
    mock_fetch = mocker.AsyncMock(side_effect=[
        Exception("Connection error"),  # First attempt fails
        Exception("Timeout"),            # Second attempt fails
        {"data": "success"}              # Third attempt succeeds
    ])
    mocker.patch("myapp.services.fetch_data", mock_fetch)

    # Act
    result = await fetch_with_retry(max_retries=3)

    # Assert
    assert result == {"data": "success"}
    assert mock_fetch.call_count == 3
