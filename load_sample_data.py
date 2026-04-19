import asyncio
from sqlalchemy import text
from app.core.database import engine, AsyncSessionLocal
from app.core.config import settings
import random
import string
from datetime import datetime

async def load_sample_data(num_records: int = 15000):
    print(f"🚀 Loading {num_records:,} sample inventory records...")

    async with AsyncSessionLocal() as session:
        # Clear existing data
        await session.execute(text("DELETE FROM inventory"))
        await session.commit()

        accounts = [f"ACC{str(i).zfill(6)}" for i in range(1, 501)]
        products = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"]
        warehouses = ["WH01", "WH02", "WH03", "WH04"]
        locations = ["MUMBAI", "DELHI", "BANGALORE", "KOLKATA", "CHENNAI"]

        for i in range(num_records):
            account_id = random.choice(accounts)
            product_code = random.choice(products)
            quantity = random.randint(50, 5000)
            unit_price = round(random.uniform(100, 4500), 2)
            total_value = round(quantity * unit_price, 2)

            batch_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            record = {
                "account_id": account_id,
                "product_code": product_code,
                "product_name": f"{product_code} - Equity",
                "quantity": quantity,
                "unit_price": unit_price,
                "total_value": total_value,
                "warehouse": random.choice(warehouses),
                "location": random.choice(locations),
                "batch_no": batch_no,
                "expiry_date": "2027-12-31" if random.random() > 0.4 else "N/A",
                "status": random.choice(["ACTIVE", "INACTIVE"]),
                "separator_used": settings.FILE_SEPARATOR
            }

            await session.execute(
                text("""
                    INSERT INTO inventory 
                    (account_id, product_code, product_name, quantity, unit_price, total_value, 
                     warehouse, location, batch_no, expiry_date, status, separator_used)
                    VALUES 
                    (:account_id, :product_code, :product_name, :quantity, :unit_price, :total_value, 
                     :warehouse, :location, :batch_no, :expiry_date, :status, :separator_used)
                """),
                record
            )

            if (i + 1) % 5000 == 0:
                await session.commit()
                print(f"✅ Loaded {i+1:,} records...")

        await session.commit()

    print(f"🎉 Successfully loaded {num_records:,} sample records into SQLite!")

if __name__ == "__main__":
    asyncio.run(load_sample_data(15000))   # Change number as needed