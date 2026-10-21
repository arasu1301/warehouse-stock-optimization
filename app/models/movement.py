from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Movement:
    sku: str
    batch_code: str
    quantity: int
    movement_type: str
    created_at: datetime
