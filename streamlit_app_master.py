import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="Ryxon Risk Dashboard",
    page_icon="📊",
    layout="wide"
)

def load_data(uploaded_file):
    """Handle both CSV and Excel files"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            file_bytes = BytesIO(uploaded_file.getvalue())
            return pd.read_excel(file_bytes, engine='openpyxl')
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a UI on top of a dataframe to filter columns"""
    modification_container = st.container()
    
    with modification_container:
        to_filter_columns = st.multiselect("Filter table by", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            # Treat columns with < 10 unique values as categorical
            if pd.api.types.is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_text_input)]
    
    return df

def main():
    st.title("📊 Ryxon Risk Analytics Dashboard")
    
    uploaded_file = st.file_uploader(
        "Upload Trade Data (Excel or CSV)",
        type=["xlsx", "csv"],
        help="Maximum file size: 200MB. Supported formats: .xlsx, .csv"
    )

    if uploaded_file is not None:
        with st.spinner("Processing your file..."):
            try:
                df = load_data(uploaded_file)
                
                if df is not None:
                    # Basic data validation
                    required_cols = {'Book Price', 'Market Price', 'Quantity'}
                    if not required_cols.issubset(df.columns):
                        missing = required_cols - set(df.columns)
                        st.error(f"Missing required columns: {', '.join(missing)}")
                        return
                    
                    # Calculate metrics
                    df['MTM'] = (df['Market Price'] - df['Book Price']) * df['Quantity']
                    df['Realized PnL'] = np.where(
                        df['Trade Action'].str.lower() == 'sell',
                        df['MTM'],
                        0
                    )
                    df['Unrealized PnL'] = df['MTM'] - df['Realized PnL']
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Trades", len(df))
                    col2.metric("Total MTM", f"${df['MTM'].sum():,.2f}")
                    col3.metric("Unique Instruments", df['Instrument Type'].nunique())
                    
                    # Filterable table
                    st.subheader("Trade Data")
                    filtered_df = filter_dataframe(df)
                    
                    # Display formatted table
                    st.dataframe(
                        filtered_df.style.format({
                            'Book Price': '{:.2f}',
                            'Market Price': '{:.2f}',
                            'MTM': '{:.2f}',
                            'Realized PnL': '{:.2f}',
                            'Unrealized PnL': '{:.2f}',
                            'Daily Return': '{:.4f}'
                        }),
                        use_container_width=True,
                        height=500
                    )
                    
                    # Visualization
                    st.subheader("MTM Distribution by Commodity")
                    fig = px.bar(
                        filtered_df.groupby('Commodity')['MTM'].sum().reset_index(),
                        x='Commodity',
                        y='MTM',
                        color='Commodity'
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
