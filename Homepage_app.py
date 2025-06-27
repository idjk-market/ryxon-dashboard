import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from PIL import Image
import time

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Commodity Risk",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SESSION STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
    st.session_state.initial_load = True  # For first-click fix

# ---- PROFESSIONAL BACKGROUNDS ----
COMMODITY_BG = "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"  # Oil rig
TRADING_FLOOR_BG = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3"  # Trading floor

def set_homepage_style():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url('{COMMODITY_BG}');
        background-size: cover;
        background-position: center;
        color: white;
    }}
    .dashboard-card {{
        background: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #FFD700;
    }}
    </style>
    """, unsafe_allow_html=True)

def set_dashboard_style():
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: #f5f5f5;
    }}
    .upload-box {{
        border: 2px dashed #6a1b9a;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- LANDING PAGE ----
def show_homepage():
    set_homepage_style()
    
    st.markdown("""
    <div class="dashboard-card">
        <h1 style="color: #FFD700;">Ryxon Commodity Risk Intelligence</h1>
        <p style="font-size: 1.2rem;">
            Advanced analytics for oil, gas, and energy markets - 
            track exposures, analyze positions, and manage risk.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fixed Launch Button
    if st.button("🚀 Launch Dashboard", key="launch_btn", use_container_width=True):
        st.session_state.show_dashboard = True
        st.session_state.initial_load = False
        st.experimental_rerun()

    # Commodity Features
    st.markdown("## 🔋 Core Features")
    features = [
        ("🛢️", "Crude Oil Analytics", "WTI/Brent spreads, crack spreads"),
        ("⚡", "Energy Futures", "NatGas, Power markets"),
        ("📊", "Physical Exposure", "Tank inventory, pipeline flows"),
        ("🛡️", "Portfolio VaR", "Commodity risk metrics")
    ]
    
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i%2]:
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.5); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ---- DASHBOARD PAGE ----
def show_dashboard():
    set_dashboard_style()
    
    # Original Dashboard Layout
    st.title("📊 Commodity Trade Dashboard")
    
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Ryxon+Energy", width=150)
        if st.button("🏠 Back to Home"):
            st.session_state.show_dashboard = False
            st.experimental_rerun()
        
        st.markdown("**Commodity Filters**")
        st.selectbox("Instrument Type", ["All", "Crude", "Products", "Gas"])
    
    # File Upload - Original Style
    st.markdown("### Upload Trade File")
    uploaded_file = st.file_uploader(
        "Drag and drop CSV/Excel files here",
        type=["csv", "xlsx"],
        help="Max file size: 200MB"
    )
    
    if uploaded_file:
        try:
            with st.spinner("Analyzing commodity trades..."):
                time.sleep(1)  # Simulate processing
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                
                # Sample commodity data structure
                required_cols = ['Commodity', 'Quantity', 'Price']
                if not all(col in df.columns for col in required_cols):
                    st.error("Missing required columns in commodity file")
                else:
                    st.session_state.df = df
                    st.success(f"Loaded {len(df)} commodity trades")
                    
                    # Display original dashboard metrics
                    cols = st.columns(3)
                    cols[0].metric("Total Positions", len(df))
                    cols[1].metric("Net Quantity", f"{df['Quantity'].sum():,}")
                    cols[2].metric("Avg Price", f"${df['Price'].mean():.2f}")
                    
                    # Original chart
                    fig = px.bar(df, x='Commodity', y='Quantity', title="Commodity Exposure")
                    st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Error processing commodity data: {str(e)}")

# ---- MAIN APP ----
if not st.session_state.show_dashboard:
    show_homepage()
else:
    show_dashboard()
