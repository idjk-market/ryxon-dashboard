import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    :root {
        --primary: #3a7bd5;
        --primary-light: #5a9df5;
        --secondary: #00d2ff;
        --success: #00C853;
        --text: #2c3e50;
        --light-bg: #f8f9fa;
        --card-bg: #ffffff;
        --border: #e0e0e0;
    }
    
    /* Main container */
    .main {
        background-color: #f5f7fa;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary), var(--secondary)) !important;
        padding: 1.5rem 1rem !important;
    }
    
    .sidebar-title {
        color: white !important;
        font-size: 1.5rem !important;
        margin-bottom: 2rem !important;
        font-weight: 700 !important;
        padding: 0 0.5rem;
    }
    
    /* Modern menu items */
    .menu-item {
        padding: 0.75rem 1rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        color: white !important;
    }
    
    .menu-item:hover {
        background: rgba(255,255,255,0.15) !important;
    }
    
    .menu-item.active {
        background: white !important;
        color: var(--primary) !important;
        font-weight: 600 !important;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
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
        color: var(--success);
    }
    
    /* Table card */
    .table-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 1.5rem;
        border: 1px solid var(--border);
    }
    
    /* Status indicators */
    .status-active {
        color: var(--success);
        font-weight: 500;
    }
    
    .status-expired {
        color: #6c757d;
    }
    
    /* Footer */
    .footer {
        color: white;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding: 0 0.5rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown('<div class="sidebar-title">Trading Dashboard</div>', unsafe_allow_html=True)
    
    # Modern navigation menu with icons
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
                "color": "white",
                "font-size": "1rem",
            },
            "nav-link": {
                "font-size": "0.9rem",
                "text-align": "left",
                "margin": "0.25rem 0",
                "padding": "0.75rem 1rem",
                "border-radius": "8px",
                "color": "white",
                "transition": "all 0.3s ease",
            },
            "nav-link-selected": {
                "background-color": "white",
                "color": "var(--primary)",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "rgba(255,255,255,0.15)",
            },
        }
    )
    
    # Footer with last updated
    st.markdown("""
    <div class="footer">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8V12L15 15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Last updated: Just now
        </div>
        <div style="display: flex; align-items: center;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 8px;">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 16V12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8H12.01" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            v2.1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====
st.title("Dashboard")

# Top Metrics Row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Open Positions</div>
        <div class="metric-value">142</div>
        <div class="metric-change positive">↑ +12% from last week</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Risk Exposure</div>
        <div class="metric-value">$4.2M</div>
        <div class="metric-change positive">↑ Within limits</div>
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

# Recent Trades Table
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

# Display styled dataframe
st.dataframe(
    trades_df.style.applymap(
        lambda x: "color: #00C853" if x == "Active" else "color: #6c757d",
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

# Bottom Metrics Row
col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Risk Exposure</div>
        <div class="metric-value">$4.2M</div>
        <div class="metric-change positive">↑ Within limits</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Today's P&L</div>
        <div class="metric-value">$124K</div>
        <div class="metric-change positive">↑ +2.4% MTD</div>
    </div>
    """, unsafe_allow_html=True)
