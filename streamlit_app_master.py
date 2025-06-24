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
                    # Calculate metrics
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Trades", len(df))
                    col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
                    col3.metric("Unique Instruments", df['Instrument Type'].nunique())
                    
                    # Configure column types for proper filtering
                    column_config = {
                        "Trade ID": st.column_config.TextColumn(),
                        "Commodity": st.column_config.SelectboxColumn(
                            options=sorted(df['Commodity'].unique())
                        ),
                        "Instrument Type": st.column_config.SelectboxColumn(
                            options=sorted(df['Instrument Type'].unique())
                        ),
                        "Trade Action": st.column_config.SelectboxColumn(
                            options=sorted(df['Trade Action'].unique())
                        ),
                        "Quantity": st.column_config.NumberColumn(),
                        "Book Price": st.column_config.NumberColumn(format="%.2f"),
                        "Market Price": st.column_config.NumberColumn(format="%.2f"),
                        "MTM": st.column_config.NumberColumn(format="%.2f"),
                        "Trade Date": st.column_config.DatetimeColumn(),
                    }
                    
                    # Display the interactive data editor with filters
                    st.subheader("Trade Data (Click ⋮ to filter)")
                    st.data_editor(
                        df,
                        column_config=column_config,
                        use_container_width=True,
                        height=500,
                        hide_index=True,
                        disabled=True  # Makes the table read-only but keeps filtering
                    )

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
