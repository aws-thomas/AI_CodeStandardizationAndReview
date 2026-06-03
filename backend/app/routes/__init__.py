"""
API routes package for myKB.
"""
from app.routes.boards import router as boards_router
from app.routes.columns import router as columns_router
from app.routes.cards import router as cards_router

__all__ = ["boards_router", "columns_router", "cards_router"]
