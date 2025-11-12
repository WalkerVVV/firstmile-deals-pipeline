import pandas as pd
import sys

# Read the specific sheet with Reid's tracking numbers
try:
    # Read the "Sent from Boxi_Issues" sheet
    df = pd.read_excel('BoxiiShip-System Beauty _11_3_25.xlsx', sheet_name='Sent from Boxi_Issues')

    print(f"Total rows: {len(df)}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst 10 rows:")
    print(df.head(10))
    print(f"\nLast 10 rows:")
    print(df.tail(10))

    # Look for tracking number column
    for col in df.columns:
        if 'track' in col.lower() or 'label' in col.lower():
            print(f"\n{col} column sample:")
            print(df[col].dropna().head(10))

except Exception as e:
    print(f"Error reading file: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
