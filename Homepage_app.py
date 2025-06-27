# ---- DASHBOARD PAGE ----
def show_dashboard():
    # Sidebar navigation
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png", width=120)
        st.markdown("## Navigation")
        
        # Dark mode toggle
        dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            set_app_style()
            st.rerun()
        
        st.markdown("---")
        if st.button("🏠 Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()
    
    # Main dashboard content
    st.title("📊 Trading Dashboard")
    
    # Add tab navigation for upload vs manual entry
    tab1, tab2 = st.tabs(["📤 Upload Trade File", "✍️ Create Manual Trade"])
    
    with tab1:
        # File uploader
        uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"], key="file_uploader")
        
        if uploaded_file:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Process data
                required_cols = ['Market Price', 'Book Price', 'Quantity']
                if not all(col in df.columns for col in required_cols):
                    st.error("Missing required columns: Market Price, Book Price, Quantity")
                    st.stop()
                
                df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                st.session_state.df = df
                display_trade_data(df)
                    
            except Exception as e:
                st.error(f"Error processing file: {e}")
    
    with tab2:
        # Manual Trade Entry Form
        with st.form("manual_trade_form"):
            st.subheader("Create New Trade")
            
            col1, col2 = st.columns(2)
            with col1:
                trade_date = st.date_input("Trade Date", datetime.now())
                instrument = st.selectbox("Instrument Type", ["Equity", "Commodity", "FX", "Fixed Income", "Derivative"])
                quantity = st.number_input("Quantity", min_value=1, value=100)
                
            with col2:
                trade_id = st.text_input("Trade ID", value=f"TRD-{datetime.now().strftime('%Y%m%d')}-001")
                price = st.number_input("Price", min_value=0.0, value=100.0, step=0.01)
                direction = st.radio("Direction", ["Buy", "Sell"])
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Submit Trade"):
                # Create trade dictionary
                new_trade = {
                    'Trade ID': trade_id,
                    'Trade Date': trade_date,
                    'Instrument Type': instrument,
                    'Quantity': quantity,
                    'Book Price': price,
                    'Market Price': price,  # Assuming same as book price initially
                    'Trade Action': direction,
                    'Notes': notes,
                    'MTM': 0  # Will be calculated
                }
                
                # Add to existing data or create new dataframe
                if 'df' not in st.session_state:
                    st.session_state.df = pd.DataFrame(columns=list(new_trade.keys()))
                
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_trade])], ignore_index=True)
                st.success("Trade successfully added!")
                st.rerun()
    
    # Display trade data if exists
    if 'df' in st.session_state and st.session_state.df is not None:
        display_trade_data(st.session_state.df)

def display_trade_data(df):
    """Helper function to display trade data metrics and visualizations"""
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
    col2.metric("Positions", len(df))
    col3.metric("Avg Price", f"${df['Book Price'].mean():.2f}")
    col4.metric("Total Quantity", f"{df['Quantity'].sum():,.0f}")
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        instrument = st.selectbox("Instrument", ["All"] + sorted(df['Instrument Type'].dropna().unique()), key="inst_filter")
    with col2:
        commodity = st.selectbox("Commodity", ["All"] + sorted(df['Commodity'].dropna().unique())) if 'Commodity' in df.columns else st.selectbox("Commodity", ["All"])
    with col3:
        direction = st.selectbox("Direction", ["All"] + sorted(df['Trade Action'].dropna().unique()), key="dir_filter")
    
    # Apply filters
    filtered_df = df.copy()
    if instrument != "All":
        filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument]
    if 'Commodity' in df.columns and commodity != "All":
        filtered_df = filtered_df[filtered_df['Commodity'] == commodity]
    if direction != "All":
        filtered_df = filtered_df[filtered_df['Trade Action'] == direction]
    
    # Show filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Charts
    st.subheader("📊 Visualizations")
    tab1, tab2, tab3 = st.tabs(["MTM Distribution", "Exposure by Commodity", "PnL Trend"])
    
    with tab1:
        fig = px.histogram(filtered_df, x="MTM", nbins=30, title="MTM Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if 'Commodity' in filtered_df.columns:
            exposure = filtered_df.groupby('Commodity')['MTM'].sum().reset_index()
            fig = px.bar(exposure, x='Commodity', y='MTM', title="Exposure by Commodity")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if 'Trade Date' in filtered_df.columns:
            filtered_df['Trade Date'] = pd.to_datetime(filtered_df['Trade Date'])
            daily = filtered_df.groupby('Trade Date')['MTM'].sum().reset_index()
            fig = px.line(daily, x='Trade Date', y='MTM', title="Daily PnL Trend")
            st.plotly_chart(fig, use_container_width=True)
