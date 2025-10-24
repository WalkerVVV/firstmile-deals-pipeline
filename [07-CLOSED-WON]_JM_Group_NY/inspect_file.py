"""Inspect the Excel file structure"""
import pandas as pd

file_path = r"C:\Users\BrettWalker\FirstMile_Deals\[07-CLOSED-WON]_JM_Group_NY\JM Group NY_FirstMile_Domestic_Tracking_9.30.25.xlsx"

# Check sheets
xl_file = pd.ExcelFile(file_path)
print(f"Sheets in file: {xl_file.sheet_names}")

# Load each sheet
for sheet in xl_file.sheet_names:
    print(f"\n{'='*60}")
    print(f"Sheet: {sheet}")
    print(f"{'='*60}")
    df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nFirst 5 rows:")
    print(df.head())
