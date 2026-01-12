# FastAPI Anti-Patterns

Common mistakes to avoid when building FastAPI applications.

## Table of Contents

- [1. Exposing Database Models Directly](#1-exposing-database-models-directly)
- [2. Mutable Default Arguments](#2-mutable-default-arguments)
- [3. Not Using Dependency Injection](#3-not-using-dependency-injection)
- [4. Hardcoding Configuration](#4-hardcoding-configuration)
- [5. Committing Sessions in Endpoints](#5-committing-sessions-in-endpoints)
- [6. Returning Wrong HTTP Status Codes](#6-returning-wrong-http-status-codes)
- [7. Missing Error Handling](#7-missing-error-handling)
- [8. Synchronous I/O in Async Routes](#8-synchronous-io-in-async-routes)
- [9. No Pagination on List Endpoints](#9-no-pagination-on-list-endpoints)
- [10. CORS Wildcard with Credentials](#10-cors-wildcard-with-credentials)
- [11. Not Using Type Hints](#11-not-using-type-hints)
- [12. Ignoring Validation Errors](#12-ignoring-validation-errors)
- [13. Creating Large Monolithic Endpoints](#13-creating-large-monolithic-endpoints)
- [14. Not Handling Database Constraints](#14-not-handling-database-constraints)
- [15. Missing Documentation](#15-missing-documentation)
- [Summary Checklist](#summary-checklist)

---

## 1. Exposing Database Models Directly

### ❌ Anti-Pattern
```python
from app.models.user import User

@router.get("/users/{user_id}", response_model=User)  # Exposes User model
def get_user(user_id: int, session: Session = Depends(get_session)):
    return session.get(User, user_id)
```

**Problems**:
- Exposes sensitive fields (hashed_password, internal_id)
- Couples API to database schema
- Breaking changes when database changes

### ✅ Correct Pattern
```python
from app.schemas.user import UserResponse  # Separate response schema

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    return user  # Serialized to UserResponse (excludes sensitive fields)
```

---

## 2. Mutable Default Arguments

### ❌ Anti-Pattern
```python
def get_users(tags: List[str] = []):  # Mutable default
    tags.append("default")  # Modifies shared list!
    return {"tags": tags}

# First call: ["default"]
# Second call: ["default", "default"]  # BUG!
```

### ✅ Correct Pattern
```python
def get_users(tags: Optional[List[str]] = None):  # None default
    if tags is None:
        tags = []
    tags.append("default")
    return {"tags": tags}
```

---

## 3. Not Using Dependency Injection

### ❌ Anti-Pattern
```python
from app.core.database import engine

@router.get("/tasks")
def get_tasks():
    with Session(engine) as session:  # Manual session management
        tasks = session.exec(select(Task)).all()
    return tasks
```

**Problems**:
- Difficult to test (can't mock session)
- Error-prone (forgot to close session?)
- Duplicated code

### ✅ Correct Pattern
```python
@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):  # Dependency injection
    tasks = session.exec(select(Task)).all()
    return tasks
```

---

## 4. Hardcoding Configuration

### ❌ Anti-Pattern
```python
DATABASE_URL = "postgresql://user:pass@localhost/db"  # Hardcoded
SECRET_KEY = "my-secret-key-123"  # Committed to git!
CORS_ORIGINS = ["*"]  # Insecure wildcard
```

### ✅ Correct Pattern
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    CORS_ORIGINS: List[str]

    class Config:
        env_file = ".env"

settings = Settings()

# .env (NOT committed to git)
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=generated-secret-key
CORS_ORIGINS=["http://localhost:3000"]
```

---

## 5. Committing Sessions in Endpoints

### ❌ Anti-Pattern
```python
@router.post("/tasks")
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_in.model_dump())
    session.add(task)
    # Forgot to commit!
    return task  # Not persisted!
```

**Problems**:
- Easy to forget
- Inconsistent patterns
- Hard to handle transactions

### ✅ Correct Pattern

**Option 1: Commit in endpoint**
```python
@router.post("/tasks")
def create_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    task = Task(**task_in.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Option 2: Use dependency with transaction**
```python
def get_session_with_commit():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise

@router.post("/tasks")
def create_task(task_in: TaskCreate, session: Session = Depends(get_session_with_commit)):
    task = Task(**task_in.model_dump())
    session.add(task)
    return task  # Auto-committed by dependency
```

---

## 6. Returning Wrong HTTP Status Codes

### ❌ Anti-Pattern
```python
@router.post("/tasks")
def create_task(task_in: TaskCreate):
    task = create_task_logic(task_in)
    return task  # Returns 200 OK instead of 201 CREATED

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    delete_task_logic(task_id)
    return {"message": "deleted"}  # Returns 200 OK with body instead of 204 NO CONTENT
```

### ✅ Correct Pattern
```python
from fastapi import status

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    task = create_task_logic(task_in)
    return task  # 201 CREATED

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    delete_task_logic(task_id)
    return None  # 204 NO CONTENT (no body)
```

---

## 7. Missing Error Handling

### ❌ Anti-Pattern
```python
@router.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    return task  # Returns None if not found! (200 with null body)
```

### ✅ Correct Pattern
```python
@router.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task
```

---

## 8. Synchronous I/O in Async Routes

### ❌ Anti-Pattern
```python
@router.get("/tasks")
async def get_tasks(session: Session = Depends(get_session)):
    # Using sync session in async route!
    tasks = session.exec(select(Task)).all()  # Blocks event loop
    return tasks
```

### ✅ Correct Pattern

**Option 1: Use sync route**
```python
@router.get("/tasks")  # Sync route
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks
```

**Option 2: Use async session**
```python
from sqlmodel.ext.asyncio.session import AsyncSession

@router.get("/tasks")
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Task))
    tasks = result.all()
    return tasks
```

---

## 9. No Pagination on List Endpoints

### ❌ Anti-Pattern
```python
@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()  # Returns ALL tasks!
    return tasks
```

**Problems**:
- Performance issues with large datasets
- High memory usage
- Slow response times

### ✅ Correct Pattern
```python
@router.get("/tasks")
def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks
```

---

## 10. CORS Wildcard with Credentials

### ❌ Anti-Pattern
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Wildcard
    allow_credentials=True,  # With credentials - SECURITY RISK!
)
```

**Problems**:
- Browsers reject this configuration
- Major security vulnerability if it worked

### ✅ Correct Pattern
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_credentials=True,
)
```

---

## 11. Not Using Type Hints

### ❌ Anti-Pattern
```python
@router.get("/tasks/{task_id}")
def get_task(task_id, session):  # No type hints
    task = session.get(Task, task_id)
    return task
```

**Problems**:
- No auto-validation
- Poor IDE support
- Missing documentation

### ✅ Correct Pattern
```python
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

---

## 12. Ignoring Validation Errors

### ❌ Anti-Pattern
```python
@router.post("/tasks")
def create_task(task_in: TaskCreate):
    try:
        task = Task(**task_in.model_dump())
        # Process task
    except:  # Bare except catches everything!
        return {"error": "something went wrong"}  # No details
```

### ✅ Correct Pattern
```python
from pydantic import ValidationError

@router.post("/tasks")
def create_task(task_in: TaskCreate):  # Pydantic validates automatically
    # If we get here, validation passed
    task = Task(**task_in.model_dump())
    # Process task
    return task

# FastAPI automatically handles ValidationError
# Returns 422 with detailed error info
```

---

## 13. Creating Large Monolithic Endpoints

### ❌ Anti-Pattern
```python
@router.post("/tasks")
def create_task_and_do_everything(
    task_in: TaskCreate,
    send_email: bool = True,
    create_calendar_event: bool = True,
    notify_slack: bool = True,
    session: Session = Depends(get_session)
):
    # 200 lines of code doing everything...
    task = Task(**task_in.model_dump())
    session.add(task)
    session.commit()

    if send_email:
        # 50 lines of email logic
        ...

    if create_calendar_event:
        # 50 lines of calendar logic
        ...

    if notify_slack:
        # 50 lines of Slack logic
        ...

    return task
```

### ✅ Correct Pattern
```python
# Separate concerns

@router.post("/tasks")
def create_task(
    task_in: TaskCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    # Create task
    task = Task(**task_in.model_dump())
    session.add(task)
    session.commit()

    # Trigger background tasks
    background_tasks.add_task(send_task_notification, task.id)
    background_tasks.add_task(create_calendar_event, task.id)

    return task

# Separate functions for each concern
def send_task_notification(task_id: int):
    ...

def create_calendar_event(task_id: int):
    ...
```

---

## 14. Not Handling Database Constraints

### ❌ Anti-Pattern
```python
@router.post("/users")
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    user = User(**user_in.model_dump())
    session.add(user)
    session.commit()  # Crashes if email already exists!
    return user
```

### ✅ Correct Pattern
```python
from sqlalchemy.exc import IntegrityError

@router.post("/users")
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        user = User(**user_in.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
```

---

## 15. Missing Documentation

### ❌ Anti-Pattern
```python
@router.post("/tasks")
def create_task(task_in: TaskCreate):
    ...
```

### ✅ Correct Pattern
```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided information. Returns the created task.",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid input"},
        401: {"description": "Not authenticated"}
    }
)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new task.

    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **due_date**: Due date in ISO format (optional)
    - **priority**: Priority level 1-5 (default: 3)
    """
    ...
```

---

## Summary Checklist

Avoid these anti-patterns:

- [ ] Exposing database models in API responses
- [ ] Using mutable default arguments
- [ ] Not using dependency injection
- [ ] Hardcoding secrets and configuration
- [ ] Forgetting to commit database sessions
- [ ] Using wrong HTTP status codes
- [ ] Missing error handling
- [ ] Mixing sync/async incorrectly
- [ ] No pagination on list endpoints
- [ ] CORS wildcard with credentials
- [ ] Missing type hints
- [ ] Catching all exceptions without proper handling
- [ ] Creating monolithic endpoints
- [ ] Not handling database constraints
- [ ] Missing API documentation
