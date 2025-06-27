# trade_register.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Register", layout="wide")

st.title("📘 Trade Register")

if 'trade_book' in st.session_state:
    st.dataframe(pd.DataFrame(st.session_state.trade_book), use_container_width=True)
else:
    st.warning("No trades submitted yet.")
