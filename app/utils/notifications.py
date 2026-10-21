def format_alerts(alerts):
    return f"{len(alerts['low_stock'])} low-stock and {len(alerts['expiring_soon'])} expiry alerts"
