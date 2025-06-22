import streamlit as st
import pandas as pd
import numpy as np

# --- HISTORICAL VAR MODULE ---
with st.expander("📉 Historical Value at Risk (Hist VaR)", expanded=False):
    st.markdown("""
    This module calculates **Historical Value at Risk** (Hist VaR) using the daily return distribution from the dataset.
    It estimates the potential loss at various confidence intervals based on past performance.
    """)

    # Load and filter the correct data (assuming it's been loaded earlier into `filtered_df`)
    if 'filtered_df' in st.session_state:
        trade_data = st.session_state['filtered_df']
    else:
        st.warning("Trade data not available. Please upload a valid Excel file with trade data.")
        st.stop()

    # --- Ensure return columns are present ---
    if {'Daily Return', '1-Day VaR'}.issubset(trade_data.columns):
        st.subheader("📊 Historical Daily Returns")
        st.line_chart(trade_data['Daily Return'].dropna())

        st.subheader("🧮 Histogram of Returns")
        st.bar_chart(trade_data['Daily Return'].dropna().value_counts().sort_index())

        # Select confidence level
        hist_conf = st.slider("Select Confidence Level for Historical VaR", 90, 99, 95)

        # Calculate Historical VaR manually (percentile method)
        var_hist = np.percentile(trade_data['Daily Return'].dropna(), 100 - hist_conf)
        st.metric(label=f"Hist VaR ({hist_conf}%)", value=f"₹ {abs(var_hist):,.2f}")

        # Display preview
        st.markdown("#### 🔍 Preview of Historical VaR Calculation")
        st.dataframe(
            trade_data[['Daily Return', 'Rolling Std Dev', '1-Day VaR']].dropna().tail(10),
            use_container_width=True
        )
    else:
        st.error("Required columns for Historical VaR not found: 'Daily Return', '1-Day VaR'")
