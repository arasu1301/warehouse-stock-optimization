from fastapi import APIRouter, Query

router = APIRouter(prefix="/data", tags=["Data import"])


def register(import_service, csv_path):
    @router.post("/import-historical-sales")
    def import_historical_sales(replace_existing: bool = Query(default=False)):
        """Import CSV once. Set replace_existing=true only to replace prior imported sales records."""
        return import_service.import_historical_sales(csv_path, replace_existing)
    return router
