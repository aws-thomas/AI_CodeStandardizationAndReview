"""
Board model for myKB Kanban application.
Represents a Kanban board that contains multiple columns.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Board(Base):
    """
    Board model representing a Kanban board.
    
    Attributes:
        id: Primary key
        name: Board name
        createdAt: Timestamp when board was created
        updatedAt: Timestamp when board was last updated
        columns: Relationship to Column model (one-to-many)
    """
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan", order_by="Column.position")
