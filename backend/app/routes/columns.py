"""
API routes for Column operations.
Handles CRUD operations for board columns.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Board, Column, Card
from app.schemas import (
    ColumnCreate,
    ColumnUpdate,
    ColumnPositionUpdate,
    ColumnResponse,
    ColumnWithCardsResponse
)

router = APIRouter(prefix="/api", tags=["columns"])


@router.post("/boards/{board_id}/columns", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
def create_column(board_id: int, column_data: ColumnCreate, db: Session = Depends(get_db)):
    """
    Create a new column in a board.
    Position is automatically set to the end of the board.
    """
    try:
        board = db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Board with id {board_id} not found"
            )
        
        max_position = db.query(func.max(Column.position)).filter(
            Column.boardId == board_id
        ).scalar()
        
        new_position = 0 if max_position is None else max_position + 1
        
        db_column = Column(
            boardId=board_id,
            name=column_data.name,
            position=new_position
        )
        
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return db_column
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create column"
        )


@router.get("/columns/{column_id}", response_model=ColumnWithCardsResponse)
def get_column(column_id: int, db: Session = Depends(get_db)):
    """
    Get a single column with all its cards.
    """
    try:
        column = db.query(Column).filter(Column.id == column_id).first()
        
        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column with id {column_id} not found"
            )
        
        return column
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch column"
        )


@router.put("/columns/{column_id}", response_model=ColumnResponse)
def update_column(column_id: int, column_data: ColumnUpdate, db: Session = Depends(get_db)):
    """
    Update a column's name.
    Only updates fields that are provided in the request.
    """
    try:
        column = db.query(Column).filter(Column.id == column_id).first()
        
        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column with id {column_id} not found"
            )
        
        if column_data.name is not None:
            column.name = column_data.name
        
        db.commit()
        db.refresh(column)
        return column
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update column"
        )


@router.put("/columns/{column_id}/position", response_model=ColumnResponse)
def update_column_position(column_id: int, position_data: ColumnPositionUpdate, db: Session = Depends(get_db)):
    """
    Update a column's position within its board.
    Reorders other columns accordingly.
    """
    try:
        column = db.query(Column).filter(Column.id == column_id).first()
        
        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column with id {column_id} not found"
            )
        
        old_position = column.position
        new_position = position_data.position
        
        if old_position == new_position:
            return column
        
        columns_in_board = db.query(Column).filter(
            Column.boardId == column.boardId,
            Column.id != column_id
        ).order_by(Column.position).all()
        
        if new_position < 0 or new_position > len(columns_in_board):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid position {new_position}"
            )
        
        if old_position < new_position:
            for col in columns_in_board:
                if old_position < col.position <= new_position:
                    col.position -= 1
        else:
            for col in columns_in_board:
                if new_position <= col.position < old_position:
                    col.position += 1
        
        column.position = new_position
        
        db.commit()
        db.refresh(column)
        return column
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update column position"
        )


@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(column_id: int, db: Session = Depends(get_db)):
    """
    Delete a column.
    Cascades to delete all cards in the column.
    Reorders remaining columns.
    """
    try:
        column = db.query(Column).filter(Column.id == column_id).first()
        
        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column with id {column_id} not found"
            )
        
        board_id = column.boardId
        deleted_position = column.position
        
        db.delete(column)
        
        remaining_columns = db.query(Column).filter(
            Column.boardId == board_id,
            Column.position > deleted_position
        ).all()
        
        for col in remaining_columns:
            col.position -= 1
        
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete column"
        )
