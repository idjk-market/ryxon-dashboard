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

# Background image
background_url = "https://images.unsplash.com/photo-1611078489935-b0379236fbd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1650&q=80"
set_background(background_url)

# ---- HOMEPAGE HEADER ----
st.markdown("<h1 style='color: #6a1b9a; font-weight: bold;'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</h1>", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: rgba(255, 255, 255, 0.90); padding: 1.5rem; border-radius: 0.5rem;'>
    <p style='font-size: 1.15rem;'>
        An integrated risk platform to manage <strong>derivatives, commodities, and exposure</strong> – built with intelligence, precision, and speed.
    </p>
    <h3 style='margin-top: 2rem;'>🚀 Choose Mode to Get Started</h3>
</div>
""", unsafe_allow_html=True)

# ---- MAIN ACTIONS ----
col1, col2 = st.columns(2)
with col1:
    uploaded = st.file_uploader("📂 Upload Trade File (CSV or Excel)", type=["csv", "xlsx"])
    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.success("File uploaded successfully. Proceed to Trade Register or Risk Analytics.")
with col2:
    if st.button("📝 Create Manual Trade", use_container_width=True):
        st.switch_page("Trade Entry")

# ---- INFO SECTION ----
st.markdown("""
<div style='margin-top: 2rem; background-color: rgba(255, 255, 255, 0.9); padding: 1rem; border-radius: 0.5rem;'>
<ul style='line-height: 1.8; font-size: 1.05rem;'>
    <li>Upload existing trade files via <strong>Trade Register</strong>.</li>
    <li>Or create a new trade manually via <strong>Trade Entry</strong>.</li>
    <li>Then analyze MTM, VaR and more in <strong>Risk Analytics</strong>.</li>
    <li>Manage square-offs and lifecycle in <strong>Lifecycle Manager</strong>.</li>
    <li>Configure defaults in <strong>Instrument Master</strong>.</li>
    <li>Export results from the <strong>Reports</strong> section.</li>
</ul>
</div>
<p style='font-size: 0.9rem; color: #555;'>Use the sidebar to navigate through the modules anytime.</p>
""", unsafe_allow_html=True)
