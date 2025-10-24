import pandas as pd
import numpy as np

# Read the CSV
df = pd.read_csv("jmgroup30daydata.csv")

print("="*60)
print("DIMENSIONAL ANALYSIS")
print("="*60)
print()

# Convert dimensions to numeric
df["Height"] = pd.to_numeric(df["Dimensions - Height"], errors="coerce")
df["Length"] = pd.to_numeric(df["Dimensions - Length"], errors="coerce")
df["Width"] = pd.to_numeric(df["Dimensions - Width"], errors="coerce")

# Calculate cubic inches
df["Cubic_Inches"] = df["Height"] * df["Length"] * df["Width"]

# Filter for packages with dimensions
has_dims = df[(df["Height"] > 0) | (df["Length"] > 0) | (df["Width"] > 0)].copy()
has_all_dims = df[(df["Height"] > 0) & (df["Length"] > 0) & (df["Width"] > 0)].copy()

print("DIMENSIONAL DATA AVAILABILITY:")
print("-"*40)
print(f"Total packages: {len(df):,}")
print(f"Packages with any dimensions: {len(has_dims):,} ({(len(has_dims)/len(df))*100:.1f}%)")
print(f"Packages with complete dimensions: {len(has_all_dims):,} ({(len(has_all_dims)/len(df))*100:.1f}%)")
print(f"Packages without dimensions: {len(df) - len(has_dims):,} ({((len(df) - len(has_dims))/len(df))*100:.1f}%)")
print()

if len(has_all_dims) > 0:
    print("AVERAGE DIMENSIONS (Complete Data Only):")
    print("-"*40)
    avg_length = has_all_dims["Length"].mean()
    avg_width = has_all_dims["Width"].mean()
    avg_height = has_all_dims["Height"].mean()
    avg_volume = has_all_dims["Cubic_Inches"].mean()
    
    print(f"Average Length: {avg_length:.1f} inches")
    print(f"Average Width: {avg_width:.1f} inches")
    print(f"Average Height: {avg_height:.1f} inches")
    print(f"Average Volume: {avg_volume:.1f} cubic inches")
    print()
    
    # Percentile analysis
    print("DIMENSION PERCENTILES:")
    print("-"*40)
    percentiles = [25, 50, 75, 90, 95]
    
    print("Length (inches):")
    for p in percentiles:
        val = has_all_dims["Length"].quantile(p/100)
        print(f"  {p}th percentile: {val:.1f}")
    
    print("\nWidth (inches):")
    for p in percentiles:
        val = has_all_dims["Width"].quantile(p/100)
        print(f"  {p}th percentile: {val:.1f}")
    
    print("\nHeight (inches):")
    for p in percentiles:
        val = has_all_dims["Height"].quantile(p/100)
        print(f"  {p}th percentile: {val:.1f}")
    
    print()
    print("CUBIC VOLUME ANALYSIS:")
    print("-"*40)
    
    # 1728 cubic inches = 1 cubic foot
    under_1_cubic = has_all_dims[has_all_dims["Cubic_Inches"] < 1728]
    over_1_cubic = has_all_dims[has_all_dims["Cubic_Inches"] >= 1728]
    
    print(f"Under 1 cubic foot (<1,728 cu in): {len(under_1_cubic):,} ({(len(under_1_cubic)/len(has_all_dims))*100:.1f}%)")
    print(f"Over 1 cubic foot (>=1,728 cu in): {len(over_1_cubic):,} ({(len(over_1_cubic)/len(has_all_dims))*100:.1f}%)")
    
    if len(under_1_cubic) > 0:
        print(f"\nUnder 1 cubic foot - Average dimensions:")
        print(f"  Length: {under_1_cubic['Length'].mean():.1f} in")
        print(f"  Width: {under_1_cubic['Width'].mean():.1f} in")
        print(f"  Height: {under_1_cubic['Height'].mean():.1f} in")
        print(f"  Volume: {under_1_cubic['Cubic_Inches'].mean():.1f} cu in")
    
    if len(over_1_cubic) > 0:
        print(f"\nOver 1 cubic foot - Average dimensions:")
        print(f"  Length: {over_1_cubic['Length'].mean():.1f} in")
        print(f"  Width: {over_1_cubic['Width'].mean():.1f} in")
        print(f"  Height: {over_1_cubic['Height'].mean():.1f} in")
        print(f"  Volume: {over_1_cubic['Cubic_Inches'].mean():.1f} cu in")
    
    print()
    print("DIMENSION RANGES:")
    print("-"*40)
    
    # Size categories
    small = has_all_dims[has_all_dims["Cubic_Inches"] < 500]
    medium = has_all_dims[(has_all_dims["Cubic_Inches"] >= 500) & (has_all_dims["Cubic_Inches"] < 1000)]
    large = has_all_dims[(has_all_dims["Cubic_Inches"] >= 1000) & (has_all_dims["Cubic_Inches"] < 1728)]
    xlarge = has_all_dims[has_all_dims["Cubic_Inches"] >= 1728]
    
    print(f"Small (<500 cu in): {len(small):,} ({(len(small)/len(has_all_dims))*100:.1f}%)")
    print(f"Medium (500-999 cu in): {len(medium):,} ({(len(medium)/len(has_all_dims))*100:.1f}%)")
    print(f"Large (1000-1727 cu in): {len(large):,} ({(len(large)/len(has_all_dims))*100:.1f}%)")
    print(f"Extra Large (>=1728 cu in): {len(xlarge):,} ({(len(xlarge)/len(has_all_dims))*100:.1f}%)")
else:
    print("No packages with complete dimensional data available for analysis.")