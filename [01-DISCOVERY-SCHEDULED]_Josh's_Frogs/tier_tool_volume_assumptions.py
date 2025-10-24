import pandas as pd
import numpy as np

# Based on July 2025 - Highest Month Analysis (31,603 total shipments)
# Mapping current services to Xparcel tiers

# Service mapping based on transit times and service types:
# Priority (1-3 days): FedEx/UPS overnight services, ProMed overnight
# Expedited (2-5 days): FedEx 2-Day, UPS 2-Day Air, DHL Expedited 
# Ground (3-8 days): USPS Ground Advantage, FedEx Ground/Home, UPS Ground

# Total July 2025 shipments: 31,603
total_shipments = 31603

# Service distribution based on analysis
priority_pct = 0.063  # 6.3% - overnight/priority services
expedited_pct = 0.260  # 26.0% - 2-day/expedited services  
ground_pct = 0.677     # 67.7% - ground services

# Calculate service volumes
priority_volume = int(total_shipments * priority_pct)   # 1,996
expedited_volume = int(total_shipments * expedited_pct) # 8,218
ground_volume = int(total_shipments * ground_pct)       # 21,389

# Weight distribution from analysis
# Under 1 lb: 43.7% total
# - 1-4 oz: 2.8%
# - 5-8 oz: 19.0%
# - 9-12 oz: 9.4%
# - 13-15 oz: 10.4%
# - 15.01-15.99 oz: 2.2%
# 1-5 lbs: 42.9%
# Over 5 lbs: 11.9%

# Create weight distribution percentages
weight_distribution = {
    1: 0.0007,    # 1 oz - breaking down 2.8% across 4 oz
    2: 0.0007,    # 2 oz
    3: 0.0007,    # 3 oz
    4: 0.0007,    # 4 oz
    5: 0.0237,    # 5 oz - breaking down 19.0% across 4 oz  
    6: 0.0237,    # 6 oz
    7: 0.0237,    # 7 oz
    8: 0.0239,    # 8 oz
    9: 0.0235,    # 9 oz - breaking down 9.4% across 4 oz
    10: 0.0235,   # 10 oz
    11: 0.0235,   # 11 oz
    12: 0.0235,   # 12 oz
    13: 0.0347,   # 13 oz - breaking down 10.4% across 3 oz
    14: 0.0347,   # 14 oz
    15: 0.0346,   # 15 oz
    15.99: 0.022, # 15.99 oz
    16: 0.259,    # 1 lb (16 oz) - 25.9% at 1-2 lbs
    32: 0.094,    # 2 lbs - 9.4% at 2-3 lbs
    48: 0.052,    # 3 lbs - 5.2% at 3-4 lbs
    64: 0.026,    # 4 lbs - 2.6% at 4-5 lbs
    80: 0.020,    # 5 lbs - start of >5 lbs (11.9% total)
    96: 0.015,    # 6 lbs
    112: 0.012,   # 7 lbs
    128: 0.010,   # 8 lbs
    144: 0.008,   # 9 lbs
    160: 0.007,   # 10 lbs
    176: 0.006,   # 11 lbs
    192: 0.005,   # 12 lbs
    208: 0.004,   # 13 lbs
    224: 0.004,   # 14 lbs
    240: 0.003,   # 15 lbs
    256: 0.003,   # 16 lbs
    272: 0.002,   # 17 lbs
    288: 0.002,   # 18 lbs
    304: 0.002,   # 19 lbs
    320: 0.002,   # 20 lbs
    336: 0.001,   # 21 lbs
    352: 0.001,   # 22 lbs
    368: 0.001,   # 23 lbs
    384: 0.001,   # 24 lbs
    400: 0.001    # 25 lbs
}

# Service allocation strategy based on weight and service type
# Priority gets more lightweight, Expedited gets medium, Ground gets full distribution
priority_weight_adj = {
    1: 1.5, 2: 1.5, 3: 1.5, 4: 1.5, 5: 1.4, 6: 1.4, 7: 1.4, 8: 1.4,
    9: 1.3, 10: 1.3, 11: 1.3, 12: 1.3, 13: 1.2, 14: 1.2, 15: 1.2, 15.99: 1.2,
    16: 0.8, 32: 0.7, 48: 0.6, 64: 0.5, 80: 0.4, 96: 0.3, 112: 0.2, 128: 0.2,
    144: 0.1, 160: 0.1, 176: 0.1, 192: 0.1, 208: 0.1, 224: 0.1, 240: 0.1,
    256: 0.05, 272: 0.05, 288: 0.05, 304: 0.05, 320: 0.05, 336: 0.05,
    352: 0.05, 368: 0.05, 384: 0.05, 400: 0.05
}

