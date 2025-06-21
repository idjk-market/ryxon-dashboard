import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ryxon MTM Dashboard", layout="wide")

st.title("📊 Ryxon - MTM Risk Calculation")

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your trade data CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ Uploaded Trade Data")
    st.dataframe(df)

    st.subheader("🔍 Filter Your Data")

    # Step 2: Select field to filter
    filter_columns = ["Commodity", "Instrument Type", "Trade Action", "UOM"]
    selected_column = st.selectbox("Filter by Field", filter_columns)

    # Step 3: Select value from that field
    options = ["All"] + sorted(df[selected_column].dropna().unique())
    selected_value = st.selectbox(f"Select {selected_column}", options)

    # Step 4: Apply filter
    if selected_value != "All":
        filtered_df = df[df[selected_column] == selected_value].copy()
    else:
        filtered_df = df.copy()

    # Step 5: Calculate MTM
    def calculate_mtm(row):
        if row['Trade Action'].lower() == 'buy':
            return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
        else:
            return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)

    filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

    st.subheader("📉 MTM Calculation")
    st.dataframe(filtered_df[['Trade Action', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

    total_mtm = filtered_df['MTM'].sum()
    st.markdown(f"### 💰 Total MTM: ₹ {total_mtm:,.2f}")
