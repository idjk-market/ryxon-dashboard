# homepage.py
import streamlit as st
import pandas as pd
from datetime import datetime

# Custom CSS for cleaner filters
st.markdown("""
<style>
    /* Cleaner filter section */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Better metric cards */
    .metric-card {
        border-left: 4px solid #4e79a7;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        background: white;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Table improvements */
    .stDataFrame {
        border-radius: 0.5rem;
    }
    
    /* Custom selectbox styling */
    div[data-baseweb="select"] > div {
        border-radius: 0.5rem !important;
    }
    
    /* Hide fullscreen button */
    button[title="View fullscreen"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample trade data
@st.cache_data
def load_trade_data():
    return pd.DataFrame([
        {
            'id': 'Tr012', 'instrument': 'Gold', 'type': 'Future', 
            'direction': 'Buy', 'price': 84.45, 'quantity': 70.81,
            'trade_date': '12/01/2025', 'mtm': 1145.76, 'realized_pnl': 0,
            'unrealized_pnl': -1145.76, 'daily_return': 5.0076, 
            'rolling_volatility': 2.4624, 'var': 5342.17
        },
        {
            'id': 'Tr013', 'instrument': 'Silver', 'type': 'Future',
            'direction': 'Sell', 'price': 22.30, 'quantity': 150.25,
            'trade_date': '01/01/2025', 'mtm': 875.42, 'realized_pnl': 125.50,
            'unrealized_pnl': -320.18, 'daily_return': 3.2056,
            'rolling_volatility': 1.8624, 'var': 4215.46
        },
        {
            'id': 'Tr014', 'instrument': 'Oil', 'type': 'Future',
            'direction': 'Buy', 'price': 75.30, 'quantity': 89.10,
            'trade_date': '01/01/2025', 'mtm': 138.00, 'realized_pnl': 0,
            'unrealized_pnl': 138.00, 'daily_return': 0.0000,
            'rolling_volatility': 0.0000, 'var': 84.49
        }
    ])

def calculate_metrics(filtered_trades):
    if filtered_trades.empty:
        return {
            'total_mtm': 0,
            'total_realized_pnl': 0,
            'total_unrealized_pnl': 0,
            'max_var': 0,
            'avg_daily_return': 0,
            'avg_volatility': 0,
            'trade_count': 0
        }
    
    return {
        'total_mtm': filtered_trades['mtm'].sum(),
        'total_realized_pnl': filtered_trades['realized_pnl'].sum(),
        'total_unrealized_pnl': filtered_trades['unrealized_pnl'].sum(),
        'max_var': filtered_trades['var'].max(),
        'avg_daily_return': filtered_trades['daily_return'].mean(),
        'avg_volatility': filtered_trades['rolling_volatility'].mean(),
        'trade_count': len(filtered_trades)
    }

def main():
    st.set_page_config(layout="wide", page_title="Trade Analytics Dashboard")
    
    # Load data
    trades = load_trade_data()
    
    # Title with custom styling
    st.markdown("""
    <div style='border-bottom: 1px solid #e6e6e6; padding-bottom: 1rem; margin-bottom: 1.5rem;'>
        <h1 style='margin: 0;'>Trade Analytics Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter section with custom layout
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            instrument_filter = st.selectbox(
                "Instrument",
                options=["All"] + sorted(trades['instrument'].unique().tolist()),
                key="instrument_filter",
                index=0
            )
        
        with col2:
            commodity_filter = st.selectbox(
                "Commodity", 
                options=["All"] + sorted(trades['instrument'].unique().tolist()),
                key="commodity_filter",
                index=0
            )
        
        with col3:
            date_filter = st.selectbox(
                "Trade Date",
                options=["All"] + sorted(trades['trade_date'].unique().tolist()),
                key="date_filter",
                index=0
            )
    
    # Apply filters
    filtered_trades = trades.copy()
    if instrument_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['instrument'] == instrument_filter]
    if commodity_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['instrument'] == commodity_filter]
    if date_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['trade_date'] == date_filter]
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_trades)
    
    # Metrics display with custom cards
    with st.container():
        st.markdown("### Performance Summary")
        
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #666;">Mark-to-Market</div>
                <div style="font-size: 1.5rem; font-weight: bold;">${metrics['total_mtm']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[1]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #666;">1-Day VaR</div>
                <div style="font-size: 1.5rem; font-weight: bold;">${metrics['max_var']:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[2]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #666;">Realized PnL</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {'red' if metrics['total_realized_pnl'] < 0 else 'green'}">
                    ${metrics['total_realized_pnl']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with metric_cols[3]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #666;">Unrealized PnL</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: {'red' if metrics['total_unrealized_pnl'] < 0 else 'green'}">
                    ${metrics['total_unrealized_pnl']:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional metrics in smaller cards
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; margin-top: 1rem;">
            <div class="metric-card" style="flex: 1;">
                <div style="font-size: 0.8rem; color: #666;">Avg Daily Return</div>
                <div style="font-size: 1.1rem;">{metrics['avg_daily_return']:.4f}</div>
            </div>
            <div class="metric-card" style="flex: 1;">
                <div style="font-size: 0.8rem; color: #666;">Avg Volatility</div>
                <div style="font-size: 1.1rem;">{metrics['avg_volatility']:.4f}</div>
            </div>
            <div class="metric-card" style="flex: 1;">
                <div style="font-size: 0.8rem; color: #666;">Trade Count</div>
                <div style="font-size: 1.1rem;">{metrics['trade_count']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Trade table with improved display
    with st.container():
        st.markdown(f"### Trade Details ({metrics['trade_count']} trades)")
        
        # Format the display dataframe
        display_df = filtered_trades[[
            'id', 'instrument', 'type', 'direction', 
            'price', 'quantity', 'trade_date', 'mtm'
        ]].copy()
        
        display_df['price'] = display_df['price'].map("${:,.2f}".format)
        display_df['mtm'] = display_df['mtm'].map("${:,.2f}".format)
        display_df['quantity'] = display_df['quantity'].map("{:,.2f}".format)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": "Trade ID",
                "instrument": "Instrument",
                "type": "Type",
                "direction": st.column_config.SelectboxColumn(
                    "Direction",
                    options=["Buy", "Sell"]
                ),
                "price": "Price",
                "quantity": "Quantity",
                "trade_date": "Trade Date",
                "mtm": "MTM"
            }
        )

if __name__ == "__main__":
    main()
