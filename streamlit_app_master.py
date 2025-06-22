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
    df.columns = [col.strip().title() for col in df.columns]

    if "Trade Date" in df.columns:
        df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    # --- Filter Sidebar ---
    st.sidebar.header("🔍 Filter Options")
    filtered_df = df.copy()
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].nunique() < 20:
            options = df[col].dropna().unique().tolist()
            selected = st.sidebar.multiselect(f"Filter {col}", options, default=options)
            filtered_df = filtered_df[filtered_df[col].isin(selected)]
        elif np.issubdtype(df[col].dtype, np.number):
            min_val, max_val = float(df[col].min()), float(df[col].max())
            selected_range = st.sidebar.slider(f"Range for {col}", min_val, max_val, (min_val, max_val))
            filtered_df = filtered_df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

    # --- Main Trade Data Table ---
    st.markdown("### 📄 Trade Details (Search/Filter Any Column Below)")
    st.dataframe(filtered_df, use_container_width=True)

    # --- MTM Calculation ---
    with st.expander("📘 MTM Calculation"):
        if all(col in filtered_df.columns for col in ["Market Price", "Book Price", "Quantity"]):
            filtered_df["MTM"] = (filtered_df["Market Price"] - filtered_df["Book Price"]) * filtered_df["Quantity"]
            st.dataframe(filtered_df[["Trade Id", "Commodity", "Instrument Type", "Quantity", "Book Price", "Market Price", "MTM"]])
            st.success(f"🔹 Total MTM: ₹ {filtered_df['MTM'].sum():,.2f}")

    # --- PnL Summary ---
    with st.expander("📙 PnL Summary"):
        filtered_df["Realized PnL"] = np.where(filtered_df["Trade Action"].str.lower() == "sell", filtered_df["MTM"], 0)
        filtered_df["Unrealized PnL"] = np.where(filtered_df["Trade Action"].str.lower() == "buy", filtered_df["MTM"], 0)
        st.dataframe(filtered_df[["Trade Id", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
        st.success(f"✅ Realized PnL: ₹ {filtered_df['Realized PnL'].sum():,.2f}")
        st.info(f"📌 Unrealized PnL: ₹ {filtered_df['Unrealized PnL'].sum():,.2f}")

    # --- VaR Calculation ---
    with st.expander("📕 Value at Risk (VaR)"):
        confidence = st.slider("Select Confidence Level (%)", 90, 99, 95)
        z = {90: 1.28, 95: 1.65, 99: 2.33}.get(confidence, 1.65)

        df_sorted = filtered_df.sort_values("Trade Date")
        df_sorted["Daily Return"] = df_sorted["MTM"].pct_change().fillna(0)
        df_sorted["Rolling Std Dev"] = df_sorted["Daily Return"].rolling(window=10).std().fillna(0)
        df_sorted["1-Day VaR"] = -1 * (df_sorted["Daily Return"].mean() - z * df_sorted["Rolling Std Dev"]) * df_sorted["MTM"].abs()

        st.dataframe(df_sorted[["Trade Id", "Daily Return", "Rolling Std Dev", "1-Day VaR"]])
        st.metric(f"VaR ({confidence}%)", f"₹ {df_sorted['1-Day VaR'].iloc[-1]:,.2f}")

    # --- Historical VaR ---
    with st.expander("📗 Historical VaR"):
        try:
            hist_window = st.slider("Select Historical Lookback Days", 5, 100, 30)
            returns = filtered_df.sort_values("Trade Date")["MTM"].pct_change().dropna()
            hist_var_value = -np.percentile(returns, 100 - confidence) * filtered_df["MTM"].abs().sum()
            st.metric(f"Historical VaR ({confidence}% | {hist_window} days)", f"₹ {hist_var_value:,.2f}")
        except Exception as e:
            st.warning("Not enough data for Historical VaR")

    # --- Final Summary ---
    st.markdown("### 🧾 Final Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total MTM", f"₹ {filtered_df['MTM'].sum():,.2f}")
    col2.metric("Realized PnL", f"₹ {filtered_df['Realized PnL'].sum():,.2f}")
    col3.metric("Unrealized PnL", f"₹ {filtered_df['Unrealized PnL'].sum():,.2f}")
    col4.metric("VaR ({confidence}%)", f"₹ {df_sorted['1-Day VaR'].iloc[-1]:,.2f}")

    st.markdown("#### 📊 PnL Breakdown Chart")
    pnl_chart = pd.DataFrame({
        'Type': ['MTM', 'Realized PnL', 'Unrealized PnL'],
        'Value': [filtered_df['MTM'].sum(), filtered_df['Realized PnL'].sum(), filtered_df['Unrealized PnL'].sum()]
    })
    fig = px.bar(pnl_chart, x='Type', y='Value', color='Type', title="PnL Composition", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Dashboard generated successfully.")
