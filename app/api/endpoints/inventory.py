from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services.inventory_service import InventoryService
from app.schemas.inventory import InventoryListResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/account/{account_id}", response_model=InventoryListResponse)
async def get_account_stock(
    account_id: str,
    db: Session = Depends(get_db)
):
    """Get all products for a specific account"""
    if not account_id or len(account_id) < 3:
        raise HTTPException(status_code=400, detail="Invalid account_id")
    
    return InventoryService.get_stock(db, account_id)

@router.get("/account/{account_id}/product/{product_code}", response_model=InventoryListResponse)
async def get_account_product_stock(
    account_id: str,
    product_code: str,
    db: Session = Depends(get_db)
):
    """Get specific product for a specific account"""
    if not account_id or not product_code:
        raise HTTPException(status_code=400, detail="Missing account_id or product_code")
    
    return InventoryService.get_stock(db, account_id, product_code)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "Azure SQL",
        "message": "API is ready for development",
        "cache": "Redis enabled" if "redis" in settings.REDIS_URL else "No Redis (fallback)"
    }