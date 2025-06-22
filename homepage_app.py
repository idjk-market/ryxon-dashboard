import streamlit as st
import base64

st.set_page_config(page_title="Ryxon – Market Risk Intelligence", layout="wide")

# --- Background & Styling ---
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .main-title {
            font-size: 3.5em;
            font-weight: 900;
            color: #4B0082;
        }
        .sub-title {
            font-size: 1.4em;
            color: #333333;
        }
        .feature-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        }
        .launch-button {
            background-color: #FFD700;
            color: #000;
            font-size: 1.2rem;
            padding: 0.7rem 1.5rem;
            border-radius: 10px;
            font-weight: bold;
        }
        .pricing-header {
            font-size: 2em;
            font-weight: 700;
            color: #2e2e2e;
        }
        .blog-section {
            font-size: 1.1em;
            line-height: 1.6;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# --- Load and Display Logo ---
with open("ryxon_logo.png", "rb") as img_file:
    img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()
    st.markdown(
        f'<div style="text-align:center;"><img src="data:image/png;base64,{img_base64}" width="180"/></div>',
        unsafe_allow_html=True
    )

# --- Title ---
st.markdown('<h1 class="main-title" style="text-align:center;">Ready to Take Control of Risk?</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title" style="text-align:center;">Upload your trade file and see risk insights in seconds.</p>', unsafe_allow_html=True)

st.markdown("---")

# --- Launch Dashboard Button ---
if st.button("🚀 Launch Dashboard", help="Open MTM & VaR Dashboard"):
    js = "window.open('https://ryxon-dashboard.streamlit.app', '_blank')"
    st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)

st.markdown("---")

# --- Features Section ---
st.subheader("📊 Key Features")
cols = st.columns(3)
features = [
    ("📈 MTM & Exposure", "Real-time mark-to-market risk visualization from trade data."),
    ("📉 Value at Risk (VaR)", "Calculate VaR with Historical, Monte Carlo, and Parametric methods."),
    ("🔍 Scenario Testing", "Simulate price shock and hedging stress tests instantly.")
]
for idx, (icon, desc) in enumerate(features):
    with cols[idx]:
        st.markdown(f'<div class="feature-card"><h4>{icon}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

# --- Pricing Plans ---
st.markdown("### 💸 Pricing Plans")
pricing_cols = st.columns(3)
pricing_data = [
    ("Free Tier", "₹0", ["1 Dashboard Access", "Basic VaR & MTM", "Upload Limits"]),
    ("Pro Tier", "₹299/mo", ["All Free Features", "Monte Carlo Simulations", "Scenario & Stress Testing"]),
    ("Enterprise", "Contact Us", ["Unlimited Trades", "Priority Support", "Custom Reports"])
]
for col, (title, price, items) in zip(pricing_cols, pricing_data):
    with col:
        st.markdown(f'<div class="feature-card"><h4 class="pricing-header">{title}</h4><h5>{price}</h5><ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul></div>', unsafe_allow_html=True)

# --- Blog Preview Section ---
st.markdown("---")
st.markdown("### 📝 From the Ryxon Blog")
blog_cols = st.columns(2)
with blog_cols[0]:
    st.markdown("""
        <div class="blog-section">
        <h4>🔐 Why Hedging Desks Fail to Measure Risk Accurately</h4>
        <p>Learn how Ryxon's real-time metrics can plug gaps in traditional CTRM systems.</p>
        </div>
    """, unsafe_allow_html=True)
with blog_cols[1]:
    st.markdown("""
        <div class="blog-section">
        <h4>📌 MTM vs VaR: Where Does Risk Truly Lie?</h4>
        <p>Understand the interplay between exposure tracking and probabilistic risk tools.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("© 2025 Ryxon Technologies | Built by djk – Market Risk Intelligence for Traders.")
