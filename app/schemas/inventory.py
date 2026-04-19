from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InventoryBase(BaseModel):
    account_id: str
    product_code: str
    product_name: Optional[str] = None
    quantity: float = 0.0
    unit_price: float = 0.0
    total_value: float = 0.0
    warehouse: Optional[str] = None
    location: Optional[str] = None
    batch_no: Optional[str] = None
    expiry_date: Optional[str] = None
    status: str = "ACTIVE"

class InventoryResponse(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryQuery(BaseModel):
    account_id: str
    product_code: Optional[str] = None   # If None → return all products for that account

class InventoryListResponse(BaseModel):
    total: int
    records: List[InventoryResponse]