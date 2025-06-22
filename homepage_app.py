import streamlit as st

st.set_page_config(page_title="Ryxon – Risk Intelligence", layout="wide")

# --- LOGO AND TITLE ---
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:15px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="60"/>
        <h1 style="color:#4B0082;">Ready to Take Control of Risk?</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")

# --- LAUNCH DASHBOARD BUTTON (updated to use hyperlink) ---
st.markdown(
    """
    <a href="https://ryxon-dashboard.streamlit.app/" target="_blank">
        <button style='font-size:16px;padding:10px 20px;border-radius:8px;background-color:#5c5cff;color:white;border:none;'>
            🚀 Launch Dashboard
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- FEATURES SECTION ---
st.subheader("📊 Key Features")
features = [
    "📈 MTM & PnL Monitoring in Real Time",
    "🛡️ Value at Risk (VaR), Historical VaR, Monte Carlo Simulation",
    "📊 Stress Testing & Scenario Analysis",
    "📂 Excel File Upload with Trade Breakdown",
    "📉 Derivatives Pricing for Futures & Options",
    "📌 Custom Risk Filters: Commodity, Counterparty, Instrument"
]
st.markdown("<ul>" + "".join(f"<li><strong>{f}</strong></li>" for f in features) + "</ul>", unsafe_allow_html=True)

st.markdown("---")

# --- PRICING SECTION ---
st.subheader("💼 Pricing Plans")

cols = st.columns(3)
plans = [
    {
        "name": "Starter",
        "price": "Free",
        "desc": "Basic MTM, PnL, and VaR tools for individuals."
    },
    {
        "name": "Pro",
        "price": "$29/month",
        "desc": "Unlimited uploads, Historical VaR, Monte Carlo."
    },
    {
        "name": "Enterprise",
        "price": "Custom",
        "desc": "Full API access, priority support, & white-labeling."
    }
]

for i in range(3):
    with cols[i]:
        st.markdown(f"### {plans[i]['name']}")
        st.markdown(f"**{plans[i]['price']}**")
        st.markdown(plans[i]['desc'])
        st.button(f"Choose {plans[i]['name']}", key=f"plan_{i}")

st.markdown("---")

# --- BLOG SECTION ---
st.subheader("📰 Latest from the Blog")
blog_list = [
    ("5 Ways to Hedge Commodity Risk Like a Pro", "#"),
    ("Understanding VaR in Real World Trading", "#"),
    ("Stress Testing: A Risk Manager's Toolkit", "#")
]
for title, link in blog_list:
    st.markdown(f"- [{title}]({link})")

st.markdown("---")

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align:center;color:gray;margin-top:30px;'>
        © 2025 Ryxon Technologies – The Edge of Trading Risk Intelligence
    </div>
    """,
    unsafe_allow_html=True
)
