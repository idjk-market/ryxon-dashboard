import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="📑 Reporting | Ryxon", layout="wide")

st.title("📑 Ryxon Reporting Module")

uploaded_file = st.file_uploader("Upload trade file for reporting", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.markdown("## 📊 Risk Summary Report")
    group_option = st.selectbox("Group by", ['Commodity', 'Instrument Type'])
    summary = df.groupby(group_option).agg({
        'MTM': 'sum',
        'Realized PnL': 'sum',
        'Unrealized PnL': 'sum'
    }).reset_index()
    st.dataframe(summary)

    st.markdown("## 💰 PnL Drilldown Report")
    drill_option = st.selectbox("Drilldown by", ['Trade ID', 'Commodity'])
    drill = df.groupby(drill_option).agg({
        'Realized PnL': 'sum',
        'Unrealized PnL': 'sum',
        'MTM': 'sum'
    }).sort_values(by='MTM', ascending=False).reset_index()
    st.dataframe(drill)

    st.markdown("## 📆 Daily MTM Trend Report")
    if 'Trade Date' in df.columns and 'MTM' in df.columns:
        df['Trade Date'] = pd.to_datetime(df['Trade Date'], errors='coerce')
        trend_df = df.groupby('Trade Date')['MTM'].sum().reset_index()
        st.line_chart(trend_df.set_index('Trade Date'))
    else:
        st.warning("Missing 'Trade Date' or 'MTM' column.")
else:
    st.info("Please upload a file to generate reports.")
