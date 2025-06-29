import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Configure page
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with professional color scheme
st.markdown("""
<style>
    :root {
        --sidebar-bg: #1a2e4a;  /* Deep navy blue */
        --sidebar-hover: #2a3e5a;
        --sidebar-active: #3a4e6a;
        --primary-text: #ffffff;
        --secondary-text: #a8c0e0;
        --card-bg: #ffffff;
        --metric-value: #2c3e50;
        --positive: #4CAF50;
        --neutral: #FFC107;
        --border: #e0e0e0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        padding: 2rem 1rem !important;
        border-right: 1px solid var(--border) !important;
    }
    
    .sidebar-title {
        color: var(--primary-text) !important;
        font-size: 1.5rem !important;
        margin-bottom: 2rem !important;
        font-weight: 600 !important;
        padding: 0 0.5rem;
    }
    
    /* Menu items */
    .st-ae {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebarNavLink"] {
        color: var(--secondary-text) !important;
        margin: 0.5rem 0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebarNavLink"]:hover {
        background-color: var(--sidebar-hover) !important;
        color: var(--primary-text) !important;
    }
    
    [data-testid="stSidebarNavLink"].active {
        background-color: var(--sidebar-active) !important;
        color: var(--primary-text) !important;
        font-weight: 600 !important;
    }
    
    /* Main content */
    .main .block-container {
        background-color: #f5f7fa;
    }
    
    /* Cards */
    .metric-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid var(--border);
        height: 100%;
    }
    
    .metric-title {
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: var(--metric-value);
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .metric-change {
        font-size: 0.9rem;
        display: flex;
        align-items: center;
    }
    
    .positive {
        color: var(--positive);
    }
    
    .neutral {
        color: var(--neutral);
    }
    
    /* Table */
    .table-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-top: 1.5rem;
        border: 1px solid var(--border);
    }
    
    .status-active {
        color: var(--positive);
        font-weight: 500;
    }
    
    .status-expired {
        color: #6c757d;
    }
    
    /* Footer */
    .footer {
        color: var(--secondary-text);
        font-size: 0.8rem;
        margin-top: 2rem;
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="sidebar-title">Trading Dashboard</div>', unsafe_allow_html=True)
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Upload Trades", "Manual Entry", "Analytics", "Settings"],
        icons=["speedometer2", "cloud-upload", "pencil-square", "graph-up", "gear"],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
            },
            "icon": {
                "color": "var(--secondary-text)",
                "font-size": "1rem",
            },
            "nav-link": {
                "font-size": "0.9rem",
                "text-align": "left",
                "margin": "0.25rem 0",
                "padding": "0.75rem 1rem",
                "border-radius": "8px",
                "color": "var(--secondary-text)",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "background-color": "var(--sidebar-active)",
                "color": "var(--primary-text)",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "var(--sidebar-hover)",
                "color": "var(--primary-text)",
            },
        }
    )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="var(--secondary-text)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8V12L15 15" stroke="var(--secondary-text)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Last updated: Just now
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====
st.title("Dashboard")

# Top Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Open Positions</div>
        <div class="metric-value">142</div>
        <div class="metric-change positive">↑ +1.2% from last week</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Risk Exposure</div>
        <div class="metric-value">$4.2M</div>
        <div class="metric-change neutral">• Within limits</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Today's P&L</div>
        <div class="metric-value">$124K</div>
        <div class="metric-change positive">↑ +2.4% MTD</div>
    </div>
    """, unsafe_allow_html=True)

# Recent Trades
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.subheader("Recent Trades")

trades_data = {
    "Trade ID": ["FX:2023-0456", "IRS:2023-0789", "OPT:2023-0321"],
    "Instrument": ["EUR/USD", "10Y IRS", "SPX Call"],
    "Notional": ["$5,000,000", "$10,000,000", "$2,500,000"],
    "Price": [1.0856, 2.3400, 35.5000],
    "Date": ["2023-05-15", "2023-05-14", "2023-05-13"],
    "Status": ["Active", "Active", "Expired"]
}
trades_df = pd.DataFrame(trades_data)

# Display dataframe with styled status
st.dataframe(
    trades_df.style.applymap(
        lambda x: "color: #4CAF50" if x == "Active" else "color: #6c757d",
        subset=["Status"]
    ),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Price": st.column_config.NumberColumn(format="%.4f"),
        "Date": st.column_config.DateColumn()
    }
)
st.markdown('</div>', unsafe_allow_html=True)
