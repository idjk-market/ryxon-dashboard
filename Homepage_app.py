def upload_page():
    set_app_style()
    show_sidebar()
    
    with st.container():
        # Back button
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        st.title("📂 Trade File Upload")
        
        # File uploader section
        with st.container():
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px;'>
                <h3>Upload Trade File</h3>
            """, unsafe_allow_html=True)
            
            # File uploader with browse option
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=["csv", "xlsx", "xls"],
                accept_multiple_files=False,
                key="file_uploader",
                help="Supported formats: CSV, Excel"
            )
            
            if uploaded_file:
                try:
                    # Read file
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Store in session state
                    st.session_state.uploaded_data = df
                    st.success(f"File uploaded successfully! ({len(df)} records)")
                    
                    # Show preview
                    with st.expander("Preview data"):
                        st.dataframe(df.head())
                    
                    # Process button
                    if st.button("Process Trades", type="primary"):
                        with st.spinner("Processing trades..."):
                            time.sleep(2)  # Simulate processing
                            st.session_state.current_page = "processing"
                            st.rerun()
                
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
