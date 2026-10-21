from fastapi import APIRouter
from app.models.stock import RetrievalRequest, StockAdjustment
router=APIRouter(prefix="/inventory",tags=["Inventory"])
def register(service):
    @router.get("")
    def list_inventory(): return service.inventory()
    @router.post("/retrieve")
    def retrieve(request:RetrievalRequest): return service.retrieve_fefo(request)
    @router.post("/adjust")
    def adjust(adjustment: StockAdjustment): return service.adjust_stock(adjustment)
    return router
