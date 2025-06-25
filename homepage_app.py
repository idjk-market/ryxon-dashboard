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
if 'dashboard_mode' not in st.session_state:
    st.session_state.dashboard_mode = None

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

# ---- MODE SELECTION ----
elif st.session_state.dashboard_mode is None:
    st.subheader("Choose Your Mode")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📂 Upload Trade File"):
            st.session_state.dashboard_mode = "upload"
            st.rerun()
    with col2:
        if st.button("📝 Create Manual Trade"):
            st.session_state.dashboard_mode = "manual"
            st.rerun()

# ---- MANUAL TRADE ENTRY ----
elif st.session_state.dashboard_mode == "manual":
    if st.button("🔙 Go Back"):
        st.session_state.dashboard_mode = None
        st.rerun()

    st.subheader("📝 Manual Trade Entry")
    st.markdown("Enter trade details below. This is useful for paper trading or strategy simulation.")

    with st.form("trade_form"):
        trade_date = st.date_input("Trade Date")
        instrument = st.selectbox("Instrument Type", ["Futures", "Options", "Forwards", "Swaps"])
        commodity = st.text_input("Commodity")
        instrument_no = st.text_input("Instrument No.")
        exchange = st.text_input("Exchange")
        index = st.text_input("Index")
        lot_type = st.selectbox("Lot Type", ["Standard", "Mini"])
        lot_size = st.number_input("Lot Size", min_value=0.0)
        lots = st.number_input("Lots", min_value=0.0)

        total_qty = lot_size * lots

        if instrument == "Options":
            option_type = st.selectbox("Option Type", ["Call", "Put"])
            option_action = st.selectbox("Option Action", ["Buy", "Sell"])
            strike_price = st.number_input("Strike Price", min_value=0.0)
            premium = st.number_input("Premium", min_value=0.0)
            total_amount = total_qty * premium
        else:
            book_price = st.number_input("Book Price", min_value=0.0)
            market_price = st.number_input("Market Price", min_value=0.0)
            total_amount = total_qty * book_price

        submitted = st.form_submit_button("Submit Trade")

    if submitted:
        if instrument == "Options":
            mtm = total_qty * premium if option_action == "Sell" else -total_qty * premium
            trade_details = {
                "Trade Date": trade_date,
                "Instrument Type": instrument,
                "Commodity": commodity,
                "Instrument No.": instrument_no,
                "Exchange": exchange,
                "Index": index,
                "Lot Type": lot_type,
                "Lot Size": lot_size,
                "Lots": lots,
                "Total Qty": total_qty,
                "Option Type": option_type,
                "Option Action": option_action,
                "Strike Price": strike_price,
                "Premium": premium,
                "Total Amount": total_amount,
                "MTM": mtm
            }
        else:
            mtm = (market_price - book_price) * total_qty
            trade_details = {
                "Trade Date": trade_date,
                "Instrument Type": instrument,
                "Commodity": commodity,
                "Instrument No.": instrument_no,
                "Exchange": exchange,
                "Index": index,
                "Lot Type": lot_type,
                "Lot Size": lot_size,
                "Lots": lots,
                "Total Qty": total_qty,
                "Book Price": book_price,
                "Market Price": market_price,
                "Total Amount": total_amount,
                "MTM": mtm
            }

        st.success(f"Trade submitted successfully! MTM = ${mtm:,.2f}")
        st.dataframe(pd.DataFrame([trade_details]), use_container_width=True)

# ---- FILE UPLOAD DASHBOARD ----
elif st.session_state.dashboard_mode == "upload":
    if st.button("🔙 Go Back"):
        st.session_state.dashboard_mode = None
        st.rerun()

    st.subheader("📁 Upload Trade File")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

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
            st.write(f"""
            This report provides a snapshot of portfolio risk:
            - Total MTM: ${mtm_total:,.2f}
            - Total Realized PnL: ${realized_pnl:,.2f}
            - Total Unrealized PnL: ${unrealized_pnl:,.2f}
            - 1-Day Historical VaR (95%): ${var_95:,.2f}
            """)

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
