from datetime import date
from fastapi import HTTPException
from app.database import Database

class StockService:
    def __init__(self, db: Database): self.db = db

    def create_product(self, product):
        with self.db.connection() as c:
            try:
                c.execute("INSERT INTO products(sku,name,barcode,reorder_level,unit_cost) VALUES(?,?,?,?,?)", (product.sku, product.name, product.barcode, product.reorder_level, product.unit_cost))
            except Exception as exc: raise HTTPException(409, f"Product/barcode already exists: {exc}")
        return self.product(product.sku)

    def product(self, sku):
        with self.db.connection() as c: row = c.execute("SELECT * FROM products WHERE sku=?", (sku,)).fetchone()
        if not row: raise HTTPException(404, "Product not found")
        return dict(row)

    def list_products(self):
        with self.db.connection() as c: return [dict(r) for r in c.execute("SELECT p.*, COALESCE(SUM(b.quantity),0) stock FROM products p LEFT JOIN batches b ON b.sku=p.sku GROUP BY p.sku ORDER BY p.sku")]

    def update_product(self, sku, changes):
        self.product(sku)
        values = changes.model_dump(exclude_unset=True)
        if not values:
            return self.product(sku)
        assignments = ", ".join(f"{field}=?" for field in values)
        with self.db.connection() as c:
            try:
                c.execute(f"UPDATE products SET {assignments} WHERE sku=?", (*values.values(), sku))
            except Exception as exc:
                raise HTTPException(409, f"Barcode already exists: {exc}")
        return self.product(sku)

    def receive_batch(self, batch):
        self.product(batch.sku)
        with self.db.connection() as c:
            try: c.execute("INSERT INTO batches(sku,batch_code,expiry_date,quantity,location) VALUES(?,?,?,?,?)", (batch.sku,batch.batch_code,str(batch.expiry_date),batch.quantity,batch.location))
            except Exception as exc: raise HTTPException(409, f"Batch already exists: {exc}")
            c.execute("INSERT INTO movements(sku,batch_code,quantity,movement_type,reference) VALUES(?,?,?,?,?)", (batch.sku,batch.batch_code,batch.quantity,"RECEIPT","batch-receipt"))
        return {"status":"received", "sku":batch.sku, "batch_code":batch.batch_code}

    def inventory(self):
        with self.db.connection() as c: return [dict(r) for r in c.execute("SELECT b.*,p.name,p.unit_cost,b.quantity*p.unit_cost AS value FROM batches b JOIN products p ON p.sku=b.sku ORDER BY b.expiry_date")]

    def retrieve_fefo(self, request):
        return self._retrieve_fefo(request, movement_type="RETRIEVAL", record_sale=False)

    def _retrieve_fefo(self, request, movement_type, record_sale):
        remaining, picks = request.quantity, []
        with self.db.connection() as c:
            rows = c.execute("SELECT * FROM batches WHERE sku=? AND quantity>0 AND expiry_date>=? ORDER BY expiry_date, id", (request.sku, str(date.today()))).fetchall()
            if sum(r['quantity'] for r in rows) < remaining: raise HTTPException(400, "Insufficient unexpired stock")
            for row in rows:
                take = min(remaining, row['quantity'])
                if take:
                    c.execute("UPDATE batches SET quantity=quantity-? WHERE id=?", (take,row['id']))
                    c.execute("INSERT INTO movements(sku,batch_code,quantity,movement_type,reference) VALUES(?,?,?,?,?)", (request.sku,row['batch_code'],-take,movement_type,request.reference))
                    picks.append({"batch_code":row['batch_code'],"quantity":take,"expiry_date":row['expiry_date']})
                    remaining -= take
            if record_sale:
                c.execute("INSERT INTO sales_history(sku,sale_date,quantity) VALUES(?,?,?)", (request.sku, str(date.today()), request.quantity))
        return {"status":"retrieved", "picks":picks}

    def adjust_stock(self, adjustment):
        if adjustment.quantity == 0:
            raise HTTPException(400, "Adjustment quantity cannot be zero")
        with self.db.connection() as c:
            batch = c.execute("SELECT id, quantity FROM batches WHERE sku=? AND batch_code=?", (adjustment.sku, adjustment.batch_code)).fetchone()
            if not batch:
                raise HTTPException(404, "Batch not found")
            if batch["quantity"] + adjustment.quantity < 0:
                raise HTTPException(400, "Adjustment would make stock negative")
            c.execute("UPDATE batches SET quantity=quantity+? WHERE id=?", (adjustment.quantity, batch["id"]))
            c.execute("INSERT INTO movements(sku,batch_code,quantity,movement_type,reference) VALUES(?,?,?,?,?)", (adjustment.sku, adjustment.batch_code, adjustment.quantity, "ADJUSTMENT", adjustment.reason))
        return {"status": "adjusted", "sku": adjustment.sku, "batch_code": adjustment.batch_code, "quantity_change": adjustment.quantity}

    def movements(self):
        with self.db.connection() as c: return [dict(r) for r in c.execute("SELECT * FROM movements ORDER BY id DESC")]
