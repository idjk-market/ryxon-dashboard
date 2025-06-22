
# streamlit_app_master.py
# This is the complete unified Streamlit app for Ryxon Risk Module

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from io import BytesIO

st.set_page_config(layout="wide", page_title="Ryxon - Risk Intelligence")

st.title("📊 Ryxon Risk Management Dashboard")

# Upload trade file
uploaded_file = st.file_uploader("Upload Trade Data", type=["xlsx", "csv"])
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()

        # Sidebar filters
        st.sidebar.header("🧮 Filter Trades")
        columns_to_filter = ['Trade ID', 'Commodity', 'Instrument Type', 'Trade Action', 'UOM']
        filtered_df = df.copy()
        for col in columns_to_filter:
            if col in df.columns:
                selected = st.sidebar.multiselect(f"Select {col}", options=["All"] + df[col].astype(str).unique().tolist(), default=["All"])
                if "All" not in selected:
                    filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected)]

        st.subheader("📌 Filtered Trade Data")
        st.dataframe(filtered_df)

        # Exposure
        st.subheader("📈 Exposure Calculation")
        if all(col in filtered_df.columns for col in ['Quantity', 'Book Price']):
            filtered_df["Exposure"] = filtered_df["Quantity"] * filtered_df["Book Price"]
            st.dataframe(filtered_df[["Trade ID", "Commodity", "Quantity", "Book Price", "Exposure"]])

        # MTM Calculation
        st.subheader("🔍 MTM Calculation")
        if all(col in filtered_df.columns for col in ['Market Price']):
            filtered_df["MTM"] = (filtered_df["Market Price"] - filtered_df["Book Price"]) * filtered_df["Quantity"]
            st.dataframe(filtered_df[["Trade ID", "Book Price", "Market Price", "Quantity", "MTM"]])

        # PnL Split
        st.subheader("💰 PnL Analysis")
        if "Trade Action" in filtered_df.columns:
            filtered_df["Realized PnL"] = np.where(filtered_df["Trade Action"].str.lower().str.contains("sell"), filtered_df["MTM"], 0)
            filtered_df["Unrealized PnL"] = np.where(filtered_df["Trade Action"].str.lower().str.contains("buy"), filtered_df["MTM"], 0)
            st.dataframe(filtered_df[["Trade ID", "Realized PnL", "Unrealized PnL"]])

        # VAR Calculation (Parametric)
        st.subheader("📉 Value at Risk (VaR) - Parametric")
        if 'MTM' in filtered_df.columns and len(filtered_df) > 10:
            pnl_series = filtered_df['MTM']
            daily_return = pnl_series.pct_change().dropna()
            mean_return = daily_return.mean()
            std_dev = daily_return.std()
            investment = 1000000

            z_95, z_99 = 1.65, 2.33
            var_95 = round((mean_return - z_95 * std_dev) * investment, 2)
            var_99 = round((mean_return - z_99 * std_dev) * investment, 2)

            st.markdown(f"**1-Day VaR @ 95% Confidence:** ₹ {var_95:,}")
            st.markdown(f"**1-Day VaR @ 99% Confidence:** ₹ {var_99:,}")

        # Placeholder for Monte Carlo, Stress Testing, Scenarios
        st.subheader("🧪 Upcoming Modules")
        st.info("Monte Carlo Simulation, Stress Testing & Scenario Analysis will be added in next phases.")

    except Exception as e:
        st.error(f"Failed to process file: {e}")
else:
    st.warning("Upload a trade file (xlsx or csv) to get started.")
