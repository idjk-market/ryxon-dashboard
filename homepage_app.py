import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Ryxon Risk Intelligence",
    layout="wide",
    page_icon="📊"
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f9f9fb;
        padding: 2rem;
    }
    h1 {
        font-size: 3.2rem;
        font-weight: 700;
        color: #1F4E79;
    }
    h3 {
        color: #444;
    }
    .menu-title {
        font-weight: 600;
        font-size: 1.2rem;
    }
    .stButton>button {
        background-color: #1F4E79;
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<h1>Ryxon – The Edge of Trading Risk Intelligence</h1>
<h3>Your real-time decision engine for derivatives and commodities.</h3>
""", unsafe_allow_html=True)

# --- Menu Bar (Top Nav) ---
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Home", "About", "Dashboard", "Contact"],
        icons=["house", "info-circle", "bar-chart", "envelope"],
        orientation="horizontal",
        styles={
            "nav-link": {"font-size": "16px", "margin": "0px", "--hover-color": "#f0f2f6"},
            "icon": {"color": "#1F4E79", "font-size": "18px"},
            "nav-link-selected": {"background-color": "#1F4E79", "color": "white"},
        }
    )

# --- Main Content ---
if selected == "Home":
    st.markdown("""
    <div style='margin-top: 2rem;'>
        <h3 class='menu-title'>What We Offer</h3>
        <ul>
            <li><b>Mark-to-Market (MTM)</b> Calculations with real-time PnL impact</li>
            <li><b>Realized & Unrealized PnL</b> summaries with drill-down</li>
            <li><b>Value at Risk (VaR)</b> with dynamic confidence level settings</li>
            <li><b>Monte Carlo Simulations</b> and Stress Testing</li>
            <li><b>Scenario Analysis</b> tailored to your book</li>
        </ul>
    </div>
    <div style='margin-top: 3rem;'>
        <h3 class='menu-title'>Built For:</h3>
        <ul>
            <li>Commodity Risk Managers</li>
            <li>Derivatives Traders</li>
            <li>Hedge Accounting Teams</li>
            <li>Algo Trading Desks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif selected == "About":
    st.subheader("About Ryxon")
    st.write("Ryxon is designed by professionals with deep expertise in CTRM, derivatives, and risk management. The platform was born out of real trading desk pain points, now transformed into one sleek intelligence layer.")

elif selected == "Dashboard":
    st.success("Please go to your main dashboard using the sidebar or direct menu. (e.g. streamlit_app.py)")

elif selected == "Contact":
    st.subheader("Get in Touch")
    st.markdown("Contact us at **support@ryxon.tech** or connect via LinkedIn")

# --- Footer ---
st.markdown("""
---
<div style='text-align:center;'>
    <small>Ryxon © 2025 | Built by djk — Markets from the desk of a trader</small>
</div>
""", unsafe_allow_html=True)
