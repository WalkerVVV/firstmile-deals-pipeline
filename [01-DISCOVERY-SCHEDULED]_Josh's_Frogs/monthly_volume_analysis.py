import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('247bef97-8663-431e-b2f5-dd2ca243633d.csv')

# Extract date from Number field (format: YYYY-MM-DD-XXXX-X)
df['date'] = pd.to_datetime(df['Number'].str[:10], format='%Y-%m-%d', errors='coerce')
df['year_month'] = df['date'].dt.to_period('M')

print("=" * 80)
print("JOSH'S FROGS - MONTHLY SHIPMENT VOLUME ANALYSIS")
print("=" * 80)
print()

# Monthly volume and spend
monthly_stats = df.groupby('year_month').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})

monthly_stats['Avg Cost'] = (monthly_stats['Cost'] / monthly_stats['Volume']).round(2)
monthly_stats['Daily Avg'] = monthly_stats['Volume'] / monthly_stats.index.to_timestamp().days_in_month

# Calculate month-over-month growth
monthly_stats['MoM Growth %'] = monthly_stats['Volume'].pct_change() * 100

print("MONTHLY SHIPMENT VOLUMES")
print("-" * 80)
print(f"{'Month':<12} {'Volume':>10} {'Daily Avg':>10} {'Total Cost':>12} {'Avg Cost':>10} {'MoM %':>8}")
print("-" * 80)

for idx, row in monthly_stats.iterrows():
    month_str = str(idx)
    volume = row['Volume']
    daily_avg = row['Daily Avg']
    total_cost = row['Cost']
    avg_cost = row['Avg Cost']
    mom_growth = row['MoM Growth %']
    
    mom_str = f"{mom_growth:+.1f}" if pd.notna(mom_growth) else "   -"
    
    print(f"{month_str:<12} {volume:>10,} {daily_avg:>10.1f} ${total_cost:>11,.2f} ${avg_cost:>9.2f} {mom_str:>8}")

print("-" * 80)
print(f"{'TOTAL':<12} {monthly_stats['Volume'].sum():>10,} {' ':>10} ${monthly_stats['Cost'].sum():>11,.2f}")
print()

# Statistics
print("SUMMARY STATISTICS")
print("-" * 40)
print(f"Average Monthly Volume: {monthly_stats['Volume'].mean():,.0f}")
print(f"Median Monthly Volume: {monthly_stats['Volume'].median():,.0f}")
print(f"Highest Month: {monthly_stats['Volume'].idxmax()} ({monthly_stats['Volume'].max():,} shipments)")
print(f"Lowest Month: {monthly_stats['Volume'].idxmin()} ({monthly_stats['Volume'].min():,} shipments)")
print(f"Std Deviation: {monthly_stats['Volume'].std():,.0f}")
print()

# Quarterly aggregation
df['quarter'] = df['date'].dt.to_period('Q')
quarterly_stats = df.groupby('quarter').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})

print("QUARTERLY VOLUMES")
print("-" * 40)
print(f"{'Quarter':<10} {'Volume':>12} {'Total Cost':>15}")
print("-" * 40)
for idx, row in quarterly_stats.iterrows():
    print(f"{str(idx):<10} {row['Volume']:>12,} ${row['Cost']:>14,.2f}")
print()

# Trend analysis
recent_6_months = monthly_stats.tail(6)
if len(recent_6_months) >= 2:
    recent_growth = recent_6_months['Volume'].pct_change().mean() * 100
    print("TREND ANALYSIS")
    print("-" * 40)
    print(f"Last 6 Months Avg Growth: {recent_growth:.1f}% per month")
    print(f"Last 6 Months Avg Volume: {recent_6_months['Volume'].mean():,.0f}")
    
    # Simple projection
    last_month_volume = monthly_stats['Volume'].iloc[-1]
    projected_next = last_month_volume * (1 + recent_growth/100)
    print(f"Projected Next Month: {projected_next:,.0f} (based on 6-month trend)")

print()
print("=" * 80)