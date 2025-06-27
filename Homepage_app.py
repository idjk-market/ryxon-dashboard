import streamlit as st

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Login",
    layout="centered"
)

# ---- STYLING ----
st.markdown(f"""
<style>
.login-container {{
    max-width: 400px;
    margin: 0 auto;
    padding: 2rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}}
</style>
""", unsafe_allow_html=True)

# ---- LOGIN FORM ----
with st.container():
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.title("Login Required")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Authenticate"):
        if username == "admin" and password == "ryxon123":
            st.session_state.authenticated = True
            st.switch_page("pages/commodity.py")
        else:
            st.error("Invalid credentials")
    
    st.markdown("</div>", unsafe_allow_html=True)
