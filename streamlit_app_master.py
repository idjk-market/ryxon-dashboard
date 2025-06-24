import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(layout="wide")
st.title("📊 Ryxon Risk Management Dashboard")

# Upload Excel File - accept both xlsx and csv
uploaded_file = st.sidebar.file_uploader(
    "Upload Trade File", 
    type=["xlsx", "csv"],
    help="Upload your trade data in Excel or CSV format"
)

@st.cache_data
def load_data(file):
    """Load data from either Excel or CSV file with error handling"""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            # Use openpyxl engine for Excel files
            return pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def validate_data(df):
    """Check if required columns exist"""
    required_columns = {'Book Price', 'Market Price', 'Quantity', 'Trade Action'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        st.error(f"Missing required columns: {', '.join(missing)}")
        return False
    return True

def calculate_mtm(df):
    """Calculate Mark-to-Market value"""
    try:
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        return df
    except Exception as e:
        st.error(f"Error calculating MTM: {str(e)}")
        return df

def calculate_pnl(df):
    """Calculate Realized and Unrealized PnL"""
    try:
        df['Realized PnL'] = np.where(
            df['Trade Action'].str.lower() == 'sell',
            (df['Market Price'] - df['Book Price']) * df['Quantity'],
            0
        )
        df['Unrealized PnL'] = df['MTM'] - df['Realized PnL']
        return df
    except Exception as e:
        st.error(f"Error calculating PnL: {str(e)}")
        return df

def calculate_var(df, confidence_level=95):
    """Calculate Value at Risk"""
    try:
        df['Daily Return'] = df['MTM'].pct_change().fillna(0)
        sorted_returns = np.sort(df['Daily Return'].dropna())
        var_percentile = 100 - confidence_level
        var_value = -np.percentile(sorted_returns, var_percentile) * df['MTM'].sum()
        return var_value
    except Exception as e:
        st.error(f"Error calculating VaR: {str(e)}")
        return 0

def show_historical_var_module(df):
    """Display Historical VaR calculator"""
    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=True):
        st.markdown("""
        **Historical VaR** calculates potential loss based on historical MTM movements.
        Filter by different dimensions to analyze specific segments.
        """)
        
        # Create filter options
        filter_options = {}
        for col in ['Commodity', 'Instrument Type', 'Trade Action']:
            if col in df.columns:
                filter_options[col] = ['All'] + sorted(df[col].unique().tolist())
        
        # Display filters
        cols = st.columns(min(3, len(filter_options)))
        filters = {}
        for i, (col, options) in enumerate(filter_options.items()):
            with cols[i % len(cols)]:
                selected = st.selectbox(f"Filter by {col}", options=options)
                if selected != 'All':
                    filters[col] = selected
        
        confidence = st.slider(
            "Confidence Level", 
            min_value=90, 
            max_value=99, 
            value=95, 
            step=1, 
            format="%d%%"
        )
        
        try:
            # Apply filters
            filtered_df = df.copy()
            for col, val in filters.items():
                filtered_df = filtered_df[filtered_df[col] == val]
            
            # Calculate Historical VaR
            if len(filtered_df) >= 2:
                filtered_df['Daily_Return'] = filtered_df['MTM'].pct_change().fillna(0)
                sorted_returns = np.sort(filtered_df['Daily_Return'].dropna())
                var_percentile = 100 - confidence
                historical_var = -np.percentile(sorted_returns, var_percentile) * filtered_df['MTM'].sum()
                
                # Display results
                st.metric(
                    label=f"Historical VaR ({confidence}%)",
                    value=f"₹ {abs(historical_var):,.2f}",
                    delta=f"{historical_var/filtered_df['MTM'].sum()*100:.2f}% of portfolio"
                )
                
                with st.expander("🔍 Detailed Analysis"):
                    # Display statistics and charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Filters Applied:**")
                        st.json(filters if filters else {"No filters applied": True})
                        st.write(f"**Trades Analyzed:** {len(filtered_df)}")
                        st.write(f"**Portfolio Value:** ₹ {filtered_df['MTM'].sum():,.2f}")
                    
                    with col2:
                        st.write("**Statistics:**")
                        st.write(f"Mean Daily Return: {filtered_df['Daily_Return'].mean():.4f}")
                        st.write(f"Std Dev of Returns: {filtered_df['Daily_Return'].std():.4f}")
                    
                    # Plot returns distribution
                    fig = px.histogram(
                        filtered_df,
                        x='Daily_Return',
                        nbins=30,
                        title="Distribution of Daily Returns",
                        labels={'Daily_Return': 'Daily Return (%)'}
                    )
                    fig.add_vline(
                        x=-abs(historical_var)/filtered_df['MTM'].sum(),
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"VaR {confidence}%",
                        annotation_position="top left"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data points for calculation (need at least 2 valid trades)")
        except Exception as e:
            st.error(f"Error in Historical VaR calculation: {str(e)}")

def display_trade_table(df):
    """Display the trade data table with filters"""
    st.subheader("📄 Trade Data Table")
    
    # Column-based filtering
    filter_cols = st.columns(4)
    filters = {}
    
    for i, col in enumerate(['Commodity', 'Instrument Type', 'Trade Action', 'Trade ID']):
        if col in df.columns:
            with filter_cols[i % 4]:
                options = ['All'] + sorted(df[col].unique().tolist())
                selected = st.selectbox(f"Filter by {col}", options=options)
                if selected != 'All':
                    filters[col] = selected
    
    # Apply filters
    filtered_df = df.copy()
    for col, val in filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]
    
    # Display formatted table
    numeric_cols = ['Book Price', 'Market Price', 'MTM', 'Realized PnL', 
                   'Unrealized PnL', 'Daily Return', 'Rolling Std Dev', '1-Day VaR']
    
    format_dict = {col: '{:.2f}' for col in numeric_cols if col in filtered_df.columns}
    st.dataframe(
        filtered_df.style.format(format_dict),
        use_container_width=True,
        height=500
    )
    
    return filtered_df

