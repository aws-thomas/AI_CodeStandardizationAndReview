"""
Pydantic schemas for Card API requests and responses.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CardBase(BaseModel):
    """
    Base schema for Card with common attributes.
    """
    title: str = Field(..., min_length=1, max_length=255, description="Card title")
    description: str = Field(default="", description="Card description")


class CardCreate(CardBase):
    """
    Schema for creating a new card.
    Position will be auto-assigned to the end of the column.
    """
    pass


class CardUpdate(BaseModel):
    """
    Schema for updating a card.
    All fields are optional.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Card title")
    description: Optional[str] = Field(None, description="Card description")


class CardMove(BaseModel):
    """
    Schema for moving a card to a different column or position.
    Used for drag-and-drop functionality.
    """
    columnId: int = Field(..., description="Target column ID")
    position: int = Field(..., ge=0, description="Target position (0-indexed)")


class CardResponse(CardBase):
    """
    Schema for card response.
    Includes all card fields including ID, column ID, position, and timestamps.
    """
    id: int
    columnId: int
    position: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
