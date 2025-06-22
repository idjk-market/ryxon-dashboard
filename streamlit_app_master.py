import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

def calculate_historical_var(df, mtm_column='MTM', trade_column=None, trade_filter=None, confidence_level=95):
    """
    Calculate Historical Value at Risk with trade filtering
    Args:
        df: Input DataFrame
        mtm_column: Column with MTM values
        trade_column: Column to filter trades (optional)
        trade_filter: Specific trade to filter by (optional)
        confidence_level: VaR confidence level
    Returns:
        Historical VaR value and filtered DataFrame
    """
    # Create a copy to avoid modifying original
    working_df = df.copy()
    
    # Apply trade filter if specified
    if trade_column and trade_filter:
        if trade_column not in working_df.columns:
            raise ValueError(f"Trade column '{trade_column}' not found")
        working_df = working_df[working_df[trade_column] == trade_filter]
    
    # Validate MTM column
    if mtm_column not in working_df.columns:
        raise ValueError(f"MTM column '{mtm_column}' not found")
    
    # Clean data
    working_df[mtm_column] = pd.to_numeric(working_df[mtm_column], errors='coerce').fillna(0)
    
    # Calculate returns
    working_df['Daily_Return'] = working_df[mtm_column].pct_change().fillna(0)
    
    # Calculate VaR
    if len(working_df) < 2:
        return None, working_df
    
    sorted_returns = np.sort(working_df['Daily_Return'].dropna())
    var_percentile = 100 - confidence_level
    historical_var = -np.percentile(sorted_returns, var_percentile) * working_df[mtm_column].sum()
    
    return historical_var, working_df

def show_historical_var_module(df):
    """Streamlit UI component with trade filtering"""
    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):
        st.markdown("""
        **Historical VaR** with trade filtering capability.
        - Filter by specific trade before calculation
        - Visualize results for selected subset
        """)
        
        # Configuration
        cols = st.columns(3)
        with cols[0]:
            mtm_col = st.selectbox(
                "MTM Column",
                options=df.columns,
                index=df.columns.get_loc('MTM') if 'MTM' in df.columns else 0
            )
        with cols[1]:
            # Only show trade filter if trade column exists
            trade_col = None
            if any('trade' in col.lower() for col in df.columns):
                trade_col = st.selectbox(
                    "Trade Column (Optional)",
                    options=['None'] + [col for col in df.columns if 'trade' in col.lower()],
                    index=0
                )
                trade_col = None if trade_col == 'None' else trade_col
        with cols[2]:
            confidence = st.slider(
                "Confidence Level",
                min_value=90,
                max_value=99,
                value=95,
                step=1,
                format="%d%%"
            )
        
        # Trade filter selection
        trade_filter = None
        if trade_col:
            trade_options = df[trade_col].unique()
            trade_filter = st.selectbox(
                f"Select {trade_col} to filter",
                options=['All'] + sorted(list(trade_options)),
                index=0
            )
            if trade_filter == 'All':
                trade_filter = None
        
        # Calculate and display results
        try:
            hist_var, filtered_df = calculate_historical_var(
                df,
                mtm_column=mtm_col,
                trade_column=trade_col,
                trade_filter=trade_filter,
                confidence_level=confidence
            )
            
            if hist_var is not None:
                # Main metric
                st.metric(
                    label=f"Historical VaR ({confidence}%)",
                    value=f"₹ {abs(hist_var):,.2f}",
                    delta=f"{hist_var/filtered_df[mtm_col].sum()*100:.2f}% of portfolio",
                    help=f"Maximum expected loss with {confidence}% confidence"
                )
                
                # Summary stats
                with st.expander("View Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Period Analyzed:** {len(filtered_df)} days")
                        st.write(f"**Portfolio Value:** ₹ {filtered_df[mtm_col].sum():,.2f}")
                    with col2:
                        st.write(f"**Filter Applied:** {trade_col}={trade_filter if trade_filter else 'None'}")
                        st.write(f"**Data Points:** {len(filtered_df['Daily_Return'].dropna())}")
                    
                    # Plot returns distribution
                    import plotly.express as px
                    fig = px.histogram(
                        filtered_df,
                        x='Daily_Return',
                        nbins=50,
                        title="Distribution of Daily Returns",
                        labels={'Daily_Return': 'Daily Return (%)'}
                    )
                    fig.add_vline(
                        x=-abs(hist_var)/filtered_df[mtm_col].sum(),
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"VaR {confidence}%",
                        annotation_position="top left"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data points for calculation (need at least 2 valid observations)")
                
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

# Example usage
if __name__ == "__main__":
    st.title("Advanced VaR Calculator with Trade Filtering")
    
    # Sample data with trade information
    @st.cache_data
    def load_sample_data():
        np.random.seed(42)
        dates = pd.date_range(end=datetime.today(), periods=100)
        trades = np.random.choice(['Trade_A', 'Trade_B', 'Trade_C'], 100)
        returns = np.random.normal(0.001, 0.02, 100)
        mtm = 1000000 * (1 + returns).cumprod()
        return pd.DataFrame({
            'Date': dates,
            'MTM': mtm,
            'Trade_ID': trades,
            'Trade_Type': np.random.choice(['Equity', 'Fixed Income', 'Commodity'], 100)
        })
    
    data = load_sample_data()
    show_historical_var_module(data)
