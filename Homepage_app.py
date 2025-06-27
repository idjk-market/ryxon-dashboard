import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from PIL import Image
import base64
import time

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
if 'df' not in st.session_state:
    st.session_state.df = None

# ---- BACKGROUND IMAGES ----
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# ---- STYLING ----
def set_app_style():
    bg_images = {
        "commodities": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
        "forex": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
        "stocks": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3",
        "crypto": "https://images.unsplash.com/photo-1621761191319-c6fb62004040"
    }
    
    bg_url = bg_images["commodities"]  # Default background
    
    st.markdown(f"""
        <style>
        /* Main background with professional market image */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url('{bg_url}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}
        
        /* Cards with glass morphism effect */
        .card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            margin-bottom: 2rem;
        }}
        
        /* Buttons with animation */
        .stButton>button {{
            background: linear-gradient(45deg, #6a1b9a, #9c27b0);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(106, 27, 154, 0.4);
        }}
        
        /* Hide Streamlit defaults */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
        }}
        ::-webkit-scrollbar-thumb {{
            background: #6a1b9a;
            border-radius: 4px;
        }}
        </style>
    """, unsafe_allow_html=True)

# ---- LANDING PAGE ----
def show_homepage():
    # Header with logo and title
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 3rem;">
        <div style="text-align: center;">
            <h1 style="color: white; font-size: 3.5rem; margin-bottom: 0.5rem;">Ryxon</h1>
            <h2 style="color: #b39ddb; font-size: 1.8rem; margin-top: 0;">Trading Risk Intelligence</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero section
    with st.container():
        st.markdown("""
        <div class='card'>
            <h2 style="color: white; text-align: center;">Edge of Trading Risk Management</h2>
            <p style="font-size: 1.2rem; text-align: center;">
                An integrated platform for <strong>derivatives, commodities, and exposure</strong> management - 
                built with intelligence, precision, and speed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Launch button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True, key="launch_btn"):
            st.session_state.show_dashboard = True
            st.experimental_rerun()
    
    # Features grid
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0;">
        <h2 style="color: white;">✨ Key Features</h2>
    </div>
    """, unsafe_allow_html=True)
    
    features = [
        ("📊", "Real-time MTM & PnL", "Live mark-to-market and profit/loss tracking", "#7e57c2"),
        ("🛡️", "Value at Risk", "Parametric & Historical VaR calculations", "#9575cd"),
        ("📈", "Scenario Testing", "Stress-test positions with custom shocks", "#b39ddb"),
        ("📉", "PnL Analysis", "Unrealized vs Realized breakdown", "#d1c4e9"),
        ("🧠", "Dynamic Filtering", "Filter by commodity, instrument, strategy", "#7e57c2"),
        ("🌍", "Exposure Analysis", "Visualize by commodity/instrument", "#9575cd")
    ]
    
    cols = st.columns(3)
    for i, (icon, title, desc, color) in enumerate(features):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class='card' style="border-color: {color};">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 2rem; margin-right: 1rem; color: {color};">{icon}</span>
                        <h3 style="color: white; margin: 0;">{title}</h3>
                    </div>
                    <p style="color: #e0e0e0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# ---- DASHBOARD PAGE ----
def show_dashboard():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: white;">Ryxon</h2>
            <p style="color: #b39ddb;">Risk Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        nav_options = {
            "📊 Dashboard": "dashboard",
            "📂 Trade Register": "register",
            "✍️ Trade Entry": "entry",
            "📈 Analytics": "analytics",
            "⚙️ Settings": "settings"
        }
        
        for label, page in nav_options.items():
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page
        
        st.markdown("---")
        
        # Dark mode toggle
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            set_app_style()
            st.experimental_rerun()
        
        st.markdown("---")
        
        if st.button("🏠 Back to Home", key="home_btn"):
            st.session_state.show_dashboard = False
            st.experimental_rerun()
    
    # Main dashboard content
    st.title("📊 Trading Dashboard")
    
    # File uploader with enhanced UI
    with st.expander("📤 Upload Trade Data", expanded=True):
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=["csv", "xlsx"],
            key="file_uploader",
            help="Upload your trade register file"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Processing your trades..."):
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Add sample data if needed for demo
                    if len(df) == 0:
                        st.warning("File is empty. Using sample data for demo.")
                        df = pd.DataFrame({
                            'Instrument': ['Gold Futures', 'Crude Oil', 'EUR/USD'],
                            'Quantity': [100, 500, 1000000],
                            'Price': [1850.50, 72.30, 1.0850],
                            'Market Price': [1865.25, 71.80, 1.0825],
                            'Trade Date': pd.date_range(start='2023-01-01', periods=3)
                        })
                    
                    # Calculate MTM
                    df['MTM'] = (df['Market Price'] - df['Price']) * df['Quantity']
                    st.session_state.df = df
                    st.success("Data loaded successfully!")
            
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.session_state.df = None
    
    # Display data if available
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Summary metrics
        st.markdown("### 📊 Trade Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Positions", len(df))
        col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
        col3.metric("Avg. Price", f"${df['Price'].mean():.2f}")
        col4.metric("Total Quantity", f"{df['Quantity'].sum():,.0f}")
        
        # Data visualization
        st.markdown("### 📈 Data Visualization")
        tab1, tab2 = st.tabs(["MTM Analysis", "Exposure Breakdown"])
        
        with tab1:
            fig = px.bar(df, x='Instrument', y='MTM', color='Instrument', title="MTM by Instrument")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if 'Instrument' in df.columns:
                exposure = df.groupby('Instrument')['Quantity'].sum().reset_index()
                fig = px.pie(exposure, values='Quantity', names='Instrument', title="Exposure Distribution")
                st.plotly_chart(fig, use_container_width=True)
        
        # Raw data view
        st.markdown("### 🔍 Raw Data View")
        st.dataframe(df, use_container_width=True)

# ---- MAIN APP ----
set_app_style()

if not st.session_state.show_dashboard:
    show_homepage()
else:
    show_dashboard()
