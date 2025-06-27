import streamlit as st
import pandas as pd

# Configure page with light theme
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light theme
st.markdown("""
<style>
    :root {
        --primary-color: #2962FF;
        --success-color: #00C853;
        --warning-color: #FFAB00;
        --danger-color: #D50000;
        --bg-color: #FFFFFF;
        --card-color: #F8F9FA;
        --text-color: #212529;
        --border-color: #DFE3E7;
    }
    
    body {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    .metric-card {
        background-color: var(--card-color);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid var(--border-color);
    }
    
    .metric-title {
        color: #6C757D;
        font-size: 1rem;
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .metric-change {
        font-size: 0.9rem;
    }
    
    .positive {
        color: var(--success-color);
    }
    
    .status-active {
        color: var(--success-color);
        font-weight: 500;
    }
    
    .status-expired {
        color: #6C757D;
    }
    
    /* Table styling */
    .stDataFrame {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid var(--border-color) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Trading Dashboard")
    
    menu_options = ["Dashboard", "Upload Trades", "Manual Entry", "Analytics", "Settings"]
    selected_menu = st.radio(
        "Navigation",
        menu_options,
        index=0
    )
    
    st.divider()
    
    # Theme toggle
    dark_mode = st.toggle("Dark Mode", value=False)

# Main content
st.title("Dashboard")

# Metrics cards in columns
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

# Recent trades table
st.subheader("Recent Trades")

# Create DataFrame
trades_data = {
    "Trade ID": ["FX-2023-0456", "IRS-2023-0789", "OPT-2023-0321"],
    "Instrument": ["EUR/USD", "10Y IRS", "SPX Call"],
    "Notional": ["$5,000,000", "$10,000,000", "$2,500,000"],
    "Price": [1.0856, 2.3400, 35.5000],
    "Date": ["2023-05-15", "2023-05-14", "2023-05-13"],
    "Status": ["Active", "Active", "Expired"]
}
trades_df = pd.DataFrame(trades_data)

# Format the DataFrame display
st.dataframe(
    trades_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Price": st.column_config.NumberColumn(format="%.4f"),
        "Date": st.column_config.DateColumn(),
        "Status": st.column_config.TextColumn()
    }
)

# Additional metrics at bottom
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
