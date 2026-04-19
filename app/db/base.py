# This file is no longer needed for Base definition
# We can delete it or keep it empty for now

from app.core.database import Base
from app.models.inventory import Inventory

# Just to make sure all models are imported when creating tables
__all__ = ["Base", "Inventory"]