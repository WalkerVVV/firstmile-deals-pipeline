import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("Loading DYLN Fulfillment data...")
df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

print(f"\nTotal Records: {len(df):,}")
print(f"\nColumn Names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print("\nFirst 5 rows preview:")
print(df.head())

print("\nData types:")
print(df.dtypes)