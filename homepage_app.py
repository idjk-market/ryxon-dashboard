import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- METRIC STYLE FIX ----
st.markdown("""
<style>
[data-testid="metric-container"] {
    width: 100% !important;
    padding: 8px !important;
}
[data-testid="metric-container"] > div {
    font-size: 1.2rem !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# ---- STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    st.title("📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence")
    st.markdown("""
    Upload your trade file and instantly gain insight into your trading risks with MTM, VaR, and more.
    """)
    if st.button("🚀 Launch Dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()
else:
    st.title("📈 Ryxon Risk Dashboard")
    uploaded_file = st.file_uploader("Upload your trade data (Excel)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # ---- FILTERED TRADE DATA TABLE ----
        st.markdown("### 📋 Filtered Trade Data")
        st.dataframe(df, use_container_width=True)

        # ---- CALCULATE METRICS ----
        df['MTM'] = df.get('MTM', 0)
        df['Realized PnL'] = df.get('Realized PnL', 0)
        df['Unrealized PnL'] = df.get('Unrealized PnL', 0)

        mtm_total = df['MTM'].sum()
        realized_pnl = df['Realized PnL'].sum()
        unrealized_pnl = df['Unrealized PnL'].sum()

        try:
            returns = df['MTM'].pct_change().dropna()
            avg_return = returns.mean()
            volatility = returns.std()
            var_95 = np.percentile(df['MTM'].dropna(), 5)
        except:
            avg_return = 0
            volatility = 0
            var_95 = 0

        with st.expander("📊 Core Risk Metrics", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mark-to-Market", f"${mtm_total:,.2f}")
            col2.metric("1-Day VaR (95%)", f"${var_95:,.2f}")
            col3.metric("Realized PnL", f"${realized_pnl:,.2f}")
            col4.metric("Unrealized PnL", f"${unrealized_pnl:,.2f}")
            st.caption(f"Avg Daily Return: {avg_return:.4f} | Avg Volatility: {volatility:.4f}")

        # ---- ADVANCED SECTION ----
        with st.expander("🧠 Advanced Risk Analytics", expanded=False):
            with st.expander("📦 Portfolio VaR (Variance-Covariance)"):
                st.write("Coming soon...")
            with st.expander("🧪 Monte Carlo Simulation"):
                st.write("Coming soon...")
            with st.expander("📉 Rolling Volatility"):
                st.line_chart(df['MTM'])
            with st.expander("🚨 Stress Testing"):
                st.write("Coming soon...")
            with st.expander("📊 Scenario Analysis"):
                st.write("Coming soon...")
            with st.expander("📉 Historical VaR"):
                st.write("Coming soon...")
    else:
        st.warning("Please upload a valid Excel trade file to proceed.")
