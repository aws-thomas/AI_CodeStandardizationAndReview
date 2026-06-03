"""
Column model for myKB Kanban application.
Represents a column within a board that contains cards.
"""
from sqlalchemy import Column as SQLColumn, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Column(Base):
    """
    Column model representing a column in a Kanban board.
    
    Attributes:
        id: Primary key
        boardId: Foreign key to Board
        name: Column name (e.g., "To Do", "In Progress", "Done")
        position: Order position within the board (0-indexed)
        createdAt: Timestamp when column was created
        updatedAt: Timestamp when column was last updated
        board: Relationship to Board model (many-to-one)
        cards: Relationship to Card model (one-to-many)
    """
    __tablename__ = "columns"

    id = SQLColumn(Integer, primary_key=True, index=True)
    boardId = SQLColumn(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    name = SQLColumn(String, nullable=False)
    position = SQLColumn(Integer, nullable=False, default=0)
    createdAt = SQLColumn(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = SQLColumn(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan", order_by="Card.position")
