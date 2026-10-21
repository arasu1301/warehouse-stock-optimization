from datetime import date, timedelta
from app.config import EXPIRY_ALERT_DAYS
class AlertService:
    def __init__(self, db): self.db=db
    def all(self):
        horizon=str(date.today()+timedelta(days=EXPIRY_ALERT_DAYS))
        with self.db.connection() as c:
            low=[dict(r) for r in c.execute("SELECT p.sku,p.name,p.reorder_level,COALESCE(SUM(b.quantity),0) stock FROM products p LEFT JOIN batches b ON b.sku=p.sku GROUP BY p.sku HAVING stock<=p.reorder_level")]
            expiry=[dict(r) for r in c.execute("SELECT sku,batch_code,expiry_date,quantity FROM batches WHERE quantity>0 AND expiry_date<=? ORDER BY expiry_date",(horizon,))]
        return {"low_stock":low,"expiring_soon":expiry}
