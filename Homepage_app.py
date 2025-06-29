# trade_input.py
import streamlit as st
import pandas as pd

def render_upload_trades():
    st.header("Upload Trades")
    
    uploaded_file = st.file_uploader(
        "Choose a trade file (CSV/Excel)",
        type=["csv", "xlsx"]
    )
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.success("File uploaded successfully!")
            st.dataframe(df)
            
            # Show basic analytics
            st.subheader("Upload Analytics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Trades", len(df))
                st.metric("Total Notional", f"${df['Notional'].sum():,.2f}")
            with col2:
                st.metric("Unique Instruments", df['Instrument'].nunique())
                st.metric("Earliest Trade Date", df['Date'].min())
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
