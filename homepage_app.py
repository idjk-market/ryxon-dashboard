import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
from datetime import datetime
import numpy as np

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- SESSION STATE INIT ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
            <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
        </div>
    """, unsafe_allow_html=True)

    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")

    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()

    # ---- FEATURES ----
    st.markdown("## 🔍 Features You'll Love")
    st.markdown("""
    <ul style="font-size: 1.1rem; line-height: 1.6;">
        <li>📊 <strong>Real-time MTM & PnL Tracking</strong> – Upload trades and instantly view live MTM values</li>
        <li>🛡️ <strong>Value at Risk (VaR)</strong> – Parametric & Historical VaR with confidence control</li>
        <li>📈 <strong>Scenario Testing</strong> – Stress-test positions for custom shocks</li>
        <li>📉 <strong>Unrealized vs Realized PnL</strong> – Automatically derived from trade status</li>
        <li>📐 <strong>Sharpe & Sortino Ratio</strong> – Risk-adjusted return analytics</li>
        <li>🧠 <strong>Dynamic Filtering</strong> – Commodity, Instrument, Strategy – Fully interactive</li>
        <li>📊 <strong>Exposure Analysis</strong> – Visualize by commodity/instrument</li>
        <li>📄 <strong>Performance Over Time</strong> – Daily MTM & PnL tracking</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
        🚀 Built with ❤️ by Ryxon Technologies – Market Risk Intelligence
    </div>
    """, unsafe_allow_html=True)

# ---- DASHBOARD SECTION ----
else:
    st.title("📊 Ryxon Risk Dashboard")
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = ['Market Price', 'Book Price', 'Quantity']
            for col in required_cols:
                if col not in df.columns:
                    st.error(f"Missing required column: {col}")
                    st.stop()

            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            df['Trade Status'] = df.get('Trade Status', 'Open')

            df['Realized PnL'] = df.apply(lambda x: x['MTM'] if x['Trade Status'] == 'Closed' else 0, axis=1)
            df['Unrealized PnL'] = df.apply(lambda x: x['MTM'] if x['Trade Status'] == 'Open' else 0, axis=1)
            df['Daily Return'] = df.get('Daily Return', df['MTM'].pct_change().fillna(0))
            df['Rolling Volatility'] = df['Daily Return'].rolling(window=5).std().fillna(0)

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

            st.subheader(f"Filtered Trade Data ({len(filtered_df)})")
            st.dataframe(filtered_df, use_container_width=True)

            with st.expander("📈 MTM, PnL, VaR Analysis", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Mark-to-Market", f"${filtered_df['MTM'].sum():,.2f}")
                param_var = np.percentile(filtered_df['MTM'].dropna(), 5)
                col2.metric("Parametric VaR (95%)", f"${param_var:,.2f}")
                col3.metric("Realized PnL", f"${filtered_df['Realized PnL'].sum():,.2f}")
                col4.metric("Unrealized PnL", f"${filtered_df['Unrealized PnL'].sum():,.2f}")
                st.caption(f"Avg Daily Return: {filtered_df['Daily Return'].mean():.4f} | Avg Volatility: {filtered_df['Rolling Volatility'].mean():.4f}")

                # Sharpe and Sortino
                rf_rate = 0.01 / 252
                sharpe_ratio = (filtered_df['Daily Return'].mean() - rf_rate) / (filtered_df['Daily Return'].std() + 1e-9)
                downside_std = filtered_df['Daily Return'][filtered_df['Daily Return'] < 0].std()
                sortino_ratio = (filtered_df['Daily Return'].mean() - rf_rate) / (downside_std + 1e-9)
                st.caption(f"Sharpe Ratio: {sharpe_ratio:.2f} | Sortino Ratio: {sortino_ratio:.2f}")

            with st.expander("📊 Exposure by Commodity"):
                exposure_df = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Net Exposure**")
                    fig_bar = px.bar(exposure_df, x='Commodity', y='MTM', color='Commodity', title="MTM Exposure by Commodity")
                    st.plotly_chart(fig_bar, use_container_width=True)
                with col2:
                    st.write("**Exposure Distribution**")
                    fig_pie = px.pie(exposure_df, names='Commodity', values='MTM', title="Percentage of Total Exposure")
                    st.plotly_chart(fig_pie, use_container_width=True)

            with st.expander("🔢 Historical VaR (Quantile-Based)"):
                confidence = st.slider("Confidence Level (%)", 90, 99, 95)
                var_hist = np.percentile(filtered_df['MTM'].dropna(), 100 - confidence)
                st.metric(f"Historical {confidence}% VaR", f"${var_hist:,.2f}")
                st.caption("Historical VaR is the loss at a given confidence level based on historical MTM distribution.")
                st.plotly_chart(px.histogram(filtered_df, x="MTM", nbins=30, title="MTM Distribution"), use_container_width=True)

            with st.expander("🧪 Scenario Testing"):
                scenario_pct = st.number_input("Enter Shock % on Market Price", value=-5.0, format="%.2f")
                shocked_df = filtered_df.copy()
                shocked_df['Shocked MTM'] = ((shocked_df['Market Price'] * (1 + scenario_pct / 100)) - shocked_df['Book Price']) * shocked_df['Quantity']
                mtm_diff = shocked_df['Shocked MTM'].sum() - shocked_df['MTM'].sum()
                st.metric("Shocked MTM", f"${shocked_df['Shocked MTM'].sum():,.2f}", delta=f"${mtm_diff:,.2f}")
                st.plotly_chart(px.histogram(shocked_df, x="Shocked MTM", nbins=30, title="Shocked MTM Distribution"), use_container_width=True)

            with st.expander("💥 Stress Testing"):
                st.write("Apply custom shocks to assess extreme outcomes")
                shocks = st.multiselect("Select Stress Scenarios", ['+10%', '+20%', '-10%', '-20%'])
                for shock in shocks:
                    pct = float(shock.replace('%', ''))
                    stress_df = filtered_df.copy()
                    stress_df['Stress MTM'] = ((stress_df['Market Price'] * (1 + pct / 100)) - stress_df['Book Price']) * stress_df['Quantity']
                    st.metric(f"Stress MTM ({shock})", f"${stress_df['Stress MTM'].sum():,.2f}")

            with st.expander("📅 Trade Performance by Date"):
                if 'Trade Date' in filtered_df.columns:
                    df_perf = filtered_df.copy()
                    df_perf['Trade Date'] = pd.to_datetime(df_perf['Trade Date'])
                    daily_perf = df_perf.groupby('Trade Date').agg({"MTM": "sum", "Realized PnL": "sum"}).reset_index()
                    fig = px.line(daily_perf, x="Trade Date", y=["MTM", "Realized PnL"], title="Daily MTM and Realized PnL")
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error processing file: {e}")

    if st.button("\u2190 Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
