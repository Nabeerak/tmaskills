# Arrange-Act-Assert Pattern

## Table of Contents

- [Introduction](#introduction)
- [The AAA Pattern Explained](#the-aaa-pattern-explained)
- [Arrange Phase](#arrange-phase)
- [Act Phase](#act-phase)
- [Assert Phase](#assert-phase)
- [AAA in Different Test Scenarios](#aaa-in-different-test-scenarios)
- [AAA with Pytest Fixtures](#aaa-with-pytest-fixtures)
- [AAA for API Testing](#aaa-for-api-testing)
- [AAA for Database Testing](#aaa-for-database-testing)
- [AAA for Async Code](#aaa-for-async-code)
- [Common Patterns and Variations](#common-patterns-and-variations)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Best Practices](#best-practices)

---

## Introduction

The **Arrange-Act-Assert (AAA)** pattern is a structured approach to writing clean, readable, and maintainable tests. It divides each test into three distinct sections:

1. **Arrange**: Set up test data and preconditions
2. **Act**: Execute the code under test
3. **Assert**: Verify the results

### Why AAA?

- **Readability**: Tests follow a consistent, predictable structure
- **Maintainability**: Easy to understand and modify
- **Debugging**: Clear separation helps identify which phase failed
- **Communication**: Tests serve as documentation

---

## The AAA Pattern Explained

### Basic Structure

```python
def test_example():
    # Arrange - Set up test data and preconditions
    # Create objects, prepare inputs, configure mocks

    # Act - Execute the code under test
    # Call the function/method being tested

    # Assert - Verify the results
    # Check return values, state changes, side effects
```

### Simple Example

```python
def test_calculate_total_price():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=1.50))
    cart.add_item(Product(name="Banana", price=0.75))

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 2.25
```

### Visual Separation

Use blank lines to visually separate phases:

```python
def test_user_registration():
    # Arrange
    user_data = {
        "email": "alice@example.com",
        "password": "SecurePass123"
    }

    # Act
    user = User.register(user_data)

    # Assert
    assert user.email == "alice@example.com"
    assert user.password != "SecurePass123"  # Password should be hashed
    assert user.is_active is False  # New users start inactive
```

---

## Arrange Phase

The **Arrange** phase sets up everything needed for the test.

### What to Arrange

- Test data and inputs
- Object instances
- Mock objects and stubs
- Database state
- Configuration
- Preconditions

### Simple Arrange

```python
def test_add_numbers():
    # Arrange
    calculator = Calculator()
    a = 5
    b = 3

    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == 8
```

### Complex Arrange

```python
def test_order_total_with_discount():
    # Arrange
    customer = Customer(
        name="John Doe",
        email="john@example.com",
        loyalty_points=100
    )

    order = Order(customer=customer)
    order.add_item(Product(name="Laptop", price=1000))
    order.add_item(Product(name="Mouse", price=50))

    discount_code = DiscountCode(
        code="SAVE10",
        percentage=10,
        min_order=500
    )

    # Act
    total = order.apply_discount(discount_code)

    # Assert
    assert total == 945  # 1050 * 0.9 = 945
```

### Arrange with Builders

Use builder pattern for complex objects:

```python
class UserBuilder:
    def __init__(self):
        self.data = {
            "name": "Test User",
            "email": "test@example.com",
            "role": "user"
        }

    def with_name(self, name):
        self.data["name"] = name
        return self

    def with_email(self, email):
        self.data["email"] = email
        return self

    def as_admin(self):
        self.data["role"] = "admin"
        return self

    def build(self):
        return User(**self.data)

def test_admin_can_delete_users():
    # Arrange
    admin = UserBuilder().with_name("Admin").as_admin().build()
    user_to_delete = UserBuilder().build()

    # Act
    result = admin.delete_user(user_to_delete)

    # Assert
    assert result is True
```

### Arrange with Factory Functions

```python
def create_sample_user(name="John", email=None):
    """Factory function for creating test users."""
    if email is None:
        email = f"{name.lower()}@example.com"
    return User(name=name, email=email)

def test_send_notification():
    # Arrange
    user = create_sample_user(name="Alice")
    message = "Welcome to our platform!"

    # Act
    notification = Notification.send(user, message)

    # Assert
    assert notification.recipient == user.email
    assert notification.message == message
    assert notification.status == "sent"
```

---

## Act Phase

The **Act** phase executes the code under test. This should typically be a single action.

### Single Action

```python
def test_withdraw_money():
    # Arrange
    account = BankAccount(balance=100)

    # Act
    account.withdraw(30)

    # Assert
    assert account.balance == 70
```

### Store Result

```python
def test_search_users():
    # Arrange
    repository = UserRepository()
    repository.add(User(name="Alice", age=25))
    repository.add(User(name="Bob", age=30))

    # Act
    results = repository.search(age=25)

    # Assert
    assert len(results) == 1
    assert results[0].name == "Alice"
```

### Multiple Actions (When Necessary)

Sometimes you need multiple actions for setup vs. the actual test:

```python
def test_user_can_update_profile_after_login():
    # Arrange
    user = User(email="alice@example.com", password="pass123")
    user.save()

    # Act - Login is part of the action for this test
    session = user.login("alice@example.com", "pass123")
    updated_user = session.update_profile(name="Alice Smith")

    # Assert
    assert updated_user.name == "Alice Smith"
```

### Exception Handling

When testing exceptions, the act is the call that raises:

```python
def test_withdraw_insufficient_funds_raises_error():
    # Arrange
    account = BankAccount(balance=50)

    # Act & Assert (combined for exceptions)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(100)
```

Or separate more clearly:

```python
def test_invalid_email_raises_error():
    # Arrange
    invalid_email = "not-an-email"

    # Act
    def create_user():
        return User(email=invalid_email)

    # Assert
    with pytest.raises(ValidationError, match="Invalid email"):
        create_user()
```

---

## Assert Phase

The **Assert** phase verifies that the code behaved as expected.

### Single Assertion

```python
def test_calculate_area():
    # Arrange
    rectangle = Rectangle(width=5, height=3)

    # Act
    area = rectangle.calculate_area()

    # Assert
    assert area == 15
```

### Multiple Related Assertions

Multiple assertions for the same concept are acceptable:

```python
def test_create_user():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # Act
    user = User.create(user_data)

    # Assert
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None
    assert user.is_active is True
```

### Assert State Changes

```python
def test_add_item_to_cart():
    # Arrange
    cart = ShoppingCart()
    product = Product(name="Book", price=15.99)

    # Act
    cart.add(product)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0] == product
    assert cart.total == 15.99
```

### Assert Side Effects

```python
def test_send_email_notification(mock_email_service):
    # Arrange
    user = User(email="alice@example.com")
    order = Order(user=user, total=100)

    # Act
    order.send_confirmation()

    # Assert
    mock_email_service.send.assert_called_once()
    call_args = mock_email_service.send.call_args
    assert call_args[0][0] == "alice@example.com"
    assert "Order Confirmation" in call_args[0][1]
```

### Assert with Custom Messages

```python
def test_discount_calculation():
    # Arrange
    order = Order(subtotal=100)

    # Act
    discounted = order.apply_percentage_discount(20)

    # Assert
    assert discounted == 80, f"Expected 80 but got {discounted}"
```

### Assert Collections

```python
def test_filter_active_users():
    # Arrange
    users = [
        User(name="Alice", active=True),
        User(name="Bob", active=False),
        User(name="Charlie", active=True)
    ]

    # Act
    active_users = filter_active(users)

    # Assert
    assert len(active_users) == 2
    assert all(u.active for u in active_users)
    assert set(u.name for u in active_users) == {"Alice", "Charlie"}
```

---

## AAA in Different Test Scenarios

### Testing Pure Functions

```python
def test_calculate_tax():
    # Arrange
    amount = 100
    tax_rate = 0.08

    # Act
    tax = calculate_tax(amount, tax_rate)

    # Assert
    assert tax == 8.0
```

### Testing Class Methods

```python
def test_user_full_name():
    # Arrange
    user = User(first_name="John", last_name="Doe")

    # Act
    full_name = user.get_full_name()

    # Assert
    assert full_name == "John Doe"
```

### Testing Static Methods

```python
def test_validate_email():
    # Arrange
    valid_email = "user@example.com"

    # Act
    result = EmailValidator.is_valid(valid_email)

    # Assert
    assert result is True
```

### Testing Properties

```python
def test_circle_diameter():
    # Arrange
    circle = Circle(radius=5)

    # Act
    diameter = circle.diameter

    # Assert
    assert diameter == 10
```

### Testing Context Managers

```python
def test_file_context_manager():
    # Arrange
    file_path = "/tmp/test.txt"
    content = "Hello, World!"

    # Act
    with FileWriter(file_path) as writer:
        writer.write(content)

    # Assert
    with open(file_path) as f:
        assert f.read() == content
```

---

## AAA with Pytest Fixtures

Fixtures help reduce duplication in the Arrange phase.

### Basic Fixture Usage

```python
@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return User(name="Alice", email="alice@example.com")

def test_user_greeting(sample_user):
    # Arrange (handled by fixture)
    # sample_user is already created

    # Act
    greeting = sample_user.get_greeting()

    # Assert
    assert greeting == "Hello, Alice!"
```

### Fixture with Parameters

```python
@pytest.fixture
def shopping_cart():
    """Provide an empty shopping cart."""
    return ShoppingCart()

def test_add_item(shopping_cart):
    # Arrange
    product = Product(name="Book", price=15.99)

    # Act
    shopping_cart.add(product)

    # Assert
    assert len(shopping_cart.items) == 1
```

### Multiple Fixtures

```python
@pytest.fixture
def user():
    return User(name="Alice")

@pytest.fixture
def product():
    return Product(name="Laptop", price=1000)

def test_create_order(user, product):
    # Arrange
    order = Order(customer=user)

    # Act
    order.add_item(product)

    # Assert
    assert order.customer == user
    assert product in order.items
```

### Fixture Factories

```python
@pytest.fixture
def user_factory():
    """Factory fixture for creating users."""
    def create_user(name="Test User", email=None):
        if email is None:
            email = f"{name.lower().replace(' ', '.')}@example.com"
        return User(name=name, email=email)
    return create_user

def test_user_comparison(user_factory):
    # Arrange
    user1 = user_factory(name="Alice")
    user2 = user_factory(name="Bob")

    # Act
    are_equal = user1 == user2

    # Assert
    assert are_equal is False
```

---

## AAA for API Testing

### FastAPI Testing

```python
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user_endpoint(client):
    # Arrange
    user_data = {
        "name": "Alice",
        "email": "alice@example.com"
    }

    # Act
    response = client.post("/users", json=user_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert "id" in response.json()
```

### Testing with Authentication

```python
def test_protected_endpoint_requires_auth(client):
    # Arrange
    endpoint = "/protected/resource"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 401

def test_protected_endpoint_with_token(client, auth_token):
    # Arrange
    endpoint = "/protected/resource"
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Act
    response = client.get(endpoint, headers=headers)

    # Assert
    assert response.status_code == 200
```

### Testing Query Parameters

```python
def test_search_users_by_name(client):
    # Arrange
    search_query = "Alice"

    # Act
    response = client.get(f"/users?name={search_query}")

    # Assert
    assert response.status_code == 200
    results = response.json()
    assert all("Alice" in user["name"] for user in results)
```

### Testing File Uploads

```python
def test_upload_avatar(client):
    # Arrange
    user_id = 1
    files = {"file": ("avatar.jpg", b"fake-image-data", "image/jpeg")}

    # Act
    response = client.post(f"/users/{user_id}/avatar", files=files)

    # Assert
    assert response.status_code == 200
    assert response.json()["avatar_url"] is not None
```

---

## AAA for Database Testing

### Testing Database Operations

```python
def test_save_user_to_database(db_session):
    # Arrange
    user = User(name="Alice", email="alice@example.com")

    # Act
    db_session.add(user)
    db_session.commit()

    # Assert
    saved_user = db_session.query(User).filter_by(email="alice@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Alice"
```

### Testing Queries

```python
def test_query_users_by_age(db_session):
    # Arrange
    db_session.add(User(name="Alice", age=25))
    db_session.add(User(name="Bob", age=30))
    db_session.add(User(name="Charlie", age=25))
    db_session.commit()

    # Act
    users_25 = db_session.query(User).filter_by(age=25).all()

    # Assert
    assert len(users_25) == 2
    assert set(u.name for u in users_25) == {"Alice", "Charlie"}
```

### Testing Relationships

```python
def test_user_orders_relationship(db_session):
    # Arrange
    user = User(name="Alice")
    order1 = Order(total=100)
    order2 = Order(total=200)
    user.orders.extend([order1, order2])

    db_session.add(user)
    db_session.commit()

    # Act
    retrieved_user = db_session.query(User).filter_by(name="Alice").first()

    # Assert
    assert len(retrieved_user.orders) == 2
    assert sum(o.total for o in retrieved_user.orders) == 300
```

---

## AAA for Async Code

### Testing Async Functions

```python
@pytest.mark.asyncio
async def test_async_fetch_user():
    # Arrange
    user_id = 123
    repository = AsyncUserRepository()

    # Act
    user = await repository.get_user(user_id)

    # Assert
    assert user.id == user_id
    assert user.name is not None
```

### Testing with Async Context Managers

```python
@pytest.mark.asyncio
async def test_async_database_transaction():
    # Arrange
    async with AsyncDatabase() as db:
        user = User(name="Alice")

        # Act
        await db.save(user)
        result = await db.query(User).filter_by(name="Alice").first()

        # Assert
        assert result.name == "Alice"
```

### Testing Async API Calls

```python
@pytest.mark.asyncio
async def test_fetch_weather_data():
    # Arrange
    city = "London"
    api_client = WeatherAPIClient()

    # Act
    weather = await api_client.get_weather(city)

    # Assert
    assert weather.city == city
    assert weather.temperature is not None
```

---

## Common Patterns and Variations

### Given-When-Then (BDD Style)

Alternative naming for AAA, common in BDD:

```python
def test_user_login():
    # Given a registered user
    user = User(email="alice@example.com", password="hashed_password")
    user.save()

    # When the user logs in with correct credentials
    result = authenticate(email="alice@example.com", password="correct_password")

    # Then the authentication succeeds
    assert result.success is True
    assert result.user == user
```

### Setup-Exercise-Verify

Another variation of AAA:

```python
def test_shopping_cart():
    # Setup
    cart = ShoppingCart()
    product = Product(name="Book", price=15.99)

    # Exercise
    cart.add(product)

    # Verify
    assert len(cart.items) == 1
```

### Four-Phase Test (with Teardown)

```python
def test_temporary_file_creation():
    # Setup (Arrange)
    temp_dir = "/tmp/test"
    os.makedirs(temp_dir, exist_ok=True)

    # Exercise (Act)
    file_path = create_temp_file(temp_dir, "test.txt")

    # Verify (Assert)
    assert os.path.exists(file_path)

    # Teardown (pytest usually handles this with fixtures)
    shutil.rmtree(temp_dir)
```

With pytest fixture (better):

```python
@pytest.fixture
def temp_directory():
    temp_dir = "/tmp/test"
    os.makedirs(temp_dir, exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_temporary_file_creation(temp_directory):
    # Act
    file_path = create_temp_file(temp_directory, "test.txt")

    # Assert
    assert os.path.exists(file_path)
```

---

## Anti-Patterns to Avoid

### Multiple Acts

```python
# ❌ Bad - Multiple unrelated actions
def test_user_operations():
    user = User(name="Alice")

    user.update_email("alice@example.com")  # First act
    user.update_password("new_password")     # Second act
    user.deactivate()                        # Third act

    assert user.is_active is False

# ✓ Good - Separate tests
def test_user_email_update():
    # Arrange
    user = User(name="Alice")

    # Act
    user.update_email("alice@example.com")

    # Assert
    assert user.email == "alice@example.com"

def test_user_deactivation():
    # Arrange
    user = User(name="Alice")

    # Act
    user.deactivate()

    # Assert
    assert user.is_active is False
```

### Assertions in Arrange

```python
# ❌ Bad - Testing setup
def test_calculate_discount():
    # Arrange
    order = Order(total=100)
    assert order.total == 100  # Don't assert in arrange

    # Act
    discounted = order.apply_discount(10)

    # Assert
    assert discounted == 90

# ✓ Good - Trust your setup
def test_calculate_discount():
    # Arrange
    order = Order(total=100)

    # Act
    discounted = order.apply_discount(10)

    # Assert
    assert discounted == 90
```

### Complex Logic in Tests

```python
# ❌ Bad - Complex logic
def test_process_orders():
    # Arrange
    orders = [Order(total=100), Order(total=200)]
    expected_totals = []
    for order in orders:
        if order.total > 150:
            expected_totals.append(order.total * 0.9)
        else:
            expected_totals.append(order.total)

    # Act
    processed = process_orders(orders)

    # Assert
    assert [o.total for o in processed] == expected_totals

# ✓ Good - Explicit expectations
def test_process_orders_with_discount():
    # Arrange
    orders = [Order(total=100), Order(total=200)]

    # Act
    processed = process_orders(orders)

    # Assert
    assert processed[0].total == 100  # No discount
    assert processed[1].total == 180  # 10% discount
```

### Unclear Phase Boundaries

```python
# ❌ Bad - Mixed phases
def test_user_registration():
    user_data = {"email": "alice@example.com"}
    user = User.register(user_data)
    assert user.email == "alice@example.com"
    user.activate()
    assert user.is_active is True

# ✓ Good - Clear separation
def test_user_registration():
    # Arrange
    user_data = {"email": "alice@example.com"}

    # Act
    user = User.register(user_data)

    # Assert
    assert user.email == "alice@example.com"
    assert user.is_active is False  # New users start inactive
```

---

## Best Practices

### 1. Use Blank Lines to Separate Phases

```python
def test_example():
    # Arrange
    data = prepare_data()

    # Act
    result = process(data)

    # Assert
    assert result == expected
```

### 2. Keep Act Phase Simple

The act should typically be a single line:

```python
# ✓ Good
def test_add():
    # Arrange
    calc = Calculator()

    # Act
    result = calc.add(2, 3)

    # Assert
    assert result == 5
```

### 3. Use Descriptive Variable Names

```python
# ✓ Good
def test_discount_calculation():
    # Arrange
    original_price = 100
    discount_percentage = 20
    expected_price = 80

    # Act
    final_price = calculate_discount(original_price, discount_percentage)

    # Assert
    assert final_price == expected_price
```

### 4. One Logical Assertion Per Test

Test one behavior, but multiple assertions are OK if they verify the same behavior:

```python
# ✓ Good - Multiple assertions for same behavior
def test_create_user():
    # Arrange
    user_data = {"name": "Alice", "email": "alice@example.com"}

    # Act
    user = User.create(user_data)

    # Assert - All verify user creation
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id is not None
```

### 5. Extract Common Arrange Logic to Fixtures

```python
@pytest.fixture
def authenticated_user():
    user = User(email="alice@example.com")
    user.authenticate()
    return user

def test_user_can_create_post(authenticated_user):
    # Arrange
    post_content = "Hello, World!"

    # Act
    post = authenticated_user.create_post(post_content)

    # Assert
    assert post.author == authenticated_user
    assert post.content == post_content
```

### 6. Make Tests Self-Contained

Each test should set up its own data:

```python
# ✓ Good - Self-contained
def test_user_deactivation():
    # Arrange
    user = User(name="Alice", active=True)

    # Act
    user.deactivate()

    # Assert
    assert user.active is False
```

### 7. Use Comments to Label Phases

Especially helpful for complex tests:

```python
def test_complex_workflow():
    # Arrange - Set up users and permissions
    admin = User(name="Admin", role="admin")
    user = User(name="Alice", role="user")

    # Act - Admin modifies user permissions
    admin.grant_permission(user, "write")

    # Assert - User has new permission
    assert user.has_permission("write")
```

---

## Summary

**The AAA Pattern**:
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code under test
- **Assert**: Verify the results

**Key Benefits**:
- Improved readability
- Easier debugging
- Better maintainability
- Self-documenting tests

**Best Practices**:
- Use blank lines to separate phases
- Keep Act phase to a single action
- Extract common setup to fixtures
- Use descriptive variable names
- One logical assertion per test
- Make tests self-contained

**Remember**: AAA is a guideline, not a strict rule. The goal is readable, maintainable tests.
