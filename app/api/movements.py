from fastapi import APIRouter
router=APIRouter(prefix="/movements",tags=["Movements"])
def register(service):
    @router.get("")
    def list_all(): return service.movements()
    return router