expedited_weight_adj = {
    1: 0.9, 2: 0.9, 3: 0.9, 4: 0.9, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0,
    9: 1.1, 10: 1.1, 11: 1.1, 12: 1.1, 13: 1.2, 14: 1.2, 15: 1.2, 15.99: 1.2,
    16: 1.3, 32: 1.2, 48: 1.0, 64: 0.9, 80: 0.8, 96: 0.7, 112: 0.6, 128: 0.5,
    144: 0.4, 160: 0.3, 176: 0.3, 192: 0.2, 208: 0.2, 224: 0.2, 240: 0.1,
    256: 0.1, 272: 0.1, 288: 0.1, 304: 0.1, 320: 0.1, 336: 0.05,
    352: 0.05, 368: 0.05, 384: 0.05, 400: 0.05
}

# Ground gets remaining distribution
ground_weight_adj = {}
for weight in weight_distribution:
    ground_weight_adj[weight] = 1.0  # Will be normalized

# Normalize adjustments for each service
def normalize_weights(weight_dict, base_dist):
    adjusted = {}
    for weight, pct in base_dist.items():
        adjusted[weight] = pct * weight_dict.get(weight, 1.0)
    total = sum(adjusted.values())
    return {k: v/total for k, v in adjusted.items()}

priority_dist = normalize_weights(priority_weight_adj, weight_distribution)
expedited_dist = normalize_weights(expedited_weight_adj, weight_distribution)
ground_dist = normalize_weights(ground_weight_adj, weight_distribution)

# Calculate volumes for each weight/service combination
print("JOSH'S FROGS - TIER TOOL VOLUME ASSUMPTIONS")
print("July 2025 (Highest Month): 31,603 Total Shipments")
print("=" * 80)
print()
print("Copy and paste the table below into the Tier Tool Volume Assumptions tab:")
print()
print(f"{'Weight':<10} {'Priority':<12} {'Expedited':<12} {'Ground':<12} {'Total Volume':<12}")
print("-" * 58)

# Format for oz (1-15.99) and lbs (1-25)
weights_oz = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15.99]
weights_lbs = [16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400]

total_priority = 0
total_expedited = 0
total_ground = 0

# Process ounces
for weight in weights_oz:
    priority_vol = int(priority_volume * priority_dist.get(weight, 0))
    expedited_vol = int(expedited_volume * expedited_dist.get(weight, 0))
    ground_vol = int(ground_volume * ground_dist.get(weight, 0))
    total_vol = priority_vol + expedited_vol + ground_vol
    
    total_priority += priority_vol
    total_expedited += expedited_vol
    total_ground += ground_vol
    
    if weight == 15.99:
        weight_label = "15.99"
    else:
        weight_label = str(int(weight))
    
    # Use dash for zero values as shown in screenshot
    priority_str = str(priority_vol) if priority_vol > 0 else "-"
    expedited_str = str(expedited_vol) if expedited_vol > 0 else "-"
    ground_str = str(ground_vol) if ground_vol > 0 else "-"
    total_str = str(total_vol) if total_vol > 0 else "-"
    
    print(f"{weight_label:<10} {priority_str:<12} {expedited_str:<12} {ground_str:<12} {total_str:<12}")

# Process pounds (convert oz to lbs for display)
for weight_oz in weights_lbs:
    weight_lbs = weight_oz // 16
    priority_vol = int(priority_volume * priority_dist.get(weight_oz, 0))
    expedited_vol = int(expedited_volume * expedited_dist.get(weight_oz, 0))
    ground_vol = int(ground_volume * ground_dist.get(weight_oz, 0))
    total_vol = priority_vol + expedited_vol + ground_vol
    
    total_priority += priority_vol
    total_expedited += expedited_vol
    total_ground += ground_vol
    
    # Use dash for zero values as shown in screenshot
    priority_str = str(priority_vol) if priority_vol > 0 else "-"
    expedited_str = str(expedited_vol) if expedited_vol > 0 else "-"
    ground_str = str(ground_vol) if ground_vol > 0 else "-"
    total_str = str(total_vol) if total_vol > 0 else "-"
    
    print(f"{weight_lbs:<10} {priority_str:<12} {expedited_str:<12} {ground_str:<12} {total_str:<12}")

print("-" * 58)
print(f"{'Total':<10} {total_priority:<12} {total_expedited:<12} {total_ground:<12} {total_priority + total_expedited + total_ground:<12}")
print()
print("Notes:")
print("- Priority (1-3 day): Maps to overnight/express services")
print("- Expedited (2-5 day): Maps to 2-day air services")  
print("- Ground (3-8 day): Maps to USPS Ground Advantage and ground services")
print("- Based on July 2025 actual shipment data (highest volume month)")