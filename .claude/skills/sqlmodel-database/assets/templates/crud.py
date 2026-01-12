"""
CRUD operations for SQLModel models.

This template demonstrates:
- Generic CRUD functions
- Type-safe operations
- Error handling patterns
- Pagination support
- Filtering and searching
- Eager loading relationships
"""

from sqlmodel import Session, select, func
from typing import TypeVar, Generic, Type, Optional, List, Any
from datetime import datetime

# Generic type for SQLModel models
ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """
    Base class for CRUD operations.

    Usage:
        user_crud = CRUDBase(User)
        user = user_crud.get(session, id=1)
    """

    def __init__(self, model: Type[ModelType]):
        """Initialize with model class."""
        self.model = model

    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        return session.get(self.model, id)

    def get_multi(
        self,
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        statement = select(self.model).offset(skip).limit(limit)
        return list(session.exec(statement).all())

    def get_by_field(
        self,
        session: Session,
        field_name: str,
        field_value: Any
    ) -> Optional[ModelType]:
        """
        Get a single record by field value.

        Args:
            session: Database session
            field_name: Name of the field to filter by
            field_value: Value to match

        Returns:
            Model instance or None if not found
        """
        field = getattr(self.model, field_name)
        statement = select(self.model).where(field == field_value)
        return session.exec(statement).first()

    def get_multi_by_field(
        self,
        session: Session,
        field_name: str,
        field_value: Any,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records by field value.

        Args:
            session: Database session
            field_name: Name of the field to filter by
            field_value: Value to match
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        field = getattr(self.model, field_name)
        statement = (
            select(self.model)
            .where(field == field_value)
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def create(self, session: Session, *, obj_in: dict) -> ModelType:
        """
        Create a new record.

        Args:
            session: Database session
            obj_in: Dictionary of field values

        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        session: Session,
        *,
        db_obj: ModelType,
        obj_in: dict
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            session: Database session
            db_obj: Existing model instance
            obj_in: Dictionary of field values to update

        Returns:
            Updated model instance
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # Update timestamp if model has updated_at field
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.utcnow())

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, *, id: Any) -> Optional[ModelType]:
        """
        Delete a record by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            Deleted model instance or None if not found
        """
        obj = session.get(self.model, id)
        if obj:
            session.delete(obj)
            session.commit()
        return obj

    def count(self, session: Session) -> int:
        """
        Count total records.

        Args:
            session: Database session

        Returns:
            Total number of records
        """
        statement = select(func.count()).select_from(self.model)
        return session.exec(statement).one()

    def exists(self, session: Session, id: Any) -> bool:
        """
        Check if a record exists by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            True if record exists, False otherwise
        """
        return self.get(session, id) is not None


# Example: User CRUD operations
from models import User, Post


class CRUDUser(CRUDBase[User]):
    """User-specific CRUD operations."""

    def get_by_email(self, session: Session, *, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    def get_by_username(self, session: Session, *, username: str) -> Optional[User]:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    def get_active_users(
        self,
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get all active users."""
        statement = (
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def search_by_name(
        self,
        session: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Search users by full name."""
        statement = (
            select(User)
            .where(User.full_name.like(f"%{query}%"))
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())


class CRUDPost(CRUDBase[Post]):
    """Post-specific CRUD operations."""

    def get_by_slug(self, session: Session, *, slug: str) -> Optional[Post]:
        """Get post by slug."""
        statement = select(Post).where(Post.slug == slug)
        return session.exec(statement).first()

    def get_published_posts(
        self,
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get all published posts."""
        statement = (
            select(Post)
            .where(Post.is_published == True)
            .order_by(Post.published_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def get_user_posts(
        self,
        session: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get all posts by a user."""
        statement = (
            select(Post)
            .where(Post.user_id == user_id)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def increment_views(self, session: Session, *, post_id: int) -> Optional[Post]:
        """Increment post view count."""
        post = self.get(session, post_id)
        if post:
            post.views += 1
            session.add(post)
            session.commit()
            session.refresh(post)
        return post


# Create CRUD instances
user_crud = CRUDUser(User)
post_crud = CRUDPost(Post)


# Example usage
def example_usage():
    """Example of using CRUD operations."""
    from database import engine, Session

    with Session(engine) as session:
        # Create user
        user_data = {
            "email": "alice@example.com",
            "username": "alice",
            "full_name": "Alice Smith"
        }
        user = user_crud.create(session, obj_in=user_data)
        print(f"Created user: {user}")

        # Get user by email
        user = user_crud.get_by_email(session, email="alice@example.com")
        print(f"Found user: {user}")

        # Update user
        update_data = {"full_name": "Alice Johnson"}
        user = user_crud.update(session, db_obj=user, obj_in=update_data)
        print(f"Updated user: {user}")

        # Get all active users
        active_users = user_crud.get_active_users(session, skip=0, limit=10)
        print(f"Active users: {len(active_users)}")

        # Count total users
        total = user_crud.count(session)
        print(f"Total users: {total}")


if __name__ == "__main__":
    example_usage()
