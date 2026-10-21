from app.ai.demand_forecasting import forecast
def test_forecast_positive(): assert forecast([{'quantity':2},{'quantity':3}])['daily_forecast'] >= 0
