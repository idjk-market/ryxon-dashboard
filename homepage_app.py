import streamlit as st

st.set_page_config(page_title="Ryxon – Market Risk Intelligence", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 2rem;
        }
        .logo {
            width: 180px;
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #511282;
        }
        .sub-text {
            font-size: 1.2rem;
            margin-top: -0.5rem;
            margin-bottom: 1.5rem;
            color: #333;
        }
        .launch-button {
            background-color: #ffcc00;
            color: #000;
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .launch-button:hover {
            background-color: #f7b500;
        }
        .feature-box {
            background-color: #f1f3f5;
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & LOGO ---
st.image("ryxon_logo.png", width=180)
st.markdown("<h1 class='hero-title'>Ready to Take Control of Risk?</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!</p>", unsafe_allow_html=True)

# --- LAUNCH BUTTON ---
st.markdown("""
<a href='https://idjk-market-ryxon-dashboard-main-streamlit-app-py.streamlit.app' target='_blank'>
    <button class='launch-button'>🚀 Launch Dashboard</button>
</a>
""", unsafe_allow_html=True)

# --- FEATURES ---
st.markdown("## ✨ Key Features")
features = [
    "📊 Real-time MTM & Exposure Analysis",
    "🧠 Value at Risk (VaR) – Parametric & Historical",
    "🎲 Monte Carlo Simulations",
    "🌪️ Stress & Scenario Testing",
    "📁 Excel Upload & Auto PnL Parsing",
    "🛡️ Credit Risk & Hedge Effectiveness Reporting"
]
for f in features:
    st.markdown(f"<div class='feature-box'>{f}</div>", unsafe_allow_html=True)

# --- PRICING SECTION ---
st.markdown("## 💰 Pricing")
st.markdown("""
- **Free Tier**: Upload file & view MTM, PnL (Limit: 200 trades)
- **Pro Plan**: ₹499/month – Full access to risk models, VaR, scenario testing
- **Enterprise**: Custom pricing – API, Integrations, Email Reports
""")

# --- BLOG HIGHLIGHTS ---
st.markdown("## 📰 From the Blog")
st.markdown("""
- 🔎 [What is VaR? How Traders Use It](https://yourbloglink.com/var)
- 🔐 [Hedging Commodities: The Smart Way](https://yourbloglink.com/hedging)
- 📈 [Why MTM Matters Daily](https://yourbloglink.com/mtm)
""")

# --- FOOTER ---
st.markdown("---")
st.markdown("📍 Built with ❤️ by djk | Powered by Ryxon – The Edge of Trading Risk Intelligence")
