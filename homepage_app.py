import streamlit as st
from PIL import Image

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- LOAD LOGO ----
logo = Image.open("ryxon_logo.png")

# ---- HEADER SECTION ----
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
""", unsafe_allow_html=True)

st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")

# ---- CTA BUTTON (WORKS ON STREAMLIT CLOUD) ----
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='https://ryxon-dashboard.streamlit.app' target='_blank'>
            <button style='background-color:#FFD700; color:black; font-size: 1.2rem; padding: 0.7rem 1.5rem; border-radius: 10px; font-weight: bold; border:none; cursor:pointer;'>
                🚀 Launch Dashboard
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# ---- FEATURE HIGHLIGHTS ----
st.markdown("## 🔍 Features You’ll Love")
st.markdown("""
<ul style="font-size: 1.1rem; line-height: 1.6;">
    <li>📊 <strong>Real-time MTM & PnL Tracking</strong> – Upload trades and instantly view live MTM values</li>
    <li>🛡️ <strong>Value at Risk (VaR)</strong> – Parametric & Historical VaR with confidence control</li>
    <li>📈 <strong>Scenario Testing</strong> – Stress-test positions for custom shocks</li>
    <li>📉 <strong>Unrealized vs Realized PnL</strong> – Clearly broken down with hedge grouping</li>
    <li>🧠 <strong>Dynamic Filtering</strong> – Commodity, Instrument, Strategy – Fully interactive</li>
</ul>
""", unsafe_allow_html=True)

# ---- BLOG / INSIGHT TEASER ----
st.markdown("---")
st.markdown("## 📚 Latest from the Ryxon Blog")
st.info("Coming Soon: ‘Top 5 Ways Risk Desks Lose Money & How Ryxon Prevents It’")

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
<div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
    🚀 Built with ❤️ by Ryxon Technologies – Market Risk Intelligence
</div>
""", unsafe_allow_html=True)
