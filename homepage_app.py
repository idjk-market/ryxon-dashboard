# [Previous imports and landing page code remain exactly the same...]

# ---- DASHBOARD SECTION ----
else:
    st.title("📊 Ryxon Risk Intelligence Workspace")
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = ['Market Price', 'Book Price', 'Quantity']
            if not all(col in df.columns for col in required_cols):
                st.error("Missing required columns: Market Price, Book Price, Quantity")
                st.stop()

            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            for col in ['Realized PnL', 'Unrealized PnL', 'Daily Return', 'Rolling Volatility', 'VaR']:
                if col not in df.columns:
                    df[col] = np.nan

            # ========== TRADE DATA TABLE ==========
            st.subheader("📋 Trade Data Overview")
            st.dataframe(
                df.style.format({
                    'MTM': '${:,.2f}',
                    'Market Price': '${:,.2f}',
                    'Book Price': '${:,.2f}'
                }),
                use_container_width=True,
                height=400
            )
            # ======================================

            st.subheader("🔍 Filters")
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                instrument = st.selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].dropna().unique()))
            with f2:
                commodity = st.selectbox("Commodity", ["All"] + sorted(df['Commodity'].dropna().unique()))
            with f3:
                direction = st.selectbox("Trade Action", ["All"] + sorted(df['Trade Action'].dropna().unique()))
            with f4:
                dates = st.selectbox("Trade Date", ["All"] + sorted(df['Trade Date'].dropna().astype(str).unique()))

            filtered_df = df.copy()
            if instrument != "All":
                filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument]
            if commodity != "All":
                filtered_df = filtered_df[filtered_df['Commodity'] == commodity]
            if direction != "All":
                filtered_df = filtered_df[filtered_df['Trade Action'] == direction]
            if dates != "All":
                filtered_df = filtered_df[filtered_df['Trade Date'].astype(str) == dates]

            st.session_state.filtered_df = filtered_df

            # [Rest of your dashboard code remains exactly the same...]
            col_main, col_risk = st.columns(2)

            with col_main:
                with st.expander("📊 Core Risk Metrics", expanded=True):
                    # [All your existing metrics and visualizations...]
                    pass

            with col_risk:
                with st.expander("🔍 Advanced Risk Analytics", expanded=True):
                    # [All your existing advanced analytics...]
                    pass

        except Exception as e:
            st.error(f"Error processing file: {e}")

    if st.button("\u2190 Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
