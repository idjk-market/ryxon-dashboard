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
            st.session_state.df = None  # Clear data when going back
            st.rerun()
    
    # Initialize dataframe in session state if not exists
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Main dashboard content
    st.title("📊 Trading Dashboard")
    
    # Tab navigation
    tab1, tab2 = st.tabs(["📤 Upload Trade File", "✍️ Create Manual Trade"])
    
    with tab1:
        uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"], key="file_uploader")
        
        if uploaded_file:
            try:
                with st.spinner("Processing trades..."):
                    # Read file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Validate required columns
                    required_cols = ['Market Price', 'Book Price', 'Quantity']
                    if not all(col in df.columns for col in required_cols):
                        st.error(f"Missing required columns: {', '.join(required_cols)}")
                    else:
                        # Calculate MTM
                        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                        st.session_state.df = df
                        st.success("File processed successfully!")
                        
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
    
    with tab2:
        with st.form("manual_trade_form", clear_on_submit=True):
            st.subheader("Create New Trade Entry")
            
            col1, col2 = st.columns(2)
            with col1:
                trade_id = st.text_input("Trade ID*", value=f"TRD-{datetime.now().strftime('%Y%m%d')}-")
                instrument = st.selectbox("Instrument Type*", ["Equity", "Commodity", "FX", "Fixed Income", "Derivative"])
                quantity = st.number_input("Quantity*", min_value=1, value=100)
                
            with col2:
                trade_date = st.date_input("Trade Date*", datetime.now())
                price = st.number_input("Price*", min_value=0.0, value=100.0, step=0.01)
                direction = st.radio("Direction*", ["Buy", "Sell"])
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Submit Trade"):
                if not trade_id:
                    st.error("Please enter a Trade ID")
                else:
                    # Create new trade record
                    new_trade = pd.DataFrame([{
                        'Trade ID': trade_id,
                        'Trade Date': trade_date,
                        'Instrument Type': instrument,
                        'Quantity': quantity,
                        'Book Price': price,
                        'Market Price': price,  # Same as book price initially
                        'Trade Action': direction,
                        'Notes': notes,
                        'MTM': 0  # Will be calculated later
                    }])
                    
                    # Add to existing data or create new dataframe
                    if st.session_state.df is None:
                        st.session_state.df = new_trade
                    else:
                        st.session_state.df = pd.concat([st.session_state.df, new_trade], ignore_index=True)
                    
                    st.success("Trade successfully added!")
    
    # Display trade data if exists
    if st.session_state.df is not None:
        display_trade_data(st.session_state.df)
    else:
        st.info("Please upload a trade file or create a manual trade to begin")

def display_trade_data(df):
    """Helper function to display trade data metrics and visualizations"""
    # Calculate MTM if not already present
    if 'MTM' not in df.columns:
        if 'Market Price' in df.columns and 'Book Price' in df.columns and 'Quantity' in df.columns:
            df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        else:
            df['MTM'] = 0  # Default to 0 if we can't calculate
    
    # Display metrics
    st.markdown("---")
    st.subheader("Trade Analysis")
    
    cols = st.columns(4)
    cols[0].metric("Total Positions", len(df))
    cols[1].metric("Total Quantity", f"{df['Quantity'].sum():,}")
    
    if 'Book Price' in df.columns:
        cols[2].metric("Avg Price", f"${df['Book Price'].mean():.2f}")
    if 'MTM' in df.columns:
        cols[3].metric("Total MTM", f"${df['MTM'].sum():,.2f}")
    
    # Filters
    st.subheader("🔍 Filters")
    filter_cols = st.columns(3)
    
    with filter_cols[0]:
        instrument_filter = st.selectbox(
            "Instrument Type",
            ["All"] + sorted(df['Instrument Type'].unique()) if 'Instrument Type' in df.columns else st.selectbox("Instrument Type", ["All"])
    
    with filter_cols[1]:
        direction_filter = st.selectbox(
            "Direction",
            ["All"] + sorted(df['Trade Action'].unique())) if 'Trade Action' in df.columns else st.selectbox("Direction", ["All"])
    
    # Apply filters
    filtered_df = df.copy()
    if instrument_filter != "All":
        filtered_df = filtered_df[filtered_df['Instrument Type'] == instrument_filter]
    if direction_filter != "All":
        filtered_df = filtered_df[filtered_df['Trade Action'] == direction_filter]
    
    # Show filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Visualizations
    st.subheader("📊 Visualizations")
    viz_tabs = st.tabs(["MTM Distribution", "Exposure Breakdown"])
    
    with viz_tabs[0]:
        if 'MTM' in filtered_df.columns:
            fig = px.histogram(filtered_df, x="MTM", nbins=20, title="MTM Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("MTM data not available for visualization")
    
    with viz_tabs[1]:
        if 'Instrument Type' in filtered_df.columns:
            exposure = filtered_df.groupby('Instrument Type')['Quantity'].sum().reset_index()
            fig = px.pie(exposure, values='Quantity', names='Instrument Type', title="Exposure by Instrument Type")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Instrument Type data not available for exposure analysis")
