import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import norm

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- SESSION STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    # [Keep your existing landing page code exactly as is]
    pass
else:
    st.title("📊 Ryxon Risk Intelligence Workspace")
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # ---- DATA PROCESSING ----
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Validate required columns
            required_cols = ['Market Price', 'Book Price', 'Quantity']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.stop()

            # Calculate core metrics
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
            df['VaR'] = abs(df['MTM'] * 0.01 * 1.645)  # 1% vol, 95% confidence
            
            # Initialize empty columns if missing
            for col in ['Realized PnL', 'Unrealized PnL']:
                if col not in df.columns:
                    df[col] = 0.0

            # ---- FILTERS ----
            st.subheader("🔍 Filters")
            cols = st.columns(4)
            filters = {
                'Instrument Type': cols[0].selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].unique())),
                'Commodity': cols[1].selectbox("Commodity", ["All"] + sorted(df['Commodity'].unique())),
                'Trade Action': cols[2].selectbox("Trade Action", ["All"] + sorted(df['Trade Action'].unique())),
                'Trade Date': cols[3].selectbox("Date", ["All"] + sorted(df['Trade Date'].astype(str).unique()))
            }

            # Apply filters
            filtered_df = df.copy()
            for col, val in filters.items():
                if val != "All":
                    filtered_df = filtered_df[filtered_df[col] == val] if col != 'Trade Date' else \
                                filtered_df[filtered_df[col].astype(str) == val]

            # ---- TRADE DATA TABLE ----
            st.subheader("📋 Trade Data")
            st.dataframe(
                filtered_df.style.format({
                    'Market Price': '${:,.2f}',
                    'Book Price': '${:,.2f}',
                    'MTM': '${:,.2f}',
                    'VaR': '${:,.2f}',
                    'Realized PnL': '${:,.2f}',
                    'Unrealized PnL': '${:,.2f}'
                }),
                height=400,
                use_container_width=True
            )

            # ---- MAIN METRICS ----
            st.subheader("📊 Core Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total MTM", f"${filtered_df['MTM'].sum():,.2f}")
            m2.metric("Portfolio VaR", f"${filtered_df['VaR'].sum():,.2f}")
            m3.metric("Realized PnL", f"${filtered_df['Realized PnL'].sum():,.2f}")
            m4.metric("Unrealized PnL", f"${filtered_df['Unrealized PnL'].sum():,.2f}")

            # ---- ADVANCED RISK ANALYTICS ----
            st.subheader("🚨 Advanced Risk Analytics")
            tab1, tab2, tab3 = st.tabs(["Portfolio VaR", "Monte Carlo", "Volatility Analysis"])

            with tab1:
                st.markdown("**Variance-Covariance VaR**")
                conf_level = st.slider("Confidence Level", 90, 99, 95, key='var_conf')
                portfolio_var = abs(filtered_df['MTM'].sum() * norm.ppf(conf_level/100) * 0.01)
                st.metric(f"Portfolio VaR ({conf_level}%)", f"${portfolio_var:,.2f}")

            with tab2:
                st.markdown("**Monte Carlo Simulation**")
                n_sims = st.number_input("Simulations", 100, 10000, 1000)
                days = st.number_input("Horizon (Days)", 1, 30, 10)
                
                if st.button("Run Simulation"):
                    returns = np.random.normal(0, filtered_df['MTM'].std(), (n_sims, days))
                    paths = np.cumsum(returns, axis=1)
                    fig = px.line(pd.DataFrame(paths.T), title=f"{n_sims} Simulated Paths")
                    st.plotly_chart(fig, use_container_width=True)

            with tab3:
                st.markdown("**Rolling Volatility**")
                window = st.slider("Window Size", 5, 60, 21)
                if 'Trade Date' in filtered_df.columns:
                    daily = filtered_df.groupby('Trade Date')['MTM'].sum()
                    rolling_vol = daily.rolling(window).std()
                    st.line_chart(rolling_vol)

            # ---- VISUALIZATIONS ----
            st.subheader("📈 Exposure Analysis")
            exp_df = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
            c1, c2 = st.columns(2)
            c1.plotly_chart(px.bar(exp_df, x='Commodity', y='MTM', title="Exposure by Commodity"))
            c2.plotly_chart(px.pie(exp_df, names='Commodity', values='MTM', title="Exposure Distribution"))

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
