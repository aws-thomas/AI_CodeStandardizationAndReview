"""
Main FastAPI application entry point for myKB Kanban board.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Board, Column, Card
from app.routes import boards_router, columns_router, cards_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="myKB API",
    description="Backend API for myKB Kanban board application",
    version="0.1.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(boards_router)
app.include_router(columns_router)
app.include_router(cards_router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint - health check.
    Returns basic API information.
    """
    return {
        "message": "myKB API is running",
        "version": "0.1.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring.
    """
    return {"status": "ok"}
