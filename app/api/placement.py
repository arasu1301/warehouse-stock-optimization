from fastapi import APIRouter
from app.models.stock import PlacementRequest

router = APIRouter(prefix="/placement", tags=["Warehouse placement"])


def register(service):
    @router.post("")
    def place(request: PlacementRequest):
        return service.move(request.sku, request.batch_code, request.location)
    return router
