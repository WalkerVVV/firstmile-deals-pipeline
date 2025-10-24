"""
Compare October 6 analysis vs October 13 analysis
Show differences in methodology and results
"""

import pandas as pd

print("=" * 80)
print("STACKD LOGISTICS - ANALYSIS COMPARISON")
print("=" * 80)
print()

# Load the October 6 Excel analysis
try:
    xl = pd.ExcelFile('Stackd_Logistics_FirstMile_Xparcel_Savings_Analysis_20251006_1813.xlsx')
    print("Excel file sheets found:", xl.sheet_names)
    print()

    # Read each sheet to understand structure
    for sheet in xl.sheet_names:
        print(f"=" * 80)
        print(f"SHEET: {sheet}")
        print("=" * 80)
        df = pd.read_excel(xl, sheet_name=sheet, nrows=50)
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        print()
        print("Column names:")
        for col in df.columns:
            print(f"  - {col}")
        print()

        # Look for key metrics
        if 'savings' in sheet.lower() or 'summary' in sheet.lower():
            print("First 20 rows of data:")
            print(df.head(20).to_string())
            print()

        # Look for totals/summary rows
        if len(df) > 0:
            print("Last 5 rows (potential summary):")
            print(df.tail(5).to_string())
            print()

except Exception as e:
    print(f"Error reading Excel file: {e}")
    print()

print("=" * 80)
print("OCTOBER 13 ANALYSIS (NEW) - SUMMARY")
print("=" * 80)
print()
print("Data Source: 8,957 packages with real label costs")
print("Rate Card: FirstMile Xparcel Ground (Select & National)")
print()
print("Results:")
print("  Target Volume: 8,418 packages (DHL eCommerce only)")
print("  Current DHL Cost: $36,815.04/month")
print("  FirstMile Cost: $33,333.93/month")
print("  Monthly Savings: $3,481.11 (9.5%)")
print("  Annual Savings: $41,773.32")
print()
print("Breakdown:")
print("  Select Network (53.4%): 15.7% savings")
print("  National Network (46.6%): 2.7% savings")
print()
print("=" * 80)
