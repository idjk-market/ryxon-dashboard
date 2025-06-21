import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ryxon MTM Daily PnL", layout="wide")
st.title("📊 Ryxon – MTM Daily PnL Summary")

uploaded_file = st.file_uploader("📥 Upload Ryxon MTM Trade Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, parse_dates=["Date"])
    st.success("✅ File uploaded successfully!")

    # Show the raw data
    st.subheader("📄 Trade Data")
    st.dataframe(df)

    # Group by date for daily PnL
    st.subheader("📅 Daily MTM PnL Summary")
    df_grouped = df.groupby("Date").agg(
        Daily_MTM_PnL=("MTM PnL", "sum"),
        Total_Trades=("Trade ID", "count")
    ).reset_index()

    st.dataframe(df_grouped)

    # Plotting
    st.subheader("📈 MTM PnL Over Time")
    fig, ax = plt.subplots()
    ax.plot(df_grouped["Date"], df_grouped["Daily_MTM_PnL"], marker='o', linestyle='-')
    ax.set_xlabel("Date")
    ax.set_ylabel("MTM PnL")
    ax.set_title("Daily MTM PnL Trend")
    st.pyplot(fig)

    # Download option
    st.download_button(
        label="📥 Download Daily PnL File",
        data=df_grouped.to_csv(index=False),
        file_name="ryxon_daily_pnl.csv",
        mime="text/csv"
    )

else:
    st.info("⬆️ Upload the MTM Excel file to get started.")
