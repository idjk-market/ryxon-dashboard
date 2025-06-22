import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])
if file:
    df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
    df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    # --- Dynamic Table Display ---
    st.markdown("### 📄 Filtered Trade Data")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- MTM Calculation Section ---
    with st.expander("📘 MTM Calculation Logic"):
        df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
        st.markdown("Calculated MTM = (Market Price - Book Price) × Quantity")
        st.dataframe(df[["Trade ID", "Commodity", "Instrument Type", "Trade Action", "Quantity", "Book Price", "Market Price", "MTM"]])
        st.success(f"🔹 Total MTM Value: ₹ {df['MTM'].sum():,.2f}")

    # --- PnL Section ---
    with st.expander("📙 Realized & Unrealized PnL"):
        df["Realized PnL"] = np.where(df["Trade Action"] == "Sell", df["MTM"], 0)
        df["Unrealized PnL"] = np.where(df["Trade Action"] == "Buy", df["MTM"], 0)
        st.dataframe(df[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
        st.success(f"✅ Realized PnL: ₹ {df['Realized PnL'].sum():,.2f}")
        st.info(f"📌 Unrealized PnL: ₹ {df['Unrealized PnL'].sum():,.2f}")

    # --- Value at Risk (VaR) Section ---
    with st.expander("📕 Value at Risk (VaR)"):
        confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95)
        z = np.interp(confidence, [90, 95, 99], [1.28, 1.65, 2.33])  # Interpolated z-value

        df = df.sort_values("Trade Date")
        df["Daily Return"] = df["MTM"].pct_change().fillna(0)
        df["Rolling Std Dev"] = df["Daily Return"].rolling(window=10).std().fillna(0)
        df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()

        st.dataframe(df[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]])
        st.warning(f"⚠️ Latest 1-Day VaR: ₹ {df['1-Day VaR'].iloc[-1]:,.2f} at {confidence}% confidence")

    # --- Final Risk Metrics Summary ---
    st.markdown("### 🧾 Final Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 MTM", f"₹ {df['MTM'].sum():,.2f}")
    col2.metric("📈 Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
    col3.metric("🧮 Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
    col4.metric(f"🔻 VaR ({confidence}%)", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

    # --- PnL Breakdown Bar Chart ---
    st.markdown("#### 📊 PnL Breakdown Chart")
    chart_df = pd.DataFrame({
        "Type": ["MTM", "Realized PnL", "Unrealized PnL"],
        "Value": [df["MTM"].sum(), df["Realized PnL"].sum(), df["Unrealized PnL"].sum()]
    })
    fig = px.bar(chart_df, x="Type", y="Value", color="Type", text_auto=True, title="PnL Components Overview")
    st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Risk dashboard successfully generated.")
