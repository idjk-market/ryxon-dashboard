import streamlit as st
from streamlit_option_menu import option_menu
import os

st.set_page_config(page_title="Ryxon Homepage", layout="wide")

# Title Section
st.title("📌 Welcome to Ryxon Risk Intelligence Dashboard")
st.markdown("""
**Ryxon** is your all-in-one dashboard for analyzing **trading risk**, **mark-to-market**, **PnL**, **VaR**, and more. Start by selecting an action from the left menu to begin your analysis journey.
""")

# Sidebar Navigation
with st.sidebar:
    selection = option_menu(
        menu_title="Main Menu",
        options=["Upload Trade File", "Dashboard", "Exit"],
        icons=["cloud-upload", "bar-chart", "box-arrow-right"],
        menu_icon="house",
        default_index=0
    )

# File uploader with session persistence
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# File Upload Section
if selection == "Upload Trade File":
    uploaded_file = st.file_uploader("📂 Upload your trade data (CSV or Excel)", type=["csv", "xlsx"])
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.success("✅ File uploaded successfully. Now go to the Dashboard tab.")

# Dashboard Section
elif selection == "Dashboard":
    if st.session_state.uploaded_file is not None:
        from streamlit_app_dynamic_analysis import run_analysis_dashboard
        run_analysis_dashboard(st.session_state.uploaded_file)
    else:
        st.warning("⚠️ Please upload a file first from the 'Upload Trade File' tab.")

# Exit
elif selection == "Exit":
    st.info("Thank you for using Ryxon. See you soon!")
