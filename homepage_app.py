import streamlit as st
from PIL import Image

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- HEADER SECTION ----
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
""", unsafe_allow_html=True)

# ---- MAIN APP SELECTION ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    # Landing page content
    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
    
    # Working launch button
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # ---- FEATURE HIGHLIGHTS ----
    st.markdown("## 🔍 Features You'll Love")
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
    st.info("Coming Soon: 'Top 5 Ways Risk Desks Lose Money & How Ryxon Prevents It'")

else:
    # ---- DASHBOARD CONTENT ----
    # Import your dashboard code here or include it directly
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    st.title("📊 Ryxon Risk Dashboard")
    
    # Add your full dashboard implementation here
    uploaded_file = st.file_uploader("Upload your trade file", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Process file and show dashboard
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.dataframe(df)
        
        # Add back button
        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()

# ---- FOOTER ----
st.markdown("---")
st.markdown("""
<div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
    🚀 Built with ❤️ by Ryxon Technologies – Market Risk Intelligence
</div>
""", unsafe_allow_html=True)
