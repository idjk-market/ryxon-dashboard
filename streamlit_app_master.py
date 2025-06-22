import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Ryxon Risk Dashboard", layout="wide")
st.title("📊 Ryxon Trading Risk Dashboard")

# --- File Upload ---
file = st.file_uploader("Upload Trade File", type=["xlsx", "csv"])

if file:
    df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
    df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    st.markdown("### 📌 Filtered Trade Data")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # --- Expandable: MTM Calculation ---
    with st.expander("📘 MTM Calculation Logic"):
        df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
        st.write("Calculated MTM = (Market Price - Book Price) × Quantity")
        st.dataframe(df[["Trade ID", "Commodity", "Quantity", "Book Price", "Market Price", "MTM"]], use_container_width=True)

    # --- Expandable: Realized / Unrealized PnL ---
    with st.expander("📙 PnL Summary"):
        df["Realized PnL"] = np.where(df["Trade Action"].str.lower() == "sell", df["MTM"], 0)
        df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower() == "buy", df["MTM"], 0)
        st.write("Based on Trade Action, classify MTM into Realized or Unrealized PnL")
        st.dataframe(df[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]], use_container_width=True)

    # --- Expandable: VaR Calculation ---
    with st.expander("📕 Value at Risk (VaR)"):
        df_sorted = df.sort_values("Trade Date")
        df_sorted["Daily Return"] = df_sorted["MTM"].pct_change().fillna(0)
        df_sorted["Rolling Std Dev"] = df_sorted["Daily Return"].rolling(window=10).std().fillna(0)

        z_95 = 1.65
        df_sorted["1-Day VaR"] = -1 * (df_sorted["Daily Return"].mean() - z_95 * df_sorted["Rolling Std Dev"]) * df_sorted["MTM"].abs()

        st.write("Calculated 1-Day VaR @ 95% Confidence")
        st.dataframe(df_sorted[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]], use_container_width=True)

    # --- Summary Section ---
    st.markdown("### 📊 Final Risk Summary")
    total_mtm = df["MTM"].sum()
    total_real = df["Realized PnL"].sum()
    total_unreal = df["Unrealized PnL"].sum()
    latest_var = df_sorted["1-Day VaR"].iloc[-1] if not df_sorted.empty else 0

    st.metric("Total MTM", f"₹ {total_mtm:,.2f}")
    st.metric("Realized PnL", f"₹ {total_real:,.2f}")
    st.metric("Unrealized PnL", f"₹ {total_unreal:,.2f}")
    st.metric("Latest 1-Day VaR", f"₹ {latest_var:,.2f}")
