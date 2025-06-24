
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
        st.error(f"Error reading file: {str(e)}")
        return None

def calculate_var(df, confidence_level=0.95):
    if len(df) > 1:
        return -np.percentile(df['MTM'].dropna(), (1 - confidence_level) * 100)
    return 0

def home_page():
    st.title("🏠 Welcome to Ryxon Risk Dashboard")
    st.markdown("""
        This dashboard helps you analyze your trade data with:
        - 📈 MTM Calculation
        - 💰 Realized & Unrealized PnL
        - 📉 Value at Risk (VaR)
        - 📊 Historical VaR
        - 🔎 Dynamic Analysis by Commodity or Instrument
    """)

def dashboard():
    st.title("📊 Risk Analysis Dashboard")

    uploaded_file = st.file_uploader("📁 Upload Trade Data File", type=["xlsx", "csv"])
    if uploaded_file:
        df = load_data(uploaded_file)

        if df is not None:
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trades", len(df))
            col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col3.metric("Unique Instruments", df['Instrument Type'].nunique())

            st.subheader("📋 Trade Data Table")
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_grid_options(suppressMenu=False)
            gb.configure_default_column(filter=True, sortable=True, resizable=True, floatingFilter=True)
            for col in ["Commodity", "Instrument Type", "Trade Action"]:
                gb.configure_column(col, filter="agSetColumnFilter", floatingFilter=True)
            gb.configure_column("Quantity", filter="agNumberColumnFilter", floatingFilter=True)
            gb.configure_column("MTM", filter="agNumberColumnFilter", floatingFilter=True)
            gridOptions = gb.build()

            AgGrid(
                df,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.NO_UPDATE,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True,
                fit_columns_on_grid_load=True,
                use_container_width=True,
                height=450
            )

            # 🔎 Analysis Filters
            st.markdown("### 🔎 Analysis View Filters")
            colf1, colf2 = st.columns(2)
            commodity_filter = colf1.selectbox("Filter by Commodity", ['All'] + sorted(df['Commodity'].unique()))
            instrument_filter = colf2.selectbox("Filter by Instrument Type", ['All'] + sorted(df['Instrument Type'].unique()))

            filtered_df = df.copy()
            if commodity_filter != 'All':
                filtered_df = filtered_df[filtered_df['Commodity'] == commodity_filter]
            if instrument_filter != 'All':
                filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument_filter]

            st.success(f"📌 Filtered {len(filtered_df)} records")

            with st.expander("📈 MTM Summary", expanded=False):
                st.write("**Total MTM:**", round(filtered_df['MTM'].sum(), 2))
                st.write("**Average MTM:**", round(filtered_df['MTM'].mean(), 2))
                st.dataframe(filtered_df.nlargest(5, 'MTM')[['Trade ID', 'Commodity', 'MTM']])

            with st.expander("💰 Realized & Unrealized PnL", expanded=False):
                if 'Realized PnL' in filtered_df.columns and 'Unrealized PnL' in filtered_df.columns:
                    st.metric("Total Realized PnL", f"{filtered_df['Realized PnL'].sum():,.2f}")
                    st.metric("Total Unrealized PnL", f"{filtered_df['Unrealized PnL'].sum():,.2f}")
                    st.bar_chart(filtered_df[['Realized PnL', 'Unrealized PnL']])
                else:
                    st.warning("PnL columns not found in uploaded data.")

            with st.expander("📉 Value at Risk (VaR)", expanded=False):
                var_95 = calculate_var(filtered_df, 0.95)
                var_99 = calculate_var(filtered_df, 0.99)
                st.metric("VaR (95%)", f"${var_95:,.2f}")
                st.metric("VaR (99%)", f"${var_99:,.2f}")
                st.line_chart(filtered_df['MTM'])

            with st.expander("📊 Historical VaR", expanded=False):
                hist_var = filtered_df['MTM'].quantile([0.01, 0.05, 0.10])
                st.write(hist_var.to_frame("Historical VaR"))
                st.area_chart(filtered_df['MTM'])

def run_app():
    menu = ["Home", "Dashboard"]
    choice = st.sidebar.radio("📂 Navigate", menu)

    if choice == "Home":
        home_page()
    elif choice == "Dashboard":
        dashboard()

if __name__ == "__main__":
    run_app()

