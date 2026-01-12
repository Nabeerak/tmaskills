# SQLModel Queries

## Table of Contents

- [Basic Queries](#basic-queries)
- [Filtering](#filtering)
- [Joins](#joins)
- [Aggregations](#aggregations)
- [Sorting](#sorting)
- [Pagination](#pagination)
- [Subqueries](#subqueries)
- [Query Optimization](#query-optimization)

---

## Basic Queries

```python
from sqlmodel import select

# Get all
statement = select(User)
users = session.exec(statement).all()

# Get first
user = session.exec(statement).first()

# Get one (raises if not found or multiple)
user = session.exec(statement).one()
```

---

## Filtering

### Single Condition

```python
statement = select(User).where(User.is_active == True)
active_users = session.exec(statement).all()
```

### Multiple AND Conditions

```python
statement = select(Product).where(
    Product.price > 100,
    Product.stock > 0,
    Product.is_active == True
)
```

### OR Conditions

```python
from sqlmodel import or_

statement = select(User).where(
    or_(User.email == "alice@example.com", User.email == "bob@example.com")
)
```

### LIKE Queries

```python
statement = select(User).where(User.email.like("%@example.com"))
```

### IN Queries

```python
statement = select(User).where(User.id.in_([1, 2, 3, 4, 5]))
```

---

## Joins

### Inner Join

```python
statement = (
    select(User, Post)
    .join(Post)
    .where(User.is_active == True)
)
results = session.exec(statement).all()

for user, post in results:
    print(f"{user.email}: {post.title}")
```

### Left Join

```python
from sqlalchemy import outerjoin

statement = select(User, Post).select_from(
    outerjoin(User, Post, User.id == Post.user_id)
)
```

### Join with Filter

```python
statement = (
    select(User)
    .join(Post)
    .where(Post.title.like("%Python%"))
    .distinct()
)
```

---

## Aggregations

### Count

```python
from sqlmodel import func

statement = select(func.count()).select_from(User)
total = session.exec(statement).one()
```

### Group By

```python
statement = (
    select(User.id, User.email, func.count(Post.id).label("post_count"))
    .join(Post)
    .group_by(User.id)
)
```

### Having

```python
statement = (
    select(User.email, func.count(Post.id).label("count"))
    .join(Post)
    .group_by(User.id)
    .having(func.count(Post.id) > 5)
)
```

---

## Sorting

```python
# Ascending
statement = select(User).order_by(User.created_at)

# Descending
statement = select(User).order_by(User.created_at.desc())

# Multiple columns
statement = select(User).order_by(User.last_name, User.first_name)
```

---

## Pagination

```python
def get_paginated(session: Session, page: int = 1, per_page: int = 20):
    skip = (page - 1) * per_page
    statement = select(User).offset(skip).limit(per_page)
    return session.exec(statement).all()
```

---

## Subqueries

```python
subquery = (
    select(func.avg(Post.views))
    .where(Post.user_id == User.id)
    .scalar_subquery()
)

statement = select(User).where(subquery > 100)
```

---

## Query Optimization

### Select Specific Columns

```python
statement = select(User.id, User.email)
```

### Eager Loading

```python
from sqlalchemy.orm import selectinload

statement = select(User).options(selectinload(User.posts))
```

### Limit Columns

```python
statement = select(User.id, User.email).where(User.is_active == True)
```
