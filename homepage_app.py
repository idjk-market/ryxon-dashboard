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
    st.markdown("Fill the trade form horizontally based on selected instrument.")

    with st.form("horizontal_trade_form"):
        instrument = st.selectbox("Instrument Type", ["Futures", "Options", "Forwards", "Swaps"])

        # Top row
        col1, col2, col3 = st.columns(3)
        trade_date = col1.date_input("Trade Date", value=datetime.today())
        commodity = col2.text_input("Commodity")
        instrument_no = col3.text_input("Instrument No.")

        # Second row
        col4, col5, col6 = st.columns(3)
        exchange = col4.text_input("Exchange")
        index = col5.text_input("Index")
        lot_type = col6.selectbox("Lot Type", ["Standard", "Mini"])

        # Third row
        col7, col8 = st.columns(2)
        lot_size = col7.number_input("Lot Size", min_value=0.0)
        lots = col8.number_input("Lots", min_value=0.0)
        total_qty = lot_size * lots

        if instrument == "Options":
            col9, col10 = st.columns(2)
            option_type = col9.selectbox("Option Type", ["Call", "Put"])
            option_action = col10.selectbox("Action", ["Buy", "Sell"])

            col11, col12 = st.columns(2)
            strike_price = col11.number_input("Strike Price", min_value=0.0)
            premium = col12.number_input("Premium", min_value=0.0)

            total_amount = total_qty * premium
        else:
            col13, col14 = st.columns(2)
            book_price = col13.number_input("Book Price", min_value=0.0)
            market_price = col14.number_input("Market Price", min_value=0.0)
            total_amount = total_qty * book_price

        submitted = st.form_submit_button("✅ Submit Trade")

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
                "Action": option_action,
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

        st.success(f"✅ Trade Submitted Successfully. MTM = ${mtm:,.2f}")
        st.dataframe(pd.DataFrame([trade_details]), use_container_width=True)
