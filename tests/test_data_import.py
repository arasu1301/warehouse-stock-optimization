from app.database.database import Database
from app.services.data_import_service import DataImportService


def test_import_and_safe_repeat(tmp_path):
    source = tmp_path / "history.csv"
    source.write_text("date,product_id,product_name,category,quantity_sold,unit_price,total_sales\n2025-01-01,P1,Item,A,4,10,40\n")
    db = Database(tmp_path / "warehouse.db")
    db.initialize()
    service = DataImportService(db)
    assert service.import_historical_sales(source)["sales_rows"] == 1
    assert service.import_historical_sales(source)["status"] == "skipped"
    assert service.import_historical_sales(source, replace_existing=True)["status"] == "imported"
