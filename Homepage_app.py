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
        instrument_options = ["All"] + sorted(df['Instrument Type'].unique()) if 'Instrument Type' in df.columns else ["All"]
        instrument_filter = st.selectbox("Instrument Type", instrument_options)
    
    with filter_cols[1]:
        direction_options = ["All"] + sorted(df['Trade Action'].unique()) if 'Trade Action' in df.columns else ["All"]
        direction_filter = st.selectbox("Direction", direction_options)
    
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
