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

# ---- GLOBAL CSS STYLE ----
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    color: #111;
    font-family: 'Segoe UI', sans-serif;
}
header, .block-container {
    padding-top: 1rem;
}
[data-testid="stSidebar"] {
    background-color: #f0f2f6;
    color: #333;
}
[data-testid="metric-container"] {
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #ffffff;
    margin-bottom: 10px;
}
[data-testid="metric-container"] > div {
    font-size: 1.1rem;
    white-space: normal;
    word-break: break-word;
}
.big-title {
    font-size: 2.2rem;
    font-weight: 900;
    color: #4B0082;
    margin-bottom: 0.5rem;
}
.subtitle {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 1rem;
}
.navbar {
    background-color: #ffffff;
    border-bottom: 2px solid #eaeaea;
    padding: 0.8rem 1.5rem;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.navbar a {
    text-decoration: none;
    color: #4B0082;
    margin: 0 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---- STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- NAVIGATION HEADER ----
st.markdown("""
<div class="navbar">
    <div class="big-title">Ryxon Technologies</div>
    <div>
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Products</a>
        <a href="#">Services</a>
        <a href="#">Instruments</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    st.markdown("<div class='big-title'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Upload your trade file and instantly gain insight into your trading risks with MTM, VaR, and more.</div>", unsafe_allow_html=True)
    if st.button("🚀 Launch Dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()
else:
    st.markdown("<div class='big-title'>📈 Ryxon Risk Dashboard</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your trade data (Excel)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        st.markdown("### 📋 Trade Data")
        st.dataframe(df, use_container_width=True)

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

        st.markdown("### 🧠 Advanced Risk Analytics")
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

        st.markdown("### 📑 Risk Reporting")
        with st.expander("📝 Risk Summary Report"):
            st.write("""
            This report provides a snapshot of portfolio risk:
            - Total MTM: ${:,.2f}
            - Total Realized PnL: ${:,.2f}
            - Total Unrealized PnL: ${:,.2f}
            - 1-Day Historical VaR (95%): ${:,.2f}
            """.format(mtm_total, realized_pnl, unrealized_pnl, var_95))

        with st.expander("📊 Exposure Breakdown Report"):
            if 'Commodity' in df.columns:
                exposure_df = df.groupby('Commodity')['MTM'].sum().reset_index()
                fig = px.bar(exposure_df, x='Commodity', y='MTM', title='Exposure by Commodity')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No 'Commodity' column found for exposure analysis.")

        with st.expander("📅 Daily Performance Report"):
            if 'Trade Date' in df.columns:
                df['Trade Date'] = pd.to_datetime(df['Trade Date'])
                perf_df = df.groupby('Trade Date').agg({'MTM': 'sum', 'Realized PnL': 'sum'}).reset_index()
                fig = px.line(perf_df, x='Trade Date', y=['MTM', 'Realized PnL'], title="Daily MTM and PnL")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No 'Trade Date' column found for daily performance chart.")
    else:
        st.warning("Please upload a valid Excel trade file to proceed.")
