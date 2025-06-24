# streamlit_app_master.py
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

# Custom CSS for better UI
st.markdown("""
<style>
    .stFileUploader > div > div > div > button {
        background-color: #4B0082;
        color: white;
    }
    .stFileUploader > div > div > div > button:hover {
        background-color: #5a1a8c;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def load_data(uploaded_file):
    """Handle both CSV and Excel files with robust error checking"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            # Read Excel file into bytes first
            file_bytes = BytesIO(uploaded_file.getvalue())
            return pd.read_excel(file_bytes, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.error("Please ensure you're uploading a valid Excel (xlsx) or CSV file")
        return None

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")
    
    # File upload with clear instructions
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
                    # Basic data validation
                    required_cols = {'Book Price', 'Market Price', 'Quantity'}
                    if not required_cols.issubset(df.columns):
                        missing = required_cols - set(df.columns)
                        st.error(f"Missing required columns: {', '.join(missing)}")
                        return
                    
                    # Calculate metrics
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    
                    # Display success message
                    st.success(f"Successfully loaded {len(df)} trades!")
                    
                    # Show data preview
                    st.subheader("Trade Data Preview")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    # Main dashboard sections would go here
                    # ... rest of your dashboard code ...

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                st.error("Please check your file format and try again")

if __name__ == "__main__":
    main()
