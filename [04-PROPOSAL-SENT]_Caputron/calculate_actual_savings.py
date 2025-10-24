import pandas as pd
import numpy as np

# Volume distribution from dashboard (daily shipments)
weight_distribution = {
    1: 20, 2: 20, 3: 20, 4: 20, 5: 20,  # 1-5 oz: 100 shipments (10%)
    6: 36, 7: 36, 8: 36, 9: 36, 10: 36,  # 6-10 oz: 180 shipments (18%)
    11: 50, 12: 60, 13: 80, 14: 100, 15: 160,  # 11-15 oz: 450 shipments (45%)
    16: 60, 32: 80, 48: 50, 64: 20, 80: 10  # 1-5 lbs: 220 shipments (22%)
}

# Current rates from tier tool
current_rates = {
    1: 4.08, 2: 4.25, 3: 4.42, 4: 4.59, 5: 4.76,
    6: 4.93, 7: 5.10, 8: 5.27, 9: 5.44, 10: 5.61,
    11: 5.78, 12: 5.95, 13: 6.12, 14: 6.29, 15: 7.27,  # Peak volume at 15 oz
    16: 6.63, 32: 7.65, 48: 8.67, 64: 9.69, 80: 10.71
}

# FirstMile rates (using Zone 3 average as representative)
# From the extracted data
firstmile_rates = {
    1: 3.50, 2: 3.57, 3: 3.62, 4: 3.68, 5: 3.74,
    6: 3.80, 7: 3.82, 8: 3.84, 9: 3.93, 10: 3.95,
    11: 3.99, 12: 4.02, 13: 4.07, 14: 4.08, 15: 4.11,
    16: 4.57, 32: 5.25, 48: 5.44, 64: 6.00, 80: 6.43  # Extrapolated for 5 lb
}

print("=== CAPUTRON ACTUAL COST ANALYSIS ===")
print("\nDaily Volume: 1,000 shipments")
print("Annual Volume: 365,000 shipments")

# Calculate savings by weight
print("\n=== DETAILED COST COMPARISON BY WEIGHT ===")
print("Weight\tDaily Vol\tCurrent Rate\tFM Rate\tSavings\t% Saved\tDaily Savings")
print("-" * 80)

total_current_cost = 0
total_fm_cost = 0
daily_volume = 0

for weight, volume in weight_distribution.items():
    current = current_rates.get(weight, 0)
    fm = firstmile_rates.get(weight, 0)
    savings_per = current - fm
    percent = (savings_per / current * 100) if current > 0 else 0
    daily_savings = savings_per * volume
    
    total_current_cost += current * volume
    total_fm_cost += fm * volume
    daily_volume += volume
    
    if weight < 16:
        weight_str = f"{weight} oz"
    else:
        weight_str = f"{weight//16} lb"
    
    print(f"{weight_str}\t{volume}\t${current:.2f}\t\t${fm:.2f}\t${savings_per:.2f}\t{percent:.1f}%\t${daily_savings:.2f}")

# Summary calculations
print("\n=== SUMMARY CALCULATIONS ===")
print(f"Total Daily Volume Analyzed: {daily_volume} shipments")
print(f"Current Daily Cost: ${total_current_cost:,.2f}")
print(f"FirstMile Daily Cost: ${total_fm_cost:,.2f}")
print(f"Daily Savings: ${total_current_cost - total_fm_cost:,.2f}")
print(f"Average Savings Per Package: ${(total_current_cost - total_fm_cost) / daily_volume:.2f}")
print(f"Overall Savings Percentage: {((total_current_cost - total_fm_cost) / total_current_cost * 100):.1f}%")

# Annual projections
annual_current = total_current_cost * 365
annual_fm = total_fm_cost * 365
annual_savings = annual_current - annual_fm

print("\n=== ANNUAL PROJECTIONS ===")
print(f"Current Annual Spend: ${annual_current:,.2f}")
print(f"FirstMile Annual Cost: ${annual_fm:,.2f}")
print(f"Annual Savings: ${annual_savings:,.2f}")

# Service level analysis
under_1lb_volume = sum(weight_distribution[w] for w in range(1, 16))
print(f"\n=== SERVICE LEVEL ALLOCATION ===")
print(f"<1 lb to Select Network: ~{int(under_1lb_volume * 0.55)} shipments/day")
print(f"<1 lb to National Network: ~{int(under_1lb_volume * 0.45)} shipments/day")
print(f"1-5 lb to National Network: 220 shipments/day")
print(f"Priority Service (3% of volume): 30 shipments/day")