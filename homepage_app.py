import streamlit as st
import pandas as pd
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
            <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
            <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
        </div>
    """, unsafe_allow_html=True)

    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
    
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # [Rest of your landing page content...]
    
# ---- DASHBOARD PAGE ----
else:
    st.title("📊 Ryxon Risk Dashboard")
    
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Basic validation
            required_cols = ['Market Price', 'Book Price', 'Quantity']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"Missing required columns: {', '.join(missing_cols)}")
                st.stop()
            
            # Calculations
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
            
            # Display data
            st.subheader("Trade Data Preview")
            st.dataframe(df.head())
            
            # Basic metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Trades", len(df))
            col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
            col3.metric("Avg MTM per Trade", f"${df['MTM'].mean():,.2f}")
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.rerun()
