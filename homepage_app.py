import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

st.set_page_config(page_title="Ryxon - Risk Intelligence for Traders", layout="wide")

# --- Load Logo ---
logo = Image.open("ryxon_logo.png")  # You can upload logo in your repo or locally

# --- Sidebar Navigation ---
with st.sidebar:
    st.image(logo, width=180)
    selected = option_menu(
        menu_title="Ryxon Navigation",
        options=["Home", "Features", "Pricing", "Blog", "Contact"],
        icons=["house", "bar-chart", "tags", "file-earmark-text", "envelope"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f8f9fa"},
            "icon": {"color": "#007bff", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#dbeafe"},
            "nav-link-selected": {"background-color": "#1d4ed8", "color": "white"},
        }
    )

# --- Home Page ---
if selected == "Home":
    st.markdown("""
        <h1 style='color:#1d4ed8;'>Ryxon – The Edge of Trading Risk Intelligence</h1>
        <h3 style='color:#374151;'>Built for professional traders, risk managers, and commodity hedgers</h3>
        <p style='font-size:18px;'>
        Ryxon is your intelligent command center for real-time risk analytics, mark-to-market, VaR, and more. Whether you trade futures, options, or physicals, we give you control and clarity.
        </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style='background-color:#eff6ff; padding:20px; border-radius:10px;'>
        <h4 style='color:#1e3a8a;'>📊 MTM & Exposure</h4>
        Real-time position MTM, book-to-market and exposure calculations across instruments.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color:#fef9c3; padding:20px; border-radius:10px;'>
        <h4 style='color:#92400e;'>📈 VaR & Scenario</h4>
        Historical, Monte Carlo and Parametric VaR with stress scenarios and thresholds.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style='background-color:#dcfce7; padding:20px; border-radius:10px;'>
        <h4 style='color:#065f46;'>💹 Realized PnL</h4>
        Dynamic profit & loss tabulation with hedge mapping and lifecycle analytics.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<center><a href='/streamlit_app_master' style='text-decoration:none;'><button style='background-color:#1d4ed8; color:white; padding:10px 30px; border:none; border-radius:5px; font-size:16px;'>Launch Dashboard</button></a></center>", unsafe_allow_html=True)

# --- Features Page ---
elif selected == "Features":
    st.markdown("<h2 style='color:#1d4ed8;'>Features</h2>", unsafe_allow_html=True)
    st.markdown("""
    - Trade Upload & Auto-MTM
    - Multi-Commodity Coverage
    - VaR Engine: Historical / Monte Carlo / Parametric
    - Realized & Unrealized PnL Tracking
    - Options Lifecycle & Hedge Mapping
    - Intercompany & Virtual Hedging
    - Excel Integration & API Push
    """)

# --- Pricing Page ---
elif selected == "Pricing":
    st.markdown("<h2 style='color:#1d4ed8;'>Pricing Plans</h2>", unsafe_allow_html=True)
    st.markdown("""
    | Plan       | Monthly | Features |
    |------------|---------|----------|
    | Starter    | ₹ 999   | Basic MTM + PnL |
    | Pro        | ₹ 2499  | Full Risk Suite + Excel Upload |
    | Enterprise | Custom | API + On-prem Integration + Support |
    """)

# --- Blog Page ---
elif selected == "Blog":
    st.markdown("<h2 style='color:#1d4ed8;'>Blog & Case Studies</h2>", unsafe_allow_html=True)
    st.markdown("""
    **1. How Risk Analytics Saves Millions in Hedging Errors**  
    Learn how Ryxon helped a trading desk cut MTM losses using real-time alerts.

    **2. The Evolution of CTRM Risk Platforms**  
    Where traditional ERPs fail, modern risk intelligence tools rise.

    **3. VaR: Historical vs Monte Carlo – What's Best?**  
    Deep dive into use cases with sample code and results.
    """)

# --- Contact Page ---
elif selected == "Contact":
    st.markdown("<h2 style='color:#1d4ed8;'>Contact Us</h2>", unsafe_allow_html=True)
    st.markdown("""
    Have questions or need a custom demo?

    📧 Email: support@ryxonrisk.com  
    📞 Phone: +91-90000-12345  
    🌐 Website: www.ryxonrisk.com
    """)

    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Your Message")
    st.button("Send Message")

# --- Footer ---
st.markdown("""
    <hr>
    <center style='color:#6b7280;'>© 2025 Ryxon by djk — Markets from the desk of a trader.</center>
""", unsafe_allow_html=True)
