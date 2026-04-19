from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.config import settings   # ← This line was missing
from app.core.database import get_db
from app.services.inventory_service import InventoryService
from app.schemas.inventory import InventoryQuery, InventoryListResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/account/{account_id}", response_model=InventoryListResponse)
async def get_account_stock(
    account_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all products for a specific account"""
    if not account_id or len(account_id) < 3:
        raise HTTPException(status_code=400, detail="Invalid account_id")
    
    return await InventoryService.get_stock(db, account_id)

@router.get("/account/{account_id}/product/{product_code}", response_model=InventoryListResponse)
async def get_account_product_stock(
    account_id: str,
    product_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get specific product for a specific account"""
    if not account_id or not product_code:
        raise HTTPException(status_code=400, detail="Missing account_id or product_code")
    
    return await InventoryService.get_stock(db, account_id, product_code)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "SQLite (Local)" if "sqlite" in settings.DATABASE_URL else "Azure SQL",
        "message": "API is ready for development",
        "cache": "Redis enabled" if settings.REDIS_URL.startswith("redis://") else "No Redis (local fallback)"
    }