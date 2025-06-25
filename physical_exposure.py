import streamlit as st

st.title("🏭 Physical Exposure Entry")

with st.form("exposure_form"):
    exposure_date = st.date_input("Exposure Date")
    commodity = st.selectbox("Commodity", ["Gold", "Silver", "Crude", "Copper"])
    location = st.text_input("Storage Location / Entity")
    quantity = st.number_input("Quantity Held", min_value=0.0)
    expected_price = st.number_input("Expected Price", min_value=0.0)

    submitted = st.form_submit_button("Add Exposure")

if submitted:
    st.success(f"{commodity} exposure of {quantity} units recorded at expected price ${expected_price}")
