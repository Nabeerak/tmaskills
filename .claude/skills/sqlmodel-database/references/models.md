# SQLModel Model Definitions

## Table of Contents

- [Basic Model Structure](#basic-model-structure)
- [Field Types](#field-types)
- [Field Constraints](#field-constraints)
- [Indexes](#indexes)
- [Default Values](#default-values)
- [Optional Fields](#optional-fields)
- [Computed Properties](#computed-properties)
- [Table Arguments](#table-arguments)
- [Model Inheritance](#model-inheritance)
- [Timestamps and Audit Fields](#timestamps-and-audit-fields)

---

## Basic Model Structure

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    """Basic user model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str
    is_active: bool = Field(default=True)
```

**Key elements**:
- `SQLModel` base class
- `table=True` creates database table
- `id` with `Optional[int]` and `primary_key=True`
- Field constraints via `Field()`

---

## Field Types

### String Fields

```python
name: str = Field(max_length=100)
email: str = Field(max_length=255)
description: Optional[str] = Field(default=None, max_length=1000)
```

### Numeric Fields

```python
age: int = Field(ge=0, le=150)  # Greater/equal 0, less/equal 150
price: float = Field(gt=0)      # Greater than 0
quantity: int = Field(ge=0)     # Non-negative
```

### Boolean Fields

```python
is_active: bool = Field(default=True)
is_verified: bool = Field(default=False)
```

### DateTime Fields

```python
from datetime import datetime

created_at: datetime = Field(default_factory=datetime.utcnow)
updated_at: Optional[datetime] = None
```

### Enum Fields

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

role: UserRole = Field(default=UserRole.USER)
```

---

## Field Constraints

### Validation Constraints

```python
from pydantic import EmailStr

email: EmailStr = Field(unique=True, index=True)
username: str = Field(min_length=3, max_length=50)
age: int = Field(ge=18, le=100)
price: float = Field(gt=0, le=1000000)
```

### Database Constraints

```python
email: str = Field(unique=True, index=True, max_length=255)
username: str = Field(unique=True, nullable=False)
foreign_key_id: int = Field(foreign_key="other_table.id")
```

### Check Constraints

```python
from sqlalchemy import CheckConstraint

class Product(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint('price > 0', name='positive_price'),
        CheckConstraint('stock >= 0', name='non_negative_stock'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    stock: int
```

---

## Indexes

### Single Column Index

```python
email: str = Field(unique=True, index=True)
```

### Composite Index

```python
from sqlalchemy import Index

class Order(SQLModel, table=True):
    __table_args__ = (
        Index('ix_user_date', 'user_id', 'created_at'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    created_at: datetime
```

### Unique Composite Index

```python
from sqlalchemy import UniqueConstraint

class UserProfile(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('user_id', 'platform', name='uq_user_platform'),
    )
```

---

## Default Values

### Static Defaults

```python
is_active: bool = Field(default=True)
role: str = Field(default="user")
```

### Factory Defaults

```python
from datetime import datetime
import uuid

created_at: datetime = Field(default_factory=datetime.utcnow)
uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
```

### Database-Level Defaults

```python
from sqlalchemy import text

created_at: datetime = Field(sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})
```

---

## Optional Fields

```python
# Optional with None default
middle_name: Optional[str] = None
phone: Optional[str] = Field(default=None, max_length=20)

# Optional with explicit default
bio: Optional[str] = Field(default=None, max_length=500)
```

---

## Computed Properties

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        """Computed property not stored in database."""
        return f"{self.first_name} {self.last_name}"
```

---

## Table Arguments

### Table Name

```python
class User(SQLModel, table=True):
    __tablename__ = "users"  # Custom table name

    id: Optional[int] = Field(default=None, primary_key=True)
```

### Schema

```python
class User(SQLModel, table=True):
    __table_args__ = {"schema": "auth"}
```

### Multiple Constraints

```python
class Product(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint('price > 0'),
        UniqueConstraint('sku'),
        Index('ix_category_name', 'category', 'name'),
        {"schema": "inventory"}
    )
```

---

## Model Inheritance

### Base Model Pattern

```python
from datetime import datetime

class TimestampModel(SQLModel):
    """Base model with timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class User(TimestampModel, table=True):
    """User inherits timestamp fields."""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
```

### Abstract Base

```python
class BaseModel(SQLModel):
    """Abstract base - not a table."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str

class Product(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
```

---

## Timestamps and Audit Fields

### Basic Timestamps

```python
from datetime import datetime

class AuditModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

### Full Audit Fields

```python
class FullAuditModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
```

### Soft Delete

```python
class SoftDeleteModel(SQLModel):
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="user.id")
```

---

## Complete Example

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(SQLModel, table=True):
    """Complete user model with all features."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint('age >= 18', name='adult_user'),
        Index('ix_email_active', 'email', 'is_active'),
    )

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required fields
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, min_length=3, max_length=50)

    # Optional fields
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    age: Optional[int] = Field(default=None, ge=18, le=150)

    # Fields with defaults
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
```

---

## Best Practices

1. **Always use type hints** for all fields
2. **Use Optional[T]** for nullable fields
3. **Set max_length** for string fields to prevent issues
4. **Use Field()** for constraints and metadata
5. **Add indexes** on frequently queried fields
6. **Use enums** for fixed choice fields
7. **Document models** with docstrings
8. **Use default_factory** for mutable defaults
9. **Consider audit fields** for production models
10. **Keep models simple** - complex logic in services

---

## Common Pitfalls

**Don't use mutable defaults**:
```python
# ❌ Bad
tags: list = []

# ✓ Good
tags: list = Field(default_factory=list)
```

**Don't forget Optional for nullable**:
```python
# ❌ Bad - will fail on None
middle_name: str = None

# ✓ Good
middle_name: Optional[str] = None
```

**Don't skip max_length**:
```python
# ❌ Bad - unlimited length
description: str

# ✓ Good
description: str = Field(max_length=1000)
```
