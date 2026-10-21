from statistics import median
def detect(history, threshold=3.5):
    values=[float(r['quantity']) for r in history]
    if len(values)<3: return []
    centre=median(values); mad=median([abs(x-centre) for x in values])
    # A constant baseline is common in small datasets. In that case MAD is
    # zero, but any value different from the baseline is still an anomaly.
    if mad == 0:
        return [{"date": r["sale_date"], "quantity": r["quantity"], "modified_z_score": "infinite"}
                for r in history if float(r["quantity"]) != centre]
    return [{"date":r['sale_date'],"quantity":r['quantity'],"modified_z_score":round(0.6745*(float(r['quantity'])-centre)/mad,2)} for r in history if abs(0.6745*(float(r['quantity'])-centre)/mad)>threshold]
