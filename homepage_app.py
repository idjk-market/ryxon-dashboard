import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- HEADER SECTION ----
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
""", unsafe_allow_html=True)

# ---- MAIN APP SELECTION ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")

    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()

    st.markdown("## 🔍 Features You'll Love")
    st.markdown("""
    <ul style="font-size: 1.1rem; line-height: 1.6;">
        <li>📊 <strong>Real-time MTM & PnL Tracking</strong> – Upload trades and instantly view live MTM values</li>
        <li>🛡️ <strong>Value at Risk (VaR)</strong> – Parametric & Historical VaR with confidence control</li>
        <li>📈 <strong>Scenario Testing</strong> – Stress-test positions for custom shocks</li>
        <li>📉 <strong>Unrealized vs Realized PnL</strong> – Clearly broken down with hedge grouping</li>
        <li>🧠 <strong>Dynamic Filtering</strong> – Commodity, Instrument, Strategy – Fully interactive</li>
        <li>📊 <strong>Exposure Analysis</strong> – Visualize by commodity/instrument</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("## 🏦 Asset Class Coverage")
    cols = st.columns(4)
    products = [
        ("Equity", "📈", "Stocks, ETFs, and equity derivatives"),
        ("Commodities", "⛏️", "Energy, metals, and agricultural products"),
        ("Cryptos", "🔗", "Spot and derivatives across major cryptocurrencies"),
        ("Bonds & Forex", "💱", "Fixed income and currency products")
    ]
    
    for i, (name, icon, desc) in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #4B0082;">{icon} {name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
        🚀 Built with ❤️ by Ryxon Technologies – Market Risk Intelligence
    </div>
    """, unsafe_allow_html=True)

else:
    st.title("📊 Ryxon Risk Dashboard")
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(df))
        col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
        col3.metric("Unique Instruments", df['Instrument Type'].nunique())

        st.subheader("Trade Data")
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(suppressMenu=False)
        gb.configure_default_column(filter=True, sortable=True, resizable=True, floatingFilter=True)
        for col in ["Commodity", "Instrument Type", "Trade Action"]:
            gb.configure_column(col, filter="agSetColumnFilter", floatingFilter=True)
        gb.configure_column("Quantity", filter="agNumberColumnFilter", floatingFilter=True)
        gb.configure_column("MTM", filter="agNumberColumnFilter", floatingFilter=True)
        gridOptions = gb.build()

        AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.NO_UPDATE,
               allow_unsafe_jscode=True, enable_enterprise_modules=True,
               fit_columns_on_grid_load=True, use_container_width=True, height=500)

        st.subheader("Exposure by Commodity")
        exposure_df = df.groupby('Commodity')['MTM'].sum().reset_index()
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(exposure_df, x='Commodity', y='MTM', color='Commodity',
                            title="MTM Exposure by Commodity")
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            fig_pie = px.pie(exposure_df, names='Commodity', values='MTM',
                            title="Percentage of Total Exposure")
            st.plotly_chart(fig_pie, use_container_width=True)
        st.write("**Detailed Exposure Metrics**")
        exposure_metrics = exposure_df.copy()
        exposure_metrics['% of Total'] = (exposure_metrics['MTM'] / exposure_metrics['MTM'].abs().sum()) * 100
        st.dataframe(
            exposure_metrics.style.format({
                'MTM': '${:,.2f}',
                '% of Total': '{:.1f}%'
            }),
            use_container_width=True
        )

        with st.expander("📈 MTM Summary", expanded=False):
            st.write("**Total MTM:**", round(df['MTM'].sum(), 2))
            st.write("**Average MTM:**", round(df['MTM'].mean(), 2))
            st.write("**Top MTM Trades:**")
            st.dataframe(df.nlargest(5, 'MTM')[['Trade ID', 'Commodity', 'MTM']])

        with st.expander("💰 Realized & Unrealized PnL", expanded=False):
            if 'Realized PnL' in df.columns and 'Unrealized PnL' in df.columns:
                st.write("**Total Realized PnL:**", round(df['Realized PnL'].sum(), 2))
                st.write("**Total Unrealized PnL:**", round(df['Unrealized PnL'].sum(), 2))
                st.bar_chart(df[['Realized PnL', 'Unrealized PnL']])
            else:
                st.warning("Columns 'Realized PnL' and 'Unrealized PnL' not found in uploaded data.")

        with st.expander("📉 Value at Risk (VaR)", expanded=False):
            def calculate_var(dataframe, confidence_level=0.95):
                pnl_series = dataframe['MTM']
                if len(pnl_series) > 1:
                    return -np.percentile(pnl_series.dropna(), (1 - confidence_level) * 100)
                return 0
            var_95 = calculate_var(df, 0.95)
            var_99 = calculate_var(df, 0.99)
            st.metric("VaR (95%)", f"${var_95:,.2f}")
            st.metric("VaR (99%)", f"${var_99:,.2f}")
            st.line_chart(df['MTM'])

        with st.expander("📊 Historical VaR", expanded=False):
            hist_var = df['MTM'].quantile([0.01, 0.05, 0.10])
            st.write(hist_var.to_frame("Historical VaR Levels"))
            st.area_chart(df['MTM'])

        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
