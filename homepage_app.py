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
    # Landing page content
    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
    
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # ... [Rest of your homepage content remains the same] ...

else:
    # ---- DASHBOARD CONTENT ----
    st.title("📊 Ryxon Risk Dashboard")
    
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Process file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Calculate MTM
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(df))
        col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
        col3.metric("Unique Instruments", df['Instrument Type'].nunique())

        # ===========================================
        # INTERACTIVE FILTERABLE TRADE TABLE (NEW)
        # ===========================================
        st.subheader("Trade Data (Filter any column)")
        
        # Configure AgGrid for advanced filtering
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(
            filterable=True,
            sortable=True,
            resizable=True,
            floatingFilter=True
        )
        
        # Special configuration for key columns
        for col in ["Commodity", "Instrument Type", "Trade Action"]:
            gb.configure_column(col, 
                              filter="agSetColumnFilter",
                              floatingFilter=True)
        
        for col in ["Quantity", "Book Price", "Market Price", "MTM"]:
            gb.configure_column(col, 
                              filter="agNumberColumnFilter",
                              floatingFilter=True)
        
        gridOptions = gb.build()
        
        # Display the interactive table
        AgGrid(
            df,
            gridOptions=gridOptions,
            update_mode=GridUpdateMode.FILTERING_CHANGED,
            height=400,
            width='100%',
            theme='streamlit',
            allow_unsafe_jscode=True
        )

        # ===========================================
        # EXPOSURE BY COMMODITY SECTION
        # ===========================================
        st.subheader("Exposure by Commodity")
        
        # Calculate exposure (will respect table filters)
        filtered_df = df  # AgGrid filters are applied automatically
        exposure_df = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
        
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(exposure_df, x='Commodity', y='MTM', 
                            title="MTM Exposure by Commodity")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(exposure_df, names='Commodity', values='MTM',
                            title="Exposure Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

        # Add back button
        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()

# ---- FOOTER ----
st.markdown("""
<div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
    🚀 Built with ❤️ by Ryxon Technologies
</div>
""", unsafe_allow_html=True)
