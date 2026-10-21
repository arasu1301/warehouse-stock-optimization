from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator

class BatchCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"sku": "P001", "batch_code": "RICE-SEP-01", "expiry_date": "2030-12-31", "quantity": 200, "location": "RACK-A1"}})
    sku: str
    batch_code: str
    expiry_date: date
    quantity: int = Field(gt=0)
    location: str = Field(default="RECEIVING", min_length=1)

    @field_validator("expiry_date")
    @classmethod
    def expiry_must_not_be_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Expiry date cannot be in the past")
        return value
