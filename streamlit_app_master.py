
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def calculate_historical_var(df, mtm_column='MTM', trade_column=None, trade_filter=None, confidence_level=95):
    working_df = df.copy()
    if trade_column and trade_filter:
        if trade_column not in working_df.columns:
            raise ValueError(f"Trade column '{trade_column}' not found")
        working_df = working_df[working_df[trade_column] == trade_filter]
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
        st.markdown("**Historical VaR** with trade filtering capability.")
        cols = st.columns(3)
        with cols[0]:
            mtm_col = st.selectbox("MTM Column", options=df.columns, index=df.columns.get_loc('MTM'))
        with cols[1]:
            trade_col = None
            if any('trade' in col.lower() for col in df.columns):
                trade_col = st.selectbox(
                    "Trade Column (Optional)",
                    options=['None'] + [col for col in df.columns if 'trade' in col.lower()],
                    index=0
                )
                trade_col = None if trade_col == 'None' else trade_col
        with cols[2]:
            confidence = st.slider("Confidence Level", min_value=90, max_value=99, value=95, step=1, format="%d%%")
        trade_filter = None
        if trade_col:
            trade_options = df[trade_col].unique()
            trade_filter = st.selectbox(f"Select {trade_col} to filter", options=['All'] + sorted(list(trade_options)), index=0)
            if trade_filter == 'All':
                trade_filter = None
        try:
            hist_var, filtered_df = calculate_historical_var(
                df, mtm_column=mtm_col, trade_column=trade_col, trade_filter=trade_filter, confidence_level=confidence
            )
            if hist_var is not None:
                st.metric(
                    label=f"Historical VaR ({confidence}%)",
                    value=f"₹ {abs(hist_var):,.2f}",
                    delta=f"{hist_var/filtered_df[mtm_col].sum()*100:.2f}% of portfolio"
                )
                with st.expander("View Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Period Analyzed:** {len(filtered_df)} days")
                        st.write(f"**Portfolio Value:** ₹ {filtered_df[mtm_col].sum():,.2f}")
                    with col2:
                        st.write(f"**Filter Applied:** {trade_col}={trade_filter if trade_filter else 'None'}")
                        st.write(f"**Data Points:** {len(filtered_df['Daily_Return'].dropna())}")
                    fig = px.histogram(
                        filtered_df,
                        x='Daily_Return',
                        nbins=50,
                        title="Distribution of Daily Returns",
                        labels={'Daily_Return': 'Daily Return (%)'}
                    )
                    fig.add_vline(
                        x=-abs(hist_var)/filtered_df[mtm_col].sum(),
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"VaR {confidence}%",
                        annotation_position="top left"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data points for calculation (need at least 2 valid observations)")
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

if uploaded_file:
    df = load_excel(uploaded_file)
    df = calculate_mtm(df)
    df = calculate_pnl(df)

    st.subheader("📄 Trade Data Table")
    st.dataframe(df, use_container_width=True)

    with st.expander("🧮 MTM Calculation Logic", expanded=False):
        st.write("MTM = (Market Price - Book Price) × Quantity")
        st.dataframe(df[['Trade ID', 'Book Price', 'Market Price', 'Quantity', 'MTM']], use_container_width=True)

    with st.expander("📈 Realized & Unrealized PnL", expanded=False):
        st.dataframe(df[['Trade ID', 'Realized PnL', 'Unrealized PnL']], use_container_width=True)

    with st.expander("📉 Value at Risk (VaR)", expanded=False):
        var_confidence = st.slider("Confidence Level (%)", 90, 99, 95, key="var_slider")
        var_result = calculate_var(df, var_confidence)
        st.metric(f"VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")

    # Show advanced Historical VaR Module
    show_historical_var_module(df)

    with st.expander("📄 Final Risk Summary", expanded=True):
        st.markdown("### 📑 Final Risk Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 MTM", f"₹ {df['MTM'].sum():,.2f}")
        col2.metric("🧾 Realized PnL", f"₹ {df['Realized PnL'].sum():,.2f}")
        col3.metric("📈 Unrealized PnL", f"₹ {df['Unrealized PnL'].sum():,.2f}")
        col4.metric(f"🔻 VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")
