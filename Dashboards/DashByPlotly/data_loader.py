import os
import pandas as pd

def load_data():
    df_1 = pd.read_excel('./Data Science Folder/Python Notebooks/KNA Notebooks/DataSets Folder/online_retail_II.xlsx', sheet_name='Year 2009-2010')
    df_2 = pd.read_excel('./Data Science Folder/Python Notebooks/KNA Notebooks/DataSets Folder/online_retail_II.xlsx', sheet_name='Year 2010-2011')
    # Loads two separate sheets from the same Excel file.
    df = pd.concat([df_1, df_2], ignore_index=True)
    # Combines the two DataFrames vertically (row-wise). resets the index in the final DataFrame.
    df = df.dropna(subset=['InvoiceDate', 'Customer ID'])
    # Drops rows where either InvoiceDate or Customer ID is missing.
    df = df[~df['Invoice'].astype(str).str.startswith('c')]
    # Removes canceled invoices, canceled invoices often start with "C" or "c" in the Invoice column
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]
    # Keeps only valid transactions with positive quantity and price
    df['Revenue'] = df['Quantity'] * df['Price']
    # Creates a new column Revenue by multiplying quantity and price
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # Ensures that the InvoiceDate is a proper datetime object
    df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    # Extracts the month from the invoice date,Converts it to a string like "2010-12" for grouping.

    return df