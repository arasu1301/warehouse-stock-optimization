from app.services.stock_service import StockService
class PurchaseService(StockService):
    receive_purchase = StockService.receive_batch
