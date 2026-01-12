# Database Setup and Configuration

## Table of Contents

- [Engine Configuration](#engine-configuration)
- [Session Management](#session-management)
- [Connection Pooling](#connection-pooling)
- [FastAPI Integration](#fastapi-integration)

---

## Engine Configuration

### SQLite

```python
from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)
```

### PostgreSQL

```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)
```

### MySQL

```python
DATABASE_URL = "mysql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
```

---

## Session Management

```python
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session
```

---

## Connection Pooling

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # Number of connections
    max_overflow=20,       # Extra connections
    pool_timeout=30,       # Seconds to wait
    pool_recycle=3600,     # Recycle after 1 hour
    pool_pre_ping=True     # Test connections
)
```

---

## FastAPI Integration

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
```
