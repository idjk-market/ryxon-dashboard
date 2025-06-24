import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Configure page - THIS MUST BE FIRST
st.set_page_config(
    page_title="Ryxon Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

def load_data(uploaded_file):
    """Load data from either Excel or CSV file"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            file_bytes = BytesIO(uploaded_file.getvalue())
            return pd.read_excel(file_bytes, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def calculate_metrics(df):
    """Calculate all required metrics"""
    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
    df['Realized PnL'] = np.where(df['Trade Action'].str.lower() == 'sell', df['MTM'], 0)
    df['Unrealized PnL'] = np.where(df['Trade Action'].str.lower() == 'buy', df['MTM'], 0)
    df['Daily Return'] = df['MTM'].pct_change().fillna(0)
    return df

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")
    
    # File uploader with clear instructions
    uploaded_file = st.file_uploader(
        "Upload Trade Data (Excel or CSV)",
        type=["xlsx", "csv"],
        help="Maximum file size: 200MB. Supported formats: .xlsx, .csv"
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                # Load and process data
                df = load_data(uploaded_file)
                
                if df is not None:
                    # Calculate all metrics
                    df = calculate_metrics(df)
                    
                    # Store in session state
                    st.session_state.processed_data = df
                    
                    # ===========================================
                    # 1. TRADE DATA TABLE (Always visible)
                    # ===========================================
                    st.subheader("Trade Data Overview")
                    st.dataframe(
                        df.style.format({
                            'Book Price': '{:.2f}',
                            'Market Price': '{:.2f}',
                            'MTM': '{:.2f}',
                            'Realized PnL': '{:.2f}',
                            'Unrealized PnL': '{:.2f}',
                            'Daily Return': '{:.4f}',
                            'Rolling Std Dev': '{:.4f}',
                            '1-Day VAR': '{:.2f}'
                        }),
                        height=400,
                        use_container_width=True
                    )
                    
                    # ===========================================
                    # 2. MTM CALCULATION SECTION (Expandable)
                    # ===========================================
                    with st.expander("🧮 MTM Calculation Details", expanded=True):
                        st.markdown("""
                        **Mark-to-Market Calculation:**  
                        `MTM = (Market Price - Book Price) × Quantity`
                        """)
                        
                        # Show calculation examples
                        st.write("Sample Calculations:")
                        example_df = df[['Trade ID', 'Commodity', 'Book Price', 'Market Price', 'Quantity', 'MTM']].head(3)
                        st.dataframe(example_df, use_container_width=True)
                        
                        # MTM Distribution visualization
                        st.subheader("MTM Value Distribution")
                        fig = px.histogram(df, x='MTM', nbins=20, 
                                         title="Distribution of MTM Values Across Trades")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # ===========================================
                    # 3. PnL ANALYSIS SECTION (Expandable)
                    # ===========================================
                    with st.expander("💰 Profit & Loss Analysis", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        # Realized PnL
                        with col1:
                            st.metric("Total Realized PnL", 
                                    f"${df['Realized PnL'].sum():,.2f}",
                                    help="Profit/Loss from closed positions")
                            st.write("Realized Trades:")
                            realized_trades = df[df['Realized PnL'] != 0][['Trade ID', 'Commodity', 'Realized PnL']]
                            st.dataframe(realized_trades, height=250, use_container_width=True)
                        
                        # Unrealized PnL
                        with col2:
                            st.metric("Total Unrealized PnL", 
                                    f"${df['Unrealized PnL'].sum():,.2f}",
                                    help="Current paper profit/loss from open positions")
                            st.write("Unrealized Trades:")
                            unrealized_trades = df[df['Unrealized PnL'] != 0][['Trade ID', 'Commodity', 'Unrealized PnL']]
                            st.dataframe(unrealized_trades, height=250, use_container_width=True)
                    
                    # ===========================================
                    # 4. VaR ANALYSIS SECTION (Expandable)
                    # ===========================================
                    with st.expander("📉 Value at Risk (VaR) Analysis", expanded=True):
                        # VaR calculation
                        def calculate_var(confidence_level):
                            sorted_returns = np.sort(df['Daily Return'].dropna())
                            var_percentile = 100 - confidence_level
                            return -np.percentile(sorted_returns, var_percentile) * df['MTM'].sum()
                        
                        # Interactive control
                        var_confidence = st.slider(
                            "Select Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="var_conf"
                        )
                        
                        var_value = calculate_var(var_confidence)
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                f"Portfolio VaR ({var_confidence}%)",
                                f"${abs(var_value):,.2f}",
                                delta=f"{var_value/df['MTM'].sum()*100:.2f}% of portfolio"
                            )
                        
                        with col2:
                            st.write("**Calculation Method:**")
                            st.write("Historical VaR based on daily MTM returns")
                        
                        # Show worst performing trades
                        st.subheader("Worst Daily Performers")
                        worst_trades = df.nsmallest(5, 'Daily Return')[['Trade ID', 'Commodity', 'Daily Return']]
                        st.dataframe(worst_trades, use_container_width=True)
                    
                    # ===========================================
                    # 5. HISTORICAL VaR SECTION (Expandable)
                    # ===========================================
                    with st.expander("📊 Historical VaR Simulation", expanded=True):
                        # Historical VaR controls
                        hist_conf = st.slider(
                            "Select Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="hist_var_conf"
                        )
                        
                        # Ensure we have returns calculated
                        if 'Daily Return' not in df.columns:
                            df['Daily Return'] = df['MTM'].pct_change().fillna(0)
                        
                        sorted_returns = np.sort(df['Daily Return'].dropna())
                        
                        if len(sorted_returns) > 0:
                            var_percentile = 100 - hist_conf
                            hist_var = -np.percentile(sorted_returns, var_percentile) * df['MTM'].sum()
                            
                            # Display metrics
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric(
                                    f"Historical VaR ({hist_conf}%)",
                                    f"${abs(hist_var):,.2f}"
                                )
                            
                            with col2:
                                st.write("**Return Distribution:**")
                                st.write(f"Mean: {df['Daily Return'].mean():.4f}")
                                st.write(f"Std Dev: {df['Daily Return'].std():.4f}")
                            
                            # Plot return distribution
                            fig = px.histogram(
                                df,
                                x='Daily Return',
                                nbins=30,
                                title="Daily Return Distribution with VaR Threshold"
                            )
                            fig.add_vline(
                                x=-abs(hist_var)/df['MTM'].sum(),
                                line_dash="dash",
                                line_color="red",
                                annotation_text=f"VaR {hist_conf}%",
                                annotation_position="top left"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Insufficient data for Historical VaR calculation")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check your file and try again")

if __name__ == "__main__":
    main()
