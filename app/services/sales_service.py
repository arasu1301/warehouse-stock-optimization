from datetime import date
from app.services.stock_service import StockService
class SalesService(StockService):
    def dispatch_sale(self, request):
        return self._retrieve_fefo(request, movement_type="SALE", record_sale=True)
