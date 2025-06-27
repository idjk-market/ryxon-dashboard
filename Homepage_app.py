import streamlit as st
from PIL import Image

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Ryxon Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---- BACKGROUND IMAGE ----
def set_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("https://images.unsplash.com/photo-1549921296-3a6b93b2f3ec?auto=format&fit=crop&w=1920&q=80")

# ---- NAVIGATION BAR ----
st.markdown("""
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.88);
            padding: 1rem 2rem;
            border-bottom: 1px solid #ddd;
        }
        .nav-links {
            display: flex;
            align-items: center;
        }
        .nav-links a, .dropdown {
            margin: 0 15px;
            text-decoration: none;
            font-weight: 600;
            color: #4B0082;
            position: relative;
        }
        .dropdown-content {
            display: none;
            position: absolute;
            background-color: #f9f9f9;
            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
            z-index: 1;
            top: 30px;
        }
        .dropdown:hover .dropdown-content {
            display: block;
        }
        .dropdown-content a {
            display: block;
            padding: 10px 15px;
            text-decoration: none;
            color: #4B0082;
        }
        .dropdown-content a:hover {
            background-color: #eee;
        }
    </style>
    <div class="navbar">
        <div class="nav-title">
            <h2 style="margin: 0; color: #4B0082;">Ryxon Risk Intelligence</h2>
        </div>
        <div class="nav-links">
            <a href="#" onclick="window.location.reload();">Home</a>
            <a href="#">About</a>
            <div class="dropdown">Products:
                <div class="dropdown-content">
                    <a href="#">Commodity</a>
                    <a href="#">Equity</a>
                    <a href="#">Real Estate</a>
                    <a href="#">Cryptos</a>
                    <a href="#">Banking Credit</a>
                </div>
            </div>
            <div class="dropdown">Instruments:
                <div class="dropdown-content">
                    <a href="#">Futures</a>
                    <a href="#">Options</a>
                    <a href="#">Forwards</a>
                    <a href="#">Swaps</a>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---- LOGIN SECTION ----
st.markdown("""
    <style>
    .login-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 10px;
        width: 350px;
        float: right;
        margin-right: 5%;
        margin-top: 5%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-box'>", unsafe_allow_html=True)
st.subheader("Login to Continue")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")
st.markdown("</div>", unsafe_allow_html=True)

if login_button and username and password:
    st.session_state.logged_in = True
    st.success(f"Welcome, {username}! Please select a product.")

    product = st.selectbox("Select Product Type", ["-- Select --", "Commodity", "Equity", "Real Estate", "Cryptos", "Banking Credit"])
    if product == "Commodity":
        st.markdown("""
        <div style='background-color: rgba(255, 255, 255, 0.92); padding: 1.5rem; margin-top: 2rem; border-radius: 10px; width: 40%;'>
        <h4>Select an Action</h4>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Upload Trade File"):
                st.session_state.mode = "upload"
                st.success("You selected to upload a trade file. Proceed to Trade Register.")
        with col2:
            if st.button("Create Manual Trade"):
                st.session_state.mode = "manual"
                st.success("You selected to create a manual trade. Proceed to Trade Entry.")

        st.markdown("</div>", unsafe_allow_html=True)

# Back button functionality
if 'mode' in st.session_state and st.session_state.mode in ["upload", "manual"]:
    if st.button("⬅ Go Back"):
        del st.session_state.mode
        st.experimental_rerun()

# Always keep sidebar visible
st.markdown("""
<style>
    [data-testid="stSidebar"] { visibility: visible !important; }
</style>
""", unsafe_allow_html=True)
