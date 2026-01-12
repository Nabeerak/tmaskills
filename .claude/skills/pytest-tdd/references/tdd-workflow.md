# TDD Workflow: Red-Green-Refactor

## Table of Contents

- [The TDD Cycle](#the-tdd-cycle)
- [Phase 1: Red (Write Failing Test)](#phase-1-red-write-failing-test)
- [Phase 2: Green (Make It Pass)](#phase-2-green-make-it-pass)
- [Phase 3: Refactor (Improve Code)](#phase-3-refactor-improve-code)
- [Complete TDD Example](#complete-tdd-example)
- [TDD with FastAPI](#tdd-with-fastapi)
- [TDD Best Practices](#tdd-best-practices)
- [Common TDD Mistakes](#common-tdd-mistakes)

---

## The TDD Cycle

Test-Driven Development follows a repetitive three-phase cycle:

```
1. RED    → Write a failing test
2. GREEN  → Write minimal code to pass
3. REFACTOR → Improve code quality
```

**Repeat** for each new feature or requirement.

### Why TDD?

- **Design First**: Forces you to think about API design before implementation
- **Documentation**: Tests serve as executable documentation
- **Confidence**: Refactor with confidence knowing tests will catch regressions
- **Quality**: Naturally leads to better code structure and testability

---

## Phase 1: Red (Write Failing Test)

Write a test for functionality that **doesn't exist yet**.

### Example: Calculator Addition

```python
# test_calculator.py
import pytest
from calculator import Calculator

def test_add_two_positive_numbers():
    """Test adding two positive numbers."""
    # Arrange
    calc = Calculator()

    # Act
    result = calc.add(2, 3)

    # Assert
    assert result == 5
```

**Run**: `pytest test_calculator.py`

```
ImportError: cannot import name 'Calculator' from 'calculator'
```

**✓ Test fails** - This is expected! The code doesn't exist yet.

### Red Phase Checklist

- [ ] Test describes the expected behavior clearly
- [ ] Test follows AAA pattern (Arrange, Act, Assert)
- [ ] Test has descriptive name explaining what it tests
- [ ] Test fails for the right reason (code doesn't exist, not syntax error)

---

## Phase 2: Green (Make It Pass)

Write **minimal code** to make the test pass. Don't over-engineer.

### Minimal Implementation

```python
# calculator.py
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
```

**Run**: `pytest test_calculator.py`

```
test_calculator.py::test_add_two_positive_numbers PASSED [100%]
```

**✓ Test passes** - You've implemented the feature!

### Green Phase Checklist

- [ ] Write the simplest code that makes the test pass
- [ ] Don't add extra features "just in case"
- [ ] All tests pass (both new and existing)
- [ ] No shortcuts that break other tests

---

## Phase 3: Refactor (Improve Code)

Improve code quality **without changing behavior**. Tests should still pass.

### Refactoring Examples

**Add type flexibility**:
```python
# calculator.py
class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return a + b
```

**Add validation**:
```python
class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        return a + b
```

**Run**: `pytest test_calculator.py` → All tests still pass ✓

### Refactor Phase Checklist

- [ ] All tests still pass after refactoring
- [ ] Code is more readable or maintainable
- [ ] No new functionality added (only improvements)
- [ ] Type hints and docstrings added where helpful

---

## Complete TDD Example

Let's build a `User` class with TDD from scratch.

### Iteration 1: Create User

**RED - Write failing test**:
```python
# test_user.py
def test_create_user_with_name_and_email():
    """Test creating a user with name and email."""
    user = User(name="Alice", email="alice@example.com")

    assert user.name == "Alice"
    assert user.email == "alice@example.com"
```

**GREEN - Make it pass**:
```python
# user.py
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
```

**REFACTOR - Add type hints and validation**:
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
```

### Iteration 2: Email Validation

**RED - Write failing test**:
```python
def test_user_email_must_contain_at_symbol():
    """Test that email validation requires @ symbol."""
    with pytest.raises(ValueError, match="Invalid email"):
        User(name="Bob", email="invalid-email")
```

**GREEN - Make it pass**:
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("Invalid email")
```

**REFACTOR - Better validation**:
```python
import re
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str

    def __post_init__(self):
        if not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

### Iteration 3: User Age (Optional)

**RED - Write failing test**:
```python
def test_user_can_have_optional_age():
    """Test creating user with optional age."""
    user = User(name="Charlie", email="charlie@example.com", age=25)

    assert user.age == 25

def test_user_age_defaults_to_none():
    """Test that age defaults to None if not provided."""
    user = User(name="Diana", email="diana@example.com")

    assert user.age is None
```

**GREEN - Make it pass**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    age: Optional[int] = None

    def __post_init__(self):
        if not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

**REFACTOR - Add age validation**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    age: Optional[int] = None

    def __post_init__(self):
        if not self._is_valid_email(self.email):
            raise ValueError(f"Invalid email: {self.email}")

        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError(f"Invalid age: {self.age}")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

---

## TDD with FastAPI

Apply TDD to API endpoint development.

### Iteration 1: Create User Endpoint

**RED - Write failing test**:
```python
# test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_returns_201():
    """Test creating a user returns 201 status."""
    user_data = {
        "name": "Alice",
        "email": "alice@example.com"
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert "id" in response.json()
```

**GREEN - Make it pass**:
```python
# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# In-memory storage for demo
users_db = []
next_id = 1

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    global next_id
    user_dict = user.model_dump()
    user_dict["id"] = next_id
    next_id += 1
    users_db.append(user_dict)
    return user_dict
```

**REFACTOR - Extract to service layer**:
```python
# app/services/user_service.py
from app.models import User
from app.schemas import UserCreate

class UserService:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def create_user(self, user_data: UserCreate) -> User:
        user = User(
            id=self.next_id,
            name=user_data.name,
            email=user_data.email
        )
        self.users.append(user)
        self.next_id += 1
        return user

# app/main.py
from fastapi import FastAPI, Depends
from app.services.user_service import UserService

app = FastAPI()
user_service = UserService()

def get_user_service():
    return user_service

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(user)
```

---

## TDD Best Practices

### 1. Start with the Simplest Test

Begin with the easiest, most basic test case:

```python
# ✓ Good - Start simple
def test_add_returns_sum():
    assert add(2, 3) == 5

# ❌ Bad - Too complex to start
def test_add_handles_overflow_and_special_cases():
    # Multiple assertions, edge cases
    ...
```

### 2. One Test, One Behavior

Each test should verify one specific behavior:

```python
# ✓ Good - One behavior
def test_division_returns_quotient():
    assert divide(10, 2) == 5

def test_division_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# ❌ Bad - Multiple behaviors
def test_division():
    assert divide(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### 3. Write Descriptive Test Names

Test name should describe what is being tested:

```python
# ✓ Good - Clear what's being tested
def test_user_registration_sends_welcome_email():
    ...

def test_user_registration_fails_with_duplicate_email():
    ...

# ❌ Bad - Vague names
def test_user():
    ...

def test_edge_case():
    ...
```

### 4. Follow Red-Green-Refactor Strictly

Don't skip phases:

```python
# ✓ Good TDD Flow
# 1. Write test (RED)
def test_calculate_discount():
    result = calculate_discount(price=100, percent=10)
    assert result == 90

# 2. Minimal implementation (GREEN)
def calculate_discount(price, percent):
    return price - (price * percent / 100)

# 3. Refactor (REFACTOR)
def calculate_discount(price: float, percent: float) -> float:
    """Calculate discounted price."""
    if percent < 0 or percent > 100:
        raise ValueError("Percent must be 0-100")
    return price * (1 - percent / 100)

# ❌ Bad - Writing implementation first
def calculate_discount(price, percent):
    # Writing code before test
    ...
```

### 5. Refactor Tests Too

Tests are code - keep them clean:

```python
# ✓ Good - DRY with fixtures
@pytest.fixture
def sample_cart():
    return Cart(items=[
        {"name": "Apple", "price": 1.00},
        {"name": "Banana", "price": 0.50}
    ])

def test_cart_total(sample_cart):
    assert sample_cart.total() == 1.50

def test_cart_item_count(sample_cart):
    assert sample_cart.item_count() == 2

# ❌ Bad - Repeated setup
def test_cart_total():
    cart = Cart(items=[{"name": "Apple", "price": 1.00}, {"name": "Banana", "price": 0.50}])
    assert cart.total() == 1.50

def test_cart_item_count():
    cart = Cart(items=[{"name": "Apple", "price": 1.00}, {"name": "Banana", "price": 0.50}])
    assert cart.item_count() == 2
```

---

## Common TDD Mistakes

### 1. Writing Tests After Implementation

**Mistake**: Writing production code first, then tests.

**Why it's bad**: Defeats the purpose of TDD - you're testing implementation, not behavior.

**Fix**: Always write the test first (RED phase).

### 2. Testing Implementation Details

**Mistake**:
```python
# ❌ Bad - Testing internal method
def test_user_has_hash_password_method():
    user = User(name="Alice", email="alice@example.com")
    assert hasattr(user, '_hash_password')
```

**Fix**:
```python
# ✓ Good - Testing behavior
def test_user_password_is_not_stored_in_plain_text():
    user = User(name="Alice", email="alice@example.com", password="secret")
    assert user.password != "secret"
    assert len(user.password) > 20  # Hashed password is longer
```

### 3. Skipping Refactor Phase

**Mistake**: Moving to next feature immediately after GREEN.

**Why it's bad**: Code quality degrades over time, technical debt accumulates.

**Fix**: Always refactor after making test pass. Clean code, add documentation, improve structure.

### 4. Writing Too Much Code in GREEN Phase

**Mistake**:
```python
# ❌ Bad - Over-engineering in GREEN phase
def add(a, b):
    # Adding validation, logging, error handling before needed
    if not isinstance(a, (int, float)):
        raise TypeError("...")
    logger.info(f"Adding {a} + {b}")
    return a + b
```

**Fix**:
```python
# ✓ Good - Minimal code in GREEN phase
def add(a, b):
    return a + b

# Add validation in REFACTOR phase when you write test for it
```

### 5. Not Running Tests Frequently

**Mistake**: Writing multiple tests before running them.

**Why it's bad**: Hard to debug when multiple tests fail.

**Fix**: Run tests after each RED and GREEN phase. Tight feedback loop.

---

## Summary

**TDD Cycle**:
1. **RED**: Write a failing test
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve code quality

**Benefits**:
- Better design
- Living documentation
- Confidence in refactoring
- Higher code quality

**Key Principles**:
- Test first, code second
- One test, one behavior
- Minimal code to pass
- Refactor with passing tests
- Run tests frequently
