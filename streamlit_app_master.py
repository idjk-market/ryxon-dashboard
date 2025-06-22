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
    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    df.columns = [col.strip().title() for col in df.columns]

    if "Trade Date" in df.columns:
        df["Trade Date"] = pd.to_datetime(df["Trade Date"])

    st.markdown("### 📄 Trade Details (With Dropdown Filters)")

    # --- Dropdown Filtering Logic ---
    filtered_df = df.copy()
    with st.expander("🔍 Filter Columns"):
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].nunique() < 50:
                unique_vals = df[col].dropna().unique().tolist()
                selected_vals = st.multiselect(f"Filter by {col}", options=sorted(unique_vals), default=unique_vals)
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
            elif np.issubdtype(df[col].dtype, np.number):
                min_val, max_val = df[col].min(), df[col].max()
                selected_range = st.slider(f"Range for {col}", min_value=float(min_val), max_value=float(max_val), value=(float(min_val), float(max_val)))
                filtered_df = filtered_df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

    st.dataframe(filtered_df, use_container_width=True, height=500)

    # --- MTM Calculation ---
    with st.expander("📘 MTM Calculation"):
        if all(col in filtered_df.columns for col in ["Market Price", "Book Price", "Quantity"]):
            filtered_df["MTM"] = (filtered_df["Market Price"] - filtered_df["Book Price"]) * filtered_df["Quantity"]
            st.write("**Formula:** MTM = (Market Price - Book Price) × Quantity")
            st.metric("Total MTM", f"₹ {filtered_df['MTM'].sum():,.2f}")
            st.dataframe(filtered_df[["Market Price", "Book Price", "Quantity", "MTM"]])
        else:
            st.warning("Missing columns for MTM Calculation")

    # --- PnL Summary ---
    with st.expander("📙 Realized & Unrealized PnL"):
        if "Trade Action" in filtered_df.columns and "MTM" in filtered_df.columns:
            filtered_df["Realized PnL"] = np.where(filtered_df["Trade Action"].str.lower() == "sell", filtered_df["MTM"], 0)
            filtered_df["Unrealized PnL"] = np.where(filtered_df["Trade Action"].str.lower() == "buy", filtered_df["MTM"], 0)
            st.metric("Realized PnL", f"₹ {filtered_df['Realized PnL'].sum():,.2f}")
            st.metric("Unrealized PnL", f"₹ {filtered_df['Unrealized PnL'].sum():,.2f}")
            st.dataframe(filtered_df[["Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
        else:
            st.warning("Missing columns for PnL calculation")

    # --- VaR Section ---
    with st.expander("📕 Value at Risk (VaR)"):
        confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95)
        from scipy.stats import norm
        z = norm.ppf(confidence / 100)

        if "MTM" in filtered_df.columns and "Trade Date" in filtered_df.columns:
            filtered_df = filtered_df.sort_values("Trade Date")
            filtered_df["Daily Return"] = filtered_df["MTM"].pct_change().fillna(0)
            filtered_df["Rolling Std"] = filtered_df["Daily Return"].rolling(window=10).std().fillna(0)
            filtered_df["1-Day VaR"] = -1 * (filtered_df["Daily Return"].mean() - z * filtered_df["Rolling Std"]) * filtered_df["MTM"].abs()
            st.metric("Latest 1-Day VaR", f"₹ {filtered_df['1-Day VaR'].iloc[-1]:,.2f}")
            st.dataframe(filtered_df[["Trade Date", "Daily Return", "Rolling Std", "1-Day VaR"]])
        else:
            st.warning("MTM and Trade Date required for VaR")

    # --- Final Risk Summary ---
    st.markdown("### 🧾 Final Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 MTM", f"₹ {filtered_df['MTM'].sum():,.2f}" if "MTM" in filtered_df else "N/A")
    col2.metric("📈 Realized PnL", f"₹ {filtered_df['Realized PnL'].sum():,.2f}" if "Realized PnL" in filtered_df else "N/A")
    col3.metric("🧮 Unrealized PnL", f"₹ {filtered_df['Unrealized PnL'].sum():,.2f}" if "Unrealized PnL" in filtered_df else "N/A")
    col4.metric(f"🔻 VaR ({confidence}%)", f"₹ {filtered_df['1-Day VaR'].iloc[-1]:,.2f}" if "1-Day VaR" in filtered_df else "N/A")

    # --- Chart ---
    st.markdown("#### 📊 PnL Breakdown")
    chart_data = []
    for metric in ["MTM", "Realized PnL", "Unrealized PnL"]:
        if metric in filtered_df:
            chart_data.append({"Metric": metric, "Value": filtered_df[metric].sum(), "Type": "Profit" if filtered_df[metric].sum() >= 0 else "Loss"})

    if chart_data:
        chart_df = pd.DataFrame(chart_data)
        fig = px.bar(chart_df, x="Metric", y="Value", color="Type", text="Value",
                     color_discrete_map={"Profit": "green", "Loss": "red"})
        st.plotly_chart(fig, use_container_width=True)

    st.success("✅ Dashboard Ready.")
