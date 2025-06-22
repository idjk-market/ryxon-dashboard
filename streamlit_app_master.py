import streamlit as st
import numpy as np

# Historical Value at Risk (Hist VaR)
with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):

    st.markdown("This metric shows the potential maximum loss based on historical MTM variations.")

    # Ensure MTM exists and is numeric
    df['MTM'] = pd.to_numeric(df['MTM'], errors='coerce').fillna(0)

    # Calculate daily returns
    df['Daily Return'] = df['MTM'].pct_change().fillna(0)

    # Allow user to choose confidence level
    hist_conf = st.slider("Select Historical VaR Confidence Level (%)", min_value=90, max_value=99, value=95)

    # Compute historical VaR
    sorted_returns = df['Daily Return'].dropna().sort_values()
    percentile_index = int((100 - hist_conf) / 100 * len(sorted_returns))

    if len(sorted_returns) > percentile_index:
        hist_var = -sorted_returns.iloc[percentile_index] * df['MTM'].sum()
        st.metric(label=f"Hist VaR ({hist_conf}%)", value=f"₹ {hist_var:,.2f}")
    else:
        st.warning("Not enough data to compute Historical VaR.")
