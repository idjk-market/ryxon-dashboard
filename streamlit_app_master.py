import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])
if file:
    try:
        df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
        
        # Convert date column if exists
        if "Trade Date" in df.columns:
            df["Trade Date"] = pd.to_datetime(df["Trade Date"])
        
        # --- Dynamic Table Display with Improved Filters ---
        st.markdown("### 📄 Filtered Trade Data")
        
        # Create a copy of the dataframe for filtering
        filtered_df = df.copy()
        
        # Create filter UI in sidebar
        st.sidebar.header("Filter Options")
        
        # Dynamic filters for each column
        for column in filtered_df.columns:
            if filtered_df[column].nunique() < 20:  # For columns with few unique values
                unique_values = filtered_df[column].unique()
                selected_values = st.sidebar.multiselect(
                    f"Filter by {column}",
                    options=unique_values,
                    default=unique_values,
                    key=f"filter_{column}"
                )
                filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
            elif pd.api.types.is_numeric_dtype(filtered_df[column]):
                min_val = float(filtered_df[column].min())
                max_val = float(filtered_df[column].max())
                slider_range = st.sidebar.slider(
                    f"Range for {column}",
                    min_val, max_val, (min_val, max_val),
                    key=f"range_{column}"
                )
                filtered_df = filtered_df[
                    (filtered_df[column] >= slider_range[0]) & 
                    (filtered_df[column] <= slider_range[1])
                ]
        
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # --- MTM Calculation Section ---
        with st.expander("📘 MTM Calculation Logic"):
            # Ensure required columns exist
            required_cols = ["Market Price", "Book Price", "Quantity"]
            if all(col in df.columns for col in required_cols):
                df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
                st.markdown("Calculated MTM = (Market Price - Book Price) × Quantity")
                st.dataframe(df[["Trade ID", "Commodity", "Instrument Type", "Trade Action", "Quantity", "Book Price", "Market Price", "MTM"]])
                st.success(f"🔹 Total MTM Value: ₹ {df['MTM'].sum():,.2f}")
            else:
                st.error("Missing required columns for MTM calculation. Need: Market Price, Book Price, Quantity")

        # --- PnL Section ---
        with st.expander("📙 Realized & Unrealized PnL"):
            if "Trade Action" in df.columns and "MTM" in df.columns:
                df["Realized PnL"] = np.where(df["Trade Action"] == "Sell", df["MTM"], 0)
                df["Unrealized PnL"] = np.where(df["Trade Action"] == "Buy", df["MTM"], 0)
                st.dataframe(df[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]])
                st.success(f"✅ Realized PnL: ₹ {df['Realized PnL'].sum():,.2f}")
                st.info(f"📌 Unrealized PnL: ₹ {df['Unrealized PnL'].sum():,.2f}")
            else:
                st.error("Missing required columns for PnL calculation. Need: Trade Action, MTM")

        # --- Value at Risk (VaR) Section ---
        with st.expander("📕 Value at Risk (VaR)"):
            confidence = st.slider("Select Confidence Level (%)", min_value=90, max_value=99, value=95, step=1)
            
            # Calculate z-score dynamically using inverse normal distribution
            z = norm.ppf(confidence / 100)
            
            if "MTM" in df.columns and "Trade Date" in df.columns:
                df = df.sort_values("Trade Date")
                df["Daily Return"] = df["MTM"].pct_change().fillna(0)
                
                # Ensure we have enough data for rolling calculations
                window_size = min(10, len(df))
                df["Rolling Std Dev"] = df["Daily Return"].rolling(window=window_size).std().fillna(0)
                df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()

                st.dataframe(df[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]])
                
                if len(df) > 0:
                    st.warning(f"⚠️ Latest 1-Day VaR: ₹ {df['1-Day VaR'].iloc[-1]:,.2f} at {confidence}% confidence")
                else:
                    st.warning("Insufficient data for VaR calculation")
            else:
                st.error("Missing required columns for VaR calculation. Need: MTM, Trade Date")

        # --- Final Risk Metrics Summary ---
        st.markdown("### 🧾 Final Risk Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        if "MTM" in df.columns:
            col1.metric("📉 MTM", f"₹ {df['MTM'].sum():,.2f}")
        if "Realized PnL" in df.columns:
            col2.metric("📈 Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
        if "Unrealized PnL" in df.columns:
            col3.metric("🧮 Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
        if "1-Day VaR" in df.columns and len(df) > 0:
            col4.metric(f"🔻 VaR ({confidence}%)", f"₹ {df['1-Day VaR'].iloc[-1]:,.2f}")

        # --- PnL Breakdown Bar Chart ---
        st.markdown("#### 📊 PnL Breakdown Chart")
        chart_data = []
        if "MTM" in df.columns:
            chart_data.append({"Type": "MTM", "Value": df["MTM"].sum()})
        if "Realized PnL" in df.columns:
            chart_data.append({"Type": "Realized PnL", "Value": df["Realized PnL"].sum()})
        if "Unrealized PnL" in df.columns:
            chart_data.append({"Type": "Unrealized PnL", "Value": df["Unrealized PnL"].sum()})
        
        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            fig = px.bar(chart_df, x="Type", y="Value", color="Type", text_auto=True, 
                         title="PnL Components Overview")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No PnL data available for chart")

        st.success("✅ Risk dashboard successfully generated.")
        
    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
