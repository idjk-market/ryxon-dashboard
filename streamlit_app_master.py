import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- File Upload ---
file = st.file_uploader("Upload Trade Data", type=["csv", "xlsx"])
if file:
    df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
    df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    # --- Filter Section ---
    st.sidebar.header("🔍 Filter Options")
    with st.sidebar:
        commodity = st.multiselect("Select Commodity", df["Commodity"].unique(), default=df["Commodity"].unique())
        instr = st.multiselect("Select Instrument", df["Instrument Type"].unique(), default=df["Instrument Type"].unique())
        action = st.multiselect("Trade Action", df["Trade Action"].unique(), default=df["Trade Action"].unique())
        date_range = st.date_input("Trade Date Range", [df["Trade Date"].min(), df["Trade Date"].max()])

    df_filtered = df[
        (df["Commodity"].isin(commodity)) &
        (df["Instrument Type"].isin(instr)) &
        (df["Trade Action"].isin(action)) &
        (df["Trade Date"] >= pd.to_datetime(date_range[0])) &
        (df["Trade Date"] <= pd.to_datetime(date_range[1]))
    ]

    st.markdown("### 📄 Trade Data")
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

    # --- Expandable MTM ---
    with st.expander("📘 MTM Calculation"):
        df_filtered["MTM"] = (df_filtered["Market Price"] - df_filtered["Book Price"]) * df_filtered["Quantity"]
        st.dataframe(df_filtered[["Trade ID", "Commodity", "Instrument Type", "Quantity", "Book Price", "Market Price", "MTM"]])
        st.success(f"🔹 Total MTM: ₹ {df_filtered['MTM'].sum():,.2f}")

    # --- Expandable PnL ---
    with st.expander("📙 PnL Summary"):
        df_filtered["Realized PnL"] = np.where(df_filtered["Trade Action"] == "Sell", df_filtered["MTM"], 0)
        df_filtered["Unrealized PnL"] = np.where(df_filtered["Trade Action"] == "Buy", df_filtered["MTM"], 0)
        st.dataframe(df_filtered[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
        st.success(f"✅ Realized PnL: ₹ {df_filtered['Realized PnL'].sum():,.2f}")
        st.info(f"📌 Unrealized PnL: ₹ {df_filtered['Unrealized PnL'].sum():,.2f}")

    # --- Expandable VaR ---
    with st.expander("📕 Value at Risk (VaR)"):
        confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95)
        z_scores = {90: 1.28, 95: 1.65, 99: 2.33}
        z = z_scores[confidence]

        df_sorted = df_filtered.sort_values("Trade Date")
        df_sorted["Daily Return"] = df_sorted["MTM"].pct_change().fillna(0)
        df_sorted["Rolling Std Dev"] = df_sorted["Daily Return"].rolling(window=10).std().fillna(0)

        df_sorted["1-Day VaR"] = -1 * (df_sorted["Daily Return"].mean() - z * df_sorted["Rolling Std Dev"]) * df_sorted["MTM"].abs()
        st.dataframe(df_sorted[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]], use_container_width=True)

    # --- Final Risk Summary ---
    st.markdown("### 📊 Final Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total MTM", f"₹ {df_filtered['MTM'].sum():,.2f}")
    col2.metric("Realized PnL", f"₹ {df_filtered['Realized PnL'].sum():,.2f}")
    col3.metric("Unrealized PnL", f"₹ {df_filtered['Unrealized PnL'].sum():,.2f}")
    col4.metric("VaR ({confidence}%)", f"₹ {df_sorted['1-Day VaR'].iloc[-1]:,.2f}")

    # --- Visual Summary ---
    st.markdown("#### 🔢 PnL Breakdown Chart")
    pnl_chart = pd.DataFrame({
        'Type': ['MTM', 'Realized PnL', 'Unrealized PnL'],
        'Value': [df_filtered['MTM'].sum(), df_filtered['Realized PnL'].sum(), df_filtered['Unrealized PnL'].sum()]
    })
    fig = px.bar(pnl_chart, x='Type', y='Value', color='Type', title="PnL Composition", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Dashboard generated successfully.")
