import streamlit as st
import pandas as pd
from PIL import Image
import base64

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Financial Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- BACKGROUND IMAGE ----
def set_bg_homepage():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .header {{
        color: white;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-top: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    .login-box {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- SESSION STATE ----
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# ---- LOGIN FUNCTION ----
def authenticate(username, password):
    # Simplified authentication - replace with your actual auth logic
    return username == "admin" and password == "ryxon123"

# ---- HOMEPAGE ----
def show_homepage():
    set_bg_homepage()
    
    # Header
    st.markdown('<div class="header">Ryxon Financial Platform</div>', unsafe_allow_html=True)
    
    # Main layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Navigation Menu
        st.markdown("""
        <div style="background: rgba(0,0,0,0.7); padding: 2rem; border-radius: 10px; margin-top: 2rem;">
            <h2 style="color: white;">Products</h2>
            <ul style="color: white; font-size: 1.1rem;">
                <li>Commodity (Energy, Metals, Agriculture)</li>
                <li>Equity (Stocks, ETFs, Indices)</li>
                <li>Real Estate (REITs, Property Derivatives)</li>
                <li>Cryptocurrencies (Spot, Futures)</li>
                <li>Banking & Credit (Loans, Bonds, Swaps)</li>
            </ul>
            
            <h2 style="color: white; margin-top: 2rem;">Instruments</h2>
            <ul style="color: white; font-size: 1.1rem;">
                <li>Futures</li>
                <li>Options</li>
                <li>Forwards</li>
                <li>Swaps</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Login Box
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            
            if not st.session_state.logged_in:
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                if st.button("Sign In"):
                    if authenticate(username, password):
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            else:
                st.subheader("Select Product")
                product = st.selectbox(
                    "Choose product to access",
                    ["Commodity", "Equity", "Real Estate", "Cryptocurrencies", "Banking & Credit"]
                )
                
                if st.button("Continue"):
                    st.session_state.selected_product = product
                    if product == "Commodity":
                        st.switch_page("pages/commodity.py")  # Will create this file next
                    else:
                        st.info(f"{product} module coming soon")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ---- MAIN APP ----
if __name__ == "__main__":
    show_homepage()
