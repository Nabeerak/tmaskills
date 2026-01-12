# Pytest Fixtures

## Table of Contents

- [Introduction](#introduction)
- [Basic Fixtures](#basic-fixtures)
- [Fixture Scopes](#fixture-scopes)
- [Fixture Dependency](#fixture-dependency)
- [Yield Fixtures](#yield-fixtures)
- [Fixture Factories](#fixture-factories)
- [Parametrized Fixtures](#parametrized-fixtures)
- [Auto-use Fixtures](#auto-use-fixtures)
- [Fixture Finalization](#fixture-finalization)
- [Built-in Fixtures](#built-in-fixtures)
- [Advanced Fixture Patterns](#advanced-fixture-patterns)
- [conftest.py Organization](#conftestpy-organization)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)

---

## Introduction

**Fixtures** are pytest's way of providing reusable setup and teardown code for tests. They replace traditional setUp/tearDown methods with a more flexible, composable approach.

### Why Use Fixtures?

- **Reusability**: Write setup code once, use in many tests
- **Modularity**: Compose complex setups from simple fixtures
- **Readability**: Explicit dependencies via function parameters
- **Flexibility**: Different scopes for different needs
- **Automatic Cleanup**: Built-in teardown with yield

### Basic Concept

```python
@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return {"name": "Alice", "age": 30}

def test_process_data(sample_data):
    # sample_data is automatically provided
    result = process(sample_data)
    assert result is not None
```

---

## Basic Fixtures

### Simple Fixture

```python
import pytest

@pytest.fixture
def user():
    """Provide a sample user."""
    return User(name="Alice", email="alice@example.com")

def test_user_greeting(user):
    greeting = user.get_greeting()
    assert greeting == "Hello, Alice!"
```

### Fixture with Setup Logic

```python
@pytest.fixture
def database_connection():
    """Provide a database connection."""
    conn = Database.connect("test.db")
    return conn

def test_query(database_connection):
    result = database_connection.execute("SELECT * FROM users")
    assert result is not None
```

### Multiple Fixtures in One Test

```python
@pytest.fixture
def user():
    return User(name="Alice")

@pytest.fixture
def product():
    return Product(name="Laptop", price=1000)

def test_create_order(user, product):
    order = Order(customer=user)
    order.add_item(product)

    assert order.customer == user
    assert product in order.items
```

### Fixture Returning Multiple Values

```python
@pytest.fixture
def user_credentials():
    """Provide test user credentials."""
    return {
        "username": "testuser",
        "password": "Test123!",
        "email": "test@example.com"
    }

def test_login(user_credentials):
    result = authenticate(
        user_credentials["username"],
        user_credentials["password"]
    )
    assert result.success is True
```

---

## Fixture Scopes

Fixtures can have different scopes that determine how often they're created and destroyed.

### Available Scopes

- **function** (default): Created for each test function
- **class**: Created once per test class
- **module**: Created once per module
- **package**: Created once per package
- **session**: Created once per test session

### Function Scope (Default)

```python
@pytest.fixture  # scope="function" is default
def fresh_database():
    """Create a fresh database for each test."""
    db = Database(":memory:")
    db.initialize()
    return db

def test_insert_user(fresh_database):
    # Gets a new database
    fresh_database.insert(User(name="Alice"))
    assert fresh_database.count() == 1

def test_insert_product(fresh_database):
    # Gets another new database
    fresh_database.insert(Product(name="Laptop"))
    assert fresh_database.count() == 1
```

### Class Scope

```python
@pytest.fixture(scope="class")
def database():
    """Create database once for all tests in a class."""
    db = Database("test.db")
    db.initialize()
    yield db
    db.close()

class TestUserOperations:
    def test_create_user(self, database):
        database.insert(User(name="Alice"))
        assert database.count() == 1

    def test_read_user(self, database):
        # Same database as previous test
        # May have data from previous tests!
        user = database.query(User).first()
        assert user is not None
```

### Module Scope

```python
@pytest.fixture(scope="module")
def app():
    """Create app once per module."""
    application = create_app(config="testing")
    return application

@pytest.fixture(scope="module")
def client(app):
    """Create test client once per module."""
    return app.test_client()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_about_page(client):
    # Same client instance
    response = client.get("/about")
    assert response.status_code == 200
```

### Session Scope

```python
@pytest.fixture(scope="session")
def database_engine():
    """Create database engine once for entire test session."""
    engine = create_engine("postgresql://localhost/test")
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup after all tests
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(database_engine):
    """Create a new session for each test."""
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Scope Selection Guidelines

```python
# Function scope - Default, safest
@pytest.fixture  # New instance for each test
def user():
    return User(name="Alice")

# Class scope - Share across class
@pytest.fixture(scope="class")  # One instance per test class
def shared_data():
    return load_test_data()

# Module scope - Expensive setup
@pytest.fixture(scope="module")  # One instance per file
def api_client():
    return ExpensiveAPIClient()

# Session scope - Very expensive setup
@pytest.fixture(scope="session")  # One instance for all tests
def docker_container():
    container = start_docker_container()
    yield container
    stop_docker_container(container)
```

---

## Fixture Dependency

Fixtures can depend on other fixtures, creating a dependency chain.

### Simple Dependency

```python
@pytest.fixture
def database():
    """Provide database connection."""
    return Database.connect("test.db")

@pytest.fixture
def user_repository(database):
    """Provide user repository using database."""
    return UserRepository(database)

def test_find_user(user_repository):
    # database is automatically created and passed to user_repository
    user = user_repository.find_by_email("alice@example.com")
    assert user is not None
```

### Nested Dependencies

```python
@pytest.fixture
def engine():
    """Database engine."""
    return create_engine("sqlite:///:memory:")

@pytest.fixture
def session(engine):
    """Database session."""
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    yield session
    session.close()

@pytest.fixture
def user(session):
    """Sample user in database."""
    user = User(name="Alice", email="alice@example.com")
    session.add(user)
    session.commit()
    return user

def test_user_exists(user, session):
    # Chain: engine → session → user
    found = session.query(User).filter_by(email="alice@example.com").first()
    assert found.name == "Alice"
```

### Multiple Dependencies

```python
@pytest.fixture
def smtp_server():
    return SMTPServer("localhost", 1025)

@pytest.fixture
def email_template():
    return EmailTemplate("welcome.html")

@pytest.fixture
def email_service(smtp_server, email_template):
    """Email service with dependencies."""
    return EmailService(
        server=smtp_server,
        template=email_template
    )

def test_send_welcome_email(email_service):
    result = email_service.send_welcome("alice@example.com")
    assert result.success is True
```

### Scope Compatibility

Higher scope fixtures can depend on same or higher scope fixtures:

```python
# ✓ Valid - module scope can depend on session scope
@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="module")
def app(config):  # OK: module depends on session
    return create_app(config)

# ❌ Invalid - session scope cannot depend on module scope
@pytest.fixture(scope="module")
def database():
    return Database()

@pytest.fixture(scope="session")
def app(database):  # ERROR: session cannot depend on module
    return create_app(database)
```

---

## Yield Fixtures

Yield fixtures provide both setup (before yield) and teardown (after yield) code.

### Basic Yield Fixture

```python
@pytest.fixture
def database():
    """Create and cleanup database."""
    # Setup
    db = Database(":memory:")
    db.initialize()

    yield db  # Provide to test

    # Teardown
    db.close()

def test_insert(database):
    database.insert(User(name="Alice"))
    assert database.count() == 1
    # database.close() is automatically called after test
```

### File Handling

```python
@pytest.fixture
def temp_file():
    """Create temporary file and clean up."""
    # Setup
    file_path = "/tmp/test_file.txt"
    with open(file_path, 'w') as f:
        f.write("test content")

    yield file_path

    # Teardown
    if os.path.exists(file_path):
        os.remove(file_path)

def test_read_file(temp_file):
    with open(temp_file) as f:
        content = f.read()
    assert content == "test content"
```

### Database Transaction

```python
@pytest.fixture
def db_session():
    """Provide database session with automatic rollback."""
    # Setup
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Teardown - rollback ensures test isolation
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(db_session):
    user = User(name="Alice")
    db_session.add(user)
    db_session.commit()

    assert db_session.query(User).count() == 1
    # Automatically rolled back after test
```

### Context Manager Fixture

```python
@pytest.fixture
def mock_server():
    """Start and stop mock HTTP server."""
    # Setup
    server = HTTPServer(("localhost", 8080), MockHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield f"http://localhost:8080"

    # Teardown
    server.shutdown()
    server_thread.join()

def test_api_call(mock_server):
    response = requests.get(f"{mock_server}/api/data")
    assert response.status_code == 200
```

### Exception Handling in Teardown

```python
@pytest.fixture
def resource():
    """Resource with error handling in teardown."""
    # Setup
    r = acquire_resource()

    yield r

    # Teardown - always runs, even if test fails
    try:
        r.close()
    except Exception as e:
        logging.error(f"Error closing resource: {e}")
```

---

## Fixture Factories

Fixtures that return factory functions for creating multiple instances.

### Basic Factory

```python
@pytest.fixture
def user_factory():
    """Factory for creating users."""
    def create_user(name="Test User", email=None):
        if email is None:
            email = f"{name.lower().replace(' ', '.')}@example.com"
        return User(name=name, email=email)

    return create_user

def test_multiple_users(user_factory):
    alice = user_factory(name="Alice")
    bob = user_factory(name="Bob")

    assert alice.email == "alice@example.com"
    assert bob.email == "bob@example.com"
```

### Factory with Database

```python
@pytest.fixture
def user_factory(db_session):
    """Factory for creating and persisting users."""
    created_users = []

    def create_user(**kwargs):
        user = User(
            name=kwargs.get("name", "Test User"),
            email=kwargs.get("email", "test@example.com")
        )
        db_session.add(user)
        db_session.commit()
        created_users.append(user)
        return user

    yield create_user

    # Cleanup
    for user in created_users:
        db_session.delete(user)
    db_session.commit()

def test_user_relationships(user_factory):
    alice = user_factory(name="Alice", email="alice@example.com")
    bob = user_factory(name="Bob", email="bob@example.com")

    alice.add_friend(bob)

    assert bob in alice.friends
```

### Parameterized Factory

```python
@pytest.fixture
def product_factory():
    """Factory for creating products with defaults."""
    defaults = {
        "category": "Electronics",
        "in_stock": True,
        "price": 100.0
    }

    def create_product(**overrides):
        data = {**defaults, **overrides}
        return Product(**data)

    return create_product

def test_product_pricing(product_factory):
    regular = product_factory(name="Laptop", price=1000)
    discounted = product_factory(name="Mouse", price=50)

    assert regular.price == 1000
    assert discounted.price == 50
```

### Builder Pattern Factory

```python
@pytest.fixture
def order_builder(db_session):
    """Builder for creating complex orders."""
    class OrderBuilder:
        def __init__(self):
            self.customer = None
            self.items = []
            self.discount = None

        def with_customer(self, customer):
            self.customer = customer
            return self

        def with_item(self, product, quantity=1):
            self.items.append({"product": product, "quantity": quantity})
            return self

        def with_discount(self, code):
            self.discount = code
            return self

        def build(self):
            order = Order(customer=self.customer)
            for item in self.items:
                order.add_item(item["product"], item["quantity"])
            if self.discount:
                order.apply_discount(self.discount)
            db_session.add(order)
            db_session.commit()
            return order

    return OrderBuilder()

def test_complex_order(order_builder, user_factory, product_factory):
    customer = user_factory(name="Alice")
    laptop = product_factory(name="Laptop", price=1000)
    mouse = product_factory(name="Mouse", price=50)

    order = (order_builder
             .with_customer(customer)
             .with_item(laptop, quantity=1)
             .with_item(mouse, quantity=2)
             .with_discount("SAVE10")
             .build())

    assert order.total == 945  # (1000 + 50*2) * 0.9
```

---

## Parametrized Fixtures

Create multiple versions of a fixture with different parameters.

### Basic Parametrization

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """Parametrized database fixture."""
    db_type = request.param

    if db_type == "sqlite":
        db = SQLiteDatabase(":memory:")
    elif db_type == "postgresql":
        db = PostgreSQLDatabase("test")
    else:
        db = MySQLDatabase("test")

    db.initialize()
    yield db
    db.close()

def test_insert_user(database):
    # This test runs 3 times, once for each database type
    database.insert(User(name="Alice"))
    assert database.count() == 1
```

### Multiple Parameter Values

```python
@pytest.fixture(params=[
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
])
def user_data(request):
    """Different user data for each test run."""
    return request.param

def test_user_creation(user_data):
    # Runs 3 times with different data
    user = User(**user_data)
    assert user.name == user_data["name"]
    assert user.age == user_data["age"]
```

### Parametrized with IDs

```python
@pytest.fixture(
    params=[
        (2, 3, 5),
        (10, 5, 15),
        (-1, 1, 0)
    ],
    ids=["simple", "double-digit", "negative"]
)
def addition_data(request):
    """Test data with custom IDs."""
    return request.param

def test_addition(addition_data):
    a, b, expected = addition_data
    assert a + b == expected

# Output:
# test_addition[simple] PASSED
# test_addition[double-digit] PASSED
# test_addition[negative] PASSED
```

### Indirect Parametrization

```python
@pytest.fixture
def user(request):
    """Create user from parameter."""
    user_type = request.param
    if user_type == "admin":
        return User(name="Admin", role="admin")
    elif user_type == "regular":
        return User(name="User", role="user")
    else:
        return User(name="Guest", role="guest")

@pytest.mark.parametrize("user", ["admin", "regular"], indirect=True)
def test_user_permissions(user):
    # user fixture is called with each parameter
    assert user.role in ["admin", "regular"]
```

### Combining Fixture Parametrization

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database(request):
    return create_database(request.param)

@pytest.fixture(params=[True, False])
def cache_enabled(request):
    return request.param

def test_repository(database, cache_enabled):
    # Runs 4 times: 2 databases × 2 cache settings
    repo = Repository(database, cache=cache_enabled)
    assert repo is not None
```

---

## Auto-use Fixtures

Fixtures that run automatically without being explicitly requested.

### Basic Auto-use

```python
@pytest.fixture(autouse=True)
def reset_database():
    """Automatically reset database before each test."""
    database.clear()
    database.seed_default_data()

def test_user_count():
    # reset_database runs automatically
    assert database.count() == 0
```

### Auto-use with Scope

```python
@pytest.fixture(scope="module", autouse=True)
def setup_module_environment():
    """Setup environment once per module."""
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"

    yield

    # Cleanup
    del os.environ["TESTING"]
    del os.environ["LOG_LEVEL"]
```

### Auto-use in conftest.py

```python
# tests/conftest.py
@pytest.fixture(autouse=True)
def isolate_tests(db_session):
    """Automatically wrap each test in transaction."""
    # Each test gets automatic rollback
    yield
    db_session.rollback()
```

### Conditional Auto-use

```python
@pytest.fixture(autouse=True)
def log_test_name(request):
    """Log test name before each test."""
    test_name = request.node.name
    logging.info(f"Starting test: {test_name}")

    yield

    logging.info(f"Finished test: {test_name}")
```

---

## Fixture Finalization

Alternative ways to ensure cleanup happens.

### Using addfinalizer

```python
@pytest.fixture
def database(request):
    """Database with cleanup via addfinalizer."""
    db = Database(":memory:")
    db.initialize()

    def cleanup():
        db.close()
        logging.info("Database closed")

    request.addfinalizer(cleanup)

    return db
```

### Multiple Finalizers

```python
@pytest.fixture
def complex_resource(request):
    """Resource with multiple cleanup steps."""
    resource = Resource()

    # Finalizers are called in LIFO order
    request.addfinalizer(lambda: resource.disconnect())
    request.addfinalizer(lambda: resource.save_state())
    request.addfinalizer(lambda: resource.cleanup_temp_files())

    return resource
```

### Yield vs Addfinalizer

```python
# Yield - Preferred, cleaner
@pytest.fixture
def resource_yield():
    r = Resource()
    yield r
    r.cleanup()

# Addfinalizer - More control
@pytest.fixture
def resource_finalizer(request):
    r = Resource()

    def cleanup():
        if r.needs_cleanup():
            r.cleanup()

    request.addfinalizer(cleanup)
    return r
```

---

## Built-in Fixtures

Pytest provides several useful built-in fixtures.

### tmp_path

```python
def test_create_file(tmp_path):
    """tmp_path provides a unique temporary directory."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello world")

    assert file_path.read_text() == "hello world"
    # Automatically cleaned up after test
```

### tmp_path_factory

```python
@pytest.fixture(scope="session")
def shared_data_dir(tmp_path_factory):
    """Create shared temp directory for session."""
    return tmp_path_factory.mktemp("shared_data")

def test_use_shared_dir(shared_data_dir):
    data_file = shared_data_dir / "data.json"
    data_file.write_text('{"key": "value"}')
    assert data_file.exists()
```

### monkeypatch

```python
def test_environment_variable(monkeypatch):
    """monkeypatch for mocking."""
    monkeypatch.setenv("API_KEY", "test_key")
    assert os.getenv("API_KEY") == "test_key"
    # Automatically restored after test

def test_mock_function(monkeypatch):
    def mock_get_user():
        return User(name="Mocked User")

    monkeypatch.setattr("myapp.get_user", mock_get_user)

    user = get_user()
    assert user.name == "Mocked User"
```

### capsys and capfd

```python
def test_print_output(capsys):
    """Capture stdout/stderr."""
    print("Hello, World!")
    captured = capsys.readouterr()

    assert captured.out == "Hello, World!\n"
    assert captured.err == ""
```

### request

```python
@pytest.fixture
def resource(request):
    """Access test context via request."""
    test_name = request.node.name
    markers = list(request.node.iter_markers())

    return Resource(test_name=test_name)
```

---

## Advanced Fixture Patterns

### Caching Expensive Operations

```python
@pytest.fixture(scope="session")
def expensive_data():
    """Cache expensive computation."""
    cache_file = "test_cache.pkl"

    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)

    # Expensive operation
    data = load_large_dataset()

    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)

    return data
```

### Dynamic Fixture Configuration

```python
@pytest.fixture
def api_client(request):
    """Configurable API client."""
    marker = request.node.get_closest_marker("api_version")
    version = marker.args[0] if marker else "v1"

    return APIClient(version=version)

@pytest.mark.api_version("v2")
def test_new_endpoint(api_client):
    # Gets v2 client
    response = api_client.get("/users")
    assert response.status_code == 200
```

### Fixture Inheritance

```python
# tests/conftest.py
@pytest.fixture
def base_user():
    return User(name="Base User")

# tests/unit/conftest.py
@pytest.fixture
def base_user():
    # Override parent fixture
    return User(name="Unit Test User", role="tester")
```

---

## conftest.py Organization

### Root conftest.py

```python
# tests/conftest.py
"""Root fixtures available to all tests."""
import pytest
from myapp import create_app

@pytest.fixture(scope="session")
def app():
    """Application instance."""
    return create_app(testing=True)

@pytest.fixture(scope="session")
def db_engine():
    """Database engine for all tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
```

### Directory-specific conftest.py

```python
# tests/unit/conftest.py
"""Fixtures for unit tests."""
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_database():
    """Mock database for unit tests."""
    return Mock()

# tests/integration/conftest.py
"""Fixtures for integration tests."""
import pytest

@pytest.fixture
def db_session(db_engine):
    """Real database session for integration tests."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

---

## Best Practices

### 1. Use Descriptive Names

```python
# ✓ Good
@pytest.fixture
def authenticated_admin_user():
    ...

# ❌ Bad
@pytest.fixture
def user():
    ...
```

### 2. Minimize Fixture Scope

```python
# ✓ Good - Function scope by default
@pytest.fixture
def user():
    return User()

# ⚠ Use wider scopes only when necessary
@pytest.fixture(scope="session")
def expensive_resource():
    return load_huge_dataset()
```

### 3. Document Fixtures

```python
@pytest.fixture
def db_session(db_engine):
    """
    Provide database session with automatic rollback.

    Creates a new session for each test and automatically
    rolls back changes after the test completes.

    Yields:
        Session: SQLAlchemy session instance
    """
    ...
```

### 4. Prefer Yield for Cleanup

```python
# ✓ Good - Clear setup/teardown
@pytest.fixture
def resource():
    r = create_resource()
    yield r
    r.cleanup()

# ❌ Less clear
@pytest.fixture
def resource(request):
    r = create_resource()
    request.addfinalizer(r.cleanup)
    return r
```

### 5. Keep Fixtures Simple

```python
# ✓ Good - Simple, focused
@pytest.fixture
def user():
    return User(name="Alice")

# ❌ Bad - Too complex
@pytest.fixture
def user():
    if os.getenv("USE_ADMIN"):
        user = User(name="Admin", role="admin")
    else:
        user = User(name="User")
    user.validate()
    user.save()
    return user
```

---

## Common Pitfalls

### Mutable Fixture Data

```python
# ❌ Problem - Shared mutable state
@pytest.fixture(scope="module")
def user_list():
    return []  # Same list for all tests!

def test_add_user(user_list):
    user_list.append("Alice")
    assert len(user_list) == 1

def test_another(user_list):
    # user_list still contains "Alice"!
    assert len(user_list) == 0  # FAILS

# ✓ Solution - Function scope or copy
@pytest.fixture
def user_list():
    return []  # New list each time
```

### Fixture Scope Issues

```python
# ❌ Problem - Function fixture depends on class fixture
@pytest.fixture(scope="class")
def database():
    return Database()

@pytest.fixture  # scope="function"
def user(database):
    # This works, but may have unexpected behavior
    return User(db=database)
```

### Over-using Auto-use

```python
# ❌ Problem - Unnecessary auto-use
@pytest.fixture(autouse=True)
def setup_something():
    # Runs for ALL tests even if not needed
    expensive_setup()

# ✓ Better - Explicit dependency
@pytest.fixture
def setup_something():
    expensive_setup()

def test_that_needs_it(setup_something):
    ...
```

---

## Summary

**Fixture Basics**:
- Reusable setup code
- Explicit dependencies
- Automatic cleanup

**Key Concepts**:
- **Scopes**: function, class, module, session
- **Yield**: Setup and teardown
- **Factories**: Create multiple instances
- **Parametrization**: Test multiple scenarios
- **Auto-use**: Automatic execution

**Best Practices**:
- Use descriptive names
- Minimize scope
- Document purpose
- Prefer yield for cleanup
- Keep fixtures simple

**Organization**:
- Use conftest.py hierarchically
- Share common fixtures
- Override when needed
