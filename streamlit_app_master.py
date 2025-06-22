import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- Fixed Z-Score Calculation ---
def calculate_z_score(confidence):
    from scipy.stats import norm
    return norm.ppf(confidence / 100)

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])

if file:
    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)

        df.columns = [col.strip() for col in df.columns]  # Clean column names

        if "Trade Date" in df.columns:
            df["Trade Date"] = pd.to_datetime(df["Trade Date"], errors='coerce')

        # --- Enhanced Filtering ---
        st.markdown(f"### 📄 Trade Details: {file.name}")
        st.sidebar.header("🔍 Filter Options")
        filtered_df = df.copy()

        for col in filtered_df.columns:
            if filtered_df[col].dtype == 'object' or filtered_df[col].nunique() < 20:
                options = filtered_df[col].dropna().astype(str).unique().tolist()
                selected = st.sidebar.multiselect(f"Filter {col}", sorted(options), default=sorted(options), key=col)
                if selected:
                    filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected)]
            elif pd.api.types.is_numeric_dtype(filtered_df[col]):
                min_val = float(filtered_df[col].min())
                max_val = float(filtered_df[col].max())
                step = (max_val - min_val) / 100 if (max_val - min_val) > 0 else 1
                val_range = st.sidebar.slider(f"Range for {col}", min_val, max_val, (min_val, max_val), step=step)
                filtered_df = filtered_df[(filtered_df[col] >= val_range[0]) & (filtered_df[col] <= val_range[1])]

        st.dataframe(filtered_df, use_container_width=True)

        # --- MTM Calculation ---
        if all(x in df.columns for x in ["Book Price", "Market Price", "Quantity"]):
            df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
            st.metric("Total MTM Value", f"₹ {df['MTM'].sum():,.2f}")

        # --- PnL ---
        if "Trade Action" in df.columns and "MTM" in df.columns:
            df["Realized PnL"] = np.where(df["Trade Action"].str.lower() == "sell", df["MTM"], 0)
            df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower() == "buy", df["MTM"], 0)
            st.metric("Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
            st.metric("Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")

        # --- Value at Risk ---
        confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95)
        z = calculate_z_score(confidence)

        if "MTM" in df.columns and "Trade Date" in df.columns:
            df = df.sort_values("Trade Date")
            df["Daily Return"] = df["MTM"].pct_change().fillna(0)
            df["Rolling Std Dev"] = df["Daily Return"].rolling(window=10).std().fillna(0)
            df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()

            st.metric(f"Latest 1-Day VaR @ {confidence}%", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

        # --- Final Risk Summary ---
        st.markdown("### 📌 Final Risk Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("MTM", f"₹ {df['MTM'].sum():,.2f}")
        col2.metric("Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
        col3.metric("Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
        col4.metric("VaR", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

        # --- Bar Graph ---
        pnl_df = pd.DataFrame({
            "Metric": ["MTM", "Realized PnL", "Unrealized PnL"],
            "Value": [df['MTM'].sum(), df['Realized PnL'].sum(), df['Unrealized PnL'].sum()]
        })
        fig = px.bar(pnl_df, x="Metric", y="Value", text_auto=True, color="Metric",
                     title="PnL Breakdown", height=400)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
