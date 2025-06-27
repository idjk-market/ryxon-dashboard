import streamlit as st
from streamlit_option_menu import option_menu

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ryxon Financial Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- BACKGROUND STYLE ----
def set_homepage_style():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
                    url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .product-card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .section-title {{
        color: white;
        font-size: 1.5rem;
        margin-top: 2rem;
        border-bottom: 2px solid white;
        padding-bottom: 0.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# ---- SESSION STATE ----
if 'current_product' not in st.session_state:
    st.session_state.current_product = None

# ---- PRODUCT DATA ----
PRODUCTS = {
    "Commodity": ["Energy", "Metals", "Agriculture"],
    "Equity": ["Stocks", "ETFs", "Indices"],
    "Real Estate": ["REITs", "Property Derivatives"],
    "Cryptocurrencies": ["Spot", "Futures"],
    "Banking & Credit": ["Loans", "Bonds", "Swaps"]
}

INSTRUMENTS = ["Futures", "Options", "Forwards", "Swaps"]

# ---- HOMEPAGE ----
def show_homepage():
    set_homepage_style()
    
    # Main title
    st.markdown("<h1 style='color: white; text-align: center;'>Ryxon Financial Platform</h1>", 
                unsafe_allow_html=True)
    
    # Products section
    st.markdown('<div class="section-title">Products</div>', unsafe_allow_html=True)
    
    cols = st.columns(len(PRODUCTS))
    for i, (product, subproducts) in enumerate(PRODUCTS.items()):
        with cols[i]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h3>{product}</h3>
                    <ul style="margin-left: 1rem;">
                        {''.join(f'<li>{sp}</li>' for sp in subproducts)}
                    </ul>
                    <button onclick="window.streamlit.setComponentValue('{product.lower()}')" 
                            style="background: #4B0082; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                        Access {product}
                    </button>
                </div>
                """, unsafe_allow_html=True)
    
    # Instruments section
    st.markdown('<div class="section-title">Instruments</div>', unsafe_allow_html=True)
    
    instrument_cols = st.columns(4)
    for i, instrument in enumerate(INSTRUMENTS):
        with instrument_cols[i % 4]:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; text-align: center;">
                <h4>{instrument}</h4>
            </div>
            """, unsafe_allow_html=True)

# Handle product selection
if st.query_params.get("product"):
    st.session_state.current_product = st.query_params.get("product")
    if st.session_state.current_product == "commodity":
        st.switch_page("pages/commodity.py")

# ---- MAIN APP ----
if __name__ == "__main__":
    show_homepage()
