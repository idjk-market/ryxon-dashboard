import streamlit as st
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary-color: #2962FF;
        --success-color: #00C853;
        --warning-color: #FFAB00;
        --danger-color: #D50000;
        --bg-color: #0E1117;
        --card-color: #1E1E1E;
        --text-color: #FAFAFA;
        --border-color: #333333;
    }
    
    .metric-card {
        background-color: var(--card-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .metric-title {
        color: #9E9E9E;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .metric-change {
        display: flex;
        align-items: center;
        font-size: 1rem;
    }
    
    .positive {
        color: var(--success-color);
    }
    
    .status-active {
        color: var(--success-color);
    }
    
    .status-expired {
        color: #9E9E9E;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--card-color) !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: var(--bg-color);
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
    
    # Dark mode toggle
    dark_mode = st.toggle("Dark Mode", value=True)

# Main content
st.title("Dashboard")

# Metrics cards
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

# Create a DataFrame with the trades data
trades_data = {
    "Trade ID": ["FX-2023-0456", "IRS-2023-0789", "OPT-2023-0321"],
    "Instrument": ["EUR/USD", "10Y IRS", "SPX Call"],
    "Notional": ["$5,000,000", "$10,000,000", "$2,500,000"],
    "Price": [1.0856, 2.34, 35.5],
    "Date": ["2023-05-15", "2023-05-14", "2023-05-13"],
    "Status": ["Active", "Active", "Expired"]
}
trades_df = pd.DataFrame(trades_data)

# Style the DataFrame
def style_status(val):
    color = "var(--success-color)" if val == "Active" else "#9E9E9E"
    return f"color: {color}"

styled_df = trades_df.style.applymap(style_status, subset=["Status"])

# Display the styled DataFrame
st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Price": st.column_config.NumberColumn(format="%.4f"),
        "Date": st.column_config.DateColumn()
    }
)
