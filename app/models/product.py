from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"sku": "P001", "name": "Rice 5kg", "barcode": "8901234567890", "reorder_level": 100, "unit_cost": 320}})
    sku: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=160)
    barcode: str | None = None
    reorder_level: int = Field(default=0, ge=0)
    unit_cost: float = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"reorder_level": 100, "unit_cost": 320}})
    name: str | None = Field(default=None, min_length=1, max_length=160)
    barcode: str | None = None
    reorder_level: int | None = Field(default=None, ge=0)
    unit_cost: float | None = Field(default=None, ge=0)
