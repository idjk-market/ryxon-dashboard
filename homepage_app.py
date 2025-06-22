# homepage_app.py
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Ryxon – Trading Risk Intelligence",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# --- Header ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    h1 {
        color: #3f51b5;
        font-size: 3rem;
    }
    h4 {
        color: #333333;
    }
    .feature-box {
        background-color: white;
        border-left: 6px solid #3f51b5;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
    }
    .footer {
        margin-top: 4rem;
        text-align: center;
        font-size: 0.9rem;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# --- Navigation ---
with st.sidebar:
    selected = option_menu(
        menu_title="Ryxon Menu",
        options=["Home", "Dashboard"],
        icons=["house", "bar-chart"],
        default_index=0,
        menu_icon="grid-3x3-gap-fill"
    )

# --- Main Page ---
if selected == "Home":
    st.markdown("""
        <h1>Ryxon – The Edge of Trading Risk Intelligence</h1>
        <h4>Built for traders who demand precision, control, and confidence.</h4>
        <p>Welcome to <strong>Ryxon</strong>, your AI-powered companion for managing commodity and derivatives risk with real-time dashboards, analytics, and actionable insights.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='feature-box'>
        <h5>📈 MTM Calculation</h5>
        Calculate mark-to-market profit/loss for every trade in real-time.
        </div>

        <div class='feature-box'>
        <h5>📊 Realized & Unrealized PnL</h5>
        Visualize your profit flow, day-by-day and trade-by-trade.
        </div>

        <div class='feature-box'>
        <h5>📉 Value at Risk (VaR)</h5>
        Understand your worst-case exposure under normal conditions.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-box'>
        <h5>🧠 Monte Carlo Simulation</h5>
        Model future market behavior with confidence intervals.
        </div>

        <div class='feature-box'>
        <h5>🔍 Stress Testing & Scenario Analysis</h5>
        Analyze your portfolio under historical or hypothetical shocks.
        </div>

        <div class='feature-box'>
        <h5>🔗 API-Based Integration</h5>
        Plug into live pricing, ERP, and trade sources in real-time.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='footer'>
        Created by djk — <i>Markets from the desk of a trader.</i>
        </div>
    """, unsafe_allow_html=True)

elif selected == "Dashboard":
    st.markdown("<meta http-equiv='refresh' content='0; url=streamlit_app_master.py'>", unsafe_allow_html=True)
