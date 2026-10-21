from app.models.product import ProductCreate
def test_product_model(): assert ProductCreate(sku='SKU',name='Name').sku=='SKU'
