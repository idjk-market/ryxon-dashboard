import streamlit as st
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ryxon Risk Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --- HEADER ---
st.markdown("""
    <h1 style='text-align: left; color: #4B0082;'>🚀 Ready to Take Control of Risk?</h1>
""", unsafe_allow_html=True)

st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")

# --- LOGO ---
logo_path = "ryxon_logo.png"
try:
    image = Image.open(logo_path)
    st.image(image, width=240)
except:
    st.warning("Logo image not found.")

# --- FEATURE HIGHLIGHTS ---
st.markdown("""
### 📊 Core Features
<ul>
    <li>📊 <strong>MTM Exposure & PnL Dashboard</strong> with Upload Support</li>
    <li>📈 <strong>Value at Risk</strong> – Parametric & Historical</li>
    <li>📊 <strong>Trade Filters & Dropdowns</strong> for dynamic analysis</li>
    <li>📊 <strong>Stress Test & Scenario Tools</strong> (Coming Soon)</li>
    <li>📚 <strong>Built by Traders, for Traders</strong> – Markets from the desk of djk</li>
</ul>
""", unsafe_allow_html=True)

# --- LAUNCH BUTTON (OPEN IN NEW TAB) ---
st.markdown("""
<div style="text-align: left; margin-top: 20px;">
    <a href="https://idjk-market-ryxon-dashboard-main-streamlit-app-py.streamlit.app" target="_blank">
        <button style="
            background-color: #ffcc00;
            color: black;
            padding: 12px 28px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        ">🚀 Launch Dashboard</button>
    </a>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
---
© 2025 Ryxon Technologies – Market Risk Intelligence
""
)
