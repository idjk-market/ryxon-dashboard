import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import base64
import logging
from io import StringIO

# ---- CONFIGURATION ----
st.set_page_config(
    page_title="Ryxon Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# ---- LOGGING ----
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---- STYLING ----
def set_app_style():
    bg_color = "#0E1117" if st.session_state.dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
    
    st.markdown(f"""
        <style>
        /* Main styling */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Cards */
        .card {{
            background-color: {"rgba(30, 30, 30, 0.9)" if st.session_state.dark_mode else "rgba(255, 255, 255, 0.93)"};
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px {"rgba(0, 0, 0, 0.3)" if st.session_state.dark_mode else "rgba(0, 0, 0, 0.1)"};
            margin-bottom: 1.5rem;
        }}
        
        /* Buttons */
        .stButton>button {{
            transition: all 0.3s ease;
            border: 1px solid {"#6a1b9a" if st.session_state.dark_mode else "#f63366"};
        }}
        .stButton>button:hover {{
            transform: scale(1.02);
            box-shadow: 0 2px 10px {"rgba(106, 27, 154, 0.5)" if st.session_state.dark_mode else "rgba(246, 51, 102, 0.5)"};
        }}
        
        /* Hide Streamlit defaults */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ---- AUTHENTICATION ----
def login_page():
    with st.container():
        st.title("🔒 Ryxon Authentication")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                if username == "admin" and password == "ryxon123":
                    st.session_state.auth = True
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ---- DASHBOARD ----
def dashboard_page():
    # Navigation sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=Ryxon", width=150)
        st.markdown("## Navigation")
        
        if st.button("📊 Dashboard"):
            st.session_state.current_page = "dashboard"
        
        if st.button("📂 Upload Trades"):
            st.session_state.current_page = "upload"
        
        if st.button("✍️ Manual Entry"):
            st.session_state.current_page = "manual"
        
        if st.button("📈 Analytics"):
            st.session_state.current_page = "analytics"
        
        if st.button("⚙️ Settings"):
            st.session_state.current_page = "settings"
        
        st.markdown("---")
        if st.button("🔒 Logout"):
            st.session_state.auth = False
            st.session_state.current_page = "login"
            st.rerun()
        
        # Dark mode toggle
        st.markdown("---")
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            set_app_style()
            st.rerun()

    # Main content
    with st.container():
        st.title("📊 Trading Dashboard")
        
        # Stats cards
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h3>Open Positions</h3>
                    <h1 style='color: #6a1b9a;'>142</h1>
                    <p>+12% from last week</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h3>Risk Exposure</h3>
                    <h1 style='color: #f63366;'>$4.2M</h1>
                    <p>Within limits</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h3>Today's P&L</h3>
                    <h1 style='color: #21c354;'>$124K</h1>
                    <p>+2.4% MTD</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent trades table
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Recent Trades</h3>
            """, unsafe_allow_html=True)
            
            # Sample data
            trades = pd.DataFrame({
                'Trade ID': ['FX-2023-0456', 'IRS-2023-0789', 'OPT-2023-0321'],
                'Instrument': ['EUR/USD', '10Y IRS', 'SPX Call'],
                'Notional': ['$5,000,000', '$10,000,000', '$2,500,000'],
                'Price': [1.0856, 2.34, 35.50],
                'Date': ['2023-05-15', '2023-05-14', '2023-05-13'],
                'Status': ['Active', 'Active', 'Expired']
            })
            
            st.dataframe(trades, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ---- FILE UPLOAD ----
def upload_page():
    with st.container():
        st.title("📂 Trade File Upload")
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Upload Trade Register</h3>
                <p>Supported formats: CSV, Excel (XLSX)</p>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Drag & drop or browse files",
                type=["csv", "xlsx"],
                accept_multiple_files=False,
                key="file_uploader"
            )
            
            if uploaded_file:
                try:
                    # Read file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Validate columns
                    required_cols = ['TradeID', 'Instrument', 'Notional', 'Price', 'TradeDate']
                    if not all(col in df.columns for col in required_cols):
                        missing = [col for col in required_cols if col not in df.columns]
                        st.error(f"Missing required columns: {', '.join(missing)}")
                    else:
                        st.session_state.uploaded_data = df
                        st.success(f"Successfully loaded {len(df)} trades")
                        
                        # Show preview
                        with st.expander("Preview Data"):
                            st.dataframe(df.head())
                        
                        # Process button
                        if st.button("Process Trades", type="primary"):
                            with st.spinner("Validating and processing trades..."):
                                time.sleep(2)
                                st.session_state.current_page = "processing"
                                st.rerun()
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    logging.error(f"File processing error: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ---- MANUAL ENTRY ----
def manual_page():
    with st.container():
        st.title("✍️ Manual Trade Entry")
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>New Trade Details</h3>
            """, unsafe_allow_html=True)
            
            with st.form("trade_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    trade_id = st.text_input("Trade ID", value=f"TRD-{datetime.now().strftime('%Y%m%d')}-")
                    instrument = st.selectbox("Instrument", ["FX Forward", "Interest Rate Swap", "Option", "Future"])
                    notional = st.number_input("Notional Amount", min_value=0.0, value=1000000.0)
                
                with col2:
                    trade_date = st.date_input("Trade Date", value=datetime.now())
                    direction = st.radio("Direction", ["Buy", "Sell"])
                    price = st.number_input("Price/Rate", min_value=0.0, value=1.0, step=0.0001)
                
                counterparty = st.text_input("Counterparty")
                comments = st.text_area("Comments")
                
                if st.form_submit_button("Submit Trade", type="primary"):
                    # Validate trade
                    if not trade_id or not counterparty:
                        st.error("Please fill all required fields")
                    else:
                        # Save trade (in session state for demo)
                        new_trade = {
                            'TradeID': trade_id,
                            'Instrument': instrument,
                            'Notional': notional,
                            'Direction': direction,
                            'Price': price,
                            'TradeDate': trade_date,
                            'Counterparty': counterparty,
                            'Comments': comments,
                            'Timestamp': datetime.now()
                        }
                        
                        if 'trades' not in st.session_state:
                            st.session_state.trades = []
                        
                        st.session_state.trades.append(new_trade)
                        st.success("Trade submitted successfully!")
                        time.sleep(1)
                        st.session_state.current_page = "dashboard"
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ---- ANALYTICS ----
def analytics_page():
    with st.container():
        st.title("📈 Risk Analytics")
        
        # Sample data
        risk_data = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=30),
            'VaR': [2.1 + 0.1*i for i in range(30)],
            'PnL': [100 + 10*i + (-1)**i * 15 for i in range(30)]
        })
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Value at Risk (VaR)</h3>
            """, unsafe_allow_html=True)
            
            fig = px.line(risk_data, x='Date', y='VaR', title="30-Day VaR Trend")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Profit & Loss</h3>
            """, unsafe_allow_html=True)
            
            fig = px.bar(risk_data, x='Date', y='PnL', title="Daily PnL")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ---- SETTINGS ----
def settings_page():
    with st.container():
        st.title("⚙️ System Settings")
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Configuration</h3>
            """, unsafe_allow_html=True)
            
            st.selectbox("Default Currency", ["USD", "EUR", "GBP", "JPY"])
            st.number_input("Risk Limit ($)", min_value=0, value=10000000)
            st.text_input("SMTP Server", value="smtp.ryxon.com")
            
            if st.button("Save Settings", type="primary"):
                st.success("Settings saved successfully")
            
            st.markdown("</div>", unsafe_allow_html=True)

# ---- PROCESSING ----
def processing_page():
    with st.container():
        st.title("🔄 Processing Trades")
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <h3>Trade Validation</h3>
            """, unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate processing steps
            steps = [
                "Loading file...",
                "Validating structure...",
                "Checking references...",
                "Calculating risk...",
                "Updating positions...",
                "Generating reports..."
            ]
            
            for i, step in enumerate(steps):
                progress = int((i + 1) * 100 / len(steps))
                progress_bar.progress(progress)
                status_text.text(f"{step} ({progress}%)")
                time.sleep(0.5)
            
            st.success("Processing complete!")
            time.sleep(1)
            st.session_state.current_page = "dashboard"
            st.rerun()

# ---- MAIN APP ----
def main():
    set_app_style()
    
    if not st.session_state.auth:
        login_page()
    else:
        if st.session_state.current_page == "dashboard":
            dashboard_page()
        elif st.session_state.current_page == "upload":
            upload_page()
        elif st.session_state.current_page == "manual":
            manual_page()
        elif st.session_state.current_page == "analytics":
            analytics_page()
        elif st.session_state.current_page == "settings":
            settings_page()
        elif st.session_state.current_page == "processing":
            processing_page()

if __name__ == "__main__":
    main()
