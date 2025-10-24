#!/usr/bin/env python3
"""
Josh's Frogs - Complete Xparcel Analysis from Excel
- Full PLD analysis with zone calculation
- Incumbent carrier rate card extraction (zone x weight matrices)
- Serviceable vs non-serviceable breakdown
- FirstMile Xparcel savings projection
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("JOSH'S FROGS - FULL XPARCEL ANALYSIS")
print("=" * 80)
print()

# Load PLD data from Excel
print("Loading PLD data from Excel...")
df = pd.read_excel("Joshs_Frogs_Current_Rate_Table.xlsx")
print(f"Total shipments: {len(df):,}")
print()

# Print column names to understand structure
print("Column names:")
for col in df.columns:
    print(f"  - {col}")
print()

# Show first few rows
print("First 3 rows of data:")
print(df.head(3).to_string())
print()
