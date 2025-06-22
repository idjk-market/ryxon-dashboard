import streamlit as st
from PIL import Image
import base64

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Ryxon – Market Risk Intelligence",
    page_icon="🚀",
    layout="wide"
)

# === LOAD LOGO ===
logo_path = "ryxon_logo.png"
try:
    logo = Image.open(logo_path)
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("Logo not found. Please upload 'ryxon_logo.png' in the same directory.")

# === CUSTOM STYLING ===
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #4B0082;
    }
    .subsection {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .cta {
        background-color: #d1f5d3;
        padding: 10px 20px;
        border-radius: 10px;
        color: #003300;
        font-weight: bold;
        font-size: 18px;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# === MAIN TITLE ===
st.markdown("<h1 class='main-title'>Welcome to Ryxon – The Edge of Trading Risk Intelligence</h1>", unsafe_allow_html=True)

# === CTA ===
st.markdown("""
<div class='cta'>
Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# === FEATURES ===
st.markdown("<h2>Core Features</h2>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <div class='feature-card'>
    📈 <strong>Real-Time MTM & PnL</strong><br>
    Live mark-to-market, realized and unrealized profit/loss view at trade level.
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div class='feature-card'>
    🌌 <strong>Dynamic Value at Risk</strong><br>
    Historical & Monte Carlo VaR fully integrated with your exposure.
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown("""
    <div class='feature-card'>
    🪨 <strong>Stress & Scenario Testing</strong><br>
    Built-in dashboards to model shocks, spikes, volatility swings.
    </div>
    """, unsafe_allow_html=True)

# === PRICING ===
st.markdown("<h2>Pricing</h2>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    st.markdown("""
    <div class='subsection'>
    💸 <strong>Free Tier</strong><br>
    Access MTM + PnL + 10 trades per day.<br><br>
    <em>Perfect for small traders.</em>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class='subsection'>
    🤝 <strong>Professional</strong><br>
    Everything + 100 trades/day + Stress Testing + Download.<br><br>
    <em>For hedge desks, commodity traders.</em>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class='subsection'>
    📊 <strong>Enterprise</strong><br>
    Unlimited use, custom models, API integration.<br><br>
    <em>Risk desks & institutions.</em>
    </div>
    """, unsafe_allow_html=True)

# === BLOG ===
st.markdown("<h2>Latest Blog Highlights</h2>", unsafe_allow_html=True)
st.markdown("""
<ul>
<li>📊 <strong>How Ryxon Helps Commodity Desks Hedge Better</strong></li>
<li>📈 <strong>Top 3 Ways to Use VaR in Intraday Trading</strong></li>
<li>🪟 <strong>Explained: Realized vs Unrealized PnL in F&O</strong></li>
</ul>
""", unsafe_allow_html=True)

# === CTA BUTTON ===
st.markdown("<h2>Ready to Take Control of Risk?</h2>", unsafe_allow_html=True)
launch = st.button("Launch Dashboard")
if launch:
    st.success("Opening dashboard app...")
    st.markdown("<meta http-equiv='refresh' content='0; url=https://ryxon-dashboard-4dwgjwhdscn6hhsrjc63tj.streamlit.app/'>", unsafe_allow_html=True)
