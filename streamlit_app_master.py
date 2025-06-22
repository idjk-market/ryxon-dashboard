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

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to filter columns
    
    Args:
        df (pd.DataFrame): Original dataframe
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")
    
    if not modify:
        return df
    
    df = df.copy()
    
    # Try to convert datetimes into standard format
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.date
    
    modification_container = st.container()
    
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            # Treat columns with < 10 unique values as categorical
            if pd.api.types.is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_text_input)]
    
    return df

if uploaded_file:
    df = load_excel(uploaded_file)
    df = calculate_mtm(df)
    df = calculate_pnl(df)

    st.subheader("📄 Trade Data Table")
    
    # Apply filters to the dataframe
    filtered_df = filter_dataframe(df)
    
    # Display the filtered dataframe with formatting
    st.dataframe(filtered_df.style.format({
        'Book Price': '{:.2f}',
        'Market Price': '{:.2f}',
        'MTM': '{:.2f}',
        'Realized PnL': '{:.2f}',
        'Unrealized PnL': '{:.2f}',
        'Daily Return': '{:.4f}',
        'Rolling Std Dev': '{:.6f}',
        '1-Day VaR': '{:.6f}'
    }), use_container_width=True, height=500)

    # Rest of your existing code remains the same...
    with st.expander("🧮 MTM Calculation Logic", expanded=False):
        st.write("MTM = (Market Price - Book Price) × Quantity")
        st.dataframe(filtered_df[['Trade ID', 'Book Price', 'Market Price', 'Quantity', 'MTM']], use_container_width=True)

    with st.expander("📈 Realized & Unrealized PnL", expanded=False):
        st.dataframe(filtered_df[['Trade ID', 'Trade Action', 'Realized PnL', 'Unrealized PnL']], use_container_width=True)

    with st.expander("📉 Value at Risk (VaR)", expanded=False):
        var_confidence = st.slider("Confidence Level (%)", 90, 99, 95, key="var_slider")
        var_result = calculate_var(filtered_df, var_confidence)
        st.metric(f"VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")

    # Show advanced Historical VaR Module (using filtered_df)
    # ... rest of your existing code
