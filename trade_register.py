import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Upload Trades", layout="wide")

# Header
st.title("📂 Trade File Upload")

# Card UI style
st.markdown("""
    <style>
        .card {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
    <div class='card'>
        <h3>Upload Trade Register</h3>
        <p>Supported formats: CSV, Excel (XLSX)</p>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a trade file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read file based on extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Required columns
        required_cols = ['TradeID', 'Instrument', 'Notional', 'Price', 'TradeDate']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"Missing required columns: {', '.join(missing_cols)}")
        else:
            st.success(f"✅ Successfully loaded {len(df)} trades")
            st.session_state['uploaded_trades'] = df

            # Display preview
            with st.expander("📋 Preview Trade Data"):
                st.dataframe(df, use_container_width=True)

            # Basic analytics
            st.markdown("""
                <div class='card'>
                <h4>Summary Analytics</h4>
            """, unsafe_allow_html=True)
            st.write("**Total Trades:**", len(df))
            st.write("**Total Notional:**", f"${df['Notional'].sum():,.2f}")
            st.write("**Instruments Used:**", df['Instrument'].nunique())
            st.markdown("</div>", unsafe_allow_html=True)

            # Optional: Save button
            if st.button("📥 Save to Register"):
                st.success("Data saved for further processing")

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

# Back button
if st.button("⬅ Go Back"):
    st.session_state.current_page = "dashboard"
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
