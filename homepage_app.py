import streamlit as st
from PIL import Image
import base64

# --- Page Configuration ---
st.set_page_config(page_title="Ryxon – Market Risk Intelligence", layout="wide")

# --- Load Logo ---
logo = Image.open("ryxon_logo.png")

# --- Styling ---
st.markdown("""
    <style>
        .main-title {
            font-size: 3.2em;
            font-weight: bold;
            color: #5A189A;
        }
        .subtitle {
            font-size: 1.3em;
            color: #555;
        }
        .section-title {
            font-size: 2em;
            font-weight: 600;
            margin-top: 1em;
            color: #3A0CA3;
        }
        .pricing-box {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 1.5em;
            margin: 0.5em;
            background-color: #fdfbff;
        }
    </style>
""", unsafe_allow_html=True)

# --- Hero Section ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=120)
with col2:
    st.markdown("<div class='main-title'>Ryxon Technologies</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>The Edge of Market Risk Intelligence – Designed for Modern Traders</div>", unsafe_allow_html=True)

st.markdown("---")

# --- Features ---
st.markdown("<div class='section-title'>\U0001F4A1 Features</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.success("\n**MTM & Daily PnL**\n\nTrack real-time mark-to-market and position-wise realized/unrealized profits.")
with col2:
    st.info("\n**VaR & Risk Modeling**\n\nBuilt-in Historical, Parametric, and Monte Carlo VaR methods.")
with col3:
    st.warning("\n**Scenario & Stress Testing**\n\nTest portfolio against real-world market shocks.")

# --- Pricing ---
st.markdown("<div class='section-title'>\U0001F4B0 Pricing</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class='pricing-box'>
        <h4>Free</h4>
        <p>Ideal for learning & testing</p>
        <ul>
            <li>Basic Dashboard</li>
            <li>Upload XLSX Trades</li>
            <li>Limited Reports</li>
        </ul>
        <strong>$0/month</strong>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='pricing-box'>
        <h4>Pro</h4>
        <p>For serious traders</p>
        <ul>
            <li>Advanced Risk Models</li>
            <li>Historical VaR, MC Sim</li>
            <li>Exportable Reports</li>
        </ul>
        <strong>$29/month</strong>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='pricing-box'>
        <h4>Enterprise</h4>
        <p>Team-wide access</p>
        <ul>
            <li>All Pro Features</li>
            <li>Multi-user Support</li>
            <li>Custom Alerts & Support</li>
        </ul>
        <strong>Contact Us</strong>
        </div>
    """, unsafe_allow_html=True)

# --- Blog/Insight ---
st.markdown("<div class='section-title'>\U0001F4DA Blog & Insights</div>", unsafe_allow_html=True)
st.info("""
**June 2025 – Why VaR Still Matters**
Explore how Value-at-Risk helps commodity and equity traders navigate volatile markets.

**May 2025 – Top 5 Stress Test Cases for 2025**
From crude collapse to currency shocks – test your portfolio resilience.

**April 2025 – The Rise of Ryxon**
How we're redefining risk management in the trading world.
""")

# --- Call to Action ---
st.markdown("---")
st.markdown("<div class='section-title'>\U0001F680 Ready to Take Control of Risk?</div>", unsafe_allow_html=True)
st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
if st.button("Launch Dashboard"):
    st.switch_page("streamlit_app.py")
