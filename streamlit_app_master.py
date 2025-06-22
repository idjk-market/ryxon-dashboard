import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="Ryxon Risk Intelligence Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# --- Improved Z-Score Calculation ---
def calculate_z_score(confidence):
    """
    Enhanced z-score calculation with better approximation
    """
    try:
        from scipy.stats import norm
        return norm.ppf(confidence / 100)
    except ImportError:
        # More accurate approximation without scipy
        p = confidence / 100
        if p <= 0 or p >= 1:
            return float('nan')
        
        # Coefficients for the approximation
        a1 = -3.969683028665376e+01
        a2 = 2.209460984245205e+02
        a3 = -2.759285104469687e+02
        a4 = 1.383577518672690e+02
        a5 = -3.066479806614716e+01
        a6 = 2.506628277459239e+00
        
        b1 = -5.447609879822406e+01
        b2 = 1.615858368580409e+02
        b3 = -1.556989798598866e+02
        b4 = 6.680131188771972e+01
        b5 = -1.328068155288572e+01
        
        c1 = -7.784894002430293e-03
        c2 = -3.223964580411365e-01
        c3 = -2.400758277161838e+00
        c4 = -2.549732539343734e+00
        c5 = 4.374664141464968e+00
        c6 = 2.938163982698783e+00
        
        d1 = 7.784695709041462e-03
        d2 = 3.224671290700398e-01
        d3 = 2.445134137142996e+00
        d4 = 3.754408661907416e+00
        
        # Define breakpoints
        p_low = 0.02425
        p_high = 1 - p_low
        
        if p < p_low:
            q = np.sqrt(-2*np.log(p))
            x = (((((c1*q+c2)*q+c3)*q+c4)*q+c5)*q+c6
            x = x / ((((d1*q+d2)*q+d3)*q+d4)
        elif p <= p_high:
            q = p - 0.5
            r = q*q
            x = (((((a1*r+a2)*r+a3)*r+a4)*r+a5)*r+a6)*q
            x = x / (((((b1*r+b2)*r+b3)*r+b4)*r+b5)
        else:
            q = np.sqrt(-2*np.log(1-p))
            x = -(((((c1*q+c2)*q+c3)*q+c4)*q+c5)*q+c6)
            x = x / ((((d1*q+d2)*q+d3)*q+d4))
        return x

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
        
        # Standardize column names (handle case sensitivity)
        df.columns = [col.strip().title() for col in df.columns]
        
        # --- Enhanced Filtering System ---
        st.markdown("### 📄 Filtered Trade Data")
        
        # Create filter UI in sidebar
        st.sidebar.header("🔍 Filter Options")
        
        # Initialize filtered dataframe
        filtered_df = df.copy()
        
        # Create dynamic filters for each column
        for col in filtered_df.columns:
            unique_values = filtered_df[col].dropna().unique()
            
            # For categorical columns
            if filtered_df[col].dtype == 'object' or len(unique_values) < 20:
                # Clean string values for better matching
                if filtered_df[col].dtype == 'object':
                    filtered_df[col] = filtered_df[col].astype(str).str.strip().str.title()
                    unique_values = filtered_df[col].dropna().unique()
                
                # Create multi-select dropdown
                selected = st.sidebar.multiselect(
                    f"Filter {col}",
                    options=sorted(unique_values),
                    default=sorted(unique_values),
                    key=f"filter_{col}"
                )
                if selected:  # Only filter if selections were made
                    filtered_df = filtered_df[filtered_df[col].isin(selected)]
            
            # For numeric columns
            elif pd.api.types.is_numeric_dtype(filtered_df[col]):
                min_val = float(filtered_df[col].min())
                max_val = float(filtered_df[col].max())
                step = (max_val - min_val) / 100 if (max_val - min_val) > 0 else 0.01
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
        
        # Display filtered data with better formatting
        st.dataframe(
            filtered_df.style.format({
                'Quantity': '{:.0f}',
                'Book Price': '{:.2f}',
                'Market Price': '{:.2f}',
                'MTM': '{:.2f}'
            }),
            use_container_width=True,
            height=min(400, 35 * (len(filtered_df) + 1))
        )

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
                # Case-insensitive trade action matching
                df["Realized PnL"] = np.where(
                    df["Trade Action"].str.strip().str.lower() == "sell", 
                    df["MTM"], 
                    0
                )
                df["Unrealized PnL"] = np.where(
                    df["Trade Action"].str.strip().str.lower() == "buy", 
                    df["MTM"], 
                    0
                )
                
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
            
            # Calculate z-score using our improved function
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
                        latest_var = df['1-Day VaR'].iloc[-1]
                        st.metric(
                            f"Latest 1-Day VaR ({confidence}% confidence)",
                            f"₹ {latest_var:,.2f}",
                            help=f"Calculated using z-score: {z:.4f}"
                        )
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

        st.success("✅ Risk dashboard successfully generated")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("ℹ️ Please check your file format and ensure it contains all required columns")

# --- Add requirements information ---
with st.expander("ℹ️ Setup Instructions", expanded=False):
    st.markdown("""
    ### Deployment Requirements
    
    For optimal performance, install these Python packages:
    
    ```requirements.txt
    streamlit
    pandas
    numpy
    plotly
    scipy
    ```
    
    The app includes a fallback z-score calculation if scipy is not available.
    """)
