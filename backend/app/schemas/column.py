"""
Pydantic schemas for Column API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ColumnBase(BaseModel):
    """
    Base schema for Column with common attributes.
    """
    name: str = Field(..., min_length=1, max_length=255, description="Column name")


class ColumnCreate(ColumnBase):
    """
    Schema for creating a new column.
    Position will be auto-assigned to the end of the board.
    """
    pass


class ColumnUpdate(BaseModel):
    """
    Schema for updating a column.
    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Column name")


class ColumnPositionUpdate(BaseModel):
    """
    Schema for updating column position.
    Used for reordering columns within a board.
    """
    position: int = Field(..., ge=0, description="New position (0-indexed)")


class ColumnResponse(ColumnBase):
    """
    Schema for column response.
    Includes all column fields including ID, position, and timestamps.
    """
    id: int
    boardId: int
    position: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ColumnWithCardsResponse(ColumnResponse):
    """
    Schema for column response with nested cards.
    Used when fetching a complete column with all its cards.
    """
    cards: List["CardResponse"] = []

    class Config:
        from_attributes = True


from app.schemas.card import CardResponse
ColumnWithCardsResponse.model_rebuild()
