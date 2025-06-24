import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Ryxon Dashboard", page_icon="📊", layout="wide")

# ---- HEADER SECTION ----
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
""", unsafe_allow_html=True)

# ---- MAIN APP SELECTION ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    # [Previous landing page code remains unchanged]
    pass
else:
    # ---- DASHBOARD CONTENT ----
    st.title("📊 Ryxon Risk Dashboard")
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Load data safely
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # === DATA VALIDATION ===
            st.session_state.original_df = df.copy()
            required_columns = ['Market Price', 'Book Price', 'Quantity']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                st.stop()

            # === CALCULATIONS (WITH ERROR HANDLING) ===
            # MTM (Mark-to-Market)
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            # PnL (Profit & Loss) - works with or without Commission
            if 'Commission' in df.columns:
                df['PnL'] = df['MTM'] - df['Commission']
            else:
                df['PnL'] = df['MTM']
                st.warning("⚠️ No 'Commission' column found. Using MTM as PnL.")

            # VaR (Value at Risk)
            try:
                confidence_level = 0.95
                z_score = 1.645  # For 95% confidence
                df['Daily VaR'] = abs(df['MTM'] * z_score * 0.01)  # 1% daily volatility
            except:
                df['Daily VaR'] = 0
                st.warning("⚠️ Could not calculate VaR. Defaulting to zero.")

            # === DYNAMIC FILTERS ===
            st.sidebar.header("🔍 Filters")
            available_columns = df.columns.tolist()

            # Commodity Filter (if column exists)
            if 'Commodity' in available_columns:
                commodities = st.sidebar.multiselect(
                    "Select Commodities",
                    options=df['Commodity'].unique(),
                    default=df['Commodity'].unique()
                )
                df = df[df['Commodity'].isin(commodities)]

            # Instrument Type Filter (if column exists)
            if 'Instrument Type' in available_columns:
                instruments = st.sidebar.multiselect(
                    "Select Instrument Types",
                    options=df['Instrument Type'].unique(),
                    default=df['Instrument Type'].unique()
                )
                df = df[df['Instrument Type'].isin(instruments)]

            # === RISK METRICS ===
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Trades", len(df))
            col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col3.metric("Total PnL", f"${df['PnL'].sum():,.2f}")
            col4.metric("Total VaR (95%)", f"${df['Daily VaR'].sum():,.2f}")

            # === TRADE DATA TABLE ===
            st.subheader("Trade Data")
            st.dataframe(df.style.format({
                'MTM': '${:,.2f}',
                'PnL': '${:,.2f}',
                'Daily VaR': '${:,.2f}'
            }), use_container_width=True)

            # === EXPOSURE CHARTS ===
            st.subheader("Exposure Analysis")
            if 'Commodity' in df.columns:
                exposure_df = df.groupby('Commodity').agg({
                    'MTM': 'sum',
                    'PnL': 'sum',
                    'Daily VaR': 'sum'
                }).reset_index()

                fig = px.bar(
                    exposure_df,
                    x='Commodity',
                    y='MTM',
                    title="MTM Exposure by Commodity"
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"🚨 An unexpected error occurred: {str(e)}")
            st.stop()

    # Back to Home Button
    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
