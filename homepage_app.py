import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Risk Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CSS STYLING ----
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .header {
        background: linear-gradient(135deg, #4B0082, #6A5ACD);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .product-card {
        background: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
    }
    .nav-item {
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ---- SIDEBAR NAVIGATION ----
with st.sidebar:
    st.image("https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png", width=120)
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Dashboard", "Products", "Instruments", "About"],
        icons=["house", "speedometer2", "boxes", "tools", "info-circle"],
        default_index=0,
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "#4B0082", "font-size": "1.1rem"}, 
            "nav-link": {"font-size": "1rem", "text-align": "left", "margin": "0.2rem 0"},
            "nav-link-selected": {"background-color": "#4B0082"},
        }
    )

# ---- HOME PAGE ----
if selected == "Home":
    # ---- HERO SECTION ----
    st.markdown("""
    <div class="header">
        <h1 style="color: white; margin-bottom: 0.5rem;">Ryxon Risk Analytics Platform</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Advanced risk management solutions for modern markets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---- CALL TO ACTION ----
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <h3 style="color: #4B0082;">Comprehensive Risk Management Across All Asset Classes</h3>
        <p style="font-size: 1.1rem;">
            Our platform provides real-time risk analytics, stress testing, and scenario analysis 
            to help you make informed decisions and protect your portfolio.
        </p>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
            selected = "Dashboard"
            st.rerun()
    
    # ---- FEATURE CARDS ----
    st.markdown("## 🔍 Core Features")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #4B0082;">📊 Real-time Analytics</h4>
            <p>Live MTM, PnL tracking, and exposure monitoring across all asset classes.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #4B0082;">🛡️ Advanced VaR</h4>
            <p>Historical, parametric, and Monte Carlo VaR with customizable confidence levels.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color: #4B0082;">📈 Scenario Analysis</h4>
            <p>Stress test your portfolio against historical events and custom scenarios.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ---- PRODUCT TEASER ----
    st.markdown("## 🏦 Asset Class Coverage")
    product_cols = st.columns(4)
    products = [
        ("Equity", "📈", "Stocks, ETFs, and equity derivatives"),
        ("Commodities", "⛏️", "Energy, metals, and agricultural products"),
        ("Cryptos", "🔗", "Spot and derivatives across major cryptocurrencies"),
        ("Bonds & Forex", "💱", "Fixed income and currency products")
    ]
    
    for i, (name, icon, desc) in enumerate(products):
        with product_cols[i]:
            st.markdown(f"""
            <div class="product-card">
                <h4 style="color: #4B0082;">{icon} {name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ---- DASHBOARD PAGE ----
elif selected == "Dashboard":
    st.title("📊 Risk Analytics Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Process file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic calculations
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(df))
        col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
        col3.metric("Unique Instruments", df['Instrument Type'].nunique())
        
        # Show data with filters
        st.subheader("Trade Data")
        st.dataframe(df)
        
        # Simple visualization
        st.subheader("Exposure by Commodity")
        fig = px.bar(df.groupby('Commodity')['MTM'].sum().reset_index(), 
                     x='Commodity', y='MTM', color='Commodity')
        st.plotly_chart(fig, use_container_width=True)

# ---- PRODUCTS PAGE ----
elif selected == "Products":
    st.title("📦 Products Coverage")
    
    tabs = st.tabs(["Equity", "Commodities", "Cryptos", "Bonds & Forex"])
    
    with tabs[0]:
        st.markdown("""
        ### 📈 Equity Products
        **Coverage:** Stocks, ETFs, Index Futures & Options, Equity Swaps
        
        **Risk Metrics:**
        - Beta-adjusted exposure
        - Sector concentration
        - Dividend risk
        - Corporate action tracking
        """)
        
    with tabs[1]:
        st.markdown("""
        ### ⛏️ Commodities
        **Coverage:** Energy, Metals, Agriculture, Commodity Indices
        
        **Risk Metrics:**
        - Basis risk
        - Seasonality patterns
        - Storage cost modeling
        - Delivery risk
        """)
        
    with tabs[2]:
        st.markdown("""
        ### 🔗 Cryptocurrencies
        **Coverage:** Spot, Futures, Options, Perpetual Swaps
        
        **Risk Metrics:**
        - Exchange-specific liquidity
        - Blockchain settlement risk
        - Volatility clustering
        - Stablecoin peg risk
        """)
        
    with tabs[3]:
        st.markdown("""
        ### 💱 Bonds & Forex
        **Coverage:** Government/Credit Bonds, FX Spot/Forwards, NDFs
        
        **Risk Metrics:**
        - Duration/convexity
        - Yield curve risk
        - Currency basis
        - Country risk
        """)

# ---- INSTRUMENTS PAGE ----
elif selected == "Instruments":
    st.title("🛠️ Instrument Coverage")
    
    instrument_data = {
        "Instrument": ["Futures", "Options", "Forwards", "Swaps", "FX", "Interest Rates"],
        "Description": [
            "Exchange-traded standardized contracts",
            "Vanilla and exotic options pricing",
            "OTC forward contracts",
            "Interest rate, equity, and commodity swaps",
            "Spot and forward currency contracts",
            "Bonds, FRAs, and rate derivatives"
        ],
        "Risk Factors": [
            "Basis, roll, and convergence risk",
            "Volatility surface, Greeks, and pin risk",
            "Counterparty and settlement risk",
            "Credit exposure and CSA terms",
            "Currency and country risk",
            "Yield curve and basis risk"
        ]
    }
    
    st.dataframe(
        pd.DataFrame(instrument_data),
        column_config={
            "Description": st.column_config.TextColumn(width="large"),
            "Risk Factors": st.column_config.TextColumn(width="large")
        },
        hide_index=True,
        use_container_width=True
    )

# ---- ABOUT PAGE ----
elif selected == "About":
    st.title("ℹ️ About Ryxon")
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h3 style="color: #4B0082;">Our Mission</h3>
        <p style="font-size: 1.1rem;">
            To empower financial institutions with cutting-edge risk analytics that are both 
            sophisticated and accessible, helping them navigate increasingly complex markets.
        </p>
        
        <h3 style="color: #4B0082; margin-top: 2rem;">Technology Stack</h3>
        <ul style="font-size: 1.1rem;">
            <li>Python-based analytics engine</li>
            <li>Streamlit for interactive visualization</li>
            <li>Cloud-native architecture</li>
            <li>Real-time market data integration</li>
        </ul>
        
        <h3 style="color: #4B0082; margin-top: 2rem;">Contact</h3>
        <p style="font-size: 1.1rem;">
            📧 info@ryxon.tech<br>
            🌐 www.ryxon.tech
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("""
<div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px; padding: 1rem; border-top: 1px solid #eee;">
    🚀 Ryxon Risk Analytics Platform • Built with Python & Streamlit • © 2023
</div>
""", unsafe_allow_html=True)
