import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ryxon Risk Dashboard", layout="wide")

# File upload
st.sidebar.title("📁 Upload Trade Excel")
uploaded_file = st.sidebar.file_uploader("Upload your trade file (.xlsx)", type=["xlsx"])

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df['MTM'] = pd.to_numeric(df['MTM'], errors='coerce').fillna(0)
    return df

if uploaded_file:
    df = load_data(uploaded_file)

    # -------------------- Filter UI --------------------
    st.title("📊 Trade Table with Filters")
    with st.expander("📄 Filtered Trade Data", expanded=True):
        filters = {}
        cols = st.columns(len(df.columns))
        for i, column in enumerate(df.columns):
            unique_vals = ['All'] + sorted(df[column].dropna().astype(str).unique().tolist())
            filters[column] = cols[i].selectbox(f"Filter: {column}", unique_vals)

        df_filtered = df.copy()
        for column, selected_value in filters.items():
            if selected_value != 'All':
                df_filtered = df_filtered[df_filtered[column].astype(str) == selected_value]

        st.dataframe(df_filtered, use_container_width=True)

    # -------------------- MTM Logic --------------------
    with st.expander("📘 MTM Calculation Logic", expanded=False):
        st.write("Mark-to-Market = (Market Price - Trade Price) * Quantity")
        st.write(f"Total MTM: ₹ {df_filtered['MTM'].sum():,.2f}")

    # -------------------- Realized & Unrealized PnL --------------------
    with st.expander("🧾 Realized & Unrealized PnL", expanded=False):
        realized = df_filtered[df_filtered['Status'] == 'SquaredOff']['MTM'].sum()
        unrealized = df_filtered[df_filtered['Status'] != 'SquaredOff']['MTM'].sum()
        st.metric("Realized PnL", f"₹ {realized:,.2f}")
        st.metric("Unrealized PnL", f"₹ {unrealized:,.2f}")

    # -------------------- Value at Risk (VaR) --------------------
    with st.expander("📉 Value at Risk (VaR)", expanded=False):
        confidence = st.slider("Select Confidence Level (%)", 90, 99, 95)
        pnl_series = df_filtered['MTM'].dropna()
        if not pnl_series.empty:
            var_value = -np.percentile(pnl_series, 100 - confidence)
            st.metric(label=f"VaR ({confidence}%)", value=f"₹ {abs(var_value):,.2f}")
        else:
            st.warning("MTM data not available for VaR calculation.")

    # -------------------- Historical VaR --------------------
    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):
        st.markdown("This metric shows the potential maximum loss based on historical MTM variations.")
        df_filtered['MTM'] = pd.to_numeric(df_filtered['MTM'], errors='coerce').fillna(0)
        df_filtered['Daily_Return'] = df_filtered['MTM'].pct_change().fillna(0)

        if len(df_filtered) >= 2:
            sorted_returns = np.sort(df_filtered['Daily_Return'].dropna())
            hist_var = -np.percentile(sorted_returns, 100 - confidence) * df_filtered['MTM'].sum()

            st.metric(label=f"Historical VaR ({confidence}%)",
                      value=f"₹ {abs(hist_var):,.2f}",
                      delta=f"{hist_var/df_filtered['MTM'].sum()*100:.2f}% of portfolio")

            with st.expander("📈 Distribution Diagnostics"):
                fig, ax = plt.subplots()
                ax.hist(df_filtered['Daily_Return'], bins=50, alpha=0.7)
                ax.axvline(x=-abs(hist_var)/df_filtered['MTM'].sum(), color='red', linestyle='--')
                ax.set_title("Distribution of Daily Returns")
                ax.set_xlabel("Daily Return")
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
        else:
            st.warning("Not enough data points for Historical VaR calculation.")

    # -------------------- Final Risk Summary --------------------
    st.subheader("🧾 Final Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 MTM", f"₹ {df_filtered['MTM'].sum():,.2f}")
    col2.metric("📈 Realized PnL", f"₹ {realized:,.2f}")
    col3.metric("📊 Unrealized PnL", f"₹ {unrealized:,.2f}")
    col4.metric(f"📉 VaR ({confidence}%)", f"₹ {abs(var_value):,.2f}")
