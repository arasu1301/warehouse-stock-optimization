from fastapi import APIRouter
router=APIRouter(prefix="/alerts",tags=["Alerts"])
def register(service):
    @router.get("")
    def list_all(): return service.all()
    return router
