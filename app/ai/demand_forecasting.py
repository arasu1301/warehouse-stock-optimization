from statistics import mean
def forecast(history, periods=7):
    """Least-squares linear trend forecast; accepts chronological quantities."""
    values=[float(r['quantity']) for r in history]
    if not values: return {"daily_forecast":0,"period_demand":0,"method":"no history"}
    xs=range(len(values)); xbar=mean(xs); ybar=mean(values)
    divisor=sum((x-xbar)**2 for x in xs)
    slope=sum((x-xbar)*(y-ybar) for x,y in zip(xs,values))/divisor if divisor else 0
    prediction=max(0,ybar+slope*len(values))
    return {"daily_forecast":round(prediction,2),"period_demand":round(prediction*periods,2),"method":"linear trend"}
