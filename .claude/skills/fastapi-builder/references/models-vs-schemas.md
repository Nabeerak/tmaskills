# SQLModel Models vs Pydantic Schemas

## Table of Contents

- [Key Distinction](#key-distinction)
- [Why Separate Them?](#why-separate-them)
- [Pattern: SQLModel for Models](#pattern-sqlmodel-for-models)
- [Pattern: Pydantic for Schemas](#pattern-pydantic-for-schemas)
- [Usage in Endpoints](#usage-in-endpoints)
- [Advanced Patterns](#advanced-patterns)
- [Common Patterns](#common-patterns)
- [When to Use SQLModel for Both?](#when-to-use-sqlmodel-for-both)

---

## Key Distinction

| Aspect | Models | Schemas |
|--------|--------|---------|
| **Purpose** | Represent database tables | Validate API requests/responses |
| **Framework** | SQLModel (SQLAlchemy + Pydantic) | Pure Pydantic |
| **Location** | `app/models/` | `app/schemas/` |
| **Usage** | Database operations | API serialization/deserialization |
| **Includes** | Database-specific fields (indexes, constraints) | API-specific fields (validation, examples) |

---

## Why Separate Them?

### 1. Security
Models often contain sensitive fields that should NOT be exposed in API responses:
- Password hashes
- Internal IDs or tokens
- Audit timestamps
- Soft delete flags

### 2. Flexibility
API contracts may differ from database structure:
- Nested relationships in API but foreign keys in DB
- Computed/derived fields in API
- Different field names for API vs database
- Multiple API representations of same model

### 3. Validation
Different validation rules for different operations:
- Create: All required fields
- Update: All fields optional (partial update)
- Response: May include computed fields

---

## Pattern: SQLModel for Models

SQLModel models define the database table structure.

```python
# app/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """Database model for users table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

**Key features**:
- `table=True` creates database table
- `Field()` defines constraints and indexes
- Includes internal fields (hashed_password, timestamps)

---

## Pattern: Pydantic for Schemas

Pydantic schemas define API request/response structure.

### Create Schema (Request)

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, description="Plain text password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepass123"
            }
        }
```

**Key features**:
- Only fields user provides
- Plain `password` (will be hashed)
- Validation rules (min_length, email format)
- Examples for documentation

### Update Schema (Request)

```python
class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
```

**Key features**:
- All fields optional (partial update)
- No `id` field (from path parameter)
- Can update subset of fields

### Response Schema (Response)

```python
from datetime import datetime

class UserResponse(BaseModel):
    """Schema for user in API responses."""

    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allow from ORM models
```

**Key features**:
- No `hashed_password` (security)
- No `is_superuser` (internal field)
- `from_attributes = True` converts from SQLModel

---

## Usage in Endpoints

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,  # Pydantic schema for validation
    session: Session = Depends(get_session)
) -> User:
    """Create new user."""

    # Check if user exists
    statement = select(User).where(User.email == user_in.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create model from schema
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user  # Serialized to UserResponse automatically

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session)
) -> User:
    """Get user by ID."""

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user  # UserResponse excludes hashed_password

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,  # Partial update schema
    session: Session = Depends(get_session)
) -> User:
    """Update user."""

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update only provided fields
    update_data = user_in.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
```

---

## Advanced Patterns

### Nested Relationships

**Model with relationship**:
```python
# app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    user_id: int = Field(foreign_key="user.id")

    # Relationship
    user: Optional["User"] = Relationship(back_populates="tasks")
```

**Schema with nested data**:
```python
# app/schemas/task.py
from pydantic import BaseModel
from app.schemas.user import UserResponse

class TaskResponse(BaseModel):
    id: int
    title: str
    user: UserResponse  # Nested user data

    class Config:
        from_attributes = True
```

### Computed Fields

**Schema with computed property**:
```python
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str  # Computed from first_name + last_name

    @classmethod
    def from_model(cls, user: User):
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=f"{user.first_name} {user.last_name}"
        )
```

---

## Common Patterns

### Base Schemas

Create base schemas for common fields:

```python
# app/schemas/base.py
from pydantic import BaseModel
from datetime import datetime

class TimestampSchema(BaseModel):
    """Base schema with timestamp fields."""
    created_at: datetime
    updated_at: Optional[datetime] = None

class ResponseBase(TimestampSchema):
    """Base response schema."""
    id: int

    class Config:
        from_attributes = True
```

### Reuse in Specific Schemas

```python
# app/schemas/user.py
from app.schemas.base import ResponseBase

class UserResponse(ResponseBase):
    """User response inherits id and timestamps."""
    email: str
    username: str
    is_active: bool
```

---

## When to Use SQLModel for Both?

SQLModel can be used for both models and schemas in simple cases:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

# Base (shared fields)
class UserBase(SQLModel):
    email: str
    username: str

# Database model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

# Create schema
class UserCreate(UserBase):
    password: str

# Response schema
class UserResponse(UserBase):
    id: int
```

**When this works**:
- Simple CRUD APIs
- No complex validation
- API structure mirrors database

**When to separate**:
- Need different validation rules
- API has computed fields
- Complex nested relationships
- Security-sensitive fields
