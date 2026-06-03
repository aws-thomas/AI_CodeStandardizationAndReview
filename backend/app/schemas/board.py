"""
Pydantic schemas for Board API requests and responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class BoardBase(BaseModel):
    """
    Base schema for Board with common attributes.
    """
    name: str = Field(..., min_length=1, max_length=255, description="Board name")


class BoardCreate(BoardBase):
    """
    Schema for creating a new board.
    Only requires the board name.
    """
    pass


class BoardUpdate(BaseModel):
    """
    Schema for updating a board.
    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Board name")


class BoardResponse(BoardBase):
    """
    Schema for board response.
    Includes all board fields including ID and timestamps.
    """
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class BoardWithColumnsResponse(BoardResponse):
    """
    Schema for board response with nested columns.
    Used when fetching a complete board with all its data.
    """
    columns: List["ColumnResponse"] = []

    class Config:
        from_attributes = True


from app.schemas.column import ColumnResponse
BoardWithColumnsResponse.model_rebuild()
