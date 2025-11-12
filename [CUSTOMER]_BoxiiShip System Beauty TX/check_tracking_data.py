import pandas as pd
import sys

# Read the Excel file with Reid's tracking numbers
try:
    df = pd.read_excel('BoxiiShip-System Beauty _11_3_25.xlsx')

    print(f"Total rows: {len(df)}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)

    # Check for sheet names
    xls = pd.ExcelFile('BoxiiShip-System Beauty _11_3_25.xlsx')
    print(f"\nSheet names: {xls.sheet_names}")

except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)
