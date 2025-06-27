import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- STYLES ----
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
    color: #111;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #f0f2f6;
    color: #333;
}
.big-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #4B0082;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}
.subtitle {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---- HOMEPAGE ----
st.markdown("<div class='big-title'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>An integrated risk platform to manage derivatives, commodities, and exposure – built with intelligence, precision, and speed.</div>", unsafe_allow_html=True)

st.markdown("""
### Quick Start Options
- Go to **Trade Entry** to manually record your futures, options, swaps, or forwards.
- Upload existing trade files via **Trade Register**.
- Analyze MTM, VaR and more in **Risk Analytics**.
- Manage square-offs and lifecycle in **Lifecycle Manager**.
- Configure defaults in **Instrument Master**.
- Export results from **Reports** section.

Use the sidebar to navigate through the modules.
""")
