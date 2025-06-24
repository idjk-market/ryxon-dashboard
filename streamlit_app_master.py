import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Configure page - THIS MUST COME FIRST
st.set_page_config(
    page_title="Ryxon Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            file_bytes = BytesIO(uploaded_file.getvalue())
            return pd.read_excel(file_bytes, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")
    
    uploaded_file = st.file_uploader(
        "Upload Trade Data (Excel or CSV)",
        type=["xlsx", "csv"],
        key="file_uploader"  # Important for reruns
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                # Clear any previous data
                if 'df' in st.session_state:
                    del st.session_state.df
                
                df = load_data(uploaded_file)
                
                if df is not None:
                    # Store in session state to persist across reruns
                    st.session_state.df = df
                    
                    # Calculate core metrics
                    st.session_state.df['MTM'] = (st.session_state.df['Market Price'] - st.session_state.df['Book Price']) * st.session_state.df['Quantity']
                    st.session_state.df['Realized PnL'] = np.where(
                        st.session_state.df['Trade Action'].str.lower() == 'sell',
                        st.session_state.df['MTM'],
                        0
                    )
                    st.session_state.df['Unrealized PnL'] = np.where(
                        st.session_state.df['Trade Action'].str.lower() == 'buy',
                        st.session_state.df['MTM'],
                        0
                    )
                    
                    # ======================
                    # 1. TRADE DATA TABLE
                    # ======================
                    st.subheader("Trade Data Overview")
                    st.dataframe(
                        st.session_state.df.style.format({
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
                    
                    # ======================
                    # 2. MTM CALCULATION
                    # ======================
                    with st.expander("🧮 MTM Calculation Details", expanded=True):
                        st.markdown("""
                        **Formula:**  
                        `MTM = (Market Price - Book Price) × Quantity`
                        """)
                        
                        # Show calculation example
                        mtm_example = st.session_state.df[['Trade ID', 'Commodity', 'Book Price', 'Market Price', 'Quantity', 'MTM']].head()
                        st.dataframe(mtm_example, use_container_width=True)
                        
                        # MTM Distribution chart
                        st.subheader("MTM Distribution")
                        fig = px.histogram(st.session_state.df, x='MTM', nbins=20, 
                                         title="Distribution of MTM Values")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # ======================
                    # 3. PnL ANALYSIS
                    # ======================
                    with st.expander("💰 PnL Breakdown (Realized vs Unrealized)", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        # Realized PnL
                        with col1:
                            st.metric("Total Realized PnL", 
                                    f"${st.session_state.df['Realized PnL'].sum():,.2f}")
                            st.dataframe(
                                st.session_state.df[st.session_state.df['Realized PnL'] != 0]
                                [['Trade ID', 'Commodity', 'Realized PnL']],
                                height=300,
                                use_container_width=True
                            )
                        
                        # Unrealized PnL
                        with col2:
                            st.metric("Total Unrealized PnL", 
                                    f"${st.session_state.df['Unrealized PnL'].sum():,.2f}")
                            st.dataframe(
                                st.session_state.df[st.session_state.df['Unrealized PnL'] != 0]
                                [['Trade ID', 'Commodity', 'Unrealized PnL']],
                                height=300,
                                use_container_width=True
                            )
                    
                    # ======================
                    # 4. VaR ANALYSIS
                    # ======================
                    with st.expander("📉 Value at Risk (VaR) Analysis", expanded=True):
                        # VaR calculation function
                        def calculate_var(confidence_level=95):
                            st.session_state.df['Daily Return'] = st.session_state.df['MTM'].pct_change().fillna(0)
                            sorted_returns = np.sort(st.session_state.df['Daily Return'].dropna())
                            var_percentile = 100 - confidence_level
                            return -np.percentile(sorted_returns, var_percentile) * st.session_state.df['MTM'].sum()
                        
                        var_confidence = st.slider(
                            "Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="var_conf"
                        )
                        
                        var_value = calculate_var(var_confidence)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                f"Portfolio VaR ({var_confidence}%)",
                                f"${abs(var_value):,.2f}",
                                help="Potential maximum loss at given confidence level"
                            )
                        
                        with col2:
                            st.write("**Calculation Method:**")
                            st.write("Historical VaR based on daily MTM returns")
                        
                        # Show worst returns
                        st.subheader("Worst Daily Returns")
                        worst_returns = st.session_state.df.nsmallest(5, 'Daily Return')
                        st.dataframe(worst_returns[['Trade ID', 'Commodity', 'Daily Return']], 
                                    use_container_width=True)
                    
                    # ======================
                    # 5. HISTORICAL VaR
                    # ======================
                    with st.expander("📊 Historical VaR Simulation", expanded=True):
                        hist_conf = st.slider(
                            "Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="hist_conf"
                        )
                        
                        # Ensure we have daily returns calculated
                        if 'Daily Return' not in st.session_state.df.columns:
                            st.session_state.df['Daily Return'] = st.session_state.df['MTM'].pct_change().fillna(0)
                        
                        sorted_returns = np.sort(st.session_state.df['Daily Return'].dropna())
                        
                        if len(sorted_returns) > 0:
                            var_percentile = 100 - hist_conf
                            hist_var = -np.percentile(sorted_returns, var_percentile) * st.session_state.df['MTM'].sum()
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric(
                                    f"Historical VaR ({hist_conf}%)",
                                    f"${abs(hist_var):,.2f}"
                                )
                            
                            with col2:
                                st.write("**Return Percentiles:**")
                                st.write(f"5th percentile: {np.percentile(sorted_returns, 5):.4f}")
                                st.write(f"1st percentile: {np.percentile(sorted_returns, 1):.4f}")
                            
                            # Plot distribution
                            fig = px.histogram(
                                st.session_state.df,
                                x='Daily Return',
                                nbins=30,
                                title="Distribution of Daily Returns"
                            )
                            fig.add_vline(
                                x=-abs(hist_var)/st.session_state.df['MTM'].sum(),
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
                st.error("Please check your file format and try again")

if __name__ == "__main__":
    main()
