import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
from datetime import datetime

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
        <li>📉 <strong>Unrealized vs Realized PnL</strong> – Clearly broken down with hedge grouping</li>
        <li>🧠 <strong>Dynamic Filtering</strong> – Commodity, Instrument, Strategy – Fully interactive</li>
        <li>📊 <strong>Exposure Analysis</strong> – Visualize by commodity/instrument</li>
    </ul>
    """, unsafe_allow_html=True)

    # ---- PRODUCT COVERAGE ----
    st.markdown("## 🏦 Asset Class Coverage")
    cols = st.columns(4)
    products = [
        ("Equity", "📈", "Stocks, ETFs, and equity derivatives"),
        ("Commodities", "⛏️", "Energy, metals, and agricultural products"),
        ("Cryptos", "🔗", "Spot and derivatives across major cryptocurrencies"),
        ("Bonds & Forex", "💱", "Fixed income and currency products")
    ]
    for i, (name, icon, desc) in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #4B0082;">{icon} {name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---- FOOTER ----
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
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            required_cols = ['Market Price', 'Book Price', 'Quantity']
            if not all(col in df.columns for col in required_cols):
                st.error("Missing required columns: Market Price, Book Price, Quantity")
                st.stop()

            # Calculate MTM
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            # Optional additional fields for demo (if not present)
            for col in ['Realized PnL', 'Unrealized PnL', 'Daily Return', 'Rolling Volatility', 'VaR']:
                if col not in df.columns:
                    df[col] = 0.0

            # Filters
            st.subheader("🔍 Filters")
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                instrument = st.selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].unique()))
            with f2:
                commodity = st.selectbox("Commodity", ["All"] + sorted(df['Commodity'].unique()))
            with f3:
                direction = st.selectbox("Trade Action", ["All"] + sorted(df['Trade Action'].unique()))
            with f4:
                dates = st.selectbox("Trade Date", ["All"] + sorted(df['Trade Date'].astype(str).unique()))

            filtered_df = df.copy()
            if instrument != "All":
                filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument]
            if commodity != "All":
                filtered_df = filtered_df[filtered_df['Commodity'] == commodity]
            if direction != "All":
                filtered_df = filtered_df[filtered_df['Trade Action'] == direction]
            if dates != "All":
                filtered_df = filtered_df[filtered_df['Trade Date'].astype(str) == dates]

            # Show filtered trade data
            st.subheader(f"Filtered Trade Data ({len(filtered_df)})")
            st.dataframe(filtered_df, use_container_width=True)

            # Metrics
            st.subheader("📊 Metrics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mark-to-Market", f"${filtered_df['MTM'].sum():,.2f}")
            col2.metric("1-Day VaR", f"${filtered_df['VaR'].max():,.2f}")
            col3.metric("Realized PnL", f"${filtered_df['Realized PnL'].sum():,.2f}")
            col4.metric("Unrealized PnL", f"${filtered_df['Unrealized PnL'].sum():,.2f}")

            st.caption(f"Avg Daily Return: {filtered_df['Daily Return'].mean():.4f} | Avg Volatility: {filtered_df['Rolling Volatility'].mean():.4f}")

        except Exception as e:
            st.error(f"Error processing file: {e}")

    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
