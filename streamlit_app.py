import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Ryxon MTM Dashboard", layout="wide")
st.title("📊 Ryxon – The Edge of Trading Risk Intelligence")

# Upload section
uploaded_file = st.file_uploader("📁 Upload Trade Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # File type handling
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("❌ Unsupported file type. Please upload a CSV or Excel file.")
        st.stop()

    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # Filter section
    st.subheader("🔍 Filter Your Data")

    filter_column = st.selectbox("Select field to filter", df.columns)
    filter_values = ["All"] + sorted(df[filter_column].dropna().astype(str).unique())
    selected_value = st.selectbox(f"Select value in '{filter_column}'", filter_values)

    if selected_value != "All":
        filtered_df = df[df[filter_column].astype(str) == selected_value].copy()
    else:
        filtered_df = df.copy()

    # MTM Calculation
    st.subheader("📉 MTM Calculation")

    def calculate_mtm(row):
        try:
            if row['Trade Action'].lower() == 'buy':
                return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
            else:
                return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)
        except:
            return 0

    filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

    st.dataframe(filtered_df[['Trade Action', 'Commodity', 'Instrument Type', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

    total_mtm = filtered_df['MTM'].sum()
    st.markdown(f"### 💰 Total MTM: ₹ {total_mtm:,.2f}")

else:
    st.info("👆 Please upload a CSV or Excel file to get started.")
