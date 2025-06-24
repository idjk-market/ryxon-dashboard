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
    # [Your existing landing page code remains unchanged]
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
            required_cols = ['Market Price', 'Book Price', 'Quantity', 'Instrument Type', 'Commodity']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.stop()

            # Calculate core metrics
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
            df['VaR'] = abs(df['MTM'] * 0.01 * 1.645)  # 1% vol, 95% confidence
            
            # Initialize empty columns if missing
            for col in ['Realized PnL', 'Unrealized PnL', 'Daily Return', 'Rolling Volatility']:
                if col not in df.columns:
                    df[col] = 0.0

            # ---- DYNAMIC FILTERS ----
            st.subheader("🔍 Dynamic Filters")
            cols = st.columns(4)
            filters = {
                'Instrument Type': cols[0].selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].unique())),
                'Commodity': cols[1].selectbox("Commodity", ["All"] + sorted(df['Commodity'].unique())),
                'Trade Action': cols[2].selectbox("Trade Action", ["All"] + sorted(df['Trade Action'].unique())) if 'Trade Action' in df.columns else "All",
                'Trade Date': cols[3].selectbox("Date", ["All"] + sorted(df['Trade Date'].astype(str).unique())) if 'Trade Date' in df.columns else "All"
            }

            # Apply filters dynamically
            filtered_df = df.copy()
            for col, val in filters.items():
                if val != "All" and col in filtered_df.columns:
                    if col == 'Trade Date':
                        filtered_df = filtered_df[filtered_df[col].astype(str) == val]
                    else:
                        filtered_df = filtered_df[filtered_df[col] == val]

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

            # ---- CORE METRICS ----
            st.subheader("📊 Core Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total MTM", f"${filtered_df['MTM'].sum():,.2f}")
            m2.metric("Portfolio VaR", f"${filtered_df['VaR'].sum():,.2f}")
            m3.metric("Realized PnL", f"${filtered_df['Realized PnL'].sum():,.2f}")
            m4.metric("Unrealized PnL", f"${filtered_df['Unrealized PnL'].sum():,.2f}")

            # ---- ORIGINAL FEATURES ----
            with st.expander("🧪 Scenario Analysis", expanded=True):
                shock = st.number_input("Market Shock (%)", -50.0, 50.0, -10.0, 0.1)
                shocked_mtm = ((filtered_df['Market Price'] * (1 + shock/100)) - filtered_df['Book Price']) * filtered_df['Quantity']
                delta = shocked_mtm.sum() - filtered_df['MTM'].sum()
                st.metric("Shocked Portfolio Value", f"${shocked_mtm.sum():,.2f}", delta=f"${delta:,.2f}")
                st.plotly_chart(px.histogram(x=shocked_mtm, title="Shocked MTM Distribution"))

            with st.expander("💥 Stress Testing", expanded=True):
                stress_scenarios = st.multiselect(
                    "Select Stress Scenarios",
                    ['Market Crash (-20%)', 'Rate Hike (+5%)', 'Commodity Spike (+30%)'],
                    default=['Market Crash (-20%)']
                )
                for scenario in stress_scenarios:
                    if 'Crash' in scenario:
                        shock = -20.0
                    elif 'Hike' in scenario:
                        shock = 5.0
                    else:
                        shock = 30.0
                    stress_mtm = ((filtered_df['Market Price'] * (1 + shock/100)) - filtered_df['Book Price']) * filtered_df['Quantity']
                    st.metric(f"Stress Scenario: {scenario}", f"${stress_mtm.sum():,.2f}")

            # ---- ADVANCED RISK ANALYTICS ----
            with st.expander("🚨 Advanced Risk Analytics", expanded=True):
                tab1, tab2, tab3 = st.tabs(["Portfolio VaR", "Monte Carlo", "Volatility"])

                with tab1:
                    conf_level = st.slider("Confidence Level", 90, 99, 95, key='var_conf')
                    var = abs(filtered_df['MTM'].sum() * norm.ppf(conf_level/100) * 0.01)
                    st.metric(f"Portfolio VaR ({conf_level}%)", f"${var:,.2f}")

                with tab2:
                    n_sims = st.number_input("Number of Simulations", 100, 10000, 1000)
                    if st.button("Run Monte Carlo"):
                        sim_returns = np.random.normal(0, filtered_df['MTM'].std(), (n_sims, 10))
                        sim_paths = np.cumsum(sim_returns, axis=1)
                        st.plotly_chart(px.line(pd.DataFrame(sim_paths.T), title="Simulated Portfolio Paths"))

                with tab3:
                    window = st.slider("Rolling Window (Days)", 5, 60, 21)
                    if 'Trade Date' in filtered_df.columns:
                        rolling_vol = filtered_df.groupby('Trade Date')['MTM'].sum().rolling(window).std()
                        st.line_chart(rolling_vol)

            # ---- VISUALIZATIONS ----
            st.subheader("📈 Exposure Analysis")
            exp_df = filtered_df.groupby('Commodity').agg({
                'MTM': 'sum',
                'VaR': 'sum'
            }).reset_index()
            
            c1, c2 = st.columns(2)
            c1.plotly_chart(px.bar(exp_df, x='Commodity', y='MTM', color='Commodity', title="MTM Exposure"))
            c2.plotly_chart(px.pie(exp_df, names='Commodity', values='MTM', title="Exposure Distribution"))

            # ---- PERFORMANCE OVER TIME ----
            if 'Trade Date' in filtered_df.columns:
                with st.expander("📅 Performance Over Time", expanded=True):
                    perf_df = filtered_df.groupby('Trade Date').agg({
                        'MTM': 'sum',
                        'Realized PnL': 'sum'
                    }).reset_index()
                    st.plotly_chart(px.line(perf_df, x='Trade Date', y=['MTM', 'Realized PnL'], title="Daily Performance"))

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
