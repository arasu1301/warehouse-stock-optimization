import streamlit as st
import urllib.request, json
BASE="http://127.0.0.1:8000"
st.set_page_config(page_title="Warehouse Optimizer",layout="wide")
st.title("Warehouse Stock Optimization")
def get(path):
    try:
        with urllib.request.urlopen(BASE+path) as r: return json.load(r)
    except Exception: return None
def post(path, payload):
    request = urllib.request.Request(BASE + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request) as response: return json.load(response)
    except Exception as error: return {"error": str(error)}
items=get("/inventory") or []; alert=get("/alerts") or {"low_stock":[],"expiring_soon":[]}
a,b,c=st.columns(3); a.metric("Batches",len(items)); b.metric("Units",sum(x['quantity'] for x in items)); c.metric("Low stock",len(alert['low_stock']))
st.subheader("Inventory by expiry (FEFO order)"); st.dataframe(items,use_container_width=True)
st.subheader("Alerts"); st.json(alert)
with st.expander("Receive a batch"):
    with st.form("receipt"):
        sku = st.text_input("SKU", "P001"); batch = st.text_input("Batch code", "BATCH-001")
        expiry = st.date_input("Expiry date"); quantity = st.number_input("Quantity", min_value=1, value=10); location = st.text_input("Location", "RACK-A1")
        if st.form_submit_button("Receive stock"):
            st.json(post("/batches", {"sku":sku,"batch_code":batch,"expiry_date":str(expiry),"quantity":quantity,"location":location}))
with st.expander("Dispatch a sale - FEFO"):
    with st.form("sale"):
        sku = st.text_input("Sales SKU", "P001"); quantity = st.number_input("Sales quantity", min_value=1, value=1); reference = st.text_input("Invoice / order", "ORDER-001")
        if st.form_submit_button("Dispatch sale"):
            st.json(post("/sales/dispatch", {"sku":sku,"quantity":quantity,"reference":reference}))
