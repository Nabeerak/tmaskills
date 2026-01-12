# CRUD Operations with SQLModel

## Table of Contents

- [Session Management](#session-management)
- [Create Operations](#create-operations)
- [Read Operations](#read-operations)
- [Update Operations](#update-operations)
- [Delete Operations](#delete-operations)
- [Bulk Operations](#bulk-operations)
- [Transactions](#transactions)
- [Error Handling](#error-handling)

---

## Session Management

```python
from sqlmodel import create_engine, Session

engine = create_engine("sqlite:///database.db")

# Context manager (recommended)
with Session(engine) as session:
    # Operations here
    session.commit()

# Dependency injection (FastAPI)
def get_session():
    with Session(engine) as session:
        yield session
```

---

## Create Operations

### Create Single Record

```python
def create_user(session: Session, user_data: dict) -> User:
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)  # Get generated ID
    return user
```

### Create with Relationships

```python
user = User(email="alice@example.com")
session.add(user)
session.commit()

post = Post(title="First Post", user_id=user.id)
session.add(post)
session.commit()
```

---

## Read Operations

### Get by ID

```python
user = session.get(User, user_id)
if not user:
    raise NotFoundException("User not found")
```

### Query with Filter

```python
from sqlmodel import select

statement = select(User).where(User.email == "alice@example.com")
user = session.exec(statement).first()
```

### Get All with Pagination

```python
def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()
```

### Count Records

```python
from sqlmodel import func

statement = select(func.count()).select_from(User)
total = session.exec(statement).one()
```

---

## Update Operations

### Update Single Field

```python
user = session.get(User, user_id)
user.email = "newemail@example.com"
session.add(user)
session.commit()
```

### Update Multiple Fields

```python
def update_user(session: Session, user_id: int, update_data: dict):
    user = session.get(User, user_id)
    if not user:
        return None

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

---

## Delete Operations

### Delete Single Record

```python
def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
```

### Soft Delete

```python
user = session.get(User, user_id)
user.is_deleted = True
user.deleted_at = datetime.utcnow()
session.add(user)
session.commit()
```

---

## Bulk Operations

### Bulk Insert

```python
users = [
    User(email=f"user{i}@example.com")
    for i in range(100)
]
session.add_all(users)
session.commit()
```

### Bulk Update

```python
from sqlmodel import update

statement = (
    update(User)
    .where(User.is_active == False)
    .values(status="inactive")
)
session.exec(statement)
session.commit()
```

---

## Transactions

```python
try:
    user = User(email="alice@example.com")
    session.add(user)

    profile = Profile(bio="Developer", user_id=user.id)
    session.add(profile)

    session.commit()
except Exception:
    session.rollback()
    raise
```

---

## Error Handling

```python
from sqlalchemy.exc import IntegrityError

try:
    session.add(user)
    session.commit()
except IntegrityError as e:
    session.rollback()
    if "unique constraint" in str(e).lower():
        raise DuplicateError("Email already exists")
    raise
```
