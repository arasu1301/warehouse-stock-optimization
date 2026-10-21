from fastapi import FastAPI
from app.database import Database
from app.services.stock_service import StockService
from app.services.batch_service import BatchService
from app.services.alert_service import AlertService
from app.services.data_import_service import DataImportService
from app.services.sales_service import SalesService
from app.services.placement_service import PlacementService
from app.barcode.scanner import BarcodeScanner
from app.ai.demand_forecasting import forecast
from app.ai.reorder_prediction import recommend
from app.ai.anomaly_detection import detect
from app.api import products,batches,inventory,movements,alerts,reports,auth,data,sales,placement

db=Database(); db.initialize()
stock=StockService(db)
app=FastAPI(title="Warehouse Stock Optimization",version="1.0.0")
app.include_router(products.register(stock)); app.include_router(batches.register(BatchService(db)))
app.include_router(inventory.register(stock)); app.include_router(movements.register(stock))
app.include_router(alerts.register(AlertService(db))); app.include_router(reports.register(stock)); app.include_router(auth.router)
app.include_router(data.register(DataImportService(db), db.path.parent / "historical_sales.csv"))
app.include_router(sales.register(SalesService(db))); app.include_router(placement.register(PlacementService(db)))

@app.get("/", tags=["System"])
def home():
    return {"name": "Warehouse Stock Optimization", "docs": "/docs", "status": "running"}

@app.get("/health",tags=["System"])
def health(): return {"status":"ok"}

@app.get("/barcode/{barcode}",tags=["Barcode"])
def barcode_lookup(barcode:str): return BarcodeScanner(db).lookup(barcode)

def history(sku):
    with db.connection() as c: return [dict(r) for r in c.execute("SELECT sale_date,quantity FROM sales_history WHERE sku=? ORDER BY sale_date",(sku,))]

@app.get("/ai/forecast/{sku}",tags=["AI / ML"])
def demand_forecast(sku:str, periods:int=7): return forecast(history(sku),periods)
@app.get("/ai/reorder/{sku}",tags=["AI / ML"])
def reorder(sku:str, lead_time_days:int=7, safety_days:int=3):
    current=sum(r['quantity'] for r in stock.inventory() if r['sku']==sku)
    return recommend(history(sku),current,lead_time_days,safety_days)
@app.get("/ai/anomalies/{sku}",tags=["AI / ML"])
def anomalies(sku:str): return detect(history(sku))
