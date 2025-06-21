import streamlit as st

st.subheader("📉 MTM Calculation")

# Step 1: Let user filter by Commodity
unique_commodities = df['Commodity'].unique()
selected_commodity = st.selectbox("Filter by Commodity", options=["All"] + list(unique_commodities))

# Step 2: Apply filter
if selected_commodity != "All":
    filtered_df = df[df['Commodity'] == selected_commodity]
else:
    filtered_df = df.copy()

# Step 3: Calculate MTM using corrected logic
def calculate_mtm(row):
    if row['Trade Action'].lower() == 'buy':
        return round(row['Quantity'] * (row['Market Price'] - row['Book Price']), 2)
    else:
        return round(row['Quantity'] * (row['Book Price'] - row['Market Price']), 2)

filtered_df['MTM'] = filtered_df.apply(calculate_mtm, axis=1)

# Step 4: Show updated MTM table
st.dataframe(filtered_df[['Trade Action', 'Quantity', 'Book Price', 'Market Price', 'MTM']])

# Step 5: Total MTM
total_mtm = filtered_df['MTM'].sum()
st.markdown(f"### Total MTM: ₹ {total_mtm:,.2f}")
