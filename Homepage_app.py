import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np
from PIL import Image
import base64

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SESSION STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ---- STYLING ----
def set_app_style():
    bg_color = "#0E1117" if st.session_state.dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
    card_bg = "rgba(30, 30, 30, 0.9)" if st.session_state.dark_mode else "rgba(255, 255, 255, 0.95)"
    
    st.markdown(f"""
        <style>
        /* Main styling */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Cards */
        .card {{
            background-color: {card_bg};
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* Buttons */
        .stButton>button {{
            transition: all 0.3s ease;
            border: 1px solid #6a1b9a;
        }}
        .stButton>button:hover {{
            transform: scale(1.02);
            box-shadow: 0 2px 10px rgba(106, 27, 154, 0.5);
        }}
        
        /* Hide Streamlit defaults */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ---- LANDING PAGE ----
def show_homepage():
    # Header with logo
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png", width=120)
    with col2:
        st.markdown("<h1 style='color: #6a1b9a;'>Ryxon Trading Risk Intelligence</h1>", unsafe_allow_html=True)
    
    # Hero section
    with st.container():
        st.markdown("""
        <div class='card'>
            <h2 style='color: #6a1b9a;'>Edge of Trading Risk Management</h2>
            <p style='font-size: 1.2rem;'>
                An integrated platform for <strong>derivatives, commodities, and exposure</strong> management - 
                built with intelligence, precision, and speed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Launch button
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True, key="launch_btn"):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # Features grid
    st.markdown("## ✨ Key Features")
    features = [
        ("📊", "Real-time MTM & PnL", "Live mark-to-market and profit/loss tracking"),
        ("🛡️", "Value at Risk", "Parametric & Historical VaR calculations"),
        ("📈", "Scenario Testing", "Stress-test positions with custom shocks"),
        ("📉", "PnL Analysis", "Unrealized vs Realized breakdown"),
        ("🧠", "Dynamic Filtering", "Filter by commodity, instrument, strategy"),
        ("🌍", "Exposure Analysis", "Visualize by commodity/instrument")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <h3>{icon} {title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Product coverage
    st.markdown("## 🏦 Asset Class Coverage")
    products = [
        ("Equity", "📈", "#4B0082", "Stocks, ETFs, and equity derivatives"),
        ("Commodities", "⛏️", "#6a1b9a", "Energy, metals, and agricultural"),
        ("Fixed Income", "💵", "#9370DB", "Bonds, rates, and credit products"),
        ("FX", "💱", "#8A2BE2", "Spot and forward currency pairs"),
        ("Cryptos", "🔗", "#9400D3", "Major cryptocurrencies"),
        ("Derivatives", "📜", "#9932CC", "Futures, options, and swaps")
    ]
    
    cols = st.columns(3)
    for i, (name, icon, color, desc) in enumerate(products):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class='card'>
                    <h3 style='color: {color};'>{icon} {name}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ by Ryxon Technologies</p>
        <p>Market Risk Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

# ---- DASHBOARD PAGE ----
def show_dashboard():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png", width=120)
        st.markdown("## Navigation")
        
        # Dark mode toggle
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            set_app_style()
            st.rerun()
        
        st.markdown("---")
        if st.button("🏠 Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
    
    # Main dashboard content
    st.title("📊 Trading Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Process data
            required_cols = ['Market Price', 'Book Price', 'Quantity']
            if not all(col in df.columns for col in required_cols):
                st.error("Missing required columns: Market Price, Book Price, Quantity")
                st.stop()
            
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col2.metric("Positions", len(df))
            col3.metric("Avg Price", f"${df['Book Price'].mean():.2f}")
            col4.metric("Total Quantity", f"{df['Quantity'].sum():,.0f}")
            
            # Filters
            st.subheader("🔍 Filters")
            col1, col2, col3 = st.columns(3)
            with col1:
                instrument = st.selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].dropna().unique()))
            with col2:
                commodity = st.selectbox("Commodity", ["All"] + sorted(df['Commodity'].dropna().unique()))
            with col3:
                direction = st.selectbox("Direction", ["All"] + sorted(df['Trade Action'].dropna().unique()))
            
            # Apply filters
            filtered_df = df.copy()
            if instrument != "All":
                filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument]
            if commodity != "All":
                filtered_df = filtered_df[filtered_df['Commodity'] == commodity]
            if direction != "All":
                filtered_df = filtered_df[filtered_df['Trade Action'] == direction]
            
            # Show filtered data
            st.dataframe(filtered_df, use_container_width=True)
            
            # Charts
            st.subheader("📊 Visualizations")
            tab1, tab2, tab3 = st.tabs(["MTM Distribution", "Exposure by Commodity", "PnL Trend"])
            
            with tab1:
                fig = px.histogram(filtered_df, x="MTM", nbins=30, title="MTM Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                if 'Commodity' in filtered_df.columns:
                    exposure = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
                    fig = px.bar(exposure, x='Commodity', y='MTM', title="Exposure by Commodity")
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                if 'Trade Date' in filtered_df.columns:
                    filtered_df['Trade Date'] = pd.to_datetime(filtered_df['Trade Date'])
                    daily = filtered_df.groupby('Trade Date')['MTM'].sum().reset_index()
                    fig = px.line(daily, x='Trade Date', y='MTM', title="Daily PnL Trend")
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ---- MAIN APP ----
set_app_style()

if not st.session_state.show_dashboard:
    show_homepage()
else:
    show_dashboard()
