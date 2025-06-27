import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Initialize all session state variables
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

# ---- STYLING ----
def set_app_style():
    bg_color = "#0E1117" if st.session_state.dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: all 0.3s ease;
    }}
    .sidebar .sidebar-content {{
        transition: margin 0.3s ease;
    }}
    .sidebar-collapsed {{
        margin-left: -300px;
    }}
    .file-uploader {{
        border: 2px dashed #6a1b9a;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- SIDEBAR COMPONENT ----
def show_sidebar():
    with st.sidebar:
        # Sidebar toggle button
        if st.button("◄" if st.session_state.sidebar_state == "expanded" else "►", 
                    key="sidebar_toggle"):
            st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
            st.rerun()
        
        if st.session_state.sidebar_state == "expanded":
            st.image("https://via.placeholder.com/150x50?text=Ryxon", width=150)
            st.markdown("## Navigation")
            
            nav_pages = {
                "📊 Dashboard": "dashboard",
                "📂 Upload Trades": "upload",
                "✍️ Manual Entry": "manual",
                "📈 Analytics": "analytics",
                "⚙️ Settings": "settings"
            }
            
            for label, page in nav_pages.items():
                if st.button(label, use_container_width=True, key=f"nav_{page}"):
                    st.session_state.current_page = page
                    st.rerun()
            
            st.markdown("---")
            if st.button("🔒 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.auth = False
                st.session_state.current_page = "login"
                st.rerun()
            
            # Dark mode toggle
            st.markdown("---")
            dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode, key="dark_mode_toggle")
            if dark_mode != st.session_state.dark_mode:
                st.session_state.dark_mode = dark_mode
                set_app_style()
                st.rerun()

# ---- PAGES ----
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

def dashboard_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        st.title("📊 Trading Dashboard")
        
        # Stats cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Open Positions", "142", "+12% from last week")
        with col2:
            st.metric("Risk Exposure", "$4.2M", "Within limits")
        with col3:
            st.metric("Today's P&L", "$124K", "+2.4% MTD")
        
        # Recent trades table
        st.markdown("### Recent Trades")
        trades = pd.DataFrame({
            'Trade ID': ['FX-2023-0456', 'IRS-2023-0789', 'OPT-2023-0321'],
            'Instrument': ['EUR/USD', '10Y IRS', 'SPX Call'],
            'Notional': ['$5,000,000', '$10,000,000', '$2,500,000'],
            'Price': [1.0856, 2.34, 35.50],
            'Date': ['2023-05-15', '2023-05-14', '2023-05-13'],
            'Status': ['Active', 'Active', 'Expired']
        })
        st.dataframe(trades, use_container_width=True)

def upload_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.title("📂 Trade File Upload")
        
        # File uploader with browse option
        with st.container():
            st.markdown('<div class="file-uploader">', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Drag and drop or click to browse files",
                type=["csv", "xlsx", "xls"],
                accept_multiple_files=False,
                key="file_uploader",
                help="Supported formats: CSV, Excel (XLSX/XLS)"
            )
            
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.session_state.uploaded_data = df
                    st.success(f"Successfully loaded {len(df)} trades")
                    
                    with st.expander("Preview data"):
                        st.dataframe(df.head())
                    
                    if st.button("Process Trades", type="primary"):
                        st.session_state.current_page = "processing"
                        st.rerun()
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def manual_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.title("✍️ Manual Trade Entry")
        
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
            
            if st.form_submit_button("Submit Trade"):
                if not trade_id or not counterparty:
                    st.error("Please fill all required fields")
                else:
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

def analytics_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.title("📈 Risk Analytics")
        
        if st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            
            # VaR Calculation
            st.subheader("Value at Risk")
            confidence = st.slider("Confidence Level", 90, 99, 95)
            var = df['Price'].quantile(1 - confidence/100)
            st.metric(f"{confidence}% VaR", f"${var:,.2f}")
            
            # Visualization
            fig = px.histogram(df, x="Price", nbins=30, title="Price Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please upload trade data first")

def settings_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.title("⚙️ Settings")
        
        with st.form("settings_form"):
            currency = st.selectbox("Default Currency", ["USD", "EUR", "GBP", "JPY"])
            risk_limit = st.number_input("Risk Limit ($)", min_value=0, value=10000000)
            smtp_server = st.text_input("SMTP Server", value="smtp.ryxon.com")
            
            if st.form_submit_button("Save Settings"):
                st.success("Settings saved successfully")

def processing_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        st.title("🔄 Processing Trades")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i+1}%")
            time.sleep(0.03)
        
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
