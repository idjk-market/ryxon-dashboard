# homepage.py
import streamlit as st
import pandas as pd

# Sample trade data - replace with your actual data
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
            'id': 'Tr014', 'instrument': 'Gold', 'type': 'Option',
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
            'trade_count': 0
        }
    
    return {
        'total_mtm': filtered_trades['mtm'].sum(),
        'total_realized_pnl': filtered_trades['realized_pnl'].sum(),
        'total_unrealized_pnl': filtered_trades['unrealized_pnl'].sum(),
        'max_var': filtered_trades['var'].max(),
        'trade_count': len(filtered_trades)
    }

def main():
    st.set_page_config(layout="wide")
    
    # Load data
    trades = load_trade_data()
    
    # Title
    st.title("Trade Dashboard")
    
    # FILTERS - Only for trade table columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        instrument_filter = st.selectbox(
            "Instrument",
            ["All"] + sorted(trades['instrument'].unique().tolist())
        )
    
    with col2:
        type_filter = st.selectbox(
            "Type", 
            ["All"] + sorted(trades['type'].unique().tolist())
        )
    
    with col3:
        direction_filter = st.selectbox(
            "Direction",
            ["All"] + sorted(trades['direction'].unique().tolist())
        )
    
    # Apply filters
    filtered_trades = trades.copy()
    if instrument_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['instrument'] == instrument_filter]
    if type_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['type'] == type_filter]
    if direction_filter != "All":
        filtered_trades = filtered_trades[filtered_trades['direction'] == direction_filter]
    
    # Calculate metrics FROM FILTERED DATA
    metrics = calculate_metrics(filtered_trades)
    
    # METRICS - Dynamically update based on filters
    st.subheader("Performance Metrics")
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric("Mark-to-Market", f"${metrics['total_mtm']:,.2f}")
    
    with metric_cols[1]:
        st.metric("1-Day VaR", f"${metrics['max_var']:,.2f}")
    
    with metric_cols[2]:
        st.metric("Realized PnL", 
                 f"${metrics['total_realized_pnl']:,.2f}",
                 delta_color="inverse")
    
    with metric_cols[3]:
        st.metric("Unrealized PnL", 
                 f"${metrics['total_unrealized_pnl']:,.2f}",
                 delta_color="inverse")
    
    # TRADE TABLE - Shows filtered data
    st.subheader(f"Filtered Trades ({metrics['trade_count']})")
    
    # Format display columns
    display_cols = ['id', 'instrument', 'type', 'direction', 
                   'price', 'quantity', 'trade_date', 'mtm']
    
    st.dataframe(
        filtered_trades[display_cols],
        column_config={
            "price": st.column_config.NumberColumn(format="$%.2f"),
            "mtm": st.column_config.NumberColumn(format="$%.2f"),
            "quantity": st.column_config.NumberColumn(format="%.2f")
        },
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
