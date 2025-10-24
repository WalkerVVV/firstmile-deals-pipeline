"""
Transit Analysis Confirmation Script
Analyzes transit data from the Raw Data tab of FirstMile Analytics file
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_raw_data():
    """Load data from Raw Data tab of FirstMile Analytics file"""
    file_path = 'FirstMile_Analytics_ship_data-2.22.2025_to_9.2.2025_BoxiiShip_System_Beauty_TX)_20250905.xlsx'
    df = pd.read_excel(file_path, sheet_name='Raw Data')
    print(f"[OK] Loaded {len(df):,} records from Raw Data tab")
    return df

def data_quality_check(df):
    """Perform data quality checks"""
    print("\n" + "="*60)
    print("DATA QUALITY CHECK")
    print("="*60)
    
    # Check for missing values in critical columns
    critical_cols = ['Tracking Number', 'Xparcel Type', 'Days In Transit', 'Delivered Status']
    for col in critical_cols:
        if col in df.columns:
            missing = df[col].isna().sum()
            pct = (missing / len(df)) * 100
            print(f"{col}: {missing:,} missing ({pct:.2f}%)")
    
    # Date range
    if 'Request Date' in df.columns:
        print(f"\nDate Range: {df['Request Date'].min()} to {df['Request Date'].max()}")
    
    # Service level distribution
    print(f"\nService Level Distribution:")
    service_dist = df['Xparcel Type'].value_counts()
    for service, count in service_dist.items():
        print(f"  {service}: {count:,} ({count/len(df)*100:.1f}%)")
    
    return True

def transit_time_analysis(df):
    """Comprehensive transit time analysis"""
    print("\n" + "="*60)
    print("TRANSIT TIME ANALYSIS")
    print("="*60)
    
    # Overall statistics
    delivered_df = df[df['Delivered Status'] == 'Delivered'].copy()
    in_transit_df = df[df['Delivered Status'] == 'In Transit'].copy()
    
    print(f"\nDelivery Status:")
    print(f"  Delivered: {len(delivered_df):,} ({len(delivered_df)/len(df)*100:.1f}%)")
    print(f"  In Transit: {len(in_transit_df):,} ({len(in_transit_df)/len(df)*100:.1f}%)")
    
    if len(delivered_df) > 0:
        print(f"\nTransit Time Statistics (Delivered Packages):")
        print(f"  Mean: {delivered_df['Days In Transit'].mean():.2f} days")
        print(f"  Median: {delivered_df['Days In Transit'].median():.1f} days")
        print(f"  Std Dev: {delivered_df['Days In Transit'].std():.2f} days")
        print(f"  Min: {delivered_df['Days In Transit'].min():.0f} days")
        print(f"  Max: {delivered_df['Days In Transit'].max():.0f} days")
        
        # Percentiles
        percentiles = [50, 75, 90, 95, 99]
        print(f"\nPercentiles:")
        for p in percentiles:
            val = delivered_df['Days In Transit'].quantile(p/100)
            print(f"  {p}th percentile: {val:.1f} days")
    
    # Transit day distribution
    print(f"\nTransit Day Distribution (Delivered):")
    if len(delivered_df) > 0:
        transit_dist = delivered_df['Days In Transit'].value_counts().sort_index()
        
        # Group into categories
        day_0 = transit_dist.get(0, 0)
        day_1 = transit_dist.get(1, 0)
        day_2 = transit_dist.get(2, 0)
        day_3 = transit_dist.get(3, 0)
        day_4 = transit_dist.get(4, 0)
        day_5_plus = sum(transit_dist[transit_dist.index >= 5].values)
        
        total_delivered = len(delivered_df)
        print(f"  Day 0 (Same Day): {day_0:,} ({day_0/total_delivered*100:.1f}%)")
        print(f"  Day 1 (Next Day): {day_1:,} ({day_1/total_delivered*100:.1f}%)")
        print(f"  Day 2: {day_2:,} ({day_2/total_delivered*100:.1f}%)")
        print(f"  Day 3: {day_3:,} ({day_3/total_delivered*100:.1f}%)")
        print(f"  Day 4: {day_4:,} ({day_4/total_delivered*100:.1f}%)")
        print(f"  Day 5+: {day_5_plus:,} ({day_5_plus/total_delivered*100:.1f}%)")
        
        # Cumulative distribution
        print(f"\nCumulative Distribution:")
        cumulative_3 = day_0 + day_1 + day_2 + day_3
        cumulative_5 = cumulative_3 + day_4 + transit_dist[(transit_dist.index == 5)].sum()
        
        print(f"  Within 3 days: {cumulative_3:,} ({cumulative_3/total_delivered*100:.1f}%)")
        print(f"  Within 5 days: {cumulative_5:,} ({cumulative_5/total_delivered*100:.1f}%)")
    
    return delivered_df

def sla_compliance_analysis(df):
    """Detailed SLA compliance analysis by service level"""
    print("\n" + "="*60)
    print("SLA COMPLIANCE ANALYSIS")
    print("="*60)
    
    # Define SLA windows
    sla_windows = {
        'Priority': 3,
        'Expedited': 5,
        'Ground': 8
    }
    
    # Only analyze delivered packages
    delivered_df = df[df['Delivered Status'] == 'Delivered'].copy()
    
    print(f"\nSLA Performance by Service Level:")
    print("-"*50)
    
    overall_results = []
    
    for service, sla_days in sla_windows.items():
        service_df = delivered_df[delivered_df['Xparcel Type'] == service]
        
        if len(service_df) > 0:
            # Calculate compliance
            on_time = service_df[service_df['Days In Transit'] <= sla_days]
            compliance_pct = (len(on_time) / len(service_df)) * 100
            
            # Performance status
            if compliance_pct == 100:
                status = "[PERFECT] Perfect Compliance"
            elif compliance_pct >= 95:
                status = "[EXCEEDS] Exceeds Standard"
            elif compliance_pct >= 90:
                status = "[MEETS] Meets Standard"
            else:
                status = "[WARNING] Below Standard"
            
            print(f"\nXparcel {service} ({sla_days}-day SLA):")
            print(f"  Total Delivered: {len(service_df):,}")
            print(f"  On-Time: {len(on_time):,}")
            print(f"  Late: {len(service_df) - len(on_time):,}")
            print(f"  SLA Compliance: {compliance_pct:.2f}%")
            print(f"  Status: {status}")
            
            # Additional statistics for this service
            print(f"  Avg Transit: {service_df['Days In Transit'].mean():.2f} days")
            print(f"  Median Transit: {service_df['Days In Transit'].median():.1f} days")
            
            # Store for summary
            overall_results.append({
                'Service': f'Xparcel {service}',
                'SLA': sla_days,
                'Delivered': len(service_df),
                'Compliance': compliance_pct
            })
    
    # Overall SLA performance
    if overall_results:
        print("\n" + "="*60)
        print("OVERALL SLA SUMMARY")
        print("="*60)
        
        total_delivered = sum(r['Delivered'] for r in overall_results)
        weighted_compliance = sum(r['Compliance'] * r['Delivered'] for r in overall_results) / total_delivered
        
        print(f"Total Delivered Packages: {total_delivered:,}")
        print(f"Weighted Average SLA Compliance: {weighted_compliance:.2f}%")
        
        if weighted_compliance >= 95:
            print("Overall Status: [EXCEEDS] EXCEEDS STANDARD")
        elif weighted_compliance >= 90:
            print("Overall Status: [MEETS] MEETS STANDARD")
        else:
            print("Overall Status: [WARNING] NEEDS IMPROVEMENT")

def service_level_performance(df):
    """Analyze performance by service level"""
    print("\n" + "="*60)
    print("SERVICE LEVEL PERFORMANCE BREAKDOWN")
    print("="*60)
    
    delivered_df = df[df['Delivered Status'] == 'Delivered']
    
    for service in ['Priority', 'Expedited', 'Ground']:
        service_df = delivered_df[delivered_df['Xparcel Type'] == service]
        
        if len(service_df) > 0:
            print(f"\n{service.upper()} SERVICE:")
            print("-"*30)
            
            # Volume
            print(f"Volume: {len(service_df):,} ({len(service_df)/len(delivered_df)*100:.1f}% of delivered)")
            
            # Transit distribution
            transit_dist = service_df['Days In Transit'].value_counts().sort_index().head(8)
            print(f"\nTransit Day Distribution:")
            for days, count in transit_dist.items():
                pct = (count / len(service_df)) * 100
                bar = '=' * int(pct/2)  # Visual bar
                print(f"  Day {days}: {count:,} ({pct:.1f}%) {bar}")

def zone_transit_analysis(df):
    """Analyze transit times by zone"""
    print("\n" + "="*60)
    print("ZONE-BASED TRANSIT ANALYSIS")
    print("="*60)
    
    delivered_df = df[df['Delivered Status'] == 'Delivered']
    
    if 'Calculated Zone' in delivered_df.columns:
        zone_stats = delivered_df.groupby('Calculated Zone').agg({
            'Days In Transit': ['mean', 'median', 'std', 'count']
        }).round(2)
        
        zone_stats.columns = ['Avg Transit', 'Median Transit', 'Std Dev', 'Volume']
        zone_stats = zone_stats.sort_index()
        
        print("\nTransit Performance by Zone:")
        print(zone_stats.to_string())
        
        # Regional vs Cross-Country
        regional = delivered_df[delivered_df['Calculated Zone'] <= 4]
        cross_country = delivered_df[delivered_df['Calculated Zone'] >= 5]
        
        print(f"\nRegional (Zones 1-4):")
        print(f"  Volume: {len(regional):,} ({len(regional)/len(delivered_df)*100:.1f}%)")
        print(f"  Avg Transit: {regional['Days In Transit'].mean():.2f} days")
        
        print(f"\nCross-Country (Zones 5-8):")
        print(f"  Volume: {len(cross_country):,} ({len(cross_country)/len(delivered_df)*100:.1f}%)")
        print(f"  Avg Transit: {cross_country['Days In Transit'].mean():.2f} days")

def main():
    """Run comprehensive transit analysis confirmation"""
    print("="*60)
    print("TRANSIT ANALYSIS CONFIRMATION")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Load data
    df = load_raw_data()
    
    # Run analyses
    data_quality_check(df)
    delivered_df = transit_time_analysis(df)
    sla_compliance_analysis(df)
    service_level_performance(df)
    zone_transit_analysis(df)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    
    return df

if __name__ == "__main__":
    df = main()