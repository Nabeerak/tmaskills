"""
Example test file demonstrating pytest best practices and AAA pattern.

This file shows various testing patterns including:
- AAA (Arrange-Act-Assert) structure
- Fixtures usage
- Parametrization
- Exception testing
- Mocking
"""

import pytest
from myapp.models import User
from myapp.services import UserService


# ==================== Basic Tests with AAA Pattern ====================

def test_user_creation_with_valid_data():
    """Test creating a user with valid data."""
    # Arrange
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(name=name, email=email)

    # Assert
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id is None  # Not saved yet


def test_user_full_name_property():
    """Test that full_name property returns formatted name."""
    # Arrange
    user = User(first_name="John", last_name="Doe", email="john@example.com")

    # Act
    full_name = user.full_name

    # Assert
    assert full_name == "John Doe"


# ==================== Tests with Fixtures ====================

def test_create_user_saves_to_database(db_session, sample_user_data):
    """Test that create_user saves user to database."""
    # Arrange
    service = UserService(db_session)

    # Act
    user = service.create_user(sample_user_data)

    # Assert
    assert user.id is not None
    assert user.name == sample_user_data["name"]
    assert user.email == sample_user_data["email"]


def test_get_user_by_id_returns_correct_user(db_session, sample_user_data):
    """Test retrieving user by ID."""
    # Arrange
    service = UserService(db_session)
    created_user = service.create_user(sample_user_data)

    # Act
    retrieved_user = service.get_user(created_user.id)

    # Assert
    assert retrieved_user.id == created_user.id
    assert retrieved_user.email == created_user.email


# ==================== Parametrized Tests ====================

@pytest.mark.parametrize("name,email,expected_valid", [
    ("Alice", "alice@example.com", True),
    ("Bob", "bob@example.com", True),
    ("", "test@example.com", False),  # Empty name
    ("Charlie", "invalid-email", False),  # Invalid email
    ("Dave", "", False),  # Empty email
])
def test_user_validation(name, email, expected_valid):
    """Test user validation with various inputs."""
    # Arrange & Act
    user = User(name=name, email=email)

    # Assert
    assert user.is_valid() == expected_valid


@pytest.mark.parametrize("age", [0, 1, 17, 18, 65, 100, 150])
def test_user_age_categories(age):
    """Test age category classification."""
    # Arrange
    user = User(name="Test", email="test@example.com", age=age)

    # Act
    category = user.get_age_category()

    # Assert
    if age < 18:
        assert category == "minor"
    elif age < 65:
        assert category == "adult"
    else:
        assert category == "senior"


# ==================== Exception Testing ====================

def test_create_user_with_duplicate_email_raises_error(db_session, sample_user_data):
    """Test that creating user with duplicate email raises ValueError."""
    # Arrange
    service = UserService(db_session)
    service.create_user(sample_user_data)  # Create first user

    # Act & Assert
    with pytest.raises(ValueError, match="Email already exists"):
        service.create_user(sample_user_data)  # Try to create duplicate


def test_get_nonexistent_user_raises_not_found(db_session):
    """Test that getting nonexistent user raises NotFoundError."""
    # Arrange
    service = UserService(db_session)
    nonexistent_id = 99999

    # Act & Assert
    with pytest.raises(service.NotFoundError):
        service.get_user(nonexistent_id)


# ==================== Mocking Tests ====================

def test_send_welcome_email_on_user_creation(db_session, sample_user_data, mock_email_service):
    """Test that welcome email is sent when user is created."""
    # Arrange
    service = UserService(db_session)

    # Act
    user = service.create_user(sample_user_data)

    # Assert
    mock_email_service.assert_called_once_with(
        to=user.email,
        subject="Welcome!",
        body=pytest.approx_match("Welcome to our platform")
    )


def test_fetch_user_from_external_api(mock_external_api):
    """Test fetching user data from external API."""
    # Arrange
    mock_external_api.return_value = {
        "name": "External User",
        "email": "external@example.com"
    }
    service = UserService()

    # Act
    user_data = service.fetch_from_external_api(user_id=123)

    # Assert
    assert user_data["name"] == "External User"
    mock_external_api.assert_called_once_with(
        endpoint="/users/123",
        method="GET"
    )


# ==================== Class-Based Tests ====================

class TestUserService:
    """Group related user service tests together."""

    def test_create_user(self, db_session, sample_user_data):
        """Test user creation."""
        service = UserService(db_session)
        user = service.create_user(sample_user_data)
        assert user.id is not None

    def test_update_user(self, db_session, sample_user_data):
        """Test user update."""
        # Arrange
        service = UserService(db_session)
        user = service.create_user(sample_user_data)
        update_data = {"name": "Updated Name"}

        # Act
        updated_user = service.update_user(user.id, update_data)

        # Assert
        assert updated_user.name == "Updated Name"
        assert updated_user.email == sample_user_data["email"]  # Unchanged

    def test_delete_user(self, db_session, sample_user_data):
        """Test user deletion."""
        # Arrange
        service = UserService(db_session)
        user = service.create_user(sample_user_data)

        # Act
        service.delete_user(user.id)

        # Assert
        with pytest.raises(service.NotFoundError):
            service.get_user(user.id)


# ==================== Markers Example ====================

@pytest.mark.slow
def test_bulk_user_import(db_session):
    """Test importing large number of users (marked as slow)."""
    # Arrange
    service = UserService(db_session)
    users_data = [
        {"name": f"User{i}", "email": f"user{i}@example.com"}
        for i in range(1000)
    ]

    # Act
    imported_count = service.bulk_import(users_data)

    # Assert
    assert imported_count == 1000


@pytest.mark.integration
def test_user_with_related_posts(db_session, sample_user_data):
    """Test user with related posts (integration test)."""
    # Arrange
    service = UserService(db_session)
    user = service.create_user(sample_user_data)

    # Act
    post = user.create_post(title="Test Post", content="Content")

    # Assert
    assert post.user_id == user.id
    assert len(user.posts) == 1


# ==================== Fixture Scope Examples ====================

@pytest.fixture(scope="module")
def expensive_resource():
    """
    Expensive resource created once per module.

    Use module scope for resources that are expensive to create
    but can be safely shared across tests.
    """
    # Setup (runs once per module)
    resource = create_expensive_resource()

    yield resource

    # Teardown (runs once after all tests in module)
    resource.cleanup()


def test_using_expensive_resource(expensive_resource):
    """Test using module-scoped expensive resource."""
    result = expensive_resource.perform_operation()
    assert result is not None
