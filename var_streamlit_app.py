import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ryxon VaR Dashboard", layout="wide")
st.title("📉 Ryxon – Value at Risk (VaR) Dashboard")

uploaded_file = st.file_uploader("📁 Upload VaR Excel File", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Show raw data
    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    # Display VaR Summary
    st.subheader("📊 Value at Risk Summary")
    var_95 = df['1-Day VaR 95%'].iloc[0] if '1-Day VaR 95%' in df.columns else 'N/A'
    var_99 = df['1-Day VaR 99%'].iloc[0] if '1-Day VaR 99%' in df.columns else 'N/A'

    st.markdown(f"**1-Day VaR @ 95% Confidence:** ₹ {var_95:,.2f}")
    st.markdown(f"**1-Day VaR @ 99% Confidence:** ₹ {var_99:,.2f}")

    # Show formula used
    st.subheader("🧮 Formula Used")
    st.markdown(f"- 95% VaR Formula: `{df['VaR Formula 95%'].iloc[0]}`")
    st.markdown(f"- 99% VaR Formula: `{df['VaR Formula 99%'].iloc[0]}`")

    # Chart of PnL
    st.subheader("📈 Daily PnL Trend")
    fig, ax = plt.subplots()
    ax.plot(df['Date'], df['Daily PnL'], marker='o', linestyle='-', color='blue')
    ax.set_title("Daily PnL")
    ax.set_xlabel("Date")
    ax.set_ylabel("PnL")
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("👆 Please upload the file 'ryxon_var_from_trade.xlsx' to proceed.")
