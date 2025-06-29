# Homepage_app.py
import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# Set page config
st.set_page_config(
    page_title="Trading Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for trades if not exists
if 'trades' not in st.session_state:
    st.session_state.trades = pd.DataFrame([
        {
            "Trade ID": "FX:2023-0456",
            "Instrument": "EUR/USD",
            "Notional": 5000000,
            "Price": 1.0856,
            "Date": "2023-05-15",
            "Status": "Active",
            "Type": "FX"
        },
        {
            "Trade ID": "IRS:2023-0789",
            "Instrument": "10Y IRS",
            "Notional": 10000000,
            "Price": 2.3400,
            "Date": "2023-05-14",
            "Status": "Active",
            "Type": "IRS"
        }
    ])

# Sidebar Navigation
with st.sidebar:
    st.image("ryxon_logo.png", width=150)
    st.title("Trading Dashboard")
    nav_choice = st.radio(
        "Menu",
        ["Dashboard", "Upload Trades", "Manual Entry", "Analytics", "Settings"],
        index=0
    )

# Dashboard Page
if nav_choice == "Dashboard":
    st.header("Dashboard")
    
    # Calculate metrics from session state
    total_positions = len(st.session_state.trades[st.session_state.trades['Status'] == 'Active'])
    total_notional = st.session_state.trades['Notional'].sum() / 1e6  # in millions
    pnl = 124000  # Placeholder - would calculate from positions
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Open Positions", f"{total_positions}", "+1.2% from last week")
    with col2:
        st.metric("Risk Exposure", f"${total_notional:.1f}M", "Within limits")
    with col3:
        st.metric("Today's P&L", f"${pnl:,.0f}", "+2.4% MTD")
    
    # Recent Trades Table
    st.subheader("Recent Trades")
    st.dataframe(st.session_state.trades, hide_index=True, use_container_width=True)

# Upload Trades Page
elif nav_choice == "Upload Trades":
    st.header("Upload Trades")
    
    uploaded_file = st.file_uploader("Choose a trade file (CSV/Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                new_trades = pd.read_csv(uploaded_file)
            else:
                new_trades = pd.read_excel(uploaded_file)
            
            # Generate Trade IDs for new trades
            new_trades['Trade ID'] = [
                f"{typ}:{datetime.now().year}-{i+1000}" 
                for i, typ in enumerate(new_trades.get('Type', ['NEW']*len(new_trades)))
            ]
            
            # Add to session state
            st.session_state.trades = pd.concat([st.session_state.trades, new_trades])
            st.success(f"Added {len(new_trades)} new trades!")
            
            # Show analytics
            st.subheader("Upload Analytics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Trades", len(st.session_state.trades))
                st.metric("Total Notional", f"${st.session_state.trades['Notional'].sum()/1e6:.2f}M")
            with col2:
                st.metric("Unique Instruments", st.session_state.trades['Instrument'].nunique())
                st.metric("Earliest Trade", st.session_state.trades['Date'].min())

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Manual Entry Page
elif nav_choice == "Manual Entry":
    st.header("Manual Trade Entry")
    
    with st.form("trade_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            trade_type = st.selectbox("Trade Type", ["FX", "IRS", "OPT", "BOND", "EQUITY"])
            instrument = st.text_input("Instrument")
            notional = st.number_input("Notional", min_value=0.0)
            
        with col2:
            price = st.number_input("Price", min_value=0.0)
            trade_date = st.date_input("Trade Date", datetime.now())
            status = st.selectbox("Status", ["Active", "Pending", "Expired", "Cancelled"])
        
        submitted = st.form_submit_button("Submit Trade")
        
        if submitted:
            if not instrument:
                st.error("Instrument is required")
            else:
                # Generate trade ID
                trade_id = f"{trade_type}:{datetime.now().year}-{len(st.session_state.trades)+1000}"
                
                # Add to session state
                new_trade = pd.DataFrame([{
                    "Trade ID": trade_id,
                    "Instrument": instrument,
                    "Notional": notional,
                    "Price": price,
                    "Date": trade_date.strftime('%Y-%m-%d'),
                    "Status": status,
                    "Type": trade_type
                }])
                
                st.session_state.trades = pd.concat([st.session_state.trades, new_trade])
                st.success(f"Trade {trade_id} submitted successfully!")

# Analytics Page
elif nav_choice == "Analytics":
    st.header("Risk Analytics")
    
    if not st.session_state.trades.empty:
        # Calculate basic analytics
        analytics = st.session_state.trades.groupby('Instrument').agg({
            'Notional': 'sum',
            'Price': 'mean'
        }).rename(columns={
            'Notional': 'Exposure',
            'Price': 'AvgPrice'
        })
        
        analytics['VaR'] = analytics['Exposure'] * 0.05  # Simple 5% VaR placeholder
        analytics['PnL'] = analytics['Exposure'] * 0.01  # Placeholder PnL calculation
        
        st.dataframe(analytics, use_container_width=True)
        
        # Visualization
        st.subheader("Exposure by Instrument")
        st.bar_chart(analytics['Exposure'])
        
        with st.expander("Detailed Metrics"):
            selected_instrument = st.selectbox(
                "Select Instrument",
                analytics.index.unique()
            )
            inst_data = analytics.loc[selected_instrument]
            
            cols = st.columns(3)
            cols[0].metric("Exposure", f"${inst_data['Exposure']:,.2f}")
            cols[1].metric("VaR (95%)", f"${inst_data['VaR']:,.2f}")
            cols[2].metric("Estimated PnL", f"${inst_data['PnL']:,.2f}")
    else:
        st.warning("No trades available for analytics")

# Settings Page
elif nav_choice == "Settings":
    st.header("Settings")
    st.write("Configuration options will appear here")
