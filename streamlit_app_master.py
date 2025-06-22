# =========================
# 📉 Historical VaR Section
# =========================

with st.expander("📉 Historical Value at Risk (HVaR)"):
    st.markdown("Historical VaR is calculated from the actual distribution of past returns.")

    confidence_level_hvar = st.slider("Select Confidence Level for Historical VaR", min_value=90, max_value=99, value=95)

    # If Daily Return column not available, calculate it
    if "Daily Return" not in df.columns:
        df['Daily Return'] = df['MTM'].pct_change().fillna(0)

    # Drop NaNs, sort returns
    sorted_returns = df['Daily Return'].dropna().sort_values()
    
    percentile_index = int((100 - confidence_level_hvar) / 100 * len(sorted_returns))
    hist_var_value = -sorted_returns.iloc[percentile_index] * df['MTM'].sum()

    st.metric(label=f"HVaR ({confidence_level_hvar}%)", value=f"₹ {hist_var_value:,.2f}")

    st.caption("HVaR is derived from the left-tail percentile of actual PnL/Return distribution.")
    st.bar_chart(df['Daily Return'], use_container_width=True)