# Main application flow
if uploaded_file:
    with st.spinner("Processing your file..."):
        df = load_data(uploaded_file)
        
        if df is not None and validate_data(df):
            # Calculate metrics
            df = calculate_mtm(df)
            df = calculate_pnl(df)
            
            # Display data and analysis
            filtered_df = display_trade_table(df)
            
            # Show MTM calculation details
            with st.expander("🧮 MTM Calculation Logic", expanded=False):
                st.write("MTM = (Market Price - Book Price) × Quantity")
                st.dataframe(
                    filtered_df[['Trade ID', 'Book Price', 'Market Price', 'Quantity', 'MTM']],
                    use_container_width=True
                )
            
            # Show PnL breakdown
            with st.expander("📈 Realized & Unrealized PnL", expanded=False):
                st.dataframe(
                    filtered_df[['Trade ID', 'Trade Action', 'Realized PnL', 'Unrealized PnL']],
                    use_container_width=True
                )
            
            # Calculate and display VaR
            with st.expander("📉 Value at Risk (VaR)", expanded=False):
                var_confidence = st.slider(
                    "Confidence Level (%)", 
                    90, 99, 95, 
                    key="var_slider"
                )
                var_result = calculate_var(filtered_df, var_confidence)
                st.metric(
                    f"VaR ({var_confidence}%)", 
                    f"₹ {abs(var_result):,.2f}",
                    help="Value at Risk at specified confidence level"
                )
            
            # Show Historical VaR module
            show_historical_var_module(filtered_df)
            
            # Final summary
            with st.expander("📄 Final Risk Summary", expanded=True):
                st.markdown("### 📑 Final Risk Summary")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📉 Total MTM", f"₹ {filtered_df['MTM'].sum():,.2f}")
                col2.metric("🧾 Total Realized PnL", f"₹ {filtered_df['Realized PnL'].sum():,.2f}")
                col3.metric("📈 Total Unrealized PnL", f"₹ {filtered_df['Unrealized PnL'].sum():,.2f}")
                col4.metric(
                    f"🔻 Portfolio VaR ({var_confidence}%)", 
                    f"₹ {abs(var_result):,.2f}"
                )
else:
    st.info("ℹ️ Please upload a trade file to begin analysis")
