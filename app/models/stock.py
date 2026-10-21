from pydantic import BaseModel, ConfigDict, Field

class StockAdjustment(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"sku": "P001", "batch_code": "RICE-SEP-01", "quantity": -2, "reason": "damage"}})
    sku: str
    batch_code: str
    quantity: int
    reason: str = "adjustment"

class PlacementRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"sku": "P001", "batch_code": "RICE-SEP-01", "location": "RACK-B2"}})
    sku: str
    batch_code: str
    location: str = Field(min_length=1, max_length=80)

class RetrievalRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"sku": "P001", "quantity": 12, "reference": "INV-1001"}})
    sku: str
    quantity: int = Field(gt=0)
    reference: str = "sales-order"
