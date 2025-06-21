import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ryxon Dashboard", layout="wide")
st.title("📊 Uploaded Trade Data & 📉 MTM Calculation")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your trade file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Step 2: Read file
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Uploaded Trade Data")
    st.dataframe(df)

    # Step 3: Filter by commodity
    st.subheader("📉 MTM Calculation")

    unique_commodities = df['Commodity'].unique()
    selected_commodity = st.selectbox("Filter by Commodity", options=["All"] + list(unique_commodities))

    if selected_commodity != "All":
        filtered_df = df[df['Commodity'] == selected_commodity]
    else:
        filtered_df = df.copy()

    # Step 4: Calculate MTM
    def calculate_mtm(row):
        if row['Trade Action'].lower() == 'buy':
            return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
        else:
            return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)

    filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

    # Step 5: Display MTM Table
    st.dataframe(filtered_df[['Trade Action', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

    total_mtm = filtered_df['MTM'].sum()
    st.markdown(f"### 💰 Total MTM: ₹ {total_mtm:,.2f}")
else:
    st.warning("📂 Please upload a trade file to proceed.")
