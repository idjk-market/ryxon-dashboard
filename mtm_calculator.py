import pandas as pd

def calculate_mtm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Mark-to-Market (MTM) based on trade action.
    Formula:
    - Buy: (Market Price - Book Price) * Quantity
    - Sell: (Book Price - Market Price) * Quantity

    Parameters:
    df (DataFrame): Should include columns:
        ['Trade Action', 'Quantity', 'Book Price', 'Market Price']

    Returns:
    DataFrame: Original with added 'MTM' column
    """
    df = df.copy()
    
    def compute_row_mtm(row):
        if row['Trade Action'].lower() == 'buy':
            return (row['Market Price'] - row['Book Price']) * row['Quantity']
        elif row['Trade Action'].lower() == 'sell':
            return (row['Book Price'] - row['Market Price']) * row['Quantity']
        else:
            return 0

    df['MTM'] = df.apply(compute_row_mtm, axis=1)
    return df
