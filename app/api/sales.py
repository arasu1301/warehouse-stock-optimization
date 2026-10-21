from fastapi import APIRouter
from app.models.stock import RetrievalRequest

router = APIRouter(prefix="/sales", tags=["Sales"])


def register(service):
    @router.post("/dispatch")
    def dispatch(request: RetrievalRequest):
        """Dispatch through FEFO and write the sale to AI history atomically."""
        return service.dispatch_sale(request)
    return router
