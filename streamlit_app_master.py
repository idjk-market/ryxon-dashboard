import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- Helper: Standardize and ensure required columns ---
def clean_dataframe(df):
    df.columns = [col.strip().title() for col in df.columns]
    required_cols = ["Trade Id", "Commodity", "Instrument Type", "Trade Action", "Quantity", "Book Price", "Market Price", "Trade Date"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan
    df["Trade Date"] = pd.to_datetime(df["Trade Date"], errors='coerce')
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')
    df["Book Price"] = pd.to_numeric(df["Book Price"], errors='coerce')
    df["Market Price"] = pd.to_numeric(df["Market Price"], errors='coerce')
    return df[required_cols]

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])

if file:
    try:
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)

        df = clean_dataframe(df)

        st.markdown("### 📄 Filtered Trade Data (Search/Filter Any Column Below 👇)")
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(enableRowGroup=True, enablePivot=True, enableValue=True, editable=False, filter=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()
        AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, height=400, fit_columns_on_grid_load=True)

        with st.expander("📘 MTM Calculation Logic", expanded=False):
            df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
            st.write("**Formula:** MTM = (Market Price - Book Price) × Quantity")
            st.dataframe(df[["Trade Id", "Quantity", "Book Price", "Market Price", "MTM"]])

        with st.expander("📙 Realized & Unrealized PnL", expanded=False):
            df["Realized PnL"] = np.where(df["Trade Action"].str.lower() == "sell", df["MTM"], 0)
            df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower() == "buy", df["MTM"], 0)
            st.dataframe(df[["Trade Id", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
            st.metric("Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
            st.metric("Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")

        with st.expander("📕 Value at Risk (VaR)", expanded=False):
            confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95)
            z = {90:1.28, 91:1.34, 92:1.41, 93:1.48, 94:1.55, 95:1.65, 96:1.75, 97:1.88, 98:2.05, 99:2.33}[confidence]
            df = df.sort_values("Trade Date")
            df["Daily Return"] = df["MTM"].pct_change().fillna(0)
            df["Rolling Std Dev"] = df["Daily Return"].rolling(window=5).std().fillna(0)
            df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()
            st.dataframe(df[["Trade Id", "Daily Return", "Rolling Std Dev", "1-Day VaR"]])
            st.metric(f"Latest 1-Day VaR ({confidence}% Confidence)", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

        st.markdown("### 🧾 Final Risk Summary")
        cols = st.columns(4)
        summary = [
            ("📉 MTM", "MTM"),
            ("📈 Realized PnL", "Realized PnL"),
            ("🧮 Unrealized PnL", "Unrealized PnL"),
            (f"🔻 VaR ({confidence}%)", "1-Day VaR")
        ]
        for i, (label, colname) in enumerate(summary):
            value = df[colname].iloc[-1] if "VaR" in colname else df[colname].sum()
            cols[i].metric(label, f"₹ {value:,.2f}")

        with st.expander("📊 PnL Breakdown Chart"):
            data = [
                {"Metric": "MTM", "Value": df["MTM"].sum()},
                {"Metric": "Realized PnL", "Value": df["Realized PnL"].sum()},
                {"Metric": "Unrealized PnL", "Value": df["Unrealized PnL"].sum()}
            ]
            chart_df = pd.DataFrame(data)
            chart_df["Type"] = chart_df["Value"].apply(lambda x: "Profit" if x >= 0 else "Loss")
            fig = px.bar(chart_df, x="Metric", y="Value", color="Type", text="Value",
                         color_discrete_map={"Profit": "green", "Loss": "red"})
            st.plotly_chart(fig, use_container_width=True)

        st.success("✅ Dashboard generated successfully.")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
else:
    st.info("📥 Please upload a trade file to begin.")
