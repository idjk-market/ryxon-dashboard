import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Ryxon – Risk Intelligence", layout="wide")

# --- Branding Header ---
st.markdown("<h1 style='color:#3E64FF;'>Ryxon – The Edge of Trading Risk Intelligence</h1>", unsafe_allow_html=True)
st.subheader("📈 Built for traders who demand real-time clarity.")

# --- Intro Text ---
st.markdown("""
Welcome to **Ryxon**, your intelligent companion for derivatives and commodities risk.

We provide real-time dashboards and analytics for:
- 📘 MTM Calculation
- 📙 Realized & Unrealized PnL
- 📕 Value at Risk (VaR)
- 🧠 Monte Carlo Simulations
- 🔍 Stress Testing & Scenario Analysis

Ryxon helps you protect, hedge, and grow with confidence.
""")

# --- Call to Action ---
st.markdown("---")
if st.button("🚀 Go to Dashboard"):
    st.switch_page("streamlit_app.py")  # or change to your dashboard filename

st.markdown("---")
st.info("Created by djk — Markets from the desk of a trader.")
