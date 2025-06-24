import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Configure page
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

def calculate_var(df, confidence_level=95):
    df['Daily Return'] = df['MTM'].pct_change().fillna(0)
    sorted_returns = np.sort(df['Daily Return'].dropna())
    var_percentile = 100 - confidence_level
    return -np.percentile(sorted_returns, var_percentile) * df['MTM'].sum()

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")
    
    uploaded_file = st.file_uploader(
        "Upload Trade Data (Excel or CSV)",
        type=["xlsx", "csv"]
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                df = load_data(uploaded_file)
                
                if df is not None:
                    # Calculate core metrics
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    df['Realized PnL'] = np.where(
                        df['Trade Action'].str.lower() == 'sell',
                        df['MTM'],
                        0
                    )
                    df['Unrealized PnL'] = np.where(
                        df['Trade Action'].str.lower() == 'buy',
                        df['MTM'],
                        0
                    )
                    
                    # ======================
                    # 1. TRADE DATA TABLE
                    # ======================
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
                    
                    # ======================
                    # 2. MTM CALCULATION (Expandable)
                    # ======================
                    with st.expander("🧮 MTM Calculation Details", expanded=False):
                        st.markdown("""
                        **Formula:**  
                        `MTM = (Market Price - Book Price) × Quantity`
                        """)
                        
                        mtm_example = df[['Trade ID', 'Commodity', 'Book Price', 'Market Price', 'Quantity', 'MTM']].head()
                        st.dataframe(mtm_example, use_container_width=True)
                        
                        st.subheader("MTM Distribution")
                        fig = px.histogram(df, x='MTM', nbins=20, title="MTM Value Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # ======================
                    # 3. PnL ANALYSIS (Expandable)
                    # ======================
                    with st.expander("💰 PnL Breakdown (Realized vs Unrealized)", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Realized PnL", f"${df['Realized PnL'].sum():,.2f}")
                            st.dataframe(
                                df[df['Realized PnL'] != 0][['Trade ID', 'Commodity', 'Realized PnL']],
                                height=300,
                                use_container_width=True
                            )
                        
                        with col2:
                            st.metric("Total Unrealized PnL", f"${df['Unrealized PnL'].sum():,.2f}")
                            st.dataframe(
                                df[df['Unrealized PnL'] != 0][['Trade ID', 'Commodity', 'Unrealized PnL']],
                                height=300,
                                use_container_width=True
                            )
                    
                    # ======================
                    # 4. VaR ANALYSIS (Expandable)
                    # ======================
                    with st.expander("📉 Value at Risk (VaR) Analysis", expanded=False):
                        var_confidence = st.slider(
                            "Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="var_conf"
                        )
                        
                        var_value = calculate_var(df, var_confidence)
                        st.metric(
                            f"Portfolio VaR ({var_confidence}%)",
                            f"${abs(var_value):,.2f}",
                            delta=f"{var_value/df['MTM'].sum()*100:.2f}% of portfolio"
                        )
                        
                        st.markdown("""
                        **Calculation Method:**  
                        Historical VaR based on daily MTM returns
                        """)
                    
                    # ======================
                    # 5. HISTORICAL VaR (Expandable)
                    # ======================
                    with st.expander("📊 Historical VaR Simulation", expanded=False):
                        hist_conf = st.slider(
                            "Confidence Level", 
                            min_value=90, 
                            max_value=99, 
                            value=95,
                            key="hist_conf"
                        )
                        
                        df['Daily Return'] = df['MTM'].pct_change().fillna(0)
                        sorted_returns = np.sort(df['Daily Return'].dropna())
                        percentile_index = int((100 - hist_conf)/100 * len(sorted_returns))
                        
                        if len(sorted_returns) > 0:
                            hist_var = -sorted_returns[percentile_index] * df['MTM'].sum()
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric(
                                    f"Historical VaR ({hist_conf}%)",
                                    f"${abs(hist_var):,.2f}"
                                )
                            
                            with col2:
                                st.write("**Worst Daily Returns:**")
                                st.write(f"5th percentile: {np.percentile(sorted_returns, 5):.4f}")
                                st.write(f"1st percentile: {np.percentile(sorted_returns, 1):.4f}")
                            
                            fig = px.histogram(
                                df,
                                x='Daily Return',
                                nbins=30,
                                title="Distribution of Daily Returns"
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

if __name__ == "__main__":
    main()
