"""
API routes for Card operations.
Handles CRUD operations for cards within columns.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Column, Card
from app.schemas import (
    CardCreate,
    CardUpdate,
    CardMove,
    CardResponse
)

router = APIRouter(prefix="/api", tags=["cards"])


@router.post("/columns/{column_id}/cards", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(column_id: int, card_data: CardCreate, db: Session = Depends(get_db)):
    """
    Create a new card in a column.
    Position is automatically set to the end of the column.
    """
    try:
        column = db.query(Column).filter(Column.id == column_id).first()
        if not column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column with id {column_id} not found"
            )
        
        max_position = db.query(func.max(Card.position)).filter(
            Card.columnId == column_id
        ).scalar()
        
        new_position = 0 if max_position is None else max_position + 1
        
        db_card = Card(
            columnId=column_id,
            title=card_data.title,
            description=card_data.description,
            position=new_position
        )
        
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return db_card
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create card"
        )


@router.get("/cards/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    """
    Get a single card by ID.
    """
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card with id {card_id} not found"
            )
        
        return card
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch card"
        )


@router.put("/cards/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card_data: CardUpdate, db: Session = Depends(get_db)):
    """
    Update a card's title and/or description.
    Only updates fields that are provided in the request.
    """
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card with id {card_id} not found"
            )
        
        if card_data.title is not None:
            card.title = card_data.title
        
        if card_data.description is not None:
            card.description = card_data.description
        
        db.commit()
        db.refresh(card)
        return card
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update card"
        )


@router.put("/cards/{card_id}/move", response_model=CardResponse)
def move_card(card_id: int, move_data: CardMove, db: Session = Depends(get_db)):
    """
    Move a card to a different column and/or position.
    Handles drag-and-drop functionality.
    Reorders cards in both source and target columns.
    """
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card with id {card_id} not found"
            )
        
        target_column = db.query(Column).filter(Column.id == move_data.columnId).first()
        if not target_column:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target column with id {move_data.columnId} not found"
            )
        
        old_column_id = card.columnId
        old_position = card.position
        new_column_id = move_data.columnId
        new_position = move_data.position
        
        if old_column_id == new_column_id:
            if old_position == new_position:
                return card
            
            cards_in_column = db.query(Card).filter(
                Card.columnId == old_column_id,
                Card.id != card_id
            ).order_by(Card.position).all()
            
            if new_position < 0 or new_position > len(cards_in_column):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid position {new_position}"
                )
            
            if old_position < new_position:
                for c in cards_in_column:
                    if old_position < c.position <= new_position:
                        c.position -= 1
            else:
                for c in cards_in_column:
                    if new_position <= c.position < old_position:
                        c.position += 1
        else:
            cards_in_old_column = db.query(Card).filter(
                Card.columnId == old_column_id,
                Card.position > old_position
            ).all()
            
            for c in cards_in_old_column:
                c.position -= 1
            
            cards_in_new_column = db.query(Card).filter(
                Card.columnId == new_column_id,
                Card.position >= new_position
            ).all()
            
            for c in cards_in_new_column:
                c.position += 1
            
            card.columnId = new_column_id
        
        card.position = new_position
        
        db.commit()
        db.refresh(card)
        return card
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to move card"
        )


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    """
    Delete a card.
    Reorders remaining cards in the column.
    """
    try:
        card = db.query(Card).filter(Card.id == card_id).first()
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card with id {card_id} not found"
            )
        
        column_id = card.columnId
        deleted_position = card.position
        
        db.delete(card)
        
        remaining_cards = db.query(Card).filter(
            Card.columnId == column_id,
            Card.position > deleted_position
        ).all()
        
        for c in remaining_cards:
            c.position -= 1
        
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete card"
        )
