# --- 📗 Historical VaR Section ---
with st.expander("📗 Historical Value at Risk (Historical VaR)", expanded=False):
    if "MTM" in df.columns and "Trade Date" in df.columns:
        st.markdown("""
        **Historical VaR** is calculated by using historical daily returns and computing the percentile loss from a rolling window of past data. It does not assume any distribution and is purely based on past PnL.
        """)

        # Historical VaR controls
        lookback_days = st.slider("Lookback Window (days)", min_value=10, max_value=100, value=30)
        hist_confidence = st.slider("Confidence Level for Historical VaR (%)", min_value=90, max_value=99, value=95)

        # Prepare sorted returns
        df = df.sort_values("Trade Date")
        df["Daily PnL"] = df["MTM"].diff().fillna(0)

        # Rolling Historical VaR (1 - confidence percentile of daily PnL)
        df["Historical VaR"] = df["Daily PnL"].rolling(window=lookback_days).apply(
            lambda x: np.percentile(x, 100 - hist_confidence), raw=True
        )

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(
                df[["Trade ID", "Trade Date", "Daily PnL", "Historical VaR"]].dropna(),
                height=300
            )
        with col2:
            if "Historical VaR" in df.columns and not df["Historical VaR"].dropna().empty:
                latest_hist_var = df["Historical VaR"].dropna().iloc[-1]
                st.metric(
                    f"Latest Historical VaR ({hist_confidence}%)",
                    f"₹ {latest_hist_var:,.2f}"
                )

        # Chart for Historical VaR trend
        st.markdown("#### 📈 Historical VaR Trend")
        fig = px.line(
            df.dropna(subset=["Historical VaR"]),
            x="Trade Date",
            y="Historical VaR",
            title="Rolling Historical VaR Over Time",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Missing columns 'MTM' and 'Trade Date'. Please ensure these exist in uploaded data.")
