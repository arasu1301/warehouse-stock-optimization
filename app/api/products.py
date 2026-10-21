from fastapi import APIRouter
from app.models.product import ProductCreate, ProductUpdate
router=APIRouter(prefix="/products",tags=["Products"])
def register(service):
    @router.post("",status_code=201)
    def create(product:ProductCreate): return service.create_product(product)
    @router.get("")
    def list_all(): return service.list_products()
    @router.get("/{sku}")
    def get_one(sku: str): return service.product(sku)
    @router.put("/{sku}")
    def update(sku: str, product: ProductUpdate): return service.update_product(sku, product)
    return router
