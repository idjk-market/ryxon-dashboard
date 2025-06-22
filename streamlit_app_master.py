import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📊 Ryxon Risk Management Dashboard")

# Upload Excel File
uploaded_file = st.sidebar.file_uploader("Upload Trade Excel File", type=[".xlsx"])

@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

def calculate_mtm(df):
    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
    return df

def calculate_pnl(df):
    df['Realized PnL'] = np.where(
        df['Trade Action'].str.lower() == 'sell',
        (df['Market Price'] - df['Book Price']) * df['Quantity'],
        0
    )
    df['Unrealized PnL'] = df['MTM'] - df['Realized PnL']
    return df

def calculate_var(df, confidence_level=95):
    df['Daily Return'] = df['MTM'].pct_change().fillna(0)
    sorted_returns = np.sort(df['Daily Return'].dropna())
    var_percentile = 100 - confidence_level
    var_value = -np.percentile(sorted_returns, var_percentile) * df['MTM'].sum()
    return var_value

def calculate_historical_var(df, mtm_column='MTM', filters=None, confidence_level=95):
    working_df = df.copy()
    
    # Apply filters if provided
    if filters:
        for column, value in filters.items():
            if column in working_df.columns:
                if value != 'All':
                    working_df = working_df[working_df[column] == value]
    
    # Validate and clean data
    if mtm_column not in working_df.columns:
        raise ValueError(f"MTM column '{mtm_column}' not found")
    
    working_df[mtm_column] = pd.to_numeric(working_df[mtm_column], errors='coerce').fillna(0)
    working_df['Daily_Return'] = working_df[mtm_column].pct_change().fillna(0)
    
    if len(working_df) < 2:
        return None, working_df
    
    sorted_returns = np.sort(working_df['Daily_Return'].dropna())
    var_percentile = 100 - confidence_level
    historical_var = -np.percentile(sorted_returns, var_percentile) * working_df[mtm_column].sum()
    
    return historical_var, working_df

def show_historical_var_module(df):
    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):
        st.markdown("""
        **Historical VaR** calculates potential loss based on historical MTM movements.
        Filter by different dimensions to analyze specific segments.
        """)
        
        # Create filter controls
        filter_options = {
            'Commodity': ['All'] + sorted(df['Commodity'].unique().tolist()),
            'Instrument Type': ['All'] + sorted(df['Instrument Type'].unique().tolist()),
            'Trade Action': ['All'] + sorted(df['Trade Action'].unique().tolist())
        }
        
        cols = st.columns(3)
        filters = {}
        with cols[0]:
            commodity_filter = st.selectbox("Filter by Commodity", options=filter_options['Commodity'])
            if commodity_filter != 'All':
                filters['Commodity'] = commodity_filter
        with cols[1]:
            instrument_filter = st.selectbox("Filter by Instrument Type", options=filter_options['Instrument Type'])
            if instrument_filter != 'All':
                filters['Instrument Type'] = instrument_filter
        with cols[2]:
            action_filter = st.selectbox("Filter by Trade Action", options=filter_options['Trade Action'])
            if action_filter != 'All':
                filters['Trade Action'] = action_filter
        
        confidence = st.slider(
            "Confidence Level", 
            min_value=90, 
            max_value=99, 
            value=95, 
            step=1, 
            format="%d%%"
        )
        
        try:
            hist_var, filtered_df = calculate_historical_var(
                df,
                mtm_column='MTM',
                filters=filters if filters else None,
                confidence_level=confidence
            )
            
            if hist_var is not None:
                # Main results display
                st.metric(
                    label=f"Historical VaR ({confidence}%)",
                    value=f"₹ {abs(hist_var):,.2f}",
                    delta=f"{hist_var/filtered_df['MTM'].sum()*100:.2f}% of portfolio",
                    help="Maximum expected loss based on historical data"
                )
                
                # Detailed analysis
                with st.expander("🔍 Detailed Analysis"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Filters Applied:**")
                        if filters:
                            for k, v in filters.items():
                                st.write(f"- {k}: {v}")
                        else:
                            st.write("No filters applied")
                        
                        st.write(f"**Period Analyzed:** {len(filtered_df)} trades")
                        st.write(f"**Portfolio Value:** ₹ {filtered_df['MTM'].sum():,.2f}")
                    
                    with col2:
                        st.write("**Statistics:**")
                        st.write(f"Mean Daily Return: {filtered_df['Daily_Return'].mean():.4f}")
                        st.write(f"Std Dev of Returns: {filtered_df['Daily_Return'].std():.4f}")
                        st.write(f"Data Points: {len(filtered_df['Daily_Return'].dropna())}")
                    
                    # Visualizations
                    tab1, tab2 = st.tabs(["Returns Distribution", "MTM Trend"])
                    
                    with tab1:
                        fig1 = px.histogram(
                            filtered_df,
                            x='Daily_Return',
                            nbins=30,
                            title="Distribution of Daily Returns",
                            labels={'Daily_Return': 'Daily Return (%)'},
                            color_discrete_sequence=['#636EFA']
                        )
                        fig1.add_vline(
                            x=-abs(hist_var)/filtered_df['MTM'].sum(),
                            line_dash="dash",
                            line_color="red",
                            annotation_text=f"VaR {confidence}%",
                            annotation_position="top left"
                        )
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with tab2:
                        fig2 = px.line(
                            filtered_df,
                            x='Trade Date',
                            y='MTM',
                            title="MTM Trend for Selected Trades",
                            markers=True
                        )
                        st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Not enough data points for calculation (need at least 2 valid trades)")
                
        except Exception as e:
            st.error(f"Error in calculation: {str(e)}")

if uploaded_file:
    df = load_excel(uploaded_file)
    df = calculate_mtm(df)
    df = calculate_pnl(df)

    st.subheader("📄 Trade Data Table")
    st.dataframe(df.style.format({
        'Book Price': '{:.2f}',
        'Market Price': '{:.2f}',
        'MTM': '{:.2f}',
        'Realized PnL': '{:.2f}',
        'Unrealized PnL': '{:.2f}',
        'Daily Return': '{:.4f}'
    }), use_container_width=True)

    with st.expander("🧮 MTM Calculation Logic", expanded=False):
        st.write("MTM = (Market Price - Book Price) × Quantity")
        st.dataframe(df[['Trade ID', 'Book Price', 'Market Price', 'Quantity', 'MTM']], use_container_width=True)

    with st.expander("📈 Realized & Unrealized PnL", expanded=False):
        st.dataframe(df[['Trade ID', 'Trade Action', 'Realized PnL', 'Unrealized PnL']], use_container_width=True)

    with st.expander("📉 Value at Risk (VaR)", expanded=False):
        var_confidence = st.slider("Confidence Level (%)", 90, 99, 95, key="var_slider")
        var_result = calculate_var(df, var_confidence)
        st.metric(f"VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")

    # Show advanced Historical VaR Module
    show_historical_var_module(df)

    with st.expander("📄 Final Risk Summary", expanded=True):
        st.markdown("### 📑 Final Risk Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 Total MTM", f"₹ {df['MTM'].sum():,.2f}")
        col2.metric("🧾 Total Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
        col3.metric("📈 Total Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
        col4.metric(f"🔻 Portfolio VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")
