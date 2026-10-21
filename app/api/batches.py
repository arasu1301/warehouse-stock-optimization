from fastapi import APIRouter
from app.models.batch import BatchCreate
router=APIRouter(prefix="/batches",tags=["Batches"])
def register(service):
    @router.post("",status_code=201)
    def receive(batch:BatchCreate): return service.receive_batch(batch)
    @router.get("")
    def list_all(sku:str|None=None): return service.list_batches(sku)
    return router
