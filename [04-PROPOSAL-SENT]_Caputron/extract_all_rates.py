import pandas as pd
import numpy as np

# Read the Excel file - try different approaches to get the data
xl_file = pd.ExcelFile('Caputron Medical Products, LLC._FirstMile_Xparcel_07-24-25.xlsx')

print("=== EXTRACTING FIRSTMILE RATES ===")

# Read Ground rates
ground_df = pd.read_excel(xl_file, sheet_name='Xparcel Ground SLT_NATL')

# Find where actual data starts (look for "Weight" header)
for idx, row in ground_df.iterrows():
    if 'Weight' in str(row.values):
        data_start = idx + 1
        break

# Extract actual rate data
ground_rates = pd.read_excel(xl_file, sheet_name='Xparcel Ground SLT_NATL', skiprows=data_start)

# Print first few rows to understand structure
print("\nGround Rates Structure:")
print(ground_rates.head(20))

# Do the same for Expedited
expedited_df = pd.read_excel(xl_file, sheet_name='Xparcel Expedited SLT_NATL')
for idx, row in expedited_df.iterrows():
    if 'Weight' in str(row.values):
        data_start = idx + 1
        break

expedited_rates = pd.read_excel(xl_file, sheet_name='Xparcel Expedited SLT_NATL', skiprows=data_start)

print("\nExpedited Rates Structure:")
print(expedited_rates.head(20))