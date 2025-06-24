st.warning("✅ Running latest version with MTM, PnL, VaR sections")

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
        st.error(f"Error reading file: {e}")
        return None

def calculate_var(df, confidence_level=0.95):
    pnl_series = df['MTM']
    if len(pnl_series) > 1:
        return -np.percentile(pnl_series.dropna(), (1 - confidence_level) * 100)
    return 0

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")

    uploaded_file = st.file_uploader("📁 Upload Excel or CSV File", type=["xlsx", "csv"])

    if uploaded_file:
        df = load_data(uploaded_file)

        if df is not None:
            # MTM Calculation
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

            # KPIs
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trades", len(df))
            col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col3.metric("Unique Instruments", df['Instrument Type'].nunique())

            # Interactive Trade Table
            st.subheader("📋 Trade Data Table with Excel-like Filters")
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
                height=500
            )

            # 🔽 Expandable: MTM Summary
            with st.expander("📈 MTM Summary", expanded=False):
                st.write("**Total MTM:**", round(df['MTM'].sum(), 2))
                st.write("**Average MTM:**", round(df['MTM'].mean(), 2))
                st.write("**Top MTM Trades:**")
                st.dataframe(df.nlargest(5, 'MTM')[['Trade ID', 'Commodity', 'MTM']])

            # 🔽 Expandable: PnL Analysis
            with st.expander("💰 Realized & Unrealized PnL", expanded=False):
                if 'Realized PnL' in df.columns and 'Unrealized PnL' in df.columns:
                    st.write("**Total Realized PnL:**", round(df['Realized PnL'].sum(), 2))
                    st.write("**Total Unrealized PnL:**", round(df['Unrealized PnL'].sum(), 2))
                    st.bar_chart(df[['Realized PnL', 'Unrealized PnL']])
                else:
                    st.warning("Columns 'Realized PnL' and 'Unrealized PnL' not found in uploaded data.")

            # 🔽 Expandable: Value at Risk
            with st.expander("📉 Value at Risk (VaR)", expanded=False):
                var_95 = calculate_var(df, 0.95)
                var_99 = calculate_var(df, 0.99)
                st.metric("VaR (95%)", f"${var_95:,.2f}")
                st.metric("VaR (99%)", f"${var_99:,.2f}")
                st.line_chart(df['MTM'])

            # 🔽 Expandable: Historical VaR
            with st.expander("📊 Historical VaR", expanded=False):
                hist_var = df['MTM'].quantile([0.01, 0.05, 0.10])
                st.write(hist_var.to_frame("Historical VaR Levels"))
                st.area_chart(df['MTM'])

if __name__ == "__main__":
    main()
