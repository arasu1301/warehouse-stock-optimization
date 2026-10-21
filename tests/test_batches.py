from app.models.batch import BatchCreate
def test_batch_model(): assert BatchCreate(sku='S',batch_code='B',expiry_date='2030-01-01',quantity=1).quantity==1
