import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, create_order, list_orders, update_order_status, list_operators, add_operator, assign_operator

st.set_page_config(page_title="Mini MES - Order Tracking", layout="wide")

@st.cache_data
def bootstrap():
    init_db()
    # Add a few demo operators
    for name in ["Alice", "Bob", "Carlos", "Devi"]:
        add_operator(name)
    return True

bootstrap()

st.title("🧭 Mini MES — Production Order Tracking")
st.caption("Create orders, update status, assign operators, and visualize WIP.")

with st.sidebar:
    st.header("Create a new order")
    product_code = st.text_input("Product code", placeholder="e.g., P-1001")
    qty = st.number_input("Quantity", min_value=1, step=1, value=10)
    due = st.date_input("Due date (optional)")
    if st.button("Create Order", use_container_width=True):
        due_str = due.isoformat() if due else None
        if product_code.strip():
            create_order(product_code.strip(), int(qty), due_str)
            st.success("Order created.")
        else:
            st.error("Please enter a product code.")

    st.header("Add operator")
    new_op = st.text_input("Name", placeholder="e.g., Priya")
    if st.button("Add Operator", use_container_width=True):
        if new_op.strip():
            add_operator(new_op.strip())
            st.success("Operator added.")
        else:
            st.error("Please enter a name.")

st.subheader("Orders")
status_filter = st.segmented_control("Filter by status", options=["all", "scheduled", "in_progress", "completed", "on_hold", "cancelled"], default="all")
orders = list_orders(None if status_filter == "all" else status_filter)

if orders:
    rows = [dict(r) for r in orders]  # ensure proper column names
    df = pd.DataFrame(rows)

    # Safely cast numeric columns if they exist
    if not df.empty:
        for col in ("id", "quantity"):
            if col in df.columns:
                df[col] = df[col].astype(int)
    st.dataframe(df[["id", "product_code", "quantity", "status", "operator_name", "due_date", "created_at"]], use_container_width=True, hide_index=True)

    st.subheader("Update status / Assign operator")
    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        order_id = st.number_input("Order ID", min_value=1, step=1)
    with col2:
        new_status = st.selectbox("New status", ["scheduled", "in_progress", "completed", "on_hold", "cancelled"])
    with col3:
        if st.button("Update Status", type="primary"):
            update_order_status(int(order_id), new_status)
            st.success("Order status updated.")

    st.divider()
    st.subheader("Assign Operator")
    ops = list_operators()
    op_names = ["(none)"] + [o["name"] for o in ops]
    selected_op_name = st.selectbox("Operator", op_names)
    assign_id = st.number_input("Order ID to assign", min_value=1, step=1, key="assign_id")
    if st.button("Assign", key="assign_btn"):
        op_id = None
        if selected_op_name != "(none)":
            op_map = {o["name"]: o["id"] for o in ops}
            op_id = op_map[selected_op_name]
        assign_operator(int(assign_id), op_id if op_id is not None else None)
        st.success("Assignment updated.")

    st.divider()
    st.subheader("WIP Summary")
    counts = df.groupby("status")["id"].count().reset_index(name="count")
    fig = px.bar(counts, x="status", y="count", title="Orders by Status")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No orders yet. Use the sidebar to create your first order.")
