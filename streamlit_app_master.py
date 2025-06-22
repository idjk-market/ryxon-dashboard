# streamlit_app_master.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ryxon Risk Intelligence", layout="wide")
st.title("📈 Ryxon Trading Risk Dashboard")

# --- FILE UPLOAD ---
st.sidebar.header("📂 Upload Trade File")
file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "csv"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("📌 Filtered Trade Data")

    # Global multi-filter across all columns
    filter_value = st.text_input("🔍 Search across all fields")
    if filter_value:
        df = df[df.apply(lambda row: row.astype(str).str.contains(filter_value, case=False).any(), axis=1)]

    st.dataframe(df, use_container_width=True)

    # --- RISK CALCULATION SECTION ---
    st.subheader("📊 Value at Risk (VaR) Summary")

    # Calculate Daily Return & Rolling Std Dev if not present
    if 'Daily Return' not in df.columns:
        df['Daily Return'] = df['MTM'].pct_change()
    if 'Rolling Std Dev' not in df.columns:
        df['Rolling Std Dev'] = df['Daily Return'].rolling(window=30).std()
    if 'Notional' not in df.columns:
        df['Notional'] = df['Quantity'] * df['Book Price']

    # --- Confidence Level Selection ---
    z_values = {"95%": 1.65, "99%": 2.33, "90%": 1.28}
    confidence = st.radio("Select Confidence Level", list(z_values.keys()), horizontal=True)
    z = z_values[confidence]

    # --- Compute VaR ---
    df[f'VaR {confidence}'] = - (df['Daily Return'].mean() - z * df['Rolling Std Dev']) * df['Notional']

    st.write(f"### Computed 1-Day VaR @ {confidence} Confidence:")
    st.dataframe(df[[
        'Trade ID', 'Commodity', 'Instrument Type', 'Trade Action', 'Quantity',
        'Book Price', 'Market Price', 'MTM', 'Realized PnL', 'Unrealized PnL', f'VaR {confidence}'
    ]].dropna(), use_container_width=True)

    # --- VaR Trend Plot ---
    st.subheader("📉 VaR Over Time")
    if 'Trade Date' in df.columns:
        df['Trade Date'] = pd.to_datetime(df['Trade Date'])
        plot_df = df.set_index('Trade Date')[[f'VaR {confidence}']].dropna()
        st.line_chart(plot_df)

    # --- Downloadable Link ---
    st.download_button(
        label="Download Updated Excel",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="ryxon_updated_var_data.csv",
        mime="text/csv"
    )

else:
    st.warning("Please upload a file to begin.")
