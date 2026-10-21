from app.services.stock_service import StockService
class BatchService(StockService):
    def list_batches(self, sku=None):
        with self.db.connection() as c:
            q="SELECT * FROM batches" + (" WHERE sku=?" if sku else "") + " ORDER BY expiry_date"
            return [dict(r) for r in c.execute(q, (sku,) if sku else ())]
