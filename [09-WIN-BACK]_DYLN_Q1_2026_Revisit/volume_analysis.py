import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("Loading DYLN Fulfillment data...")
df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

print("\n" + "="*80)
print("DYLN FULFILLMENT - COMPLETE VOLUME ANALYSIS")
print("="*80)

# Basic data overview
print(f"\nTotal Records: {len(df):,}")
print(f"Date Range: {df['Order Date'].min()} to {df['Order Date'].max()}")
print(f"\nColumns in dataset:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

# Clean and prepare data
print("\n" + "-"*50)
print("DATA PREPARATION")
print("-"*50)

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Calculate shipping metrics
df['Days to Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

print(f"Data prepared for analysis")
print(f"Unique Orders: {df['Order'].nunique():,}")
print(f"Unique SKUs: {df['Item Name'].nunique():,}")

# Save cleaned dataframe for further analysis
df.to_pickle('dyln_data_cleaned.pkl')
print("\nCleaned data saved for detailed analysis...")