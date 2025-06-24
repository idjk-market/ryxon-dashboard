import streamlit as st
import pandas as pd
from datetime import datetime

# Sample trade data
def load_trade_data():
    return pd.DataFrame([
        {
            'id': 'Tr012',
            'instrument': 'Gold',
            'type': 'Future',
            'direction': 'Buy',
            'price': 84.45,
            'quantity': 70.81,
            'trade_date': '12/01/2025',
            'mtm': 1145.76,
            'realized_pnl': 0,
            'unrealized_pnl': -1145.76,
            'daily_return': 5.0075503356,
            'rolling_volatility': 2.4624088284,
            'var': 5342.16807
        },
        {
            'id': 'Tr013',
            'instrument': 'Silver',
            'type': 'Future',
            'direction': 'Sell',
            'price': 22.30,
            'quantity': 150.25,
            'trade_date': '01/01/2025',
            'mtm': 875.42,
            'realized_pnl': 125.50,
            'unrealized_pnl': -320.18,
            'daily_return': 3.2055503356,
            'rolling_volatility': 1.8624088284,
            'var': 4215.45821
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
            'avg_volatility': 0
        }
    
    return {
        'total_mtm': filtered_trades['mtm'].sum(),
        'total_realized_pnl': filtered_trades['realized_pnl'].sum(),
        'total_unrealized_pnl': filtered_trades['unrealized_pnl'].sum(),
        'max_var': filtered_trades['var'].max(),
        'avg_daily_return': filtered_trades['daily_return'].mean(),
        'avg_volatility': filtered_trades['rolling_volatility'].mean()
    }

def main():
    st.set_page_config(layout="wide")
    trades = load_trade_data()
    st.title("Trade Dashboard")

    # Display Trade Table with dynamic filters directly
    st.subheader("Filtered Trades with Dynamic Filters")
    filtered_trades = trades.copy()

    selected_cols = ['instrument', 'type', 'direction', 'trade_date']
    for col in selected_cols:
        unique_vals = ['All'] + sorted(trades[col].unique().tolist())
        selected_val = st.selectbox(f"Filter by {col.capitalize()}", unique_vals, key=col)
        if selected_val != "All":
            filtered_trades = filtered_trades[filtered_trades[col] == selected_val]

    # Display metrics based on filtered data
    metrics = calculate_metrics(filtered_trades)

    st.subheader("Performance Metrics")
    metric_cols = st.columns(4)
    with metric_cols[0]:
        st.metric("Mark-to-Market", f"${metrics['total_mtm']:,.2f}")
    with metric_cols[1]:
        st.metric("1-Day VaR", f"${metrics['max_var']:,.2f}")
    with metric_cols[2]:
        st.metric("Realized PnL", f"${metrics['total_realized_pnl']:,.2f}")
    with metric_cols[3]:
        st.metric("Unrealized PnL", f"${metrics['total_unrealized_pnl']:,.2f}")

    st.caption(f"Avg Daily Return: {metrics['avg_daily_return']:.4f} | Avg Volatility: {metrics['avg_volatility']:.4f}")

    st.subheader(f"Filtered Trades ({len(filtered_trades)})")
    st.dataframe(
        filtered_trades[[
            'id', 'instrument', 'type', 'direction', 
            'price', 'quantity', 'trade_date', 'mtm'
        ]],
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
