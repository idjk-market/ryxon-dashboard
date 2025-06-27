import streamlit as st
import base64

st.set_page_config(page_title="Ryxon Dashboard", layout="wide")

# ---- BACKGROUND ----
def set_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: url({image_url});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

background_url = "https://images.unsplash.com/photo-1611078489935-b0379236fbd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1650&q=80"
set_background(background_url)

# ---- HOMEPAGE ----
st.markdown("""
<div style='background-color: rgba(255,255,255,0.92); padding: 2rem; border-radius: 12px;'>
    <h1 style='color: #4B0082; font-weight: 900; font-size: 2.6rem;'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</h1>
    <p style='font-size: 1.1rem; color: #333;'>
        A smart platform to manage <strong>derivatives, commodities, and exposure</strong> — built with intelligence, precision, and speed.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='margin-top: 2rem; background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 10px;'>
    <h3 style='color: #4B0082;'>🚀 Get Started</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("📂 Upload Trade File", type=["csv", "xlsx"])
    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.success("✅ File uploaded successfully. Go to Trade Register or Risk Analytics to view insights.")

with col2:
    if st.button("📝 Create Manual Trade", use_container_width=True):
        st.session_state.dashboard_mode = "manual"
        st.switch_page("trade_entry.py")

st.markdown("""
    <br>
    <h4 style='color: #4B0082;'>📌 Navigation Overview</h4>
    <ul style='font-size: 1.05rem; line-height: 1.8;'>
        <li><strong>Trade Entry</strong> – Manually record trades with full instrument control.</li>
        <li><strong>Trade Register</strong> – View, filter, and export all submitted trades.</li>
        <li><strong>Risk Analytics</strong> – MTM, VaR, exposure and stress testing analysis.</li>
        <li><strong>Lifecycle Manager</strong> – Manage square-offs, expiry, and exercise.</li>
        <li><strong>Instrument Master</strong> – Configure commodities, lot sizes, and types.</li>
        <li><strong>Reports</strong> – Generate professional PnL and position reports.</li>
    </ul>
</div>
<p style='text-align: center; font-size: 0.9rem; color: #555; margin-top: 3rem;'>Use the sidebar on the left to switch between modules.</p>
""", unsafe_allow_html=True)
