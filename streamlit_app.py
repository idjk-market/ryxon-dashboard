import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ryxon MTM Dashboard", layout="wide")

st.title("📊 Ryxon – MTM Risk Intelligence")

uploaded_file = st.file_uploader("📁 Upload trade data CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    st.subheader("🔍 Filter Your Data")

    # Step 1: Let user select column to filter
    filter_column = st.selectbox("Select field to filter", df.columns)

    # Step 2: Show dropdown of unique values in that column
    unique_vals = ["All"] + sorted(df[filter_column].dropna().unique())
    selected_val = st.selectbox(f"Select value in '{filter_column}'", unique_vals)

    # Step 3: Apply filter
    if selected_val != "All":
        filtered_df = df[df[filter_column] == selected_val].copy()
    else:
        filtered_df = df.copy()

    # Step 4: MTM Calculation
    def calculate_mtm(row):
        if row['Trade Action'].lower() == 'buy':
            return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
        else:
            return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)

    filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

    st.subheader("📉 MTM Calculation")
    st.dataframe(filtered_df[['Trade Action', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

    st.markdown(f"### 💰 Total MTM: ₹ {filtered_df['MTM'].sum():,.2f}")
