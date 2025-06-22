import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- Fallback Z-Score Calculation (if scipy not available) ---
def calculate_z_score(confidence):
    """
    Calculate z-score for given confidence level
    Uses scipy if available, otherwise uses approximation
    """
    try:
        from scipy.stats import norm
        return norm.ppf(confidence / 100)
    except ImportError:
        # Approximation if scipy not available
        st.warning("⚠️ SciPy not installed - using z-score approximation")
        p = confidence / 100
        if p <= 0 or p >= 1:
            return float('nan')
        t = np.sqrt(-2.0 * np.log(min(p, 1-p)))
        c0 = 2.515517
        c1 = 0.802853
        c2 = 0.010328
        d1 = 1.432788
        d2 = 0.189269
        d3 = 0.001308
        x = t - ((c0 + c1*t + c2*t**2) / (1 + d1*t + d2*t**2 + d3*t**3))
        return -x if p < 0.5 else x

# --- File Upload ---
file = st.file_uploader("📤 Upload Trade Data File (.csv or .xlsx)", type=["csv", "xlsx"])

if file:
    try:
        # Read file based on extension
        if file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        
        # Data Preprocessing
        if "Trade Date" in df.columns:
            df["Trade Date"] = pd.to_datetime(df["Trade Date"])
        
        # --- Dynamic Table Display with Improved Filters ---
        st.markdown("### 📄 Filtered Trade Data")
        
        # Create filter UI in sidebar
        st.sidebar.header("🔍 Filter Options")
        
        # Initialize filtered dataframe
        filtered_df = df.copy()
        
        # Create dynamic filters for each column
        for col in filtered_df.columns:
            unique_values = filtered_df[col].unique()
            
            # For categorical columns with limited unique values
            if filtered_df[col].dtype == 'object' or len(unique_values) < 20:
                selected = st.sidebar.multiselect(
                    f"Filter {col}",
                    options=sorted(unique_values),
                    default=sorted(unique_values),
                    key=f"filter_{col}"
                )
                filtered_df = filtered_df[filtered_df[col].isin(selected)]
            
            # For numeric columns
            elif pd.api.types.is_numeric_dtype(filtered_df[col]):
                min_val = float(filtered_df[col].min())
                max_val = float(filtered_df[col].max())
                step = (max_val - min_val) / 100
                val_range = st.sidebar.slider(
                    f"Range for {col}",
                    min_val, max_val, (min_val, max_val),
                    step=step,
                    key=f"range_{col}"
                )
                filtered_df = filtered_df[
                    (filtered_df[col] >= val_range[0]) & 
                    (filtered_df[col] <= val_range[1])
                ]
        
        # Display filtered data
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # --- MTM Calculation Section ---
        with st.expander("📘 MTM Calculation Logic", expanded=False):
            required_cols = ["Market Price", "Book Price", "Quantity"]
            if all(col in df.columns for col in required_cols):
                df["MTM"] = (df["Market Price"] - df["Book Price"]) * df["Quantity"]
                st.markdown("""
                **Calculation Formula:**  
                `MTM = (Market Price - Book Price) × Quantity`
                """)
                
                # Display MTM summary
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(
                        df[["Trade ID", "Commodity", "Instrument Type", "Trade Action", 
                            "Quantity", "Book Price", "Market Price", "MTM"]],
                        height=300
                    )
                with col2:
                    st.metric("Total MTM Value", f"₹ {df['MTM'].sum():,.2f}")
            else:
                st.error(f"Missing required columns for MTM calculation. Need: {', '.join(required_cols)}")

        # --- PnL Section ---
        with st.expander("📙 Realized & Unrealized PnL", expanded=False):
            if "Trade Action" in df.columns and "MTM" in df.columns:
                df["Realized PnL"] = np.where(df["Trade Action"].str.lower() == "sell", df["MTM"], 0)
                df["Unrealized PnL"] = np.where(df["Trade Action"].str.lower() == "buy", df["MTM"], 0)
                
                # Display PnL summary
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(
                        df[["Trade ID", "Trade Action", "MTM", "Realized PnL", "Unrealized PnL"]],
                        height=300
                    )
                with col2:
                    st.metric("Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
                    st.metric("Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
            else:
                st.error("Missing required columns for PnL calculation. Need: Trade Action, MTM")

        # --- Value at Risk (VaR) Section ---
        with st.expander("📕 Value at Risk (VaR)", expanded=False):
            confidence = st.slider(
                "Select Confidence Level (%)", 
                min_value=90, 
                max_value=99, 
                value=95, 
                step=1,
                help="The probability level for VaR calculation (e.g., 95% means 5% chance of exceeding the VaR)"
            )
            
            # Calculate z-score using our function
            z = calculate_z_score(confidence)
            
            if "MTM" in df.columns and "Trade Date" in df.columns:
                df = df.sort_values("Trade Date")
                
                # Calculate daily returns and rolling standard deviation
                df["Daily Return"] = df["MTM"].pct_change().fillna(0)
                window_size = min(10, len(df))
                df["Rolling Std Dev"] = df["Daily Return"].rolling(window=window_size).std().fillna(0)
                
                # Calculate 1-Day VaR
                df["1-Day VaR"] = -1 * (df["Daily Return"].mean() - z * df["Rolling Std Dev"]) * df["MTM"].abs()
                
                # Display VaR results
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(
                        df[["Trade ID", "Daily Return", "Rolling Std Dev", "1-Day VaR"]],
                        height=300
                    )
                with col2:
                    if len(df) > 0:
                        st.warning(f"⚠️ Latest 1-Day VaR: ₹ {df['1-Day VaR'].iloc[-1]:,.2f} at {confidence}% confidence")
                        st.info(f"Z-Score used: {z:.4f}")
                    else:
                        st.warning("Insufficient data for VaR calculation")
            else:
                st.error("Missing required columns for VaR calculation. Need: MTM, Trade Date")

        # --- Final Risk Metrics Summary ---
        st.markdown("### 🧾 Final Risk Summary")
        
        # Create metrics columns
        cols = st.columns(4)
        metrics = [
            ("📉 MTM", "MTM"),
            ("📈 Realized PnL", "Realized PnL"),
            ("🧮 Unrealized PnL", "Unrealized PnL"),
            (f"🔻 VaR ({confidence}%)", "1-Day VaR")
        ]
        
        for i, (title, col_name) in enumerate(metrics):
            if col_name in df.columns:
                value = df[col_name].sum() if col_name != "1-Day VaR" else df[col_name].iloc[-1] if len(df) > 0 else 0
                cols[i].metric(title, f"₹ {value:,.2f}")

        # --- PnL Breakdown Visualization ---
        st.markdown("#### 📊 PnL Breakdown")
        
        # Prepare chart data
        chart_data = []
        for metric in ["MTM", "Realized PnL", "Unrealized PnL"]:
            if metric in df.columns:
                chart_data.append({
                    "Metric": metric.replace("PnL", " PnL"),
                    "Value": df[metric].sum(),
                    "Type": "Profit" if df[metric].sum() >= 0 else "Loss"
                })
        
        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            fig = px.bar(
                chart_df,
                x="Metric",
                y="Value",
                color="Type",
                text=[f"₹ {x:,.2f}" for x in chart_df["Value"]],
                color_discrete_map={"Profit": "#2ecc71", "Loss": "#e74c3c"},
                title="PnL Components Overview"
            )
            fig.update_layout(
                yaxis_title="Amount (₹)",
                xaxis_title="Metric",
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No PnL data available for visualization")

        # --- Additional Visualizations ---
        st.markdown("#### 📈 MTM Distribution")
        if "MTM" in df.columns:
            fig = px.histogram(df, x="MTM", nbins=50, title="MTM Value Distribution")
            st.plotly_chart(fig, use_container_width=True)

        st.success("✅ Risk dashboard successfully generated")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("ℹ️ Please check your file format and ensure it contains all required columns")

# --- Add requirements information ---
with st.expander("ℹ️ Setup Instructions", expanded=False):
    st.markdown("""
    ### Deployment Requirements
    
    Ensure your environment has these Python packages installed:
    
    ```requirements.txt
    streamlit
    pandas
    numpy
    plotly
    scipy
    ```
    
    The app will work without scipy but with slightly less accurate VaR calculations.
    """)
