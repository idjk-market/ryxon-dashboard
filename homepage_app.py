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
    st.markdown("Fill the trade form based on selected instrument.")

    with st.form("horizontal_trade_form"):
        instrument = st.selectbox("Instrument Type", ["Futures", "Options", "Forwards", "Swaps"])

        row1 = st.columns(6)
        trade_date = row1[0].date_input("Trade Date", value=datetime.today())
        commodity = row1[1].text_input("Commodity")
        instrument_no = row1[2].text_input("Instrument No.")
        exchange = row1[3].text_input("Exchange")
        index = row1[4].text_input("Index")
        position = row1[5].selectbox("Position", ["Long", "Short"])

        row2 = st.columns(4)
        lot_type = row2[0].selectbox("Lot Type", ["Standard", "Mini"])
        lot_size = row2[1].number_input("Lot Size", min_value=0.0)
        lots = row2[2].number_input("Lots", min_value=0.0)
        total_qty = lot_size * lots

        if instrument == "Options":
            row3 = st.columns(4)
            option_type = row3[0].selectbox("Option Type", ["Call", "Put"])
            option_action = row3[1].selectbox("Action", ["Buy", "Sell"])
            strike_price = row3[2].number_input("Strike Price", min_value=0.0)
            premium = row3[3].number_input("Premium", min_value=0.0)
            total_amount = total_qty * premium
        else:
            row4 = st.columns(2)
            book_price = row4[0].number_input("Book Price", min_value=0.0)
            market_price = row4[1].number_input("Market Price", min_value=0.0)
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
                "Position": position,
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
                "Position": position,
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
