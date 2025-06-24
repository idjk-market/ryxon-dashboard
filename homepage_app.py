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
        
        # ======================
        # RISK CALCULATIONS
        # ======================
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        df['PnL'] = df['MTM'] - df['Commission']  # Assuming commission column exists
        
        # VaR Calculation (Parametric)
        confidence_level = 0.95
        z_score = 1.645  # For 95% confidence
        df['Daily VaR'] = abs(df['MTM'] * z_score * 0.01)  # Assuming 1% daily volatility
        
        # ======================
        # DYNAMIC FILTERS
        # ======================
        st.sidebar.header("🔍 Global Filters")
        
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
        
        # Apply global filters
        filtered_df = df.copy()
        filtered_df = filtered_df[filtered_df['Commodity'].isin(commodities)]
        filtered_df = filtered_df[filtered_df['Instrument Type'].isin(instrument_types)]
        if 'Strategy' in df.columns:
            filtered_df = filtered_df[filtered_df['Strategy'].isin(strategies)]
        
        # ======================
        # RISK METRICS
        # ======================
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Trades", len(filtered_df))
        col2.metric("Total MTM", f"${filtered_df['MTM'].sum():,.2f}", 
                   delta=f"${filtered_df['PnL'].sum():,.2f} PnL")
        col3.metric("Total VaR (95%)", f"${filtered_df['Daily VaR'].sum():,.2f}")
        col4.metric("Risk/Return Ratio", 
                   f"{(filtered_df['Daily VaR'].sum()/filtered_df['MTM'].abs().sum()):.2%}")
        
        # ======================
        # TRADE DATA WITH COLUMN FILTERS
        # ======================
        st.subheader("Trade Data with Column Filters")
        
        # Create filter UI for each column
        column_filters = {}
        columns_to_filter = ['Commodity', 'Instrument Type', 'Strategy'] if 'Strategy' in df.columns else ['Commodity', 'Instrument Type']
        
        for column in columns_to_filter:
            unique_values = filtered_df[column].unique()
            selected_values = st.multiselect(
                f"Filter {column}",
                options=unique_values,
                default=unique_values,
                key=f"filter_{column}"
            )
            column_filters[column] = selected_values
        
        # Apply column filters
        column_filtered_df = filtered_df.copy()
        for column, values in column_filters.items():
            column_filtered_df = column_filtered_df[column_filtered_df[column].isin(values)]
        
        # Display filtered data
        st.dataframe(
            column_filtered_df.style.format({
                'MTM': '${:,.2f}',
                'PnL': '${:,.2f}',
                'Daily VaR': '${:,.2f}'
            }),
            use_container_width=True,
            height=400
        )
        
        # ======================
        # EXPOSURE ANALYSIS
        # ======================
        st.subheader("Exposure Analysis")
        
        # Calculate exposure from filtered data
        exposure_df = column_filtered_df.groupby('Commodity').agg({
            'MTM': 'sum',
            'Daily VaR': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["MTM Exposure", "VaR Exposure", "Quantity Exposure"])
        
        with tab1:
            fig_bar = px.bar(
                exposure_df,
                x='Commodity',
                y='MTM',
                color='Commodity',
                title="MTM Exposure by Commodity",
                text='MTM'
            )
            fig_bar.update_traces(texttemplate='$%{text:,.2f}')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            fig_pie = px.pie(
                exposure_df,
                names='Commodity',
                values='Daily VaR',
                title="VaR Allocation by Commodity"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab3:
            fig_scatter = px.scatter(
                exposure_df,
                x='Quantity',
                y='MTM',
                size='Daily VaR',
                color='Commodity',
                title="Quantity vs MTM (Size=VaR)"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # ======================
        # RISK/REWARD ANALYSIS
        # ======================
        st.subheader("Risk/Reward Profile")
        
        risk_reward_df = column_filtered_df.groupby('Instrument Type').agg({
            'MTM': 'sum',
            'PnL': 'sum',
            'Daily VaR': 'sum'
        }).reset_index()
        
        risk_reward_df['Return/VaR'] = risk_reward_df['PnL'] / risk_reward_df['Daily VaR']
        
        fig = px.bar(
            risk_reward_df,
            x='Instrument Type',
            y=['PnL', 'Daily VaR'],
            barmode='group',
            title="PnL vs VaR by Instrument Type"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add back button
        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
