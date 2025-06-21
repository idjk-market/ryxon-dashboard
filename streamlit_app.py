
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ryxon - Risk Intelligence", layout="wide")

st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")
st.caption("Markets from the desk of djk")

# Sidebar navigation
st.sidebar.title("📁 Upload Your Trade File")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv", "xlsx"])

# Branding footer
st.markdown("---")
st.markdown("© 2025 Ryxon Technologies | Built by djk")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("✅ Uploaded Trade Data")
        st.dataframe(df)

        if all(col in df.columns for col in ["Instrument", "Quantity", "Book Price", "Market Price"]):
            df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
            st.subheader("📉 MTM Calculation")
            st.dataframe(df[["Instrument", "Quantity", "Book Price", "Market Price", "MTM"]])

            total_mtm = df["MTM"].sum()
            st.metric("Total MTM", f"₹ {total_mtm:,.2f}")

            st.subheader("📊 VaR (Coming Soon)")
            st.info("VaR calculation module will be added in the next version.")
        else:
            st.warning("Your file must contain columns: Instrument, Quantity, Book Price, Market Price")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Upload a trade file to begin. Sample format: Instrument, Quantity, Book Price, Market Price")

# Paper hedge input (placeholder)
st.sidebar.title("📝 Paper Hedge Simulation")
st.sidebar.text_input("Instrument")
st.sidebar.number_input("Strike Price", min_value=0.0, step=0.1)
st.sidebar.number_input("Premium", min_value=0.0, step=0.1)
st.sidebar.number_input("Quantity", min_value=1, step=1)
st.sidebar.selectbox("Type", ["Call Buy", "Call Sell", "Put Buy", "Put Sell"])
st.sidebar.button("Simulate Hedge")
