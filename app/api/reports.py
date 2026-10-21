from fastapi import APIRouter
router=APIRouter(prefix="/reports",tags=["Reports"])
def register(stock_service):
    @router.get("/inventory")
    def inventory_report():
        rows=stock_service.inventory()
        return {"items":rows,"total_units":sum(r['quantity'] for r in rows),"total_value":round(sum(r['value'] for r in rows),2)}
    return router
