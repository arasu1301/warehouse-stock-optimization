from app.ai.demand_forecasting import forecast
def recommend(history, current_stock, lead_time_days=7, safety_days=3):
    model=forecast(history, lead_time_days+safety_days)
    target=round(model['daily_forecast']*(lead_time_days+safety_days))
    return {**model,"current_stock":current_stock,"target_stock":target,"recommended_order":max(0,target-current_stock)}
