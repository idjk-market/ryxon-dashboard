import streamlit as st
import base64

st.set_page_config(page_title="Ryxon Dashboard", layout="wide")

# Initialize session state variables if they don't exist
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False
if 'dashboard_mode' not in st.session_state:
    st.session_state.dashboard_mode = None

# ---- CUSTOM BACKGROUND ----
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

# Example image (stock market themed)
background_url = "https://images.unsplash.com/photo-1611078489935-b0379236fbd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1650&q=80"
set_background(background_url)

# ---- MAIN PAGE ----
def show_homepage():
    st.markdown("<h1 style='color: #6a1b9a; font-weight: bold;'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.90); padding: 1.5rem; border-radius: 0.5rem;'>
        <p style='font-size: 1.15rem;'>
            An integrated risk platform to manage <strong>derivatives, commodities, and exposure</strong> – built with intelligence, precision, and speed.
        </p>
        <h3 style='margin-top: 2rem;'>🚀 Choose Mode to Get Started</h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📂 Upload Trade File", use_container_width=True):
            st.session_state.show_dashboard = True
            st.session_state.dashboard_mode = "upload"

    with col2:
        if st.button("📝 Create Manual Trade", use_container_width=True):
            st.session_state.show_dashboard = True
            st.session_state.dashboard_mode = "manual"

    st.markdown("""
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

# ---- DASHBOARD PAGES ----
def show_upload_page():
    st.title("📂 Upload Trade File")
    st.write("Upload your trade file here...")
    # Add your upload functionality here
    
    if st.button("🔙 Back to Homepage"):
        st.session_state.show_dashboard = False
        st.session_state.dashboard_mode = None

def show_manual_page():
    st.title("📝 Create Manual Trade")
    st.write("Create a manual trade here...")
    # Add your manual trade creation functionality here
    
    if st.button("🔙 Back to Homepage"):
        st.session_state.show_dashboard = False
        st.session_state.dashboard_mode = None

# ---- MAIN APP LOGIC ----
if st.session_state.show_dashboard:
    if st.session_state.dashboard_mode == "upload":
        show_upload_page()
    elif st.session_state.dashboard_mode == "manual":
        show_manual_page()
else:
    show_homepage()
