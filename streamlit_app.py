import streamlit as st

st.set_page_config(
    page_title="Ryxon – Trading Risk Intelligence",
    layout="wide"
)

# Logo
st.image("ryxon_logo.png", width=160)

st.title("Ryxon – The Edge of Trading Risk Intelligence")

st.markdown("""
Welcome to **Ryxon**, your intelligent companion for trading and commodity risk management.  
Track exposure, MTM, VaR, stress testing and hedging all in one place — backed by powerful analytics.
""")

# Features
st.subheader("🔍 Core Features")
st.markdown("""
- 📊 MTM, PnL, and VaR Dashboards  
- 📈 Real-time Trade Filtering  
- 🧠 Advanced Risk Models: Historical, Monte Carlo, Stress  
- 🧾 Interactive Reporting & Export  
- ⚙️ Built with dynamic filters and customizable UI
""")

# Pricing Placeholder
st.subheader("💼 Pricing")
st.info("Contact us for pricing and early access.")

# Blog Placeholder
st.subheader("📚 Learn More")
st.markdown("""
Stay tuned for upcoming tutorials and case studies on risk management best practices.
""")

# Launch dashboard button
st.markdown("---")
st.markdown("## 🚀 Launch the Risk Dashboard")

st.page_link("pages/1_Dashboard.py", label="🔓 Open Dashboard", icon="📂")
