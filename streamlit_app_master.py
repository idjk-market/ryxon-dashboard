import streamlit as st
import pandas as pd
import numpy as np
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
                    # Calculate MTM
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Trades", len(df))
                    col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
                    col3.metric("Unique Instruments", df['Instrument Type'].nunique())
                    
                    # --------------------------------------------------
                    # SIMPLE VISIBLE FILTER CONTROLS
                    # --------------------------------------------------
                    st.subheader("Filter Options")
                    
                    # Create 3 columns for filters
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        commodities = ['All'] + sorted(df['Commodity'].unique().tolist())
                        commodity_filter = st.selectbox("Filter by Commodity", commodities)
                    
                    with col2:
                        actions = ['All'] + sorted(df['Trade Action'].unique().tolist())
                        action_filter = st.selectbox("Filter by Trade Action", actions)
                    
                    with col3:
                        min_qty, max_qty = int(df['Quantity'].min()), int(df['Quantity'].max())
                        qty_filter = st.slider("Filter by Quantity", min_qty, max_qty, (min_qty, max_qty))
                    
                    # Apply filters
                    filtered_df = df.copy()
                    if commodity_filter != 'All':
                        filtered_df = filtered_df[filtered_df['Commodity'] == commodity_filter]
                    if action_filter != 'All':
                        filtered_df = filtered_df[filtered_df['Trade Action'] == action_filter]
                    filtered_df = filtered_df[
                        (filtered_df['Quantity'] >= qty_filter[0]) & 
                        (filtered_df['Quantity'] <= qty_filter[1])
                    ]
                    
                    # Show filtered count
                    st.info(f"Showing {len(filtered_df)} of {len(df)} trades")
                    
                    # --------------------------------------------------
                    # DISPLAY THE FILTERED TABLE
                    # --------------------------------------------------
                    st.subheader("Trade Data")
                    st.dataframe(
                        filtered_df.style.format({
                            'Book Price': '{:.2f}',
                            'Market Price': '{:.2f}',
                            'MTM': '{:.2f}',
                            'Realized PnL': '{:.2f}',
                            'Unrealized PnL': '{:.2f}',
                            'Daily Return': '{:.4f}'
                        }),
                        height=500,
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
