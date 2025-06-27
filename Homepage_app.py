import streamlit as st
import pandas as pd
import time
from io import StringIO

# Configuration - Set first to avoid Streamlit warnings
st.set_page_config(
    page_title="Ryxon Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state with defaults
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# ---- CUSTOM STYLING ----
def set_app_style():
    st.markdown(f"""
        <style>
        /* Main background */
        .stApp {{
            background: url('https://images.unsplash.com/photo-1611078489935-b0379236fbd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1650&q=80');
            background-size: cover;
            background-attachment: fixed;
        }}
        
        /* Card styling */
        .card {{
            background-color: rgba(255, 255, 255, 0.93) !important;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        
        /* Button styling */
        .stButton>button {{
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            transform: scale(1.02);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        /* File uploader area */
        .stFileUploader>div>div {{
            border: 2px dashed #6a1b9a;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.8);
        }}
        
        /* Remove Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

set_app_style()

# ---- PAGE FUNCTIONS ----
def show_homepage():
    with st.container():
        st.markdown("<h1 style='color: #6a1b9a; font-weight: bold;'>📊 Welcome to Ryxon – The Edge of Trading Risk Intelligence</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div class='card'>
                <p style='font-size: 1.15rem;'>
                    An integrated risk platform to manage <strong>derivatives, commodities, and exposure</strong> – built with intelligence, precision, and speed.
                </p>
                <h3 style='margin-top: 2rem;'>🚀 Choose Mode to Get Started</h3>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📂 Upload Trade File", key="upload_btn", use_container_width=True, type="primary"):
                    st.session_state.current_page = "upload"
                    st.rerun()
            
            with col2:
                if st.button("📝 Create Manual Trade", key="manual_btn", use_container_width=True, type="secondary"):
                    st.session_state.current_page = "manual"
                    st.rerun()
            
            st.markdown("""
                <ul style='line-height: 1.8; font-size: 1.05rem;'>
                    <li>Upload existing trade files via <strong>Trade Register</strong></li>
                    <li>Create new trades manually via <strong>Trade Entry</strong></li>
                    <li>Analyze MTM, VaR and more in <strong>Risk Analytics</strong></li>
                    <li>Manage square-offs in <strong>Lifecycle Manager</strong></li>
                    <li>Configure defaults in <strong>Instrument Master</strong></li>
                    <li>Export results from <strong>Reports</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_upload_page():
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back to Home", key="upload_back"):
                st.session_state.current_page = "home"
                st.session_state.uploaded_file = None
                st.rerun()
        
        with col2:
            st.title("📂 Trade File Upload")
            
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h4>Upload Your Trade Data</h4>
                    <p>Supported formats: CSV, Excel (.xlsx, .xls)</p>
                """, unsafe_allow_html=True)
                
                # Enhanced file uploader with progress
                uploaded_file = st.file_uploader(
                    "Drag & drop or browse files",
                    type=["csv", "xlsx", "xls"],
                    accept_multiple_files=False,
                    key="file_uploader",
                    help="Upload your trade register or position file"
                )
                
                if uploaded_file:
                    with st.spinner("Processing file..."):
                        try:
                            # Store file in session state
                            st.session_state.uploaded_file = uploaded_file
                            
                            # Preview the file
                            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or uploaded_file.type == "application/vnd.ms-excel":
                                df = pd.read_excel(uploaded_file)
                            else:
                                df = pd.read_csv(uploaded_file)
                            
                            st.success("✅ File uploaded successfully!")
                            st.markdown(f"**File name:** `{uploaded_file.name}`")
                            st.markdown(f"**Size:** `{uploaded_file.size/1024:.2f} KB`")
                            st.markdown(f"**Rows:** `{len(df)}`")
                            
                            with st.expander("Preview first 10 rows"):
                                st.dataframe(df.head(10))
                            
                            # Action buttons after upload
                            st.markdown("---")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("Process File", type="primary"):
                                    # Add your processing logic here
                                    with st.spinner("Analyzing trades..."):
                                        time.sleep(2)  # Simulate processing
                                        st.session_state.current_page = "processing"
                                        st.rerun()
                            
                            with col2:
                                if st.button("Clear File", type="secondary"):
                                    st.session_state.uploaded_file = None
                                    st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
                            st.session_state.uploaded_file = None
                
                st.markdown("</div>", unsafe_allow_html=True)

def show_manual_page():
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Back to Home", key="manual_back"):
                st.session_state.current_page = "home"
                st.rerun()
        
        with col2:
            st.title("📝 Manual Trade Entry")
            
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h4>Create New Trade</h4>
                    <p>Enter trade details manually below</p>
                """, unsafe_allow_html=True)
                
                # Trade entry form
                with st.form("manual_trade_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        trade_date = st.date_input("Trade Date")
                        instrument = st.selectbox("Instrument", ["FX Forward", "IRS", "Option", "Future"])
                        notional = st.number_input("Notional Amount", min_value=0.0)
                    
                    with col2:
                        value_date = st.date_input("Value Date")
                        buy_sell = st.radio("Buy/Sell", ["Buy", "Sell"])
                        price = st.number_input("Price/Rate")
                    
                    comments = st.text_area("Comments")
                    
                    if st.form_submit_button("Submit Trade", type="primary"):
                        with st.spinner("Saving trade..."):
                            time.sleep(1)  # Simulate save operation
                            st.success("Trade saved successfully!")
                            time.sleep(1)
                            st.session_state.current_page = "home"
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

# ---- MAIN APP ROUTING ----
if st.session_state.current_page == "home":
    show_homepage()
elif st.session_state.current_page == "upload":
    show_upload_page()
elif st.session_state.current_page == "manual":
    show_manual_page()
elif st.session_state.current_page == "processing":
    with st.container():
        st.title("🔍 Processing Trades")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Processing... {i+1}%")
            time.sleep(0.02)
        
        st.success("Analysis complete!")
        time.sleep(1)
        st.session_state.current_page = "home"
        st.rerun()
