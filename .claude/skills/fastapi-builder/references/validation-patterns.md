# Pydantic Validation Patterns

## Table of Contents

- [Field Validation with Field()](#field-validation-with-field)
- [Custom Validators](#custom-validators)
- [Model Validators](#model-validators)
- [Constrained Types](#constrained-types)
- [Separate Create/Update Schemas](#separate-createupdate-schemas)
- [Nested Models](#nested-models)
- [Custom Types](#custom-types)
- [Enum Validation](#enum-validation)
- [Request Body Examples](#request-body-examples)
- [Conditional Validation](#conditional-validation)
- [File Upload Validation](#file-upload-validation)
- [Query Parameter Validation](#query-parameter-validation)
- [Error Response Format](#error-response-format)
- [Best Practices](#best-practices)

---

## Field Validation with Field()

Use Pydantic's `Field()` for constraints and metadata.

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """User creation schema with field validation."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120, description="User age (18+)")
    website: Optional[str] = Field(None, pattern="^https?://")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "securepass123",
                "age": 25,
                "website": "https://example.com"
            }
        }
```

### Common Field Constraints

| Constraint | Type | Example |
|------------|------|---------|
| `min_length` | str | `Field(min_length=3)` |
| `max_length` | str | `Field(max_length=50)` |
| `pattern` | str | `Field(pattern="^[A-Z]")` |
| `gt` | int/float | `Field(gt=0)` - greater than |
| `ge` | int/float | `Field(ge=0)` - greater or equal |
| `lt` | int/float | `Field(lt=100)` - less than |
| `le` | int/float | `Field(le=100)` - less or equal |
| `multiple_of` | int/float | `Field(multiple_of=5)` |

---

## Custom Validators

Use `@field_validator` for custom validation logic.

```python
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: int

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @field_validator('priority')
    @classmethod
    def priority_must_be_valid(cls, v: int) -> int:
        """Validate priority is 1-5."""
        if v < 1 or v > 5:
            raise ValueError('Priority must be between 1 and 5')
        return v

    @field_validator('due_date')
    @classmethod
    def due_date_must_be_future(cls, v: datetime) -> datetime:
        """Validate due date is in the future."""
        if v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v
```

---

## Model Validators

Use `@model_validator` for validation across multiple fields.

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    def check_dates(self) -> 'DateRange':
        """Ensure start_date is before end_date."""
        if self.start_date >= self.end_date:
            raise ValueError('start_date must be before end_date')
        return self

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self) -> 'PasswordChange':
        """Ensure new passwords match."""
        if self.new_password != self.confirm_password:
            raise ValueError('New passwords do not match')
        if self.current_password == self.new_password:
            raise ValueError('New password must be different from current password')
        return self
```

---

## Constrained Types

Use Pydantic's constrained types for common patterns.

```python
from pydantic import BaseModel, constr, conint, confloat, conlist
from typing import List

class Product(BaseModel):
    # Constrained string (regex + length)
    sku: constr(pattern=r'^[A-Z]{3}-\d{6}$') = Field(..., description="SKU format: ABC-123456")

    # Constrained integer (range)
    quantity: conint(ge=0, le=10000)

    # Constrained float (precision)
    price: confloat(gt=0, le=999999.99)

    # Constrained list (length)
    tags: conlist(str, min_length=1, max_length=10)
```

---

## Separate Create/Update Schemas

Create different schemas for different operations.

```python
# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

# Create schema: All fields required
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Update schema: All fields optional (partial update)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    password: Optional[str] = Field(None, min_length=8)

# Response schema: Excludes sensitive fields
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode
```

---

## Nested Models

Validate nested structures.

```python
class Address(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(pattern="^[A-Z]{2}$")
    zip_code: str = Field(pattern=r'^\d{5}(-\d{4})?$')

class UserProfile(BaseModel):
    user_id: int
    bio: Optional[str] = Field(None, max_length=500)
    address: Address  # Nested model
    phone_numbers: List[str] = Field(..., min_length=1, max_length=3)

    @field_validator('phone_numbers')
    @classmethod
    def validate_phone_numbers(cls, v: List[str]) -> List[str]:
        """Validate phone number format."""
        pattern = r'^\+?1?\d{10,15}$'
        for phone in v:
            if not re.match(pattern, phone):
                raise ValueError(f'Invalid phone number: {phone}')
        return v
```

---

## Custom Types

Create reusable custom types.

```python
from pydantic import BeforeValidator, AfterValidator
from typing import Annotated

def validate_hex_color(v: str) -> str:
    """Validate hex color format."""
    if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
        raise ValueError('Must be valid hex color (e.g., #FF5733)')
    return v.upper()

HexColor = Annotated[str, AfterValidator(validate_hex_color)]

def normalize_email(v: str) -> str:
    """Normalize email to lowercase."""
    return v.lower().strip()

NormalizedEmail = Annotated[EmailStr, BeforeValidator(normalize_email)]

class ThemeSettings(BaseModel):
    primary_color: HexColor
    secondary_color: HexColor
    admin_email: NormalizedEmail
```

---

## Enum Validation

Use Python enums for fixed choices.

```python
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"

class TaskPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class TaskCreate(BaseModel):
    title: str
    status: TaskStatus = TaskStatus.TODO  # Default value
    priority: TaskPriority

# In endpoint
@router.post("/tasks")
def create_task(task_in: TaskCreate):
    # task_in.status is guaranteed to be valid TaskStatus
    # task_in.priority is guaranteed to be valid TaskPriority
    return {"status": task_in.status.value, "priority": task_in.priority.value}
```

---

## Request Body Examples

Add examples for API documentation.

```python
class TaskCreate(BaseModel):
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Detailed description")
    due_date: Optional[datetime] = None
    priority: int = Field(default=3, ge=1, le=5)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "Complete project proposal",
                    "description": "Write and submit the Q2 project proposal",
                    "due_date": "2025-02-01T17:00:00Z",
                    "priority": 4
                },
                {
                    "title": "Quick task",
                    "priority": 2
                }
            ]
        }
```

---

## Conditional Validation

Validate based on other field values.

```python
from typing import Literal

class ShippingInfo(BaseModel):
    shipping_type: Literal["standard", "express", "overnight"]
    shipping_cost: float = Field(gt=0)
    delivery_date: Optional[datetime] = None

    @model_validator(mode='after')
    def validate_delivery_date(self) -> 'ShippingInfo':
        """Express and overnight require delivery date."""
        if self.shipping_type in ["express", "overnight"] and not self.delivery_date:
            raise ValueError(f'{self.shipping_type} shipping requires delivery_date')
        return self
```

---

## File Upload Validation

Validate uploaded files.

```python
from fastapi import UploadFile, File, HTTPException

class FileUploadValidator:
    """Validate uploaded files."""

    @staticmethod
    def validate_image(file: UploadFile):
        """Validate image file."""
        # Check extension
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {ext} not allowed. Allowed: {allowed_extensions}"
            )

        # Check content type
        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Content type {file.content_type} not allowed"
            )

        # Check file size (in dependency)
        return file

# In endpoint
@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...)
):
    """Upload image with validation."""
    FileUploadValidator.validate_image(file)

    # Process file
    contents = await file.read()
    # ... save file logic

    return {"filename": file.filename, "size": len(contents)}
```

---

## Query Parameter Validation

Validate query parameters.

```python
from fastapi import Query
from typing import List, Optional

@router.get("/tasks")
def search_tasks(
    q: Optional[str] = Query(None, min_length=1, max_length=100, description="Search query"),
    status: List[str] = Query(default=[], description="Filter by status"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority"),
    skip: int = Query(0, ge=0, description="Skip records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit records"),
    sort_by: str = Query("created_at", regex="^(title|created_at|priority)$"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    """
    Search and filter tasks.

    - **q**: Search in title and description
    - **status**: Filter by one or more statuses
    - **priority**: Filter by priority (1-5)
    """
    ...
```

---

## Error Response Format

Standardize validation error responses.

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation error handler."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )

# Example error response:
# {
#     "detail": "Validation error",
#     "errors": [
#         {
#             "field": "body.email",
#             "message": "value is not a valid email address",
#             "type": "value_error.email"
#         },
#         {
#             "field": "body.age",
#             "message": "ensure this value is greater than or equal to 18",
#             "type": "value_error.number.not_ge"
#         }
#     ]
# }
```

---

## Best Practices

### 1. Be Specific
Use specific constraints rather than generic validation:
```python
# ❌ Generic
age: int

# ✅ Specific
age: int = Field(ge=18, le=120, description="User age must be 18+")
```

### 2. Provide Good Error Messages
```python
@field_validator('username')
@classmethod
def validate_username(cls, v: str) -> str:
    if len(v) < 3:
        raise ValueError('Username must be at least 3 characters')  # Clear message
    if not v.isalnum():
        raise ValueError('Username can only contain letters and numbers')
    return v
```

### 3. Use Type Hints
Always use proper type hints for better validation:
```python
from typing import List, Optional
from datetime import datetime

tasks: List[str]  # List of strings
created_at: datetime  # DateTime object
count: Optional[int] = None  # Optional integer
```

### 4. Document Validation
Add descriptions to fields for API documentation:
```python
email: EmailStr = Field(..., description="User email address")
password: str = Field(..., min_length=8, description="Minimum 8 characters")
```
