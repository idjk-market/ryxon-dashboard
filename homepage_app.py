import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- SESSION STATE ----
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'show_dashboard': False,
        'current_mode': None,
        'uploaded_data': None,
        'manual_trades': []
    }

# ---- LANDING PAGE ----
if not st.session_state.app_state['show_dashboard']:
    st.title("📊 Ryxon Risk Intelligence Platform")
    if st.button("🚀 Launch Dashboard", type="primary"):
        st.session_state.app_state['show_dashboard'] = True
        st.rerun()

# ---- DASHBOARD PAGE ----
else:
    # ======================
    # 1. MODE SELECTION SCREEN
    # ======================
    if st.session_state.app_state['current_mode'] is None:
        st.subheader("Select Input Method")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📂 File Upload")
            st.markdown("Upload existing trade data in Excel format")
            if st.button("Select Upload Mode", key="upload_btn"):
                st.session_state.app_state['current_mode'] = "upload"
                st.rerun()
        
        with col2:
            st.markdown("### 📝 Manual Entry")
            st.markdown("Enter trades manually for paper trading")
            if st.button("Select Manual Mode", key="manual_btn"):
                st.session_state.app_state['current_mode'] = "manual"
                st.rerun()

    # ======================
    # 2. UPLOAD MODE
    # ======================
    elif st.session_state.app_state['current_mode'] == "upload":
        st.subheader("📁 Trade File Upload")
        
        # Back button
        if st.button("← Back to Mode Selection"):
            st.session_state.app_state['current_mode'] = None
            st.rerun()
        
        # File uploader
        uploaded_file = st.file_uploader("Drag & drop Excel file here", type=["xlsx"])
        
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state.app_state['uploaded_data'] = df
                
                # Display data
                st.success("✅ File successfully loaded!")
                with st.expander("View Raw Data", expanded=True):
                    st.dataframe(df, use_container_width=True)
                
                # Risk metrics
                st.subheader("📊 Risk Analysis")
                if 'MTM' not in df.columns:
                    df['MTM'] = (df['MarketPrice'] - df['BookPrice']) * df['Quantity']
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Exposure", f"${df['MTM'].sum():,.2f}")
                col2.metric("Max Drawdown", f"${df['MTM'].min():,.2f}")
                col3.metric("Trade Count", len(df))
                
                # Visualization
                if 'Commodity' in df.columns:
                    fig = px.bar(df.groupby('Commodity')['MTM'].sum(), 
                                title="Exposure by Commodity")
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")

    # ======================
    # 3. MANUAL MODE
    # ======================
    elif st.session_state.app_state['current_mode'] == "manual":
        st.subheader("📝 Manual Trade Entry")
        
        # Back button
        if st.button("← Back to Mode Selection"):
            st.session_state.app_state['current_mode'] = None
            st.rerun()
        
        # Trade form
        with st.form("trade_entry_form"):
            cols = st.columns(3)
            trade_date = cols[0].date_input("Trade Date")
            instrument = cols[1].selectbox("Instrument", ["Future", "Option", "Swap"])
            direction = cols[2].selectbox("Direction", ["Buy", "Sell"])
            
            quantity = st.number_input("Quantity", min_value=0.01, step=0.01)
            price = st.number_input("Price", min_value=0.01, step=0.01)
            
            if st.form_submit_button("Add Trade"):
                new_trade = {
                    'date': trade_date,
                    'instrument': instrument,
                    'direction': direction,
                    'quantity': quantity,
                    'price': price,
                    'mtm': quantity * price * (-1 if direction == "Sell" else 1)
                }
                st.session_state.app_state['manual_trades'].append(new_trade)
                st.success("Trade added successfully!")
        
        # Display manual trades
        if st.session_state.app_state['manual_trades']:
            st.subheader("Your Portfolio")
            trades_df = pd.DataFrame(st.session_state.app_state['manual_trades'])
            st.dataframe(trades_df)
            
            total_mtm = trades_df['mtm'].sum()
            st.metric("Total Portfolio Value", f"${total_mtm:,.2f}")

# ---- FOOTER ---- 
st.markdown("---")
st.markdown("""
<style>
footer {visibility: hidden;}
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    font-size: 0.8rem;
    color: #777;
}
</style>
<div class="footer">Ryxon Technologies • Market Risk Intelligence</div>
""", unsafe_allow_html=True)
