# ---- MANUAL TRADE ENTRY ----
elif st.session_state.dashboard_mode == "manual":
    if st.button("🔙 Go Back"):
        st.session_state.dashboard_mode = None
        st.rerun()

    st.subheader("📝 Vertical Trade Entry Form")
    st.markdown("Complete all fields as per exchange requirements")
    
    with st.form("vertical_trade_form"):
        # Create 2-column layout for better organization
        col1, col2 = st.columns(2)
        
        with col1:
            # Core Trade Information
            st.markdown("### Trade Details")
            trade_date = st.date_input("Trade Date*")
            instrument_type = st.selectbox("Instrument Type*", 
                                        ["Futures", "Options", "Forwards", "Swaps"],
                                        key='inst_type')
            commodity = st.text_input("Commodity*")
            instrument_no = st.text_input("Instrument No.")
            exchange = st.text_input("Exchange*")
            index = st.text_input("Index")
            
        with col2:
            # Quantity and Pricing
            st.markdown("### Quantity & Pricing")
            lot_type = st.selectbox("Lot Type*", ["Standard", "Mini"])
            lot_size = st.number_input("Lot Size*", min_value=0.01, step=0.01)
            lots = st.number_input("Lots*", min_value=1, step=1)
            total_qty = lot_size * lots
            st.text_input("Total Quantity", value=f"{total_qty:,}", disabled=True)
            
            # Dynamic fields based on instrument type
            if instrument_type == "Options":
                option_type = st.selectbox("Option Type*", ["Call", "Put"])
                option_action = st.selectbox("Option Action*", ["Buy", "Sell"])
                strike_price = st.number_input("Strike Price*", min_value=0.01, step=0.01)
                premium = st.number_input("Premium*", min_value=0.0001, step=0.0001, format="%.4f")
            else:
                book_price = st.number_input("Book Price*", min_value=0.01, step=0.01)
                market_price = st.number_input("Market Price*", min_value=0.01, step=0.01)
        
        # Form submission
        submitted = st.form_submit_button("Submit Trade", type="primary")
        
        if submitted:
            # Validation
            required_fields = {
                "Trade Date": trade_date,
                "Commodity": commodity,
                "Exchange": exchange,
                "Lot Size": lot_size,
                "Lots": lots
            }
            
            missing_fields = [k for k, v in required_fields.items() if not v]
            if missing_fields:
                st.error(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                # Calculate MTM based on instrument type
                if instrument_type == "Options":
                    mtm = total_qty * premium * (-1 if option_action == "Buy" else 1)
                    trade_details = {
                        "Instrument Type": instrument_type,
                        "Commodity": commodity,
                        "Option Type": option_type,
                        "Option Action": option_action,
                        "Strike Price": strike_price,
                        "Premium": premium,
                        "Total Qty": total_qty,
                        "MTM": mtm
                    }
                else:
                    mtm = (market_price - book_price) * total_qty
                    trade_details = {
                        "Instrument Type": instrument_type,
                        "Commodity": commodity,
                        "Book Price": book_price,
                        "Market Price": market_price,
                        "Total Qty": total_qty,
                        "MTM": mtm
                    }
                
                # Add common fields
                trade_details.update({
                    "Trade Date": trade_date.strftime("%Y-%m-%d"),
                    "Exchange": exchange,
                    "Lot Type": lot_type,
                    "Lot Size": lot_size,
                    "Lots": lots
                })
                
                # Display results
                st.success("### Trade Submitted Successfully")
                st.balloons()
                
                # Show trade summary in expandable section
                with st.expander("View Trade Details", expanded=True):
                    # Create display dataframe
                    display_df = pd.DataFrame.from_dict(trade_details, orient='index', columns=['Value'])
                    st.dataframe(display_df.style.format({
                        "MTM": "${:,.2f}",
                        "Premium": "${:,.4f}",
                        "Strike Price": "${:,.2f}",
                        "Book Price": "${:,.2f}",
                        "Market Price": "${:,.2f}",
                        "Total Qty": "{:,.2f}",
                        "Lot Size": "{:,.2f}"
                    }))
