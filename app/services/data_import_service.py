"""Import external historical sales data into the normalized warehouse schema."""
import csv
from datetime import date
from pathlib import Path
from fastapi import HTTPException


class DataImportService:
    REQUIRED_COLUMNS = {"date", "product_id", "product_name", "quantity_sold", "unit_price"}

    def __init__(self, db):
        self.db = db

    def import_historical_sales(self, path: Path, replace_existing: bool = False):
        if not path.exists():
            raise HTTPException(404, f"Sales file not found: {path.name}")
        with path.open("r", newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            if not reader.fieldnames or not self.REQUIRED_COLUMNS.issubset(reader.fieldnames):
                raise HTTPException(400, "CSV must contain date, product_id, product_name, quantity_sold and unit_price")
            rows = list(reader)

        imported = 0
        with self.db.connection() as connection:
            existing = connection.execute("SELECT COUNT(*) FROM sales_history").fetchone()[0]
            if existing and not replace_existing:
                return {"status": "skipped", "reason": "sales history already imported", "sales_rows": existing}
            if replace_existing:
                connection.execute("DELETE FROM sales_history")
            for row in rows:
                try:
                    quantity = int(float(row["quantity_sold"]))
                    unit_cost = float(row["unit_price"])
                    date.fromisoformat(row["date"].strip())
                    if quantity < 0:
                        continue
                except (TypeError, ValueError):
                    continue
                sku = row["product_id"].strip()
                connection.execute(
                    "INSERT OR IGNORE INTO products(sku,name,reorder_level,unit_cost) VALUES(?,?,?,?)",
                    (sku, row["product_name"].strip(), 0, unit_cost),
                )
                connection.execute(
                    "INSERT INTO sales_history(sku,sale_date,quantity) VALUES(?,?,?)",
                    (sku, row["date"].strip(), quantity),
                )
                imported += 1
        return {"status": "imported", "sales_rows": imported, "products_available": len({r['product_id'] for r in rows})}
