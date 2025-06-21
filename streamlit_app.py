import streamlit as st
import pandas as pd
import numpy as np
from mtm_calculator import calculate_mtm  # ✅ importing new MTM logic

st.set_page_config(page_title="Ryxon - Risk Intelligence", layout="wide")

st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")
st.caption("Markets from the desk of djk")

st.sidebar.title("📁 Upload Your Trade File")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

st.markdown("---")
st.markdown("© 2025 Ryxon Technologies | Built by djk")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("✅ Uploaded Trade Data")
        st.dataframe(df)

        required_cols = ["Trade Action", "Quantity", "Book Price", "Market Price"]
        if all(col in df.columns for col in required_cols):
            df = calculate_mtm(df)  # ✅ Use our imported MTM function
            st.subheader("📉 MTM Calculation")
            st.dataframe(df[["Trade Action", "Quantity", "Book Price", "Market Price", "MTM"]])

            total_mtm = df["MTM"].sum()
            st.metric("Total MTM", f"₹ {total_mtm:,.2f}")

        else:
            st.warning("Missing required columns: Trade Action, Quantity, Book Price, Market Price")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Upload a trade file to begin. Format must include: Trade Action, Quantity, Book Price, Market Price")
