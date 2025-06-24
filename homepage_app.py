import streamlit as st
import pandas as pd

# Initialize session state
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# ---- LANDING PAGE ----
if not st.session_state.show_dashboard:
    # Header with logo
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    st.write("Try Ryxon Dashboard Now - Upload your trade file and see risk insights in seconds!")
    
    # Working launch button
    if st.button("🚀 Launch Dashboard", type="primary"):
        st.session_state.show_dashboard = True
        st.experimental_rerun()

# ---- DASHBOARD PAGE ----
else:
    # Dashboard header
    st.title("📊 Ryxon Risk Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Show basic data preview
            st.subheader("Your Trade Data")
            st.write(f"Loaded {len(df)} trades")
            st.dataframe(df.head())
            
            # Simple analysis example
            if 'Price' in df.columns:
                st.subheader("Basic Analysis")
                st.write(f"Average price: ${df['Price'].mean():.2f}")
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.show_dashboard = False
        st.experimental_rerun()
