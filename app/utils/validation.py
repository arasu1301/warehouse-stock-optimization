def positive_quantity(value: int) -> int:
    if value <= 0: raise ValueError("Quantity must be positive")
    return value
