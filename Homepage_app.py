import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from PIL import Image
import time

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Commodity Dashboard",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SESSION STATE ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
    st.session_state.first_click = True  # Track first click

# ---- ENERGY-COMMODITY BACKGROUND ----
def set_homepage_bg():
    st.markdown(f"""
    <style>
    .homepage {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url('https://images.unsplash.com/photo-1600891964599-f61ba0e24092?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- DASHBOARD STYLE ----
def set_dashboard_style():
    st.markdown(f"""
    <style>
    .dashboard {{
        background-color: #f0f2f6;
        color: #333;
    }}
    .stButton>button {{
        transition: all 0.3s !important;
    }}
    .stButton>button:hover {{
        transform: scale(1.02) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- LANDING PAGE ----
def show_homepage():
    set_homepage_bg()
    st.markdown("""
    <div class="homepage">
        <div style="padding: 2rem; border-radius: 15px; background: rgba(0,0,0,0.5);">
            <h1 style="color: #FFD700;">⛽ Ryxon Commodity Risk Platform</h1>
            <p style="font-size: 1.2rem;">
                Energy & Commodities trading intelligence for crude oil, natural gas, 
                and refined products - with real-time exposure management.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Fixed Launch Button
    if st.button("🚀 Launch Dashboard", key="launch_btn", type="primary"):
        if st.session_state.first_click:
            st.session_state.first_click = False
            st.session_state.show_dashboard = True
            st.rerun()
        else:
            st.session_state.show_dashboard = True
            st.rerun()

    # Commodity Features
    st.markdown("## 🔋 Key Features")
    cols = st.columns(3)
    features = [
        ("🛢️", "Crude Oil Analytics", "WTI/Brent spreads, crack spreads"),
        ("⚡", "Energy Futures", "NatGas, Power, Carbon markets"),
        ("📉", "Physical Exposure", "Tank inventory, pipeline flows"),
        ("📊", "Refined Products", "Gasoline, Diesel, Jet Fuel"),
        ("🛡️", "VaR for Commodities", "Portfolio risk metrics"),
        ("🌐", "Global Exchange Data", "CME, ICE, SGX, DME")
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with cols[i%3]:
            st.markdown(f"""
            <div style="background: rgba(255,215,0,0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #FFD700;">
                <h3>{icon} {title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ---- DASHBOARD PAGE ----
def show_dashboard():
    set_dashboard_style()
    
    # Reliable Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Ryxon+Energy", width=150)
        if st.button("🏠 Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
        
        st.markdown("### Commodity Tools")
        st.selectbox("Data View", ["Live Prices", "Exposure", "Risk Metrics"])
        st.selectbox("Commodity Type", ["Crude", "Products", "Gas", "Power"])
    
    # Main Dashboard
    st.title("🛢️ Commodity Trading Dashboard")
    
    # Fixed File Uploader
    uploaded_file = st.file_uploader("Upload Energy Trade File", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            with st.spinner("Processing commodity data..."):
                time.sleep(1)  # Simulate processing
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                
                # Sample commodity data if empty
                if df.empty:
                    df = pd.DataFrame({
                        'Contract': ['WTI Jan24', 'Brent Feb24', 'Gasoline RBOB'],
                        'Price': [72.50, 76.30, 2.45],
                        'Position': [1000, -500, 2000]
                    })
                
                st.session_state.df = df
                st.success("Commodity data loaded!")
                
                # Show Energy-specific metrics
                cols = st.columns(3)
                cols[0].metric("Total Contracts", len(df))
                cols[1].metric("Net Exposure", f"{df['Position'].sum():,} bbl")
                cols[2].metric("Avg Price", f"${df['Price'].mean():.2f}")
                
                # Commodity-specific chart
                fig = px.bar(df, x='Contract', y='Position', title="Energy Position Exposure")
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error in energy data: {str(e)}")

# ---- MAIN APP ----
if not st.session_state.show_dashboard:
    show_homepage()
else:
    show_dashboard()
