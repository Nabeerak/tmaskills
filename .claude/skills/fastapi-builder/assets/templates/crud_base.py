"""
Generic CRUD base class for database operations.

Provides reusable create, read, update, delete operations for any SQLModel.

Usage:
    from app.crud.base import CRUDBase
    from app.models.task import Task
    from app.schemas.task import TaskCreate, TaskUpdate

    class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
        # Add custom methods here
        def get_by_user(self, session: Session, user_id: int):
            return session.exec(
                select(Task).where(Task.user_id == user_id)
            ).all()

    crud_task = CRUDTask(Task)
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlmodel import SQLModel, Session, select
from pydantic import BaseModel

# Type variables for generic CRUD
ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD operations for SQLModel.

    Type Parameters:
        ModelType: SQLModel database model
        CreateSchemaType: Pydantic schema for creating items
        UpdateSchemaType: Pydantic schema for updating items
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD with model class.

        Args:
            model: SQLModel class (e.g., Task, User)
        """
        self.model = model

    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        """
        Get single item by ID.

        Args:
            session: Database session
            id: Item ID

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
        Get multiple items with pagination.

        Args:
            session: Database session
            skip: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of model instances
        """
        statement = select(self.model).offset(skip).limit(limit)
        return list(session.exec(statement).all())

    def create(self, session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create new item.

        Args:
            session: Database session
            obj_in: Create schema with item data

        Returns:
            Created model instance
        """
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        session: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """
        Update item.

        Args:
            session: Database session
            db_obj: Existing database object
            obj_in: Update schema or dict with updated data

        Returns:
            Updated model instance
        """
        # Convert to dict if needed
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Update fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, *, id: Any) -> ModelType:
        """
        Delete item by ID.

        Args:
            session: Database session
            id: Item ID

        Returns:
            Deleted model instance
        """
        obj = session.get(self.model, id)
        if obj:
            session.delete(obj)
            session.commit()
        return obj

    def count(self, session: Session) -> int:
        """
        Count total items.

        Args:
            session: Database session

        Returns:
            Total number of items
        """
        from sqlalchemy import func
        statement = select(func.count()).select_from(self.model)
        return session.exec(statement).one()

    def exists(self, session: Session, *, id: Any) -> bool:
        """
        Check if item exists.

        Args:
            session: Database session
            id: Item ID

        Returns:
            True if exists, False otherwise
        """
        return self.get(session, id) is not None


# Example: Specific CRUD class
"""
from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_by_user(
        self,
        session: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

    def get_by_status(
        self,
        session: Session,
        *,
        status: str
    ) -> List[Task]:
        statement = select(Task).where(Task.status == status)
        return list(session.exec(statement).all())

    def search(
        self,
        session: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        from sqlmodel import col
        statement = (
            select(Task)
            .where(col(Task.title).contains(query))
            .offset(skip)
            .limit(limit)
        )
        return list(session.exec(statement).all())

# Create instance
crud_task = CRUDTask(Task)

# Usage in endpoints
@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    tasks = crud_task.get_multi(session, skip=skip, limit=limit)
    return tasks

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session)
):
    task = crud_task.create(session, obj_in=task_in)
    return task
"""
