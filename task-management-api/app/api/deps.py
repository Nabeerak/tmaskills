"""
Shared dependencies for API endpoints.
"""
from typing import Annotated
from fastapi import Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.core.config import settings


# Type alias for database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]


class CommonQueryParams:
    """
    Reusable pagination query parameters.

    Usage:
        @app.get("/items")
        async def get_items(commons: Annotated[CommonQueryParams, Depends()]):
            skip = commons.skip
            limit = commons.limit
    """
    def __init__(
        self,
        skip: int = Query(default=settings.DEFAULT_SKIP, ge=0, description="Number of records to skip"),
        limit: int = Query(default=settings.DEFAULT_LIMIT, ge=1, le=settings.MAX_LIMIT, description="Maximum number of records to return")
    ):
        self.skip = skip
        self.limit = limit


# Type alias for pagination dependency
PaginationDep = Annotated[CommonQueryParams, Depends()]
