# Mocking and Test Doubles

## Table of Contents

- [Introduction](#introduction)
- [Types of Test Doubles](#types-of-test-doubles)
- [unittest.mock Basics](#unittestmock-basics)
- [Mock Objects](#mock-objects)
- [Patching](#patching)
- [Mocking APIs](#mocking-apis)
- [Mocking Databases](#mocking-databases)
- [Mocking File Systems](#mocking-file-systems)
- [Mocking External Services](#mocking-external-services)
- [pytest-mock Plugin](#pytest-mock-plugin)
- [Advanced Mocking Patterns](#advanced-mocking-patterns)
- [Assertions on Mocks](#assertions-on-mocks)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)

---

## Introduction

**Mocking** replaces real objects with test doubles that simulate behavior, allowing you to test code in isolation without dependencies on external systems.

### Why Mock?

- **Isolation**: Test code without external dependencies
- **Speed**: Avoid slow operations (network, database, file I/O)
- **Reliability**: Tests don't fail due to external issues
- **Control**: Simulate edge cases and error conditions
- **Safety**: Don't affect real systems during testing

### When to Mock

```python
# Mock external dependencies
- HTTP API calls
- Database operations
- File system access
- Email sending
- Payment processing
- Time-dependent code

# Don't mock
- Your own code under test
- Simple data structures
- Pure functions
```

---

## Types of Test Doubles

### Dummy

Passed around but never used:

```python
def test_user_creation():
    # Dummy - not actually used
    dummy_logger = None
    user = User(name="Alice", logger=dummy_logger)
    assert user.name == "Alice"
```

### Stub

Provides canned answers:

```python
class StubDatabase:
    def get_user(self, user_id):
        # Always returns the same result
        return User(id=user_id, name="Test User")

def test_user_service():
    db = StubDatabase()
    service = UserService(db)

    user = service.get_user(123)
    assert user.name == "Test User"
```

### Fake

Working implementation with shortcuts:

```python
class FakeDatabase:
    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.id] = user

    def get(self, user_id):
        return self.users.get(user_id)

def test_user_repository():
    db = FakeDatabase()
    repo = UserRepository(db)

    user = User(id=1, name="Alice")
    repo.save(user)

    retrieved = repo.get(1)
    assert retrieved.name == "Alice"
```

### Mock

Records calls and can verify behavior:

```python
from unittest.mock import Mock

def test_email_notification():
    mock_email = Mock()
    service = NotificationService(email_sender=mock_email)

    service.notify_user("alice@example.com", "Welcome!")

    # Verify the mock was called correctly
    mock_email.send.assert_called_once_with(
        to="alice@example.com",
        subject="Welcome!"
    )
```

### Spy

Wraps real object and records calls:

```python
from unittest.mock import Mock

def test_cache_usage():
    real_database = Database()
    spy = Mock(wraps=real_database)

    service = UserService(spy)
    service.get_user(123)  # Uses real database
    service.get_user(123)  # Should use cache

    # Verify database called only once
    assert spy.query.call_count == 1
```

---

## unittest.mock Basics

### Creating Mocks

```python
from unittest.mock import Mock

# Basic mock
mock_obj = Mock()
mock_obj.method()
mock_obj.method.assert_called_once()

# Mock with return value
mock_db = Mock()
mock_db.get_user.return_value = User(name="Alice")

user = mock_db.get_user(123)
assert user.name == "Alice"

# Mock with side effect (exception)
mock_api = Mock()
mock_api.call.side_effect = ConnectionError("Network error")

with pytest.raises(ConnectionError):
    mock_api.call()
```

### MagicMock

Supports magic methods:

```python
from unittest.mock import MagicMock

# MagicMock supports __len__, __iter__, etc.
mock_list = MagicMock()
mock_list.__len__.return_value = 5
mock_list.__iter__.return_value = iter([1, 2, 3])

assert len(mock_list) == 5
assert list(mock_list) == [1, 2, 3]
```

### Spec

Restrict mock to match real object:

```python
class UserService:
    def get_user(self, user_id):
        pass

    def save_user(self, user):
        pass

# Mock with spec - only allows real methods
mock_service = Mock(spec=UserService)
mock_service.get_user(123)  # OK
mock_service.invalid_method()  # AttributeError!
```

---

## Mock Objects

### Return Values

```python
from unittest.mock import Mock

def test_api_client():
    mock_client = Mock()
    mock_client.get_user.return_value = {
        "id": 123,
        "name": "Alice"
    }

    result = mock_client.get_user(123)
    assert result["name"] == "Alice"
```

### Side Effects

```python
def test_retry_logic():
    mock_api = Mock()
    # First call fails, second succeeds
    mock_api.fetch.side_effect = [
        ConnectionError("Network error"),
        {"data": "success"}
    ]

    with pytest.raises(ConnectionError):
        mock_api.fetch()

    result = mock_api.fetch()
    assert result["data"] == "success"
```

### Side Effect Function

```python
def test_custom_behavior():
    def custom_side_effect(user_id):
        if user_id == 1:
            return User(name="Alice")
        else:
            raise ValueError("User not found")

    mock_db = Mock()
    mock_db.get_user.side_effect = custom_side_effect

    user = mock_db.get_user(1)
    assert user.name == "Alice"

    with pytest.raises(ValueError):
        mock_db.get_user(999)
```

### Mock Attributes

```python
def test_mock_attributes():
    mock_user = Mock()
    mock_user.name = "Alice"
    mock_user.email = "alice@example.com"
    mock_user.is_active = True

    assert mock_user.name == "Alice"
    assert mock_user.is_active is True
```

### Configure Mock

```python
from unittest.mock import Mock

def test_configured_mock():
    mock_response = Mock(
        status_code=200,
        json=Mock(return_value={"data": "test"})
    )

    assert mock_response.status_code == 200
    assert mock_response.json()["data"] == "test"
```

---

## Patching

### patch Decorator

```python
from unittest.mock import patch

# Code to test
def send_notification(user_id):
    user = get_user_from_db(user_id)
    send_email(user.email, "Hello!")

# Test with patch
@patch('myapp.send_email')
@patch('myapp.get_user_from_db')
def test_send_notification(mock_get_user, mock_send_email):
    # Setup
    mock_get_user.return_value = User(email="alice@example.com")

    # Execute
    send_notification(123)

    # Verify
    mock_get_user.assert_called_once_with(123)
    mock_send_email.assert_called_once_with("alice@example.com", "Hello!")
```

### patch Context Manager

```python
from unittest.mock import patch

def test_with_context_manager():
    with patch('myapp.get_user_from_db') as mock_get_user:
        mock_get_user.return_value = User(name="Alice")

        result = get_user_from_db(123)
        assert result.name == "Alice"
```

### patch.object

```python
from unittest.mock import patch

class UserService:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        return self.db.query(user_id)

def test_user_service():
    service = UserService(Database())

    with patch.object(service.db, 'query') as mock_query:
        mock_query.return_value = User(name="Alice")

        user = service.get_user(123)
        assert user.name == "Alice"
```

### Patching Class Methods

```python
from unittest.mock import patch

@patch.object(Database, 'connect')
def test_database_connection(mock_connect):
    mock_connect.return_value = "fake_connection"

    db = Database()
    conn = db.connect()

    assert conn == "fake_connection"
    mock_connect.assert_called_once()
```

### Patching Multiple Targets

```python
@patch('myapp.service3')
@patch('myapp.service2')
@patch('myapp.service1')
def test_multiple_patches(mock_s1, mock_s2, mock_s3):
    # Note: decorators are applied bottom-up!
    # mock_s1 corresponds to service1
    # mock_s2 corresponds to service2
    # mock_s3 corresponds to service3
    pass
```

---

## Mocking APIs

### HTTP Requests

```python
from unittest.mock import Mock, patch
import requests

def fetch_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

@patch('requests.get')
def test_fetch_user_data(mock_get):
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "id": 123,
        "name": "Alice"
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Test
    user = fetch_user_data(123)

    # Verify
    assert user["name"] == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/123")
```

### Using responses Library

```python
import responses
import requests

@responses.activate
def test_api_call():
    # Mock API response
    responses.add(
        responses.GET,
        "https://api.example.com/users/123",
        json={"id": 123, "name": "Alice"},
        status=200
    )

    # Make real request (but intercepted)
    response = requests.get("https://api.example.com/users/123")

    assert response.status_code == 200
    assert response.json()["name"] == "Alice"
```

### Error Responses

```python
@patch('requests.get')
def test_api_error_handling(mock_get):
    # Simulate 404 error
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        response = requests.get("https://api.example.com/users/999")
        response.raise_for_status()
```

### Timeout and Network Errors

```python
@patch('requests.get')
def test_network_timeout(mock_get):
    mock_get.side_effect = requests.Timeout("Connection timeout")

    with pytest.raises(requests.Timeout):
        fetch_user_data(123)

@patch('requests.get')
def test_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError("Network unreachable")

    with pytest.raises(requests.ConnectionError):
        fetch_user_data(123)
```

---

## Mocking Databases

### Mock Database Connection

```python
from unittest.mock import Mock, patch

@patch('psycopg2.connect')
def test_database_query(mock_connect):
    # Mock connection and cursor
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        (1, "Alice"),
        (2, "Bob")
    ]

    mock_conn = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    # Test
    db = Database()
    users = db.get_all_users()

    # Verify
    assert len(users) == 2
    mock_cursor.execute.assert_called_once()
```

### Mock ORM Queries

```python
from unittest.mock import Mock

def test_user_repository():
    # Mock SQLAlchemy session
    mock_session = Mock()
    mock_session.query.return_value.filter_by.return_value.first.return_value = \
        User(id=1, name="Alice")

    repo = UserRepository(mock_session)
    user = repo.find_by_email("alice@example.com")

    assert user.name == "Alice"
    mock_session.query.assert_called_once_with(User)
```

### Mock Query Results

```python
def test_user_search():
    mock_session = Mock()

    # Mock query chain
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [
        User(name="Alice"),
        User(name="Alicia")
    ]

    mock_session.query.return_value = mock_query

    repo = UserRepository(mock_session)
    results = repo.search("Ali")

    assert len(results) == 2
```

### In-Memory Database (Fake)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

@pytest.fixture
def in_memory_db():
    """Use real SQLite in-memory database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

def test_with_real_db(in_memory_db):
    user = User(name="Alice", email="alice@example.com")
    in_memory_db.add(user)
    in_memory_db.commit()

    retrieved = in_memory_db.query(User).filter_by(email="alice@example.com").first()
    assert retrieved.name == "Alice"
```

---

## Mocking File Systems

### Mock open()

```python
from unittest.mock import mock_open, patch

def read_config_file():
    with open("config.json") as f:
        return f.read()

def test_read_config():
    mock_data = '{"key": "value"}'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        content = read_config_file()

    assert content == mock_data
```

### Mock File Operations

```python
from unittest.mock import mock_open, patch

def save_user_data(user):
    with open(f"users/{user.id}.json", "w") as f:
        f.write(user.to_json())

def test_save_user():
    user = User(id=123, name="Alice")
    mock_file = mock_open()

    with patch("builtins.open", mock_file):
        save_user_data(user)

    # Verify file was opened correctly
    mock_file.assert_called_once_with("users/123.json", "w")

    # Verify write was called
    handle = mock_file()
    handle.write.assert_called_once()
```

### Mock os.path

```python
from unittest.mock import patch

def test_file_exists():
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = True

        result = check_file_exists("config.json")
        assert result is True

    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False

        result = check_file_exists("missing.json")
        assert result is False
```

### Using tmp_path (Better)

```python
def test_with_real_file(tmp_path):
    """Use pytest's tmp_path for real file operations."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")

    content = read_file(str(file_path))
    assert content == "test content"
```

---

## Mocking External Services

### Mock Email Service

```python
from unittest.mock import Mock, patch

def send_welcome_email(user):
    email_service = EmailService()
    email_service.send(
        to=user.email,
        subject="Welcome!",
        body=f"Hello {user.name}"
    )

@patch('myapp.EmailService')
def test_send_welcome_email(mock_email_class):
    mock_email = Mock()
    mock_email_class.return_value = mock_email

    user = User(name="Alice", email="alice@example.com")
    send_welcome_email(user)

    mock_email.send.assert_called_once_with(
        to="alice@example.com",
        subject="Welcome!",
        body="Hello Alice"
    )
```

### Mock Payment Gateway

```python
@patch('myapp.PaymentGateway')
def test_process_payment(mock_gateway_class):
    mock_gateway = Mock()
    mock_gateway.charge.return_value = {
        "success": True,
        "transaction_id": "txn_123"
    }
    mock_gateway_class.return_value = mock_gateway

    result = process_order_payment(order_id=1, amount=100)

    assert result["success"] is True
    mock_gateway.charge.assert_called_once_with(amount=100, currency="USD")
```

### Mock AWS Services (boto3)

```python
from unittest.mock import Mock, patch

@patch('boto3.client')
def test_s3_upload(mock_boto_client):
    mock_s3 = Mock()
    mock_boto_client.return_value = mock_s3

    upload_to_s3("file.txt", "bucket-name")

    mock_s3.upload_file.assert_called_once_with(
        "file.txt",
        "bucket-name",
        "file.txt"
    )
```

### Mock Redis

```python
from unittest.mock import Mock

def test_cache_service():
    mock_redis = Mock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True

    cache = CacheService(mock_redis)

    # Cache miss
    value = cache.get("key")
    assert value is None

    # Cache set
    cache.set("key", "value", ttl=300)
    mock_redis.set.assert_called_once_with("key", "value", ex=300)
```

---

## pytest-mock Plugin

### mocker Fixture

```python
# Install: pip install pytest-mock

def test_with_mocker(mocker):
    # No need to import patch
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_data()
    assert result["data"] == "test"
```

### Spy

```python
def test_spy(mocker):
    real_list = [1, 2, 3]
    spy = mocker.spy(real_list, 'append')

    real_list.append(4)

    # Real method was called
    assert real_list == [1, 2, 3, 4]

    # Verify it was called
    spy.assert_called_once_with(4)
```

### Mock Property

```python
def test_mock_property(mocker):
    user = User(name="Alice")

    mocker.patch.object(
        type(user),
        'is_admin',
        new_callable=mocker.PropertyMock,
        return_value=True
    )

    assert user.is_admin is True
```

### Stub

```python
def test_stub(mocker):
    stub = mocker.stub(name='feature_flag_stub')
    stub.return_value = True

    result = check_feature_flag()
    assert result is True
```

---

## Advanced Mocking Patterns

### Mocking Time

```python
from unittest.mock import patch
from datetime import datetime

def test_time_dependent_code(mocker):
    # Mock datetime.now()
    fake_now = datetime(2024, 1, 1, 12, 0, 0)
    mocker.patch('datetime.datetime').now.return_value = fake_now

    result = get_current_timestamp()
    assert result == fake_now
```

### Mocking Environment Variables

```python
def test_env_variables(mocker):
    mocker.patch.dict('os.environ', {'API_KEY': 'test_key'})

    config = load_config()
    assert config.api_key == 'test_key'
```

### Mocking Random

```python
from unittest.mock import patch

def test_random_generation():
    with patch('random.randint') as mock_random:
        mock_random.return_value = 42

        result = generate_random_number()
        assert result == 42
```

### Mocking Class Constructor

```python
@patch('myapp.Database')
def test_service_initialization(mock_database_class):
    mock_db_instance = Mock()
    mock_database_class.return_value = mock_db_instance

    service = UserService()  # Creates Database() internally

    # Verify Database was instantiated
    mock_database_class.assert_called_once()
```

### Partial Mocking

```python
from unittest.mock import Mock

def test_partial_mock():
    real_service = UserService()

    # Mock only specific method
    real_service.send_email = Mock()

    real_service.create_user("alice@example.com")

    # Real logic runs, but email is mocked
    real_service.send_email.assert_called_once()
```

---

## Assertions on Mocks

### Call Assertions

```python
from unittest.mock import Mock

mock = Mock()
mock.method(1, 2, key="value")

# Assert called
mock.method.assert_called()

# Assert called once
mock.method.assert_called_once()

# Assert called with specific args
mock.method.assert_called_with(1, 2, key="value")

# Assert called once with specific args
mock.method.assert_called_once_with(1, 2, key="value")

# Assert any call with args
mock.method.assert_any_call(1, 2, key="value")

# Assert not called
another_mock = Mock()
another_mock.method.assert_not_called()
```

### Call Count

```python
mock = Mock()
mock.method()
mock.method()
mock.method()

assert mock.method.call_count == 3
```

### Call History

```python
from unittest.mock import call

mock = Mock()
mock.method(1)
mock.method(2)
mock.method(3)

assert mock.method.call_args_list == [
    call(1),
    call(2),
    call(3)
]
```

### ANY Matcher

```python
from unittest.mock import ANY, Mock

mock = Mock()
mock.method(123, "data")

# Match anything for first argument
mock.method.assert_called_with(ANY, "data")
```

---

## Best Practices

### 1. Mock at the Right Level

```python
# ✓ Good - Mock external boundary
@patch('myapp.requests.get')
def test_api_client(mock_get):
    ...

# ❌ Bad - Mocking internal logic
@patch('myapp.process_data')  # Your own function!
def test_service(mock_process):
    ...
```

### 2. Use Spec to Catch Errors

```python
# ✓ Good - Will catch typos
mock_service = Mock(spec=UserService)
mock_service.get_user()  # OK
mock_service.gt_user()   # AttributeError!

# ❌ Bad - Won't catch typos
mock_service = Mock()
mock_service.gt_user()  # No error, returns Mock
```

### 3. Verify Behavior, Not Implementation

```python
# ✓ Good - Test behavior
def test_send_notification(mock_email):
    service.notify_user("alice@example.com")
    mock_email.send.assert_called_once()

# ❌ Bad - Testing implementation details
def test_internal_method(mock_formatter):
    service.notify_user("alice@example.com")
    mock_formatter._format_message.assert_called()  # Private method!
```

### 4. Keep Mocks Simple

```python
# ✓ Good - Simple mock
mock_db = Mock()
mock_db.get_user.return_value = User(name="Alice")

# ❌ Bad - Overly complex
mock_db = Mock()
mock_db.query.return_value.filter.return_value.join.return_value.all.return_value = [...]
```

### 5. Use Fixtures for Reusable Mocks

```python
@pytest.fixture
def mock_database(mocker):
    mock = mocker.Mock()
    mock.get_user.return_value = User(name="Alice")
    return mock

def test_service(mock_database):
    service = UserService(mock_database)
    ...
```

---

## Common Pitfalls

### Wrong Patch Target

```python
# myapp/service.py
from external_lib import function

def my_function():
    return function()

# ❌ Wrong - Patches original location
@patch('external_lib.function')
def test_wrong(mock_fn):
    my_function()  # Doesn't use mock!

# ✓ Right - Patch where it's used
@patch('myapp.service.function')
def test_right(mock_fn):
    my_function()  # Uses mock!
```

### Mocking Too Much

```python
# ❌ Bad - Mocking your own code
@patch('myapp.calculate_total')
@patch('myapp.apply_discount')
@patch('myapp.validate_items')
def test_checkout(mock_val, mock_disc, mock_calc):
    # Not testing anything real!
    checkout()

# ✓ Better - Only mock external dependencies
@patch('myapp.payment_gateway.charge')
def test_checkout(mock_charge):
    # Tests your logic, mocks external service
    checkout()
```

### Not Resetting Mocks

```python
# ❌ Problem - State carries over
mock = Mock()

def test_first():
    mock.method()
    assert mock.method.call_count == 1

def test_second():
    # Fails! call_count is 2
    assert mock.method.call_count == 0

# ✓ Solution - Use fresh mock or reset
def test_second():
    mock.reset_mock()
    assert mock.method.call_count == 0
```

---

## Summary

**Test Doubles**:
- **Dummy**: Placeholder
- **Stub**: Canned answers
- **Fake**: Working implementation
- **Mock**: Verify behavior
- **Spy**: Wrap real object

**Key Tools**:
- `unittest.mock`: Standard library
- `pytest-mock`: Pytest integration
- `responses`: HTTP mocking
- Fixtures: Reusable mocks

**Best Practices**:
- Mock external boundaries
- Use spec for safety
- Test behavior not implementation
- Keep mocks simple
- Prefer fakes for complex logic

**Common Mocking Targets**:
- HTTP APIs
- Databases
- File systems
- Email services
- Payment gateways
- Time and random
