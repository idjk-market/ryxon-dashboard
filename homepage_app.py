import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from PIL import Image

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

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
    # Landing page content
    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
    
    # Working launch button
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # ---- FEATURE HIGHLIGHTS ----
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

else:
    # ---- DASHBOARD CONTENT ----
    st.title("📊 Ryxon Risk Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Process file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Store original data
        if 'original_df' not in st.session_state:
            st.session_state.original_df = df.copy()
        
        # Basic calculations
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        
        # ===========================================
        # DYNAMIC FILTERS SECTION (NEW)
        # ===========================================
        st.sidebar.header("🔍 Filters")
        
        # Commodity filter
        commodities = st.sidebar.multiselect(
            "Select Commodities",
            options=df['Commodity'].unique(),
            default=df['Commodity'].unique()
        )
        
        # Instrument type filter
        instrument_types = st.sidebar.multiselect(
            "Select Instrument Types",
            options=df['Instrument Type'].unique(),
            default=df['Instrument Type'].unique()
        )
        
        # Strategy filter (if column exists)
        if 'Strategy' in df.columns:
            strategies = st.sidebar.multiselect(
                "Select Strategies",
                options=df['Strategy'].unique(),
                default=df['Strategy'].unique()
            )
        
        # Apply filters
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df['Commodity'].isin(commodities)]
        filtered_df = filtered_df[filtered_df['Instrument Type'].isin(instrument_types)]
        if 'Strategy' in df.columns:
            filtered_df = filtered_df[filtered_df['Strategy'].isin(strategies)]
        
        # Display metrics (using filtered data)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(filtered_df))
        col2.metric("Total MTM", f"${filtered_df['MTM'].sum():,.2f}")
        col3.metric("Unique Instruments", filtered_df['Instrument Type'].nunique())
        
        # Show data with filters
        st.subheader("Trade Data")
        st.dataframe(filtered_df)
        
        # ===========================================
        # EXPOSURE BY COMMODITY SECTION (UPDATED TO USE FILTERED DATA)
        # ===========================================
        st.subheader("Exposure by Commodity")
        
        # Calculate exposure from filtered data
        exposure_df = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart of exposure by commodity
            st.write("**Net Exposure**")
            fig_bar = px.bar(
                exposure_df,
                x='Commodity',
                y='MTM',
                color='Commodity',
                title="MTM Exposure by Commodity"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie chart of exposure distribution
            st.write("**Exposure Distribution**")
            fig_pie = px.pie(
                exposure_df,
                names='Commodity',
                values='MTM',
                title="Percentage of Total Exposure"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Additional exposure metrics
        st.write("**Detailed Exposure Metrics**")
        exposure_metrics = exposure_df.copy()
        exposure_metrics['% of Total'] = (exposure_metrics['MTM'] / exposure_metrics['MTM'].abs().sum()) * 100
        st.dataframe(
            exposure_metrics.style.format({
                'MTM': '${:,.2f}',
                '% of Total': '{:.1f}%'
            }),
            use_container_width=True
        )
        
        # Add back button
        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
