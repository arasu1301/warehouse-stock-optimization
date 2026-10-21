# Warehouse Stock Optimization

A Python conversion blueprint for a warehouse-management mini project. It provides product, batch, inventory, movement, FEFO retrieval, barcode, reporting, alerting, and explainable AI/ML features through a FastAPI API and optional Streamlit dashboard.

## Delivery phases

1. **Discovery and Java-to-Python mapping** - identify Java entities, services, controllers and repository responsibilities; map them to Python dataclasses/Pydantic models, services, API routers and SQLite.
2. **Foundation** - create the project structure, configuration, schema initialization and validation rules.
3. **Core warehouse operations** - products, batches, stock receipt, location placement, sales/dispatch, immutable movement log and barcode lookup.
4. **Optimization** - FEFO selection (earliest non-expired batch first), low-stock/expiry alerts, inventory valuation and operational reports.
5. **AI/ML** - historical-sales preprocessing, linear demand trend forecast, reorder recommendation and robust anomaly detection. These are deliberately transparent baseline models that run without a heavy ML dependency.
6. **Presentation and quality** - REST routes, Streamlit dashboard, tests, sample sales history and deployment documentation.

## Java to Python conversion guide

| Existing Java responsibility | Python equivalent |
| --- | --- |
| POJO / Entity | `app/models` dataclass or Pydantic request model |
| DAO / Repository | `app/database/database.py` parameterized SQLite access |
| Service class | `app/services` business rules |
| Controller | `app/api` FastAPI router |
| JDBC / MySQL bootstrap | SQLite schema in `app/database/tables.py` |
| Scheduled stock checks | `AlertService` callable from API, UI, or scheduler |
| Java ML integration | `app/ai` deterministic Python analytics |

## Run

```powershell
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
# optional dashboard in another terminal
py -m streamlit run frontend/dashboard.py
```

Open API docs at `http://127.0.0.1:8000/docs`. The database is created automatically at `data/warehouse.db`.

## Typical flow

1. `POST /products` to register a SKU and barcode.
2. `POST /batches` to receive a dated batch into a location.
3. `POST /inventory/retrieve` to dispatch quantity using FEFO.
4. Dispatch customer orders through `POST /sales/dispatch`, not the generic retrieval endpoint. This preserves FEFO and adds each sale to the AI history.
5. Review `/alerts`, `/reports/inventory`, and `/ai/*`.

## Use the supplied historical-sales data

Start the API, open `/docs`, and execute `POST /data/import-historical-sales` once. It imports `data/historical_sales.csv`, creates products from `product_id` where needed, and saves daily sales records for the AI module. Then execute `GET /ai/forecast/P001`, `GET /ai/reorder/P001`, or `GET /ai/anomalies/P001`. The import is idempotent: repeat calls are skipped instead of duplicating sales history. If you replace the source file and want to rebuild only its stored history, use the `replace_existing=true` query option; this does not remove physical stock batches or movements.

## Operating without a live sales feed

Live sales data is not required. Import a CSV periodically (weekly or monthly) and use `POST /sales/dispatch` for each new order entered into this application. In a real deployment, the same endpoint can be called by a POS, billing, ERP, or e-commerce system after an invoice is completed. Forecast quality improves as these confirmed sales accumulate. Use the forecast as a decision aid, not an automatic purchase order, until its accuracy has been measured against several months of actual results.

## Specification note

The supplied `OOSE_mini_project_print1.pdf` was zero bytes when inspected, and the supplied ChatGPT share URL could not be fetched. This implementation therefore follows the user-provided architecture and workflow rather than inventing requirements from either reference.
