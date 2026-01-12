# Dependency Injection in FastAPI

FastAPI's dependency injection system is a powerful feature for managing reusable components, database sessions, authentication, and more.

## Table of Contents

- [Basic Dependency Pattern](#basic-dependency-pattern)
- [Common Dependencies](#common-dependencies)
- [Dependency Chains](#dependency-chains)
- [Class-Based Dependencies](#class-based-dependencies)
- [Dependencies with Yield](#dependencies-with-yield)
- [Caching Dependencies](#caching-dependencies)
- [Global Dependencies](#global-dependencies)
- [Optional Dependencies](#optional-dependencies)
- [Dependency Override (Testing)](#dependency-override-testing)
- [Best Practices](#best-practices)
- [Common Dependency Patterns](#common-dependency-patterns)

---

## Basic Dependency Pattern

```python
from fastapi import Depends

# Define dependency
def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Use in endpoint
@router.get("/items")
def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

---

## Common Dependencies

### 1. Database Session

Most important dependency for database operations.

```python
# app/core/database.py
from sqlmodel import create_engine, Session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_session():
    """Dependency that provides database session."""
    with Session(engine) as session:
        yield session
```

**Usage**:
```python
@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks
```

**Why yield**: Ensures session is closed after request, even if exception occurs.

### 2. Pagination Parameters

Reusable pagination logic.

```python
# app/api/deps.py
from fastapi import Query

class CommonQueryParams:
    """Common pagination parameters."""

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, ge=1, le=100, description="Max items to return")
    ):
        self.skip = skip
        self.limit = limit

# Usage
@router.get("/tasks")
def get_tasks(
    commons: CommonQueryParams = Depends(),
    session: Session = Depends(get_session)
):
    statement = select(Task).offset(commons.skip).limit(commons.limit)
    return session.exec(statement).all()
```

### 3. Current User

Extract and validate current user from token.

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user

# Usage
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
```

### 4. Active User Check

Ensure user is active.

```python
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Check if current user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
```

### 5. Admin Permission

Require admin privileges.

```python
async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require admin privileges."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Usage
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Delete user (admin only)."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted"}
```

---

## Dependency Chains

Dependencies can depend on other dependencies:

```python
# Chain: token → current_user → active_user → admin
get_current_user          # Depends on: oauth2_scheme, get_session
↓
get_current_active_user   # Depends on: get_current_user
↓
require_admin             # Depends on: get_current_active_user
```

---

## Class-Based Dependencies

### Using __call__ Method

```python
class PermissionChecker:
    """Check if user has specific permission."""

    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if self.required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{self.required_permission}' required"
            )
        return current_user

# Usage
@router.post("/tasks", dependencies=[Depends(PermissionChecker("tasks:create"))])
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    """Create task (requires 'tasks:create' permission)."""
    task = Task(**task_in.model_dump())
    session.add(task)
    session.commit()
    return task
```

---

## Dependencies with Yield

Use yield for setup/teardown logic:

```python
def get_db_with_transaction():
    """Database session with automatic transaction handling."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()  # Commit on success
        except Exception:
            session.rollback()  # Rollback on error
            raise

# Usage
@router.post("/tasks")
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_db_with_transaction)
):
    """Create task with automatic transaction handling."""
    task = Task(**task_in.model_dump())
    session.add(task)
    # No need to explicitly commit - dependency handles it
    return task
```

### Context Manager Pattern

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_async_session():
    """Async database session."""
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

---

## Caching Dependencies

FastAPI caches dependency results within a request:

```python
def expensive_operation():
    """Expensive operation called once per request."""
    print("Computing expensive result...")
    return {"result": "expensive"}

@router.get("/endpoint1")
def endpoint1(data: dict = Depends(expensive_operation)):
    return data

@router.get("/endpoint2")
def endpoint2(
    data1: dict = Depends(expensive_operation),  # Same instance
    data2: dict = Depends(expensive_operation)   # Same instance
):
    # expensive_operation() called only once
    return {"data1": data1, "data2": data2}
```

**Disable caching**:
```python
@router.get("/endpoint")
def endpoint(data: dict = Depends(expensive_operation, use_cache=False)):
    return data
```

---

## Global Dependencies

Apply dependencies to all routes in a router or app:

### Router-Level

```python
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)]  # All routes require admin
)

@router.get("/users")
def list_users(session: Session = Depends(get_session)):
    """List users (automatically requires admin)."""
    return session.exec(select(User)).all()
```

### App-Level

```python
app = FastAPI(
    dependencies=[Depends(verify_api_key)]  # All routes require API key
)
```

---

## Optional Dependencies

Make dependencies optional for some routes:

```python
async def get_current_user_optional(
    token: str | None = Depends(OAuth2PasswordBearer(tokenUrl="login", auto_error=False)),
    session: Session = Depends(get_session)
) -> User | None:
    """Get current user if token provided, otherwise None."""
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        return session.get(User, user_id)
    except JWTError:
        return None

# Usage
@router.get("/tasks")
def get_tasks(
    current_user: User | None = Depends(get_current_user_optional),
    session: Session = Depends(get_session)
):
    """Get tasks (public if not authenticated, filtered if authenticated)."""
    statement = select(Task)

    if current_user:
        # User authenticated: show only their tasks
        statement = statement.where(Task.user_id == current_user.id)
    else:
        # Public: show only public tasks
        statement = statement.where(Task.is_public == True)

    return session.exec(statement).all()
```

---

## Dependency Override (Testing)

Override dependencies for testing:

```python
# test_tasks.py
from fastapi.testclient import TestClient

def override_get_session():
    """Test database session."""
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

def test_create_task():
    response = client.post("/api/v1/tasks", json={"title": "Test"})
    assert response.status_code == 201
```

---

## Best Practices

### 1. Single Responsibility
Each dependency should do one thing:
- ❌ `get_user_and_check_permission`
- ✅ `get_current_user` + `require_permission`

### 2. Reusability
Extract common logic into dependencies:
- Pagination
- Authentication
- Permission checks
- Rate limiting

### 3. Type Hints
Always use type hints for better IDE support:
```python
def get_user(session: Session = Depends(get_session)) -> User:
    ...
```

### 4. Error Handling
Raise HTTPException in dependencies for consistent error responses:
```python
def get_item(item_id: int, session: Session = Depends(get_session)) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

### 5. Documentation
Document what dependency does and when to use it:
```python
def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.

    Raises:
        HTTPException 403: If user is not active
    """
    ...
```

---

## Common Dependency Patterns

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.get("/tasks")
@limiter.limit("5/minute")
def get_tasks(request: Request):
    ...
```

### Request Validation

```python
from fastapi import Header

async def verify_token(x_token: str = Header()):
    """Verify custom token header."""
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

async def log_request(request: Request):
    """Log incoming request."""
    logger.info(f"{request.method} {request.url}")
```
