# Warehouse Stock Optimization: Project Plan

## Objective

Build a warehouse system that keeps accurate stock by product, batch and location; removes stock using FEFO; detects operational risk; and uses sales history to predict demand and recommend replenishment.

## Scope and modules

| Area | Responsibility | Delivered module |
| --- | --- | --- |
| Master data | SKU, name, barcode, reorder level, unit cost | `products` |
| Batch control | batch code, expiry, quantity, location | `batches` |
| Inventory | receive, view quantity/value, adjust, dispatch | `inventory`, `stock_service` |
| Warehouse flow | place stock and select FEFO batches | `placement_service`, `retrieval_service` |
| Traceability | append-only receipt/retrieval records | `movements` |
| Risk management | low-stock and near-expiry warnings | `alerts` |
| Decision support | inventory valuation and operational summary | `reports` |
| AI/ML | forecasting, reorder target, sales outliers | `app/ai` |
| Interface | REST API and Streamlit dashboard | `app/api`, `frontend` |

## Step-by-step implementation process

1. Collect the legacy Java classes and list every entity, field, validation and transaction. Preserve rules such as unique SKU/barcode, non-negative quantity, and movement auditing.
2. Translate Java layers: POJO/entity -> Python model; DAO -> parameterized SQLite query; service -> Python service; controller -> FastAPI route; Java UI -> Streamlit page.
3. Initialize SQLite tables and indexes. Test a fresh database startup before adding business features.
4. Implement product creation and barcode lookup. A product must exist before stock can be received.
5. Implement batch receipt: save batch, expiry, location and quantity in one transaction; write a positive receipt movement.
6. Implement placement and inventory views. Inventory is batch-level so location and expiry remain visible.
7. Implement FEFO dispatch: query only unexpired, positive-quantity batches in ascending expiry order; reject insufficient stock; decrement each selected batch and append negative movements in the same transaction.
8. Implement alerts and reports: stock at/below reorder level, batches expiring within 30 days, units and stock value.
9. Load or import sales history, preprocess it by SKU/date, then evaluate baseline forecasts against held-out dates before using recommendations operationally.
10. Add dashboard screens, API documentation, unit/integration tests, role-based auth, backups and deployment settings for production.

## AI/ML design

`demand_forecasting.py` uses least-squares trend forecasting as a transparent baseline. `reorder_prediction.py` converts daily demand into a target stock quantity using lead time + safety days, then returns `max(0, target - current stock)`. `anomaly_detection.py` uses robust median absolute deviation (MAD) scores to flag unusually large or small sales. In a production phase, replace or compare these baselines with seasonal models after enough clean historical data is available.

## Acceptance checks

- A duplicate SKU or barcode is rejected.
- Receiving a batch creates both a batch row and a receipt movement.
- Dispatching a SKU takes the earliest unexpired batch first, splitting across batches only when required.
- A dispatch never makes quantity negative and is rejected if usable stock is insufficient.
- Alert output identifies low-stock and near-expiry inventory.
- Reorder recommendation explains current stock, forecast, target and proposed order quantity.
