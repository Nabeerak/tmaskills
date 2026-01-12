# Async Testing with Pytest

## Table of Contents

- [Introduction](#introduction)
- [pytest-asyncio Setup](#pytest-asyncio-setup)
- [Basic Async Testing](#basic-async-testing)
- [Testing Async Functions](#testing-async-functions)
- [Async Fixtures](#async-fixtures)
- [Testing FastAPI Applications](#testing-fastapi-applications)
- [Testing WebSocket Connections](#testing-websocket-connections)
- [Testing Async Database Operations](#testing-async-database-operations)
- [Testing Async API Calls](#testing-async-api-calls)
- [Mocking Async Functions](#mocking-async-functions)
- [Testing Concurrent Operations](#testing-concurrent-operations)
- [Advanced Patterns](#advanced-patterns)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)

---

## Introduction

**Async testing** allows you to test asynchronous code using `async`/`await` syntax in Python.

### Why Async Testing?

- **Modern Python**: Many frameworks use async (FastAPI, aiohttp, etc.)
- **Real-world Simulation**: Test concurrent operations
- **Performance**: Test async efficiency
- **I/O Operations**: Database, network, file operations

### When to Use Async

```python
# Async is beneficial for:
- HTTP API calls
- Database queries
- File I/O operations
- WebSocket connections
- Message queue operations

# Not needed for:
- Pure computations
- Synchronous operations
- Simple data transformations
```

---

## pytest-asyncio Setup

### Installation

```bash
pip install pytest-asyncio
```

### Configuration

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Manual Mode

```python
# If not using auto mode
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result == expected
```

---

## Basic Async Testing

### Simple Async Test

```python
import pytest

async def fetch_data():
    await asyncio.sleep(0.1)
    return {"data": "test"}

@pytest.mark.asyncio
async def test_fetch_data():
    # Arrange
    expected = {"data": "test"}

    # Act
    result = await fetch_data()

    # Assert
    assert result == expected
```

### Testing Async with Auto Mode

```python
# With asyncio_mode = auto, no decorator needed
async def test_async_function():
    result = await async_operation()
    assert result == "expected"
```

### Multiple Async Operations

```python
async def test_multiple_operations():
    # Sequential
    result1 = await operation1()
    result2 = await operation2()

    assert result1 == "expected1"
    assert result2 == "expected2"
```

### Concurrent Operations

```python
import asyncio

async def test_concurrent_operations():
    # Run in parallel
    results = await asyncio.gather(
        operation1(),
        operation2(),
        operation3()
    )

    assert len(results) == 3
    assert all(r is not None for r in results)
```

---

## Testing Async Functions

### Async Function with Parameters

```python
async def get_user(user_id: int):
    await asyncio.sleep(0.1)
    return User(id=user_id, name=f"User{user_id}")

async def test_get_user():
    user = await get_user(123)

    assert user.id == 123
    assert user.name == "User123"
```

### Testing Async Exceptions

```python
async def fetch_user(user_id: int):
    if user_id == 0:
        raise ValueError("Invalid user ID")
    return User(id=user_id)

async def test_invalid_user_id():
    with pytest.raises(ValueError, match="Invalid user ID"):
        await fetch_user(0)
```

### Testing Timeouts

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "done"

async def test_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1.0)
```

### Testing Async Context Managers

```python
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

    async def connect(self):
        await asyncio.sleep(0.1)

    async def disconnect(self):
        await asyncio.sleep(0.1)

async def test_async_context_manager():
    async with AsyncDatabase() as db:
        assert db is not None
    # disconnect() is automatically called
```

---

## Async Fixtures

### Basic Async Fixture

```python
import pytest

@pytest.fixture
async def async_client():
    """Provide async HTTP client."""
    client = AsyncHTTPClient()
    await client.initialize()
    yield client
    await client.close()

async def test_api_call(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
```

### Async Fixture with Scope

```python
@pytest.fixture(scope="module")
async def database():
    """Module-scoped async database."""
    db = AsyncDatabase()
    await db.connect()
    await db.initialize_schema()

    yield db

    await db.close()

async def test_query(database):
    users = await database.query("SELECT * FROM users")
    assert isinstance(users, list)
```

### Async Fixture Factory

```python
@pytest.fixture
async def user_factory(database):
    """Factory for creating test users."""
    created_users = []

    async def create_user(name="Test User", email=None):
        if email is None:
            email = f"{name.lower().replace(' ', '.')}@example.com"

        user = User(name=name, email=email)
        await database.save(user)
        created_users.append(user)
        return user

    yield create_user

    # Cleanup
    for user in created_users:
        await database.delete(user)

async def test_user_creation(user_factory):
    alice = await user_factory(name="Alice")
    bob = await user_factory(name="Bob")

    assert alice.email == "alice@example.com"
    assert bob.email == "bob@example.com"
```

### Mixing Sync and Async Fixtures

```python
@pytest.fixture
def sync_config():
    """Synchronous fixture."""
    return {"host": "localhost", "port": 8080}

@pytest.fixture
async def async_client(sync_config):
    """Async fixture using sync fixture."""
    client = AsyncClient(**sync_config)
    await client.connect()
    yield client
    await client.disconnect()

async def test_with_both_fixtures(sync_config, async_client):
    assert sync_config["host"] == "localhost"
    response = await async_client.ping()
    assert response == "pong"
```

---

## Testing FastAPI Applications

### Basic FastAPI Testing

```python
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_root_endpoint(client):
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Testing POST Endpoints

```python
@app.post("/users")
async def create_user(user: UserCreate):
    return {"id": 1, "name": user.name, "email": user.email}

async def test_create_user(client):
    user_data = {
        "name": "Alice",
        "email": "alice@example.com"
    }

    response = await client.post("/users", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert "id" in data
```

### Testing with Dependencies

```python
from fastapi import Depends

async def get_current_user():
    return User(id=1, name="Alice")

@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

async def test_with_dependency_override(client):
    # Override dependency
    async def override_get_current_user():
        return User(id=999, name="Test User")

    app.dependency_overrides[get_current_user] = override_get_current_user

    response = await client.get("/me")

    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

    # Clear override
    app.dependency_overrides.clear()
```

### Testing Authentication

```python
@pytest.fixture
async def authenticated_client(client):
    """Client with authentication token."""
    # Get auth token
    response = await client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json()["access_token"]

    # Add to headers
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

async def test_protected_endpoint(authenticated_client):
    response = await authenticated_client.get("/protected")
    assert response.status_code == 200
```

### Testing File Uploads

```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

async def test_file_upload(client):
    files = {"file": ("test.txt", b"test content", "text/plain")}

    response = await client.post("/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["size"] == 12
```

---

## Testing WebSocket Connections

### Basic WebSocket Test

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")

async def test_websocket():
    async with AsyncClient(app=app, base_url="http://test") as client:
        async with client.websocket_connect("/ws") as websocket:
            await websocket.send_text("Hello")
            data = await websocket.receive_text()

            assert data == "Echo: Hello"
```

### Testing WebSocket Messages

```python
async def test_websocket_multiple_messages():
    async with AsyncClient(app=app, base_url="http://test") as client:
        async with client.websocket_connect("/ws") as websocket:
            # Send multiple messages
            messages = ["msg1", "msg2", "msg3"]

            for msg in messages:
                await websocket.send_text(msg)
                response = await websocket.receive_text()
                assert response == f"Echo: {msg}"
```

### Testing WebSocket Errors

```python
@app.websocket("/ws/auth")
async def websocket_auth(websocket: WebSocket, token: str):
    if token != "valid_token":
        await websocket.close(code=1008)
        return

    await websocket.accept()
    await websocket.send_text("Connected")

async def test_websocket_authentication_failure():
    async with AsyncClient(app=app, base_url="http://test") as client:
        with pytest.raises(WebSocketDisconnect):
            async with client.websocket_connect("/ws/auth?token=invalid"):
                pass
```

---

## Testing Async Database Operations

### SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def async_db():
    """Async database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()

async def test_create_user(async_db):
    user = User(name="Alice", email="alice@example.com")

    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)

    assert user.id is not None
    assert user.name == "Alice"
```

### Testing Queries

```python
async def test_query_users(async_db):
    # Create test data
    users = [
        User(name="Alice", age=25),
        User(name="Bob", age=30),
        User(name="Charlie", age=25)
    ]

    async_db.add_all(users)
    await async_db.commit()

    # Query
    from sqlalchemy import select
    result = await async_db.execute(
        select(User).where(User.age == 25)
    )
    found_users = result.scalars().all()

    assert len(found_users) == 2
    assert set(u.name for u in found_users) == {"Alice", "Charlie"}
```

### Transaction Rollback

```python
@pytest.fixture
async def db_session():
    """Session with automatic rollback."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(bind=conn) as session:
            async with session.begin():
                yield session
                await session.rollback()

async def test_with_rollback(db_session):
    user = User(name="Alice")
    db_session.add(user)
    await db_session.flush()

    # Changes are visible in this test
    assert user.id is not None

    # But rolled back after test
```

---

## Testing Async API Calls

### Mocking with aioresponses

```python
from aioresponses import aioresponses
import aiohttp

async def fetch_user(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/users/{user_id}") as resp:
            return await resp.json()

async def test_fetch_user():
    with aioresponses() as mocked:
        # Mock the API response
        mocked.get(
            "https://api.example.com/users/123",
            payload={"id": 123, "name": "Alice"}
        )

        user = await fetch_user(123)

        assert user["name"] == "Alice"
```

### Testing Retry Logic

```python
async def fetch_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.json()
        except aiohttp.ClientError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(0.1 * (2 ** attempt))

async def test_retry_logic():
    with aioresponses() as mocked:
        url = "https://api.example.com/data"

        # Fail twice, then succeed
        mocked.get(url, exception=aiohttp.ClientError())
        mocked.get(url, exception=aiohttp.ClientError())
        mocked.get(url, payload={"data": "success"})

        result = await fetch_with_retry(url)

        assert result["data"] == "success"
```

### Testing Rate Limiting

```python
class RateLimiter:
    def __init__(self, calls_per_second):
        self.calls_per_second = calls_per_second
        self.calls = []

    async def acquire(self):
        now = asyncio.get_event_loop().time()
        self.calls = [c for c in self.calls if c > now - 1]

        if len(self.calls) >= self.calls_per_second:
            wait_time = self.calls[0] - (now - 1)
            await asyncio.sleep(wait_time)

        self.calls.append(asyncio.get_event_loop().time())

async def test_rate_limiter():
    limiter = RateLimiter(calls_per_second=2)

    start = asyncio.get_event_loop().time()

    for _ in range(3):
        await limiter.acquire()

    duration = asyncio.get_event_loop().time() - start

    # Third call should be delayed
    assert duration >= 1.0
```

---

## Mocking Async Functions

### Basic Async Mock

```python
from unittest.mock import AsyncMock

async def send_email(to, subject, body):
    email_service = EmailService()
    await email_service.send(to, subject, body)

async def test_send_email(mocker):
    mock_service = AsyncMock()
    mocker.patch('myapp.EmailService', return_value=mock_service)

    await send_email("alice@example.com", "Hello", "Test")

    mock_service.send.assert_called_once_with(
        "alice@example.com",
        "Hello",
        "Test"
    )
```

### Async Mock Return Value

```python
async def get_user_data(user_id):
    api = UserAPI()
    return await api.fetch(user_id)

async def test_get_user_data(mocker):
    mock_api = AsyncMock()
    mock_api.fetch.return_value = {"id": 123, "name": "Alice"}

    mocker.patch('myapp.UserAPI', return_value=mock_api)

    result = await get_user_data(123)

    assert result["name"] == "Alice"
```

### Async Mock Side Effect

```python
async def test_async_side_effect(mocker):
    mock_db = AsyncMock()

    # First call fails, second succeeds
    mock_db.query.side_effect = [
        Exception("Connection error"),
        [User(name="Alice")]
    ]

    with pytest.raises(Exception):
        await mock_db.query()

    result = await mock_db.query()
    assert len(result) == 1
```

### Mocking Async Context Managers

```python
from unittest.mock import AsyncMock

async def process_with_lock():
    async with acquire_lock() as lock:
        return await do_work(lock)

async def test_with_mocked_lock(mocker):
    mock_lock = AsyncMock()
    mock_lock.__aenter__.return_value = "fake_lock"
    mock_lock.__aexit__.return_value = None

    mocker.patch('myapp.acquire_lock', return_value=mock_lock)
    mocker.patch('myapp.do_work', return_value="done")

    result = await process_with_lock()

    assert result == "done"
    mock_lock.__aenter__.assert_called_once()
    mock_lock.__aexit__.assert_called_once()
```

---

## Testing Concurrent Operations

### Testing asyncio.gather

```python
async def process_items(items):
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

async def test_concurrent_processing(mocker):
    mock_process = mocker.patch('myapp.process_item')
    mock_process.side_effect = lambda x: f"processed_{x}"

    items = [1, 2, 3, 4, 5]
    results = await process_items(items)

    assert len(results) == 5
    assert results[0] == "processed_1"
    assert mock_process.call_count == 5
```

### Testing Task Cancellation

```python
async def cancellable_operation():
    try:
        await asyncio.sleep(10)
        return "completed"
    except asyncio.CancelledError:
        return "cancelled"

async def test_task_cancellation():
    task = asyncio.create_task(cancellable_operation())

    await asyncio.sleep(0.1)
    task.cancel()

    result = await task
    assert result == "cancelled"
```

### Testing Race Conditions

```python
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate work
            self.value = current + 1

async def test_thread_safe_counter():
    counter = Counter()

    # Run 10 concurrent increments
    await asyncio.gather(*[counter.increment() for _ in range(10)])

    # Should be exactly 10
    assert counter.value == 10
```

### Testing Async Queues

```python
async def producer(queue, items):
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0.01)
    await queue.put(None)  # Sentinel

async def consumer(queue):
    results = []
    while True:
        item = await queue.get()
        if item is None:
            break
        results.append(item)
    return results

async def test_producer_consumer():
    queue = asyncio.Queue()
    items = [1, 2, 3, 4, 5]

    producer_task = asyncio.create_task(producer(queue, items))
    consumer_task = asyncio.create_task(consumer(queue))

    await producer_task
    results = await consumer_task

    assert results == items
```

---

## Advanced Patterns

### Testing Async Generators

```python
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async def test_async_generator():
    results = []

    async for value in async_range(5):
        results.append(value)

    assert results == [0, 1, 2, 3, 4]
```

### Testing with AsyncExitStack

```python
from contextlib import AsyncExitStack

async def test_multiple_async_contexts():
    async with AsyncExitStack() as stack:
        db = await stack.enter_async_context(AsyncDatabase())
        cache = await stack.enter_async_context(AsyncCache())
        lock = await stack.enter_async_context(AsyncLock())

        # All contexts are active
        assert db.is_connected
        assert cache.is_connected
        assert lock.is_acquired

    # All automatically exited
```

### Testing Event Loops

```python
async def test_custom_event_loop():
    # Get current event loop
    loop = asyncio.get_event_loop()

    # Schedule callback
    future = loop.create_future()
    loop.call_later(0.1, lambda: future.set_result("done"))

    result = await future
    assert result == "done"
```

---

## Best Practices

### 1. Use Auto Mode

```python
# pytest.ini
[pytest]
asyncio_mode = auto

# No need for @pytest.mark.asyncio
async def test_something():
    result = await async_function()
    assert result == "expected"
```

### 2. Proper Cleanup

```python
@pytest.fixture
async def resource():
    """Always cleanup async resources."""
    r = await create_resource()

    yield r

    await r.cleanup()  # Ensure cleanup
```

### 3. Test Isolation

```python
# ✓ Good - Each test gets fresh database
@pytest.fixture
async def db():
    db = await create_db()
    yield db
    await db.drop_all()

# ❌ Bad - Tests share state
@pytest.fixture(scope="module")
async def db():
    return await create_db()
```

### 4. Use AsyncMock

```python
# ✓ Good - Use AsyncMock for async functions
mock = AsyncMock()
mock.fetch.return_value = "data"

# ❌ Bad - Regular Mock won't work properly
mock = Mock()
mock.fetch.return_value = "data"  # Not awaitable!
```

### 5. Test Concurrency Explicitly

```python
async def test_concurrent_requests():
    """Explicitly test concurrent behavior."""
    results = await asyncio.gather(
        api_call(1),
        api_call(2),
        api_call(3)
    )

    assert len(results) == 3
```

---

## Common Pitfalls

### Forgetting await

```python
# ❌ Wrong - Forgot await
async def test_wrong():
    result = async_function()  # Returns coroutine, not result!
    assert result == "expected"  # Fails

# ✓ Right
async def test_right():
    result = await async_function()
    assert result == "expected"
```

### Mixing Sync and Async

```python
# ❌ Wrong - Can't call async from sync
def test_sync():
    result = async_function()  # Error!

# ✓ Right - Use async test
async def test_async():
    result = await async_function()
```

### Not Cleaning Up Tasks

```python
# ❌ Wrong - Tasks left running
async def test_no_cleanup():
    task = asyncio.create_task(long_running_task())
    # Test ends, task still running!

# ✓ Right - Clean up tasks
async def test_with_cleanup():
    task = asyncio.create_task(long_running_task())
    try:
        # Test logic
        pass
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
```

### Using Regular Mock for Async

```python
# ❌ Wrong - Mock not awaitable
mock = Mock()
await mock.method()  # TypeError!

# ✓ Right - Use AsyncMock
mock = AsyncMock()
await mock.method()  # Works!
```

---

## Summary

**Key Concepts**:
- Use `pytest-asyncio` for async testing
- `AsyncMock` for mocking async functions
- Proper cleanup with yield fixtures
- Test concurrent operations explicitly

**FastAPI Testing**:
- Use `AsyncClient` from httpx
- Override dependencies for testing
- Test WebSocket connections
- Test authentication flows

**Best Practices**:
- Enable `asyncio_mode = auto`
- Always await async functions
- Clean up async resources
- Use AsyncMock for async mocks
- Test isolation with fixtures

**Common Patterns**:
- Async fixtures
- Mocking async API calls
- Testing concurrent operations
- Database transaction rollback
- WebSocket testing
