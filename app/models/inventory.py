from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.core.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(50), index=True, nullable=False)
    product_code = Column(String(50), index=True, nullable=False)
    product_name = Column(String(200))
    quantity = Column(Float, default=0.0)
    unit_price = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    warehouse = Column(String(50))
    location = Column(String(100))
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    batch_no = Column(String(50))
    expiry_date = Column(String(50))
    status = Column(String(20), default="ACTIVE")
    separator_used = Column(String(10), default="|")

    # Correct way to define indexes in SQLAlchemy 2.0
    __table_args__ = (
        Index('ix_inventory_account_product', 'account_id', 'product_code'),
        Index('ix_inventory_account', 'account_id'),
        Index('ix_inventory_product', 'product_code'),
    )