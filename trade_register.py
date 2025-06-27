import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trade Register", layout="wide")
st.title("📘 Trade Register")

if 'trade_book' not in st.session_state or not st.session_state.trade_book:
    st.warning("No trades submitted yet.")
else:
    trades_df = pd.DataFrame(st.session_state.trade_book)

    with st.expander("🔍 Filter Trades"):
        columns = trades_df.columns.tolist()
        filters = {}
        cols = st.columns(len(columns))
        for i, col in enumerate(columns):
            filters[col] = cols[i].selectbox(f"{col} Filter", options=["All"] + sorted(trades_df[col].dropna().unique().astype(str).tolist()))

        for key, value in filters.items():
            if value != "All":
                trades_df = trades_df[trades_df[key].astype(str) == value]

    st.dataframe(trades_df, use_container_width=True)
    st.download_button("📥 Download as Excel", data=trades_df.to_csv(index=False), file_name="ryxon_trade_register.csv", mime="text/csv")
