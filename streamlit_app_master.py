import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        var_confidence = st.slider("Confidence Level (%)", 90, 99, 95)
        df['Daily Return'] = df['MTM'].pct_change().fillna(0)
        var_result = calculate_var(df, var_confidence)
        st.metric(f"VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")

    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):
        mtm_col = st.selectbox("Select MTM Column", options=df.columns, index=df.columns.get_loc('MTM'))
        hist_conf = st.slider("Historical Confidence Level (%)", 90, 99, 95)

        try:
            df[mtm_col] = pd.to_numeric(df[mtm_col], errors='coerce').fillna(0)
            df['Daily_Return'] = df[mtm_col].pct_change().fillna(0)
            sorted_returns = np.sort(df['Daily_Return'].dropna())
            hist_var = -np.percentile(sorted_returns, 100 - hist_conf) * df[mtm_col].sum()

            st.metric(
                label=f"Historical VaR ({hist_conf}%)",
                value=f"₹ {abs(hist_var):,.2f}",
                delta=f"{hist_var/df[mtm_col].sum()*100:.2f}% of portfolio"
            )

            with st.expander("📌 Diagnostics"):
                st.write(f"Analysis period: {len(df)} days")
                st.write(f"Portfolio value: ₹ {df[mtm_col].sum():,.2f}")
                fig, ax = plt.subplots()
                ax.hist(df['Daily_Return'], bins=50, alpha=0.7)
                ax.axvline(x=-abs(hist_var)/df[mtm_col].sum(), color='red', linestyle='--')
                ax.set_title("Distribution of Daily Returns")
                ax.set_xlabel("Daily Return")
                ax.set_ylabel("Frequency")
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error calculating Historical VaR: {str(e)}")

    with st.expander("📄 Final Risk Summary", expanded=True):
        mtm_total = df['MTM'].sum()
        realized_total = df['Realized PnL'].sum()
        unrealized_total = df['Unrealized PnL'].sum()
        st.markdown("""
        ### 📑 Final Risk Summary
        """)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📉 MTM", f"₹ {mtm_total:,.2f}")
        col2.metric("🧾 Realized PnL", f"₹ {realized_total:,.2f}")
        col3.metric("📈 Unrealized PnL", f"₹ {unrealized_total:,.2f}")
        col4.metric(f"🔻 VaR ({var_confidence}%)", f"₹ {abs(var_result):,.2f}")
