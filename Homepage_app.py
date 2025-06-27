import streamlit as st
from trade_register import show_trade_register
from trade_entry import show_trade_entry
from risk_analytics import show_risk_analytics
from mtm_daily_pnl_app import show_mtm_pnl
from physical_exposure import show_exposure
from lifecycle_manager import show_lifecycle
from instrument_master import show_instruments
from reporting_app import show_reporting

# Configuration
st.set_page_config(
    page_title="Ryxon Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Navigation
def show_navigation():
    st.sidebar.image("ryxon_logo.png", width=200)
    st.sidebar.title("Navigation")
    
    pages = {
        "🏠 Home": "home",
        "📂 Trade Register": "register",
        "✍️ Trade Entry": "entry",
        "📊 Risk Analytics": "analytics",
        "💹 MTM & PnL": "mtm",
        "🌍 Physical Exposure": "exposure",
        "🔄 Lifecycle Manager": "lifecycle",
        "📋 Instrument Master": "instruments",
        "📄 Reports": "reports"
    }
    
    for label, page in pages.items():
        if st.sidebar.button(label, use_container_width=True):
            st.session_state.current_page = page
            st.rerun()

# Main App Logic
def main():
    show_navigation()
    
    if st.session_state.current_page == "home":
        show_homepage()
    elif st.session_state.current_page == "register":
        show_trade_register()
    elif st.session_state.current_page == "entry":
        show_trade_entry()
    elif st.session_state.current_page == "analytics":
        show_risk_analytics()
    elif st.session_state.current_page == "mtm":
        show_mtm_pnl()
    elif st.session_state.current_page == "exposure":
        show_exposure()
    elif st.session_state.current_page == "lifecycle":
        show_lifecycle()
    elif st.session_state.current_page == "instruments":
        show_instruments()
    elif st.session_state.current_page == "reports":
        show_reporting()

def show_homepage():
    st.title("📊 Ryxon Trading Risk Intelligence")
    st.markdown("""
    <div style='background-color: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 10px;'>
        <h3>Integrated risk platform for derivatives, commodities, and exposure management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open Positions", "142", "+12%")
    with col2:
        st.metric("Risk Exposure", "$4.2M", "Within limits")
    with col3:
        st.metric("Today's P&L", "$124K", "+2.4%")
    
    st.markdown("---")
    st.subheader("Get Started")
    st.write("Use the sidebar to navigate to different modules")

if __name__ == "__main__":
    main()
