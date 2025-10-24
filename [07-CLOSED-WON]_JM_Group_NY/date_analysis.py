"""
Analyze JM Group shipments before September 18, 2025
"""

import pandas as pd
from datetime import datetime

# Load the data
df = pd.read_excel('Domestic_Tracking_JM_Group_Aug_2025.xlsx')

# Display available date columns
print("Available date columns:")
for col in df.columns:
    if 'date' in col.lower() or 'Date' in col:
        print(f"  - {col}")

# Parse dates - try multiple possible date columns
date_columns = ['Request Date', 'Start Date', 'ShipDate', 'Ship Date']
date_col_found = None

for col in date_columns:
    if col in df.columns:
        date_col_found = col
        df['Parsed_Date'] = pd.to_datetime(df[col], errors='coerce')
        break

if date_col_found:
    print(f"\nUsing date column: {date_col_found}")

    # Filter for dates before September 18, 2025
    cutoff_date = pd.to_datetime('2025-09-18')

    # Remove any NaT values
    valid_dates = df['Parsed_Date'].notna()
    df_valid = df[valid_dates]

    # Filter shipments before cutoff
    before_cutoff = df_valid[df_valid['Parsed_Date'] < cutoff_date]
    after_cutoff = df_valid[df_valid['Parsed_Date'] >= cutoff_date]

    print(f"\nAnalysis Results:")
    print(f"=" * 60)
    print(f"Total shipments with valid dates: {len(df_valid)}")
    print(f"Shipments BEFORE Sep 18, 2025: {len(before_cutoff)}")
    print(f"Shipments ON/AFTER Sep 18, 2025: {len(after_cutoff)}")
    print(f"Percentage before Sep 18: {len(before_cutoff)/len(df_valid)*100:.1f}%")

    # Date range analysis
    if len(before_cutoff) > 0:
        print(f"\nShipments BEFORE Sep 18, 2025:")
        print(f"  - Earliest: {before_cutoff['Parsed_Date'].min().strftime('%B %d, %Y')}")
        print(f"  - Latest: {before_cutoff['Parsed_Date'].max().strftime('%B %d, %Y')}")

        # Daily breakdown for dates close to cutoff
        print(f"\nDaily breakdown (last 7 days before cutoff):")
        for i in range(7, 0, -1):
            check_date = cutoff_date - pd.Timedelta(days=i)
            daily_count = len(before_cutoff[before_cutoff['Parsed_Date'].dt.date == check_date.date()])
            if daily_count > 0:
                print(f"  {check_date.strftime('%b %d, %Y')}: {daily_count} shipments")

    if len(after_cutoff) > 0:
        print(f"\nShipments ON/AFTER Sep 18, 2025:")
        print(f"  - Earliest: {after_cutoff['Parsed_Date'].min().strftime('%B %d, %Y')}")
        print(f"  - Latest: {after_cutoff['Parsed_Date'].max().strftime('%B %d, %Y')}")

        # Daily breakdown for dates after cutoff
        print(f"\nDaily breakdown (first 7 days from cutoff):")
        for i in range(0, 7):
            check_date = cutoff_date + pd.Timedelta(days=i)
            daily_count = len(after_cutoff[after_cutoff['Parsed_Date'].dt.date == check_date.date()])
            if daily_count > 0:
                print(f"  {check_date.strftime('%b %d, %Y')}: {daily_count} shipments")

    # Summary statistics
    print(f"\n" + "=" * 60)
    print(f"ANSWER: {len(before_cutoff)} shipments were sent before Sep 18, 2025")
    print(f"=" * 60)

else:
    print("No date column found in the data!")
    print("Available columns:", list(df.columns))