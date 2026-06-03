"""
API routes for Board operations.
Handles CRUD operations for Kanban boards.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Board, Column, Card
from app.schemas import (
    BoardCreate,
    BoardUpdate,
    BoardResponse,
    BoardWithColumnsResponse
)

router = APIRouter(prefix="/api/boards", tags=["boards"])


@router.get("", response_model=List[BoardResponse])
def get_all_boards(db: Session = Depends(get_db)):
    """
    Get all boards.
    Returns a list of all boards without their columns.
    """
    try:
        boards = db.query(Board).order_by(Board.createdAt.desc()).all()
        return boards
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch boards"
        )


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(board_data: BoardCreate, db: Session = Depends(get_db)):
    """
    Create a new board.
    Requires a board name in the request body.
    """
    try:
        db_board = Board(name=board_data.name)
        db.add(db_board)
        db.commit()
        db.refresh(db_board)
        return db_board
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create board"
        )


@router.get("/{board_id}", response_model=BoardWithColumnsResponse)
def get_board(board_id: int, db: Session = Depends(get_db)):
    """
    Get a single board with all its columns and cards.
    Returns complete board data including nested columns and cards.
    """
    try:
        board = db.query(Board).options(
            joinedload(Board.columns).joinedload(Column.cards)
        ).filter(Board.id == board_id).first()
        
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Board with id {board_id} not found"
            )
        
        return board
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch board"
        )


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(board_id: int, board_data: BoardUpdate, db: Session = Depends(get_db)):
    """
    Update a board's name.
    Only updates fields that are provided in the request.
    """
    try:
        board = db.query(Board).filter(Board.id == board_id).first()
        
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Board with id {board_id} not found"
            )
        
        if board_data.name is not None:
            board.name = board_data.name
        
        db.commit()
        db.refresh(board)
        return board
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update board"
        )


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(board_id: int, db: Session = Depends(get_db)):
    """
    Delete a board.
    Cascades to delete all columns and cards in the board.
    """
    try:
        board = db.query(Board).filter(Board.id == board_id).first()
        
        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Board with id {board_id} not found"
            )
        
        db.delete(board)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete board"
        )
