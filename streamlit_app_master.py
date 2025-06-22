import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

def calculate_historical_var(df, mtm_column='MTM', confidence_level=95):
    """
    Calculate Historical Value at Risk for a given DataFrame
    Args:
        df: Pandas DataFrame containing MTM data
        mtm_column: Name of the column containing MTM values
        confidence_level: VaR confidence level (e.g., 95 for 95%)
    Returns:
        Historical VaR value
    """
    # Validate inputs
    if mtm_column not in df.columns:
        raise ValueError(f"Column '{mtm_column}' not found in DataFrame")
    
    # Clean and prepare data
    df[mtm_column] = pd.to_numeric(df[mtm_column], errors='coerce').fillna(0)
    
    # Calculate daily returns (percentage changes)
    df['Daily_Return'] = df[mtm_column].pct_change().fillna(0)
    
    # Calculate VaR
    if len(df) < 2:
        return None  # Not enough data
    
    sorted_returns = np.sort(df['Daily_Return'].dropna())
    var_percentile = 100 - confidence_level
    historical_var = -np.percentile(sorted_returns, var_percentile) * df[mtm_column].sum()
    
    return historical_var

def show_historical_var_module(df):
    """Streamlit UI component for Historical VaR"""
    with st.expander("📊 Historical Value at Risk (Hist VaR)", expanded=False):
        st.markdown("""
        **Historical VaR** estimates potential loss based on actual historical market movements.
        - Uses your portfolio's historical MTM changes
        - Non-parametric approach (no distribution assumptions)
        """)
        
        # Configuration
        col1, col2 = st.columns(2)
        with col1:
            mtm_col = st.selectbox(
                "Select MTM Column",
                options=df.columns,
                index=df.columns.get_loc('MTM') if 'MTM' in df.columns else 0
            )
        with col2:
            confidence = st.slider(
                "Confidence Level (%)",
                min_value=90,
                max_value=99,
                value=95,
                help="Probability level for VaR calculation (e.g., 95% = 5% chance of exceeding this loss)"
            )
        
        # Calculate and display results
        try:
            hist_var = calculate_historical_var(df, mtm_col, confidence)
            
            if hist_var is not None:
                st.metric(
                    label=f"Historical VaR ({confidence}%)",
                    value=f"₹ {abs(hist_var):,.2f}",
                    delta=f"{hist_var/df[mtm_col].sum()*100:.2f}% of portfolio",
                    help=f"Maximum expected loss with {confidence}% confidence based on historical data"
                )
                
                # Additional diagnostics
                with st.expander("Diagnostics"):
                    st.write(f"Analysis period: {len(df)} days")
                    st.write(f"Portfolio value: ₹ {df[mtm_col].sum():,.2f}")
                    
                    # Plot historical returns distribution
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()
                    ax.hist(df['Daily_Return'].dropna(), bins=50, alpha=0.7)
                    ax.axvline(x=-abs(hist_var)/df[mtm_col].sum(), color='red', linestyle='--')
                    ax.set_title("Distribution of Daily Returns")
                    ax.set_xlabel("Daily Return")
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)
            else:
                st.warning("Not enough data points (need at least 2) to compute Historical VaR.")
                
        except Exception as e:
            st.error(f"Error calculating Historical VaR: {str(e)}")

# Example usage in a Streamlit app
if __name__ == "__main__":
    st.title("Risk Management Dashboard")
    
    # Sample data - replace with your actual data loading logic
    @st.cache_data
    def load_sample_data():
        dates = pd.date_range(end=datetime.today(), periods=100)
        returns = np.random.normal(0.001, 0.02, 100)
        mtm = 1000000 * (1 + returns).cumprod()
        return pd.DataFrame({'Date': dates, 'MTM': mtm})
    
    data = load_sample_data()
    
    # Show the module
    show_historical_var_module(data)
