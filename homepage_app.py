import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- HEADER SECTION ----
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/idjk-market/ryxon-dashboard/main/ryxon_logo.png" width="80">
        <h1 style="color: #4B0082; font-weight: 900;">Ready to Take Control of Risk?</h1>
    </div>
""", unsafe_allow_html=True)

# ---- MAIN APP SELECTION ----
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    # Landing page content
    st.success("Try Ryxon Dashboard Now – Upload your trade file and see risk insights in seconds!")
    
    # Working launch button
    if st.button("🚀 Launch Dashboard", type="primary", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    
    # ---- FEATURE HIGHLIGHTS ----
    st.markdown("## 🔍 Features You'll Love")
    st.markdown("""
    <ul style="font-size: 1.1rem; line-height: 1.6;">
        <li>📊 <strong>Real-time MTM & PnL Tracking</strong> – Upload trades and instantly view live MTM values</li>
        <li>🛡️ <strong>Value at Risk (VaR)</strong> – Parametric & Historical VaR with confidence control</li>
        <li>📈 <strong>Scenario Testing</strong> – Stress-test positions for custom shocks</li>
        <li>📉 <strong>Unrealized vs Realized PnL</strong> – Clearly broken down with hedge grouping</li>
        <li>🧠 <strong>Dynamic Filtering</strong> – Commodity, Instrument, Strategy – Fully interactive</li>
    </ul>
    """, unsafe_allow_html=True)

    # ---- PRODUCT COVERAGE ----
    st.markdown("## 🏦 Asset Class Coverage")
    cols = st.columns(4)
    products = [
        ("Equity", "📈", "Stocks, ETFs, and equity derivatives"),
        ("Commodities", "⛏️", "Energy, metals, and agricultural products"),
        ("Cryptos", "🔗", "Spot and derivatives across major cryptocurrencies"),
        ("Bonds & Forex", "💱", "Fixed income and currency products")
    ]
    
    for i, (name, icon, desc) in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; border-radius: 0.5rem; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); height: 100%;">
                <h4 style="color: #4B0082;">{icon} {name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---- INSTRUMENT COVERAGE ----
    st.markdown("## 🛠️ Instrument Types")
    st.markdown("""
    <div style="background: white; border-radius: 0.5rem; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">
            <div style="padding: 0.5rem;">
                <p>• Futures</p>
                <p>• Options</p>
                <p>• Forwards</p>
            </div>
            <div style="padding: 0.5rem;">
                <p>• Swaps</p>
                <p>• FX Spots</p>
                <p>• Interest Rate Derivatives</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- BLOG TEASER ----
    st.markdown("---")
    st.markdown("## 📚 Latest from the Ryxon Blog")
    st.info("Coming Soon: 'Top 5 Ways Risk Desks Lose Money & How Ryxon Prevents It'")

else:
    # ---- DASHBOARD CONTENT ----
    import streamlit as st
    import pandas as pd
    import numpy as np
    
    st.title("📊 Ryxon Risk Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your trade file (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Process file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Basic calculations
        df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(df))
        col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
        col3.metric("Unique Instruments", df['Instrument Type'].nunique())
        
        # Show data with filters
        st.subheader("Trade Data")
        st.dataframe(df)
        
        # Simple visualization
        st.subheader("Exposure by Commodity")
        fig = px.bar(df.groupby('Commodity')['MTM'].sum().reset_index(), 
                     x='Commodity', y='MTM', color='Commodity')
        st.plotly_chart(fig, use_container_width=True)
        
        # Add back button
        if st.button("← Back to Home"):
            st.session_state.show_dashboard = False
            st.rerun()

# ---- FOOTER ----
st.markdown("""
<div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 40px;">
    🚀 Built with ❤️ by Ryxon Technologies – Market Risk Intelligence
</div>
""", unsafe_allow_html=True)
