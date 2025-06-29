# Homepage_app.py
import streamlit as st
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
with st.sidebar:
    st.image("ryxon_logo.png", width=150)
    st.title("Trading Dashboard")
    
    # Navigation menu
    nav_choice = st.radio(
        "Menu",
        ["Dashboard", "Upload Trades", "Manual Entry", "Analytics", "Settings"],
        index=0
    )

# Main Content Area
if nav_choice == "Dashboard":
    st.header("Dashboard")
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Open Positions",
            value="142",
            delta="+1.2% from last week"
        )
    with col2:
        st.metric(
            label="Risk Exposure",
            value="$4.2M",
            delta="Within limits"
        )
    with col3:
        st.metric(
            label="Today's P&L",
            value="$124K",
            delta="+2.4% MTD"
        )
    
    # Recent Trades Table
    st.subheader("Recent Trades")
    recent_trades = pd.DataFrame([
        {
            "Trade ID": "FX:2023-0456",
            "Instrument": "EUR/USD",
            "Notional": "$5,000,000",
            "Price": 1.0856,
            "Date": "2023-05-15",
            "Status": "Active"
        },
        {
            "Trade ID": "IRS:2023-0789",
            "Instrument": "10Y IRS",
            "Notional": "$10,000,000",
            "Price": 2.3400,
            "Date": "2023-05-14",
            "Status": "Active"
        },
        {
            "Trade ID": "OPT:2023-0321",
            "Instrument": "SPX Call",
            "Notional": "$2,500,000",
            "Price": 35.5000,
            "Date": "2023-05-13",
            "Status": "Expired"
        }
    ])
    st.dataframe(recent_trades, hide_index=True, use_container_width=True)

elif nav_choice == "Upload Trades":
    from trade_input import render_upload_trades
    render_upload_trades()

elif nav_choice == "Manual Entry":
    from trade_entry import render_manual_entry
    render_manual_entry()

elif nav_choice == "Analytics":
    from risk_analytics import render_analytics
    render_analytics()

elif nav_choice == "Settings":
    st.header("Settings")
    # Settings content would go here
