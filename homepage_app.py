import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- METRIC STYLE FIX ----
st.markdown("""
<style>
[data-testid="metric-container"] {
    width: 100% !important;
    padding: 8px !important;
}
[data-testid="metric-container"] > div {
    font-size: 1.2rem !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# ---- STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    st.title("📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence")
    st.markdown("""
    Upload your trade file and instantly gain insight into your trading risks with MTM, VaR, and more.
    """)
    if st.button("🚀 Launch Dashboard"):
        st.session_state.show_dashboard = True
        st.rerun()
else:
    st.title("📈 Ryxon Risk Dashboard")
    uploaded_file = st.file_uploader("Upload your trade data (Excel)", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        # ---- DYNAMIC COLUMN FILTERS ----
        st.subheader("🔍 Filter Controls")
        col1, col2, col3 = st.columns(3)
        
        # Instrument Filter
        instrument_options = ["All"] + sorted(df['Instrument'].unique()) if 'Instrument' in df.columns else ["All"]
        instrument_filter = col1.selectbox("Instrument Type", instrument_options)
        
        # Commodity Filter
        commodity_options = ["All"] + sorted(df['Commodity'].unique()) if 'Commodity' in df.columns else ["All"]
        commodity_filter = col2.selectbox("Commodity", commodity_options)
        
        # Date Filter
        if 'TradeDate' in df.columns:
            date_options = ["All"] + sorted(pd.to_datetime(df['TradeDate']).dt.strftime('%Y-%m-%d').unique())
            date_filter = col3.selectbox("Trade Date", date_options)
        else:
            date_filter = "All"

        # Apply filters dynamically
        filtered_df = df.copy()
        if instrument_filter != "All":
            filtered_df = filtered_df[filtered_df['Instrument'] == instrument_filter]
        if commodity_filter != "All":
            filtered_df = filtered_df[filtered_df['Commodity'] == commodity_filter]
        if date_filter != "All" and 'TradeDate' in df.columns:
            filtered_df = filtered_df[pd.to_datetime(filtered_df['TradeDate']).dt.strftime('%Y-%m-%d') == date_filter]

        # ---- FILTERED TRADE DATA TABLE ----
        st.markdown("### 📋 Filtered Trade Data")
        st.dataframe(filtered_df, use_container_width=True)

        # ---- DYNAMIC RISK METRICS CALCULATION ----
        def calculate_metrics(data):
            metrics = {}
            data['MTM'] = data.get('MTM', (data['MarketPrice'] - data['BookPrice']) * data['Quantity'])
            data['RealizedPnL'] = data.get('RealizedPnL', 0)
            data['UnrealizedPnL'] = data.get('UnrealizedPnL', 0)
            
            metrics['mtm_total'] = data['MTM'].sum()
            metrics['realized_pnl'] = data['RealizedPnL'].sum()
            metrics['unrealized_pnl'] = data['UnrealizedPnL'].sum()
            
            try:
                returns = data['MTM'].pct_change().dropna()
                metrics['avg_return'] = returns.mean()
                metrics['volatility'] = returns.std()
                metrics['var_95'] = np.percentile(data['MTM'].dropna(), 5)
            except:
                metrics.update({'avg_return': 0, 'volatility': 0, 'var_95': 0})
            
            return metrics

        metrics = calculate_metrics(filtered_df)

        # ---- DYNAMIC METRICS DISPLAY ----
        with st.expander("📊 Core Risk Metrics", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mark-to-Market", f"${metrics['mtm_total']:,.2f}")
            col2.metric("1-Day VaR (95%)", f"${abs(metrics['var_95']):,.2f}")
            col3.metric("Realized PnL", f"${metrics['realized_pnl']:,.2f}")
            col4.metric("Unrealized PnL", f"${metrics['unrealized_pnl']:,.2f}")
            st.caption(f"Avg Daily Return: {metrics['avg_return']:.4f} | Avg Volatility: {metrics['volatility']:.4f}")

        # ---- DYNAMIC VISUALIZATIONS ----
        with st.expander("📈 Exposure Analysis", expanded=True):
            if 'Commodity' in filtered_df.columns:
                exposure = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
                fig = px.bar(exposure, x='Commodity', y='MTM', title="Exposure by Commodity")
                st.plotly_chart(fig, use_container_width=True)

        # ---- ADVANCED ANALYTICS ----
        with st.expander("🧠 Advanced Risk Analytics", expanded=True):
            tab1, tab2, tab3 = st.tabs(["Stress Testing", "Scenario Analysis", "Historical VaR"])
            
            with tab1:
                st.markdown("#### 💥 Stress Testing")
                shock = st.slider("Market Shock (%)", -50, 50, -10)
                shocked_mtm = ((filtered_df['MarketPrice'] * (1 + shock/100)) - filtered_df['BookPrice']) * filtered_df['Quantity']
                st.metric("Shocked Portfolio Value", f"${shocked_mtm.sum():,.2f}")
            
            with tab2:
                st.markdown("#### 🧪 Scenario Analysis")
                scenario = st.selectbox("Select Scenario", ["Base Case", "Rate Hike", "Market Crash"])
                if scenario == "Rate Hike":
                    scenario_mtm = ((filtered_df['MarketPrice'] * 0.95) - filtered_df['BookPrice']) * filtered_df['Quantity']
                elif scenario == "Market Crash":
                    scenario_mtm = ((filtered_df['MarketPrice'] * 0.80) - filtered_df['BookPrice']) * filtered_df['Quantity']
                else:
                    scenario_mtm = filtered_df['MTM']
                st.metric(f"Scenario: {scenario}", f"${scenario_mtm.sum():,.2f}")
            
            with tab3:
                st.markdown("#### 📉 Historical VaR")
                if 'TradeDate' in filtered_df.columns:
                    historical_var = filtered_df.groupby('TradeDate')['MTM'].sum().rolling(21).quantile(0.05)
                    st.line_chart(historical_var)
                else:
                    st.warning("No trade date data available")

    else:
        st.warning("Please upload a valid Excel trade file to proceed.")
