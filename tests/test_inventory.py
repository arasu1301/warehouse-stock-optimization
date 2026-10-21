from datetime import date, timedelta
from app.database.database import Database
from app.services.stock_service import StockService
from app.models.product import ProductCreate
from app.models.batch import BatchCreate
from app.models.stock import RetrievalRequest

def test_fefo_retrieves_earliest_batch(tmp_path):
    db=Database(tmp_path/'test.db'); db.initialize(); service=StockService(db)
    service.create_product(ProductCreate(sku='A',name='Apple'))
    service.receive_batch(BatchCreate(sku='A',batch_code='late',expiry_date=date.today()+timedelta(days=20),quantity=5))
    service.receive_batch(BatchCreate(sku='A',batch_code='early',expiry_date=date.today()+timedelta(days=10),quantity=5))
    assert service.retrieve_fefo(RetrievalRequest(sku='A',quantity=4))['picks'][0]['batch_code']=='early'
