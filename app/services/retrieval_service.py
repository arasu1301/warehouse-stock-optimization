from app.services.stock_service import StockService
class RetrievalService(StockService):
    retrieve = StockService.retrieve_fefo
