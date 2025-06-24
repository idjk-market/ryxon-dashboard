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
                    
                    # Enable filtering for all columns
                    st.subheader("Trade Data - Click column headers to filter")
                    
                    # Convert to AgGrid for advanced filtering
                    from st_aggrid import AgGrid, GridOptionsBuilder
                    
                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_default_column(
                        filterable=True,
                        sortable=True,
                        resizable=True
                    )
                    
                    grid_options = gb.build()
                    
                    AgGrid(
                        df,
                        gridOptions=grid_options,
                        height=500,
                        width='100%',
                        theme='streamlit',
                        enable_enterprise_modules=False
                    )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Please ensure your file has the correct columns")

if __name__ == "__main__":
    main()
