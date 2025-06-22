import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])

if file:
    # Load data
    df = pd.read_excel(file) if file.name.endswith(".xlsx") else pd.read_csv(file)
    df.columns = df.columns.str.strip().str.title()

    # Parse dates safely
    if "Trade Date" in df.columns:
        df["Trade Date"] = pd.to_datetime(df["Trade Date"], errors='coerce')

    st.markdown("## 🧾 Trade Table with Filters")
    with st.expander("Filtered Trade Table (📥 Click to expand/collapse)", expanded=True):
        # Column filters
        for col in df.select_dtypes(include=['object', 'category']).columns:
            df[col] = df[col].astype(str)
            selected = st.multiselect(f"Filter by {col}", options=sorted(df[col].unique()), default=list(df[col].unique()))
            df = df[df[col].isin(selected)]

        for col in df.select_dtypes(include=['int64', 'float64']).columns:
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            val = st.slider(f"Select {col} Range", min_val, max_val, (min_val, max_val))
            df = df[(df[col] >= val[0]) & (df[col] <= val[1])]

        st.dataframe(df, use_container_width=True)

    # --- MTM Calculation ---
    if set(["Market Price", "Book Price", "Quantity"]).issubset(df.columns):
        df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
        st.markdown("## 💰 MTM Calculation")
        with st.expander("📘 MTM Breakdown", expanded=False):
            st.dataframe(df[["Commodity", "Instrument Type", "Trade Action", "Market Price", "Book Price", "Quantity", "MTM"]])
            st.metric("Total MTM", f"₹ {df['MTM'].sum():,.2f}")

    # --- PnL Calculation ---
    if "Trade Action" in df.columns:
        df["Realized PnL"] = np.where(df["Trade Action"].str.lower().str.strip() == "sell", df["MTM"], 0)
        df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower().str.strip() == "buy", df["MTM"], 0)
        st.markdown("## 📈 PnL Summary")
        with st.expander("📙 Realized & Unrealized PnL", expanded=False):
            st.dataframe(df[["Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
            col1, col2 = st.columns(2)
            col1.metric("Total Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
            col2.metric("Total Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")

    # --- VaR Calculation ---
    st.markdown("## ⚠️ Value at Risk (VaR)")
    with st.expander("📕 VaR Calculation", expanded=False):
        conf = st.slider("Select Confidence Level (%)", 90, 99, 95)
        z = {90: 1.2816, 91: 1.34, 92: 1.4051, 93: 1.4758, 94: 1.5548, 95: 1.645,
             96: 1.7507, 97: 1.8808, 98: 2.0537, 99: 2.3263}.get(conf, 1.645)

        if "MTM" in df.columns and "Trade Date" in df.columns:
            df = df.sort_values("Trade Date")
            df["Daily Return"] = df["MTM"].pct_change().fillna(0)
            df["Rolling Std"] = df["Daily Return"].rolling(5).std().fillna(0)
            df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std"]) * df["MTM"].abs()

            st.dataframe(df[["Trade Date", "Daily Return", "Rolling Std", "1-Day VaR"]])
            st.metric(f"Latest 1-Day VaR at {conf}%", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

    # --- Final Risk Summary ---
    st.markdown("## 🧾 Final Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 MTM", f"₹ {df['MTM'].sum():,.2f}")
    col2.metric("📈 Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
    col3.metric("🧮 Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
    col4.metric("🔻 Latest VaR", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")
