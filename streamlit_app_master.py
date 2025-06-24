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
        type=["xlsx", "csv"],
        help="Maximum file size: 200MB. Supported formats: .xlsx, .csv"
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                df = load_data(uploaded_file)
                
                if df is not None:
                    # Calculate metrics
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Trades", len(df))
                    col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
                    col3.metric("Unique Instruments", df['Instrument Type'].nunique())
                    
                    # --------------------------------------------------
                    # NEW FILTERING CONTROLS (VISIBLE ABOVE THE TABLE)
                    # --------------------------------------------------
                    st.subheader("Filter Trade Data")
                    
                    # Create 4 filter columns
                    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
                    
                    # Initialize filtered dataframe
                    filtered_df = df.copy()
                    
                    # Filter 1: Commodity
                    with filter_col1:
                        commodities = ['All'] + sorted(df['Commodity'].unique().tolist())
                        selected_commodity = st.selectbox(
                            "Filter by Commodity",
                            options=commodities,
                            index=0
                        )
                        if selected_commodity != 'All':
                            filtered_df = filtered_df[filtered_df['Commodity'] == selected_commodity]
                    
                    # Filter 2: Instrument Type
                    with filter_col2:
                        instruments = ['All'] + sorted(df['Instrument Type'].unique().tolist())
                        selected_instrument = st.selectbox(
                            "Filter by Instrument",
                            options=instruments,
                            index=0
                        )
                        if selected_instrument != 'All':
                            filtered_df = filtered_df[filtered_df['Instrument Type'] == selected_instrument]
                    
                    # Filter 3: Trade Action
                    with filter_col3:
                        actions = ['All'] + sorted(df['Trade Action'].unique().tolist())
                        selected_action = st.selectbox(
                            "Filter by Trade Action",
                            options=actions,
                            index=0
                        )
                        if selected_action != 'All':
                            filtered_df = filtered_df[filtered_df['Trade Action'] == selected_action]
                    
                    # Filter 4: Quantity Range
                    with filter_col4:
                        min_qty, max_qty = int(df['Quantity'].min()), int(df['Quantity'].max())
                        selected_qty = st.slider(
                            "Filter by Quantity",
                            min_value=min_qty,
                            max_value=max_qty,
                            value=(min_qty, max_qty)
                        )
                        filtered_df = filtered_df[
                            (filtered_df['Quantity'] >= selected_qty[0]) & 
                            (filtered_df['Quantity'] <= selected_qty[1])
                        ]
                    
                    # Display filtered results count
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
                            'Daily Return': '{:.4f}',
                            'Rolling Std Dev': '{:.4f}',
                            '1-Day VAR': '{:.2f}'
                        }),
                        use_container_width=True,
                        height=500
                    )

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
