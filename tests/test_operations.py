from datetime import date, timedelta
from app.database.database import Database
from app.models.batch import BatchCreate
from app.models.product import ProductCreate
from app.models.stock import RetrievalRequest, StockAdjustment
from app.services.sales_service import SalesService


def test_sale_updates_stock_movement_and_history(tmp_path):
    db = Database(tmp_path / "warehouse.db")
    db.initialize()
    service = SalesService(db)
    service.create_product(ProductCreate(sku="S1", name="Item"))
    service.receive_batch(BatchCreate(sku="S1", batch_code="B1", expiry_date=date.today()+timedelta(days=30), quantity=8))
    service.dispatch_sale(RetrievalRequest(sku="S1", quantity=3))
    with db.connection() as connection:
        assert connection.execute("SELECT quantity FROM batches").fetchone()[0] == 5
        assert connection.execute("SELECT COUNT(*) FROM sales_history").fetchone()[0] == 1
        assert connection.execute("SELECT movement_type FROM movements ORDER BY id DESC").fetchone()[0] == "SALE"


def test_adjustment_cannot_create_negative_stock(tmp_path):
    db = Database(tmp_path / "warehouse.db")
    db.initialize()
    service = SalesService(db)
    service.create_product(ProductCreate(sku="S1", name="Item"))
    service.receive_batch(BatchCreate(sku="S1", batch_code="B1", expiry_date=date.today()+timedelta(days=30), quantity=1))
    try:
        service.adjust_stock(StockAdjustment(sku="S1", batch_code="B1", quantity=-2))
        assert False, "Expected negative stock protection"
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
