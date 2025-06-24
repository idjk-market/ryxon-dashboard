import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Set up the Streamlit page
st.set_page_config(
    page_title="Ryxon Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load CSV or Excel
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

# Main app
def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")

    uploaded_file = st.file_uploader(
        "Upload Trade Data (Excel or CSV)",
        type=["xlsx", "csv"],
        help="Max file size: 200MB"
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                df = load_data(uploaded_file)

                if df is not None:
                    # Calculate MTM
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

                    # Display top metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Trades", len(df))
                    col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
                    col3.metric("Unique Instruments", df['Instrument Type'].nunique())

                    st.subheader("Trade Data (Interactive Grid with Filters)")

                    # AgGrid configuration with dropdown filters
                    gb = GridOptionsBuilder.from_dataframe(df)
                    gb.configure_default_column(
                        filter=True,
                        sortable=True,
                        resizable=True,
                        floatingFilter=True
                    )

                    # Explicit filter types for dropdowns
                    gb.configure_column("Commodity", filter="agSetColumnFilter")
                    gb.configure_column("Instrument Type", filter="agSetColumnFilter")
                    gb.configure_column("Trade Action", filter="agSetColumnFilter")
                    gb.configure_column("Quantity", filter="agNumberColumnFilter")

                    # Final grid options
                    gridOptions = gb.build()

                    # Display interactive table
                    AgGrid(
                        df,
                        gridOptions=gridOptions,
                        update_mode=GridUpdateMode.NO_UPDATE,
                        allow_unsafe_jscode=True,
                        enable_enterprise_modules=True,  # ✅ Enables dropdown filters
                        fit_columns_on_grid_load=True,
                        use_container_width=True,
                        height=500
                    )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
