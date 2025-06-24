# ---- ADD THIS AFTER YOUR EXISTING IMPORTS ----
from scipy.stats import norm
import numpy as np

# ---- ADD THIS IN THE DASHBOARD SECTION (AFTER UPLOADED_FILE CHECK) ----
if uploaded_file:
    try:
        # [Keep all your existing code until after the stress testing section...]
        
        # =============================================
        # NEW ADVANCED RISK ANALYTICS TAB
        # =============================================
        tab1, tab2 = st.tabs(["Main Dashboard", "Advanced Risk Analytics"])
        
        with tab1:
            # [All your existing dashboard content remains exactly the same]
            pass
            
        with tab2:
            st.header("🚨 Advanced Risk Analytics")
            
            # 1. PORTFOLIO VaR (Variance-Covariance)
            st.subheader("📉 Portfolio VaR (Variance-Covariance)")
            var_conf = st.slider("Confidence Level", 90, 99, 95, key='var_conf') / 100
            
            if len(filtered_df) > 1:
                # Calculate correlations and volatilities
                corr_matrix = filtered_df.pivot_table(index='Trade Date', columns='Commodity', values='MTM', aggfunc='sum').corr()
                volatilities = filtered_df.groupby('Commodity')['MTM'].std()
                portfolio_var = np.sqrt(
                    filtered_df.groupby('Commodity')['MTM'].sum().T @ 
                    (corr_matrix * volatilities * volatilities.reshape(-1,1)) @ 
                    filtered_df.groupby('Commodity')['MTM'].sum()
                ) * norm.ppf(var_conf)
                
                col1, col2 = st.columns(2)
                col1.metric(f"Portfolio VaR ({int(var_conf*100)}%)", f"${abs(portfolio_var):,.2f}")
                
                # Correlation heatmap
                fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto")
                col2.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("Need at least 2 positions for portfolio VaR")
            
            # 2. MONTE CARLO SIMULATION
            st.subheader("🎲 Monte Carlo Simulation")
            mc_col1, mc_col2 = st.columns(2)
            n_simulations = mc_col1.number_input("Number of Simulations", 100, 10000, 1000)
            days = mc_col2.number_input("Time Horizon (Days)", 1, 30, 1)
            
            if st.button("Run Simulation"):
                with st.spinner("Running Monte Carlo..."):
                    # Generate random returns based on historical volatility
                    returns = np.random.normal(
                        loc=filtered_df['MTM'].mean(),
                        scale=filtered_df['MTM'].std(),
                        size=(n_simulations, days)
                    )
                    
                    # Calculate portfolio paths
                    portfolio_paths = np.cumsum(returns, axis=1)
                    
                    # Plot results
                    fig_mc = px.line(
                        pd.DataFrame(portfolio_paths.T),
                        title=f"Monte Carlo Simulation ({n_simulations} paths)"
                    )
                    fig_mc.update_layout(showlegend=False)
                    st.plotly_chart(fig_mc, use_container_width=True)
                    
                    # Show VaR from simulation
                    final_values = portfolio_paths[:,-1]
                    mc_var = np.percentile(final_values, 100*(1-var_conf))
                    st.metric(f"Simulated {int(var_conf*100)}% VaR ({days}D)", 
                             f"${abs(mc_var):,.2f}")
            
            # 3. ROLLING VOLATILITY
            st.subheader("📈 Rolling Volatility Analysis")
            window = st.slider("Rolling Window (Days)", 5, 60, 21)
            
            if 'Trade Date' in filtered_df.columns:
                # Calculate daily MTM
                daily_mtm = filtered_df.groupby('Trade Date')['MTM'].sum().sort_index()
                
                # Calculate rolling volatility
                rolling_vol = daily_mtm.rolling(window=window).std()
                
                # Plot
                fig_vol = px.line(
                    rolling_vol, 
                    title=f"{window}-Day Rolling Volatility",
                    labels={"value": "Volatility", "Trade Date": "Date"}
                )
                st.plotly_chart(fig_vol, use_container_width=True)
            else:
                st.warning("Need Trade Date column for volatility analysis")
                
        # [Keep all your existing code after this...]
        
    except Exception as e:
        st.error(f"Error in advanced analytics: {str(e)}")
