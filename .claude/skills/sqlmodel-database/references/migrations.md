# Database Migrations with Alembic

## Table of Contents

- [Alembic Setup](#alembic-setup)
- [Configuration](#configuration)
- [Creating Migrations](#creating-migrations)
- [Applying Migrations](#applying-migrations)
- [Rollback](#rollback)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)

---

## Alembic Setup

### Installation

```bash
pip install alembic
```

### Initialize Alembic

```bash
alembic init migrations
```

Creates:
```
migrations/
├── versions/       # Migration files
├── env.py          # Alembic configuration
├── script.py.mako  # Migration template
└── README
alembic.ini         # Alembic settings
```

---

## Configuration

### Configure env.py

```python
# migrations/env.py
from sqlmodel import SQLModel
from app.models import User, Post, Product  # Import ALL models

target_metadata = SQLModel.metadata

# For async (if using async SQLModel)
import asyncio
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# ... rest of configuration
```

### Configure alembic.ini

```ini
[alembic]
script_location = migrations
sqlalchemy.url = sqlite:///./app.db

# For production
# sqlalchemy.url = postgresql://user:pass@localhost/dbname
```

---

## Creating Migrations

### Auto-generate Migration

```bash
alembic revision --autogenerate -m "Add user and post tables"
```

Creates file in `migrations/versions/`:
```python
def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('user')
```

### Manual Migration

```bash
alembic revision -m "Add index to email"
```

Edit generated file:
```python
def upgrade():
    op.create_index('ix_user_email', 'user', ['email'])

def downgrade():
    op.drop_index('ix_user_email', 'user')
```

---

## Applying Migrations

### Apply All Pending

```bash
alembic upgrade head
```

### Apply Specific Revision

```bash
alembic upgrade abc123
```

### Apply Next Migration

```bash
alembic upgrade +1
```

---

## Rollback

### Rollback One Migration

```bash
alembic downgrade -1
```

### Rollback to Specific Revision

```bash
alembic downgrade abc123
```

### Rollback All

```bash
alembic downgrade base
```

---

## Best Practices

1. **Review auto-generated migrations** before applying
2. **Test on development database** first
3. **Make migrations reversible** (implement downgrade)
4. **Keep migrations small** and focused
5. **Don't edit applied migrations** - create new ones
6. **Commit migrations** to version control
7. **Use meaningful names** for migrations
8. **Handle data migrations** separately if complex
9. **Test rollback** before production deployment
10. **Backup database** before migrating production

---

## Common Issues

### SQLModel Type Mapping

Add to migrations/env.py:
```python
import sqlmodel.sql.sqltypes

from alembic import context
context.configure(
    use_module_prefix=True,  # Add this
    # ... other config
)
```

### Naming Conventions

```python
# migrations/env.py
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

target_metadata = SQLModel.metadata
target_metadata.naming_convention = naming_convention
```

### Data Migrations

```python
def upgrade():
    # Schema change
    op.add_column('user', sa.Column('status', sa.String()))

    # Data migration
    from sqlalchemy import table, column
    user_table = table('user', column('status'))

    op.execute(
        user_table.update().values(status='active')
    )
```
