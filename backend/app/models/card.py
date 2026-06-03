"""
Card model for myKB Kanban application.
Represents a card within a column.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Card(Base):
    """
    Card model representing a task card in a Kanban column.
    
    Attributes:
        id: Primary key
        columnId: Foreign key to Column
        title: Card title
        description: Card description (optional, can be empty)
        position: Order position within the column (0-indexed)
        createdAt: Timestamp when card was created
        updatedAt: Timestamp when card was last updated
        column: Relationship to Column model (many-to-one)
    """
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    columnId = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="")
    position = Column(Integer, nullable=False, default=0)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    column = relationship("Column", back_populates="cards")
