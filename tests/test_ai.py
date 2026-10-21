from app.ai.anomaly_detection import detect
def test_anomaly_detects_spike():
    result = detect([{'sale_date':'1','quantity':1},{'sale_date':'2','quantity':1},{'sale_date':'3','quantity':100}])
    assert len(result) == 1
    assert result[0]["quantity"] == 100
    assert result[0]["modified_z_score"] == "infinite"
