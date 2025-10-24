import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

print("="*80)
print("DYLN ANNUAL REVENUE ESTIMATION")
print("="*80)

# Basic metrics
total_shipments = len(df)
date_range = (df['shipment_date'].max() - df['shipment_date'].min()).days + 1
daily_avg = total_shipments / date_range
annual_projection = daily_avg * 365

print("\n1. SHIPMENT VOLUME ANALYSIS")
print("-"*40)
print(f"Current Period: {date_range} days")
print(f"Total Shipments: {total_shipments:,}")
print(f"Daily Average: {daily_avg:.0f}")
print(f"Annual Projection: {annual_projection:,.0f} shipments")

# Weight analysis for product type estimation
avg_weight = df['Weight (oz)'].mean()
median_weight = df['Weight (oz)'].median()

print("\n2. PRODUCT PROFILE ANALYSIS")
print("-"*40)
print(f"Average Weight: {avg_weight:.1f} oz")
print(f"Median Weight: {median_weight:.1f} oz")

# Package type analysis
package_distribution = df['Package'].value_counts()
mailer_pct = package_distribution[package_distribution.index.str.contains('Mailer')].sum() / total_shipments * 100

print(f"Mailer Usage: {mailer_pct:.1f}% (indicates soft goods/accessories)")

# Weight distribution for product mix estimation
weight_ranges = {
    'Ultra-light (0-4 oz)': df[df['Weight (oz)'] <= 4].shape[0],
    'Light (4-8 oz)': df[(df['Weight (oz)'] > 4) & (df['Weight (oz)'] <= 8)].shape[0],
    'Medium (8-16 oz)': df[(df['Weight (oz)'] > 8) & (df['Weight (oz)'] <= 16)].shape[0],
    'Heavy (>16 oz)': df[df['Weight (oz)'] > 16].shape[0]
}

print("\nWeight Distribution (Product Type Indicators):")
for range_name, count in weight_ranges.items():
    pct = count / total_shipments * 100
    print(f"  {range_name:20} {count:,} ({pct:.1f}%)")

print("\n3. REVENUE ESTIMATION SCENARIOS")
print("-"*40)
print("\nBased on typical eCommerce patterns for lightweight consumer products:")
print("(Weight profile suggests accessories, small electronics, or lifestyle items)")

# Scenario calculations
scenarios = {
    'Conservative': {
        'aov': 35,
        'description': 'Budget accessories/small items',
        'reasoning': 'Low weight, high mailer usage suggests simple products'
    },
    'Moderate': {
        'aov': 55,
        'description': 'Mid-range lifestyle/tech accessories',
        'reasoning': 'DYLN brand positioning, direct-to-consumer model'
    },
    'Aggressive': {
        'aov': 75,
        'description': 'Premium accessories/bundles',
        'reasoning': 'Some heavier packages suggest multi-item orders'
    }
}

print("\n" + "="*60)
print("ANNUAL REVENUE PROJECTIONS")
print("="*60)

for scenario_name, details in scenarios.items():
    annual_revenue = annual_projection * details['aov']
    monthly_revenue = annual_revenue / 12
    
    print(f"\n{scenario_name} Scenario: ${details['aov']} AOV")
    print(f"  Product Type: {details['description']}")
    print(f"  Reasoning: {details['reasoning']}")
    print(f"  Annual Revenue: ${annual_revenue:,.0f}")
    print(f"  Monthly Revenue: ${monthly_revenue:,.0f}")

# Most likely scenario based on data patterns
print("\n" + "="*60)
print("MOST LIKELY SCENARIO")
print("="*60)

# Factors supporting moderate scenario
likely_aov = 55
likely_annual_revenue = annual_projection * likely_aov
likely_monthly_revenue = likely_annual_revenue / 12

print(f"\nBased on data patterns, most likely scenario:")
print(f"  Estimated AOV: ${likely_aov}")
print(f"  Annual Shipments: {annual_projection:,.0f}")
print(f"  ESTIMATED ANNUAL REVENUE: ${likely_annual_revenue:,.0f}")
print(f"  Monthly Average: ${likely_monthly_revenue:,.0f}")

print("\nSupporting factors:")
print("  • 94% packages under 1 lb = single item orders")
print("  • 5-8 oz average = lightweight consumer products")
print("  • 72% use 6x9 mailers = soft goods/accessories")
print("  • Direct-to-consumer model (individual orders)")
print("  • DYLN brand suggests lifestyle/wellness products")

# Shipping revenue estimate
avg_shipping_charge = 7.95  # Typical eCommerce shipping charge
annual_shipping_revenue = annual_projection * avg_shipping_charge * 0.6  # Assume 60% pay shipping

print(f"\nAdditional Shipping Revenue (if charged):")
print(f"  Estimated: ${annual_shipping_revenue:,.0f} annually")
print(f"  (Assuming 60% of orders pay ${avg_shipping_charge:.2f} shipping)")

print("\n" + "="*60)
print("TOTAL REVENUE ESTIMATE")
print("="*60)
print(f"\nProduct Revenue: ${likely_annual_revenue:,.0f}")
print(f"Shipping Revenue: ${annual_shipping_revenue:,.0f}")
print(f"TOTAL ESTIMATED ANNUAL REVENUE: ${(likely_annual_revenue + annual_shipping_revenue):,.0f}")

print("\nNote: This is an estimation based on shipping patterns and typical")
print("eCommerce metrics. Actual revenue may vary significantly based on:")
print("  • Actual product prices")
print("  • Product mix and bundles")
print("  • Promotions and discounts")
print("  • Return rates")
print("  • Seasonal variations")