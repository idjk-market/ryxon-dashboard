import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ryxon Dashboard", layout="wide")
st.title("📊 Uploaded Trade Data & 📉 MTM Calculation")

# Upload file
uploaded_file = st.file_uploader("Upload your trade file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Uploaded Trade Data")
    st.dataframe(df)

    st.subheader("🔍 Filter Your Data")

    # === Smart Filters ===
    filters = {}

    # Commodity Filter
    commodities = ["All"] + sorted(df['Commodity'].dropna().unique())
    selected_commodity = st.selectbox("Filter by Commodity", commodities)
    if selected_commodity != "All":
        filters['Commodity'] = selected_commodity

    # Instrument Type Filter
    instruments = ["All"] + sorted(df['Instrument Type'].dropna().unique())
    selected_instrument = st.selectbox("Filter by Instrument Type", instruments)
    if selected_instrument != "All":
        filters['Instrument Type'] = selected_instrument

    # Trade Action Filter
    actions = ["All"] + sorted(df['Trade Action'].dropna().unique())
    selected_action = st.selectbox("Filter by Trade Action", actions)
    if selected_action != "All":
        filters['Trade Action'] = selected_action

    # UOM Filter
    uoms = ["All"] + sorted(df['UOM'].dropna().unique())
    selected_uom = st.selectbox("Filter by UOM", uoms)
    if selected_uom != "All":
        filters['UOM'] = selected_uom

    # Apply filters
    filtered_df = df.copy()
    for col, val in filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]

    st.subheader("📉 MTM Calculation")

    # Calculate MTM
    def calculate_mtm(row):
        if row['Trade Action'].lower() == 'buy':
            return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
        else:
            return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)

    filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

    st.dataframe(filtered_df[['Trade Action', 'Commodity', 'Instrument Type', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

    # Show MTM summary
    total_mtm = filtered_df['MTM'].sum()
    st.markdown(f"### 💰 Total MTM: ₹ {total_mtm:,.2f}")

else:
    st.warning("📂 Please upload a trade file to proceed.")
