# FastAPI Integration with SQLModel

## Table of Contents

- [Database Setup](#database-setup)
- [Dependency Injection](#dependency-injection)
- [CRUD Endpoints](#crud-endpoints)
- [Pydantic Models](#pydantic-models)
- [Error Handling](#error-handling)
- [Startup Events](#startup-events)
- [Complete Example](#complete-example)

---

## Database Setup

### Engine and Session

```python
# database.py
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries
    connect_args={"check_same_thread": False}  # SQLite only
)

def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session
```

### PostgreSQL Configuration

```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

---

## Dependency Injection

### Session Dependency

```python
from fastapi import Depends
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()
    return users
```

### Multiple Dependencies

```python
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/users/me")
def read_users_me(
    session: SessionDep,
    current_user: CurrentUser
):
    return current_user
```

---

## CRUD Endpoints

### Create

```python
from fastapi import HTTPException

@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    # Check if user exists
    existing = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    # Create user
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
```

### Read (List)

```python
@app.get("/users", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users
```

### Read (Single)

```python
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

### Update

```python
@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only provided fields
    user_data = user_update.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
```

### Delete

```python
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}
```

---

## Pydantic Models

### Separate Read/Write Models

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Database model
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Create model (input)
class UserCreate(SQLModel):
    email: str
    password: str
    full_name: str

# Update model (partial input)
class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

# Response model (output)
class UserResponse(SQLModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    # hashed_password excluded for security
```

### With Relationships

```python
# Response with related data
class UserWithPosts(UserResponse):
    posts: list["PostResponse"] = []

class PostResponse(SQLModel):
    id: int
    title: str
    content: str
    created_at: datetime

@app.get("/users/{user_id}/posts", response_model=UserWithPosts)
def read_user_with_posts(
    user_id: int,
    session: Session = Depends(get_session)
):
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

---

## Error Handling

### Custom Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Database integrity error",
            "error": str(exc.orig)
        }
    )
```

### Validation Errors

```python
from pydantic import ValidationError

@app.exception_handler(ValidationError)
async def validation_error_handler(
    request: Request,
    exc: ValidationError
):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

---

## Startup Events

### Create Tables on Startup

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(lifespan=lifespan)
```

### Legacy Startup Event

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

---

## Complete Example

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from datetime import datetime
from contextlib import asynccontextmanager

# Database setup
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    email: str
    full_name: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(SQLModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

# App setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Endpoints
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_update.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
```

### Running the Application

```bash
# Install dependencies
pip install fastapi sqlmodel uvicorn

# Run server
uvicorn main:app --reload

# API docs available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```
