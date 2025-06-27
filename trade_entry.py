import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Trade Entry", layout="wide")
st.title("📝 Manual Trade Entry")

if 'trade_book' not in st.session_state:
    st.session_state.trade_book = []
if 'trade_counter' not in st.session_state:
    st.session_state.trade_counter = 1

with st.form("trade_form"):
    st.subheader("Trade Details")
    trade_id = st.session_state.trade_counter
    col1, col2, col3, col4 = st.columns(4)
    instrument = col1.selectbox("Instrument Type", ["Futures", "Options", "Forwards", "Swaps"])
    trade_date = col2.date_input("Trade Date", value=datetime.today())
    position = col3.selectbox("Position", ["Long", "Short"])
    commodity = col4.text_input("Commodity")

    col5, col6, col7, col8 = st.columns(4)
    instrument_no = col5.text_input("Instrument No.")
    exchange = col6.text_input("Exchange")
    index = col7.text_input("Index")
    lot_type = col8.selectbox("Lot Type", ["Standard", "Mini"])

    col9, col10, col11 = st.columns(3)
    lot_size = col9.number_input("Lot Size", min_value=0.0, value=1.0)
    lots = col10.number_input("Lots", min_value=0.0, value=1.0)
    total_qty = lot_size * lots
    col11.number_input("Total Qty", value=total_qty, disabled=True)

    if instrument == "Options":
        col12, col13, col14, col15 = st.columns(4)
        option_type = col12.selectbox("Option Type", ["Call", "Put"])
        option_action = col13.selectbox("Action", ["Buy", "Sell"])
        strike_price = col14.number_input("Strike Price", min_value=0.0, value=0.0)
        premium = col15.number_input("Premium", min_value=0.0, value=0.0)
        total_amount = total_qty * premium
        st.number_input("Total Amount", value=total_amount, disabled=True)
    else:
        col16, col17 = st.columns(2)
        book_price = col16.number_input("Book Price", min_value=0.0, value=0.0)
        market_price = col17.number_input("Market Price", min_value=0.0, value=0.0)
        total_amount = total_qty * book_price
        st.number_input("Total Amount", value=total_amount, disabled=True)

    expiry_date = st.date_input("Expiry Date (optional)")
    counterparty = st.text_input("Counterparty")

    submitted = st.form_submit_button("✅ Submit Trade")

if submitted:
    st.session_state.trade_counter += 1
    if instrument == "Options":
        mtm = total_qty * premium if option_action == "Sell" else -total_qty * premium
        trade = {
            "Trade ID": trade_id,
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
            "MTM": mtm,
            "Expiry": expiry_date,
            "Counterparty": counterparty
        }
    else:
        mtm = (market_price - book_price) * total_qty
        trade = {
            "Trade ID": trade_id,
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
            "MTM": mtm,
            "Expiry": expiry_date,
            "Counterparty": counterparty
        }

    st.session_state.trade_book.append(trade)
    st.success(f"✅ Trade #{trade_id} submitted. MTM = ${mtm:,.2f}")
    st.dataframe(pd.DataFrame([trade]), use_container_width=True)

