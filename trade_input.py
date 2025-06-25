import streamlit as st
import pandas as pd

st.title("📝 Manual Trade Entry")

st.markdown("Enter trade details below. This is useful for paper trading or strategy simulation.")

with st.form("trade_form"):
    trade_date = st.date_input("Trade Date")
    commodity = st.selectbox("Commodity", ["Gold", "Silver", "Crude", "Copper"])
    instrument = st.selectbox("Instrument Type", ["Future", "Option", "Swap"])
    direction = st.selectbox("Trade Direction", ["Buy", "Sell"])
    quantity = st.number_input("Quantity", min_value=0.0)
    book_price = st.number_input("Book Price", min_value=0.0)
    market_price = st.number_input("Market Price", min_value=0.0)
    
    submitted = st.form_submit_button("Submit Trade")

if submitted:
    mtm = (market_price - book_price) * quantity if direction == "Buy" else (book_price - market_price) * quantity
    st.success(f"Trade submitted successfully! MTM = ${mtm:,.2f}")

    new_trade = pd.DataFrame([{
        "Trade Date": trade_date,
        "Commodity": commodity,
        "Instrument Type": instrument,
        "Trade Action": direction,
        "Quantity": quantity,
        "Book Price": book_price,
        "Market Price": market_price,
        "MTM": mtm
    }])

    st.dataframe(new_trade, use_container_width=True)
