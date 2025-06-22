import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
from scipy.stats import norm

st.set_page_config(page_title="Ryxon Risk Dashboard", layout="wide")
st.title("📊 Ryxon – Trading Risk Intelligence")

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade File (.csv/.xlsx)", type=["csv", "xlsx"])
if file:
    df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
    df.columns = [c.strip().title() for c in df.columns]

    if "Trade Date" in df.columns:
        df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    # --- MTM Calculation ---
    if all(col in df.columns for col in ["Book Price", "Market Price", "Quantity"]):
        df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]

    # --- PnL ---
    if "Trade Action" in df.columns and "MTM" in df.columns:
        df["Realized PnL"] = np.where(df["Trade Action"].str.lower() == "sell", df["MTM"], 0)
        df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower() == "buy", df["MTM"], 0)

    # --- VaR Calculation ---
    confidence = st.slider("Confidence Level (%)", 90, 99, 95)
    z = norm.ppf(confidence / 100)
    if "Trade Date" in df.columns and "MTM" in df.columns:
        df = df.sort_values("Trade Date")
        df["Daily Return"] = df["MTM"].pct_change().fillna(0)
        df["Rolling Std Dev"] = df["Daily Return"].rolling(window=10).std().fillna(0)
        df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()

    # --- Display Trade Data with Excel-style Filters ---
    st.subheader("📋 Filtered Trade Data (Excel-style Column Filters)")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(filter=True, editable=False, sortable=True, resizable=True)
    gb.configure_pagination(enabled=True)
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, height=400, enable_enterprise_modules=True)

    # --- Expanders: MTM ---
    with st.expander("📘 MTM Breakdown"):
        st.dataframe(df[["Trade ID", "Commodity", "Instrument Type", "Trade Action", 
                         "Quantity", "Book Price", "Market Price", "MTM"]])

    # --- Expanders: PnL ---
    with st.expander("📙 Realized and Unrealized PnL"):
        st.dataframe(df[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])

    # --- Expanders: VaR ---
    with st.expander("📕 Value at Risk (VaR)"):
        st.dataframe(df[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]])
        st.metric(f"Latest 1-Day VaR ({confidence}%)", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

    # --- Summary Metrics ---
    st.subheader("📊 Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MTM", f"₹ {df['MTM'].sum():,.2f}")
    col2.metric("Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
    col3.metric("Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
    col4.metric(f"VaR ({confidence}%)", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

    # --- PnL Breakdown Chart ---
    pnl_df = pd.DataFrame({
        "Metric": ["MTM", "Realized PnL", "Unrealized PnL"],
        "Value": [df["MTM"].sum(), df["Realized PnL"].sum(), df["Unrealized PnL"].sum()]
    })
    fig = px.bar(pnl_df, x="Metric", y="Value", text="Value", title="PnL Components")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload a trade data file to get started.")
