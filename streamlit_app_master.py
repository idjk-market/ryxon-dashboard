import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="Ryxon Risk Dashboard", layout="wide")

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(BytesIO(uploaded_file.getvalue()), engine='openpyxl')
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")

    uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])

    if uploaded_file:
        df = load_data(uploaded_file)

        if df is not None:
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trades", len(df))
            col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col3.metric("Unique Instruments", df['Instrument Type'].nunique())

            st.subheader("🔍 Trade Data (Filter any column below 👇)")

            gb = GridOptionsBuilder.from_dataframe(df)

            gb.configure_grid_options(suppressMenu=False)  # ← VERY IMPORTANT

            gb.configure_default_column(
                filter=True,
                sortable=True,
                resizable=True,
                floatingFilter=True
            )

            # Set dropdown filters with floating bar
            for col in ["Commodity", "Instrument Type", "Trade Action"]:
                gb.configure_column(col, filter="agSetColumnFilter", floatingFilter=True)

            gb.configure_column("Quantity", filter="agNumberColumnFilter", floatingFilter=True)

            gridOptions = gb.build()

            AgGrid(
                df,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.NO_UPDATE,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True,  # <-- CRITICAL
                fit_columns_on_grid_load=True,
                use_container_width=True,
                height=500
            )

if __name__ == "__main__":
    main()
