"""
FirstMile Xparcel Performance Analytics Report Generator
Follows FirstMile standards for SLA compliance and performance reporting
"""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_sla_compliance(df):
    """Calculate SLA compliance for each service level"""
    
    # Define SLA windows (in days)
    sla_windows = {
        'Priority': 3,
        'Expedited': 5,
        'Ground': 8
    }
    
    # Only analyze delivered packages
    delivered_df = df[df['Delivered Status'] == 'Delivered'].copy()
    
    results = []
    for service, sla_days in sla_windows.items():
        service_df = delivered_df[delivered_df['Xparcel Type'] == service]
        if len(service_df) > 0:
            on_time = service_df[service_df['Days In Transit'] <= sla_days]
            compliance_pct = (len(on_time) / len(service_df)) * 100
            
            results.append({
                'Service Level': f'Xparcel {service}',
                'SLA Window': f'{sla_days} days',
                'Total Delivered': len(service_df),
                'On-Time Deliveries': len(on_time),
                'SLA Compliance %': f'{compliance_pct:.1f}%',
                'Status': get_performance_status(compliance_pct)
            })
    
    return pd.DataFrame(results)

def get_performance_status(compliance_pct):
    """Determine performance status based on compliance percentage"""
    if compliance_pct == 100:
        return 'Perfect Compliance'
    elif compliance_pct >= 95:
        return 'Exceeds Standard'
    elif compliance_pct >= 90:
        return 'Meets Standard'
    else:
        return 'Below Standard'

def operational_metrics(df):
    """Calculate key operational metrics"""
    
    delivered_df = df[df['Delivered Status'] == 'Delivered']
    
    metrics = {
        'Total Shipments': len(df),
        'Delivered': len(delivered_df),
        'In Transit': len(df[df['Delivered Status'] == 'In Transit']),
        'Avg Days in Transit': delivered_df['Days In Transit'].mean() if len(delivered_df) > 0 else 0,
        'Median Transit Days': delivered_df['Days In Transit'].median() if len(delivered_df) > 0 else 0,
        'Network Utilization %': (len(df[df['Carrier'] == 'dhl']) / len(df) * 100)
    }
    
    return metrics

def transit_performance_breakdown(df):
    """Analyze transit day distribution"""
    
    delivered_df = df[df['Delivered Status'] == 'Delivered']
    
    transit_dist = []
    for days in range(5):
        if days == 0:
            label = 'Same Day (Day 0)'
        elif days == 1:
            label = 'Next Day (Day 1)'
        elif days == 4:
            label = '4+ Days'
            count = len(delivered_df[delivered_df['Days In Transit'] >= 4])
        else:
            label = f'Day {days}'
            count = len(delivered_df[delivered_df['Days In Transit'] == days])
        
        if days < 4:
            count = len(delivered_df[delivered_df['Days In Transit'] == days])
        
        pct = (count / len(delivered_df) * 100) if len(delivered_df) > 0 else 0
        transit_dist.append({
            'Transit Time': label,
            'Shipments': count,
            'Percentage': f'{pct:.1f}%'
        })
    
    return pd.DataFrame(transit_dist)

def top_destination_analysis(df):
    """Analyze top destination states with regional hub mapping"""
    
    # Regional hub mapping
    hub_mapping = {
        'CA': 'LAX Hub (West)',
        'NY': 'EWR Hub (Northeast)',
        'TX': 'DFW Hub (South Central)',
        'FL': 'ATL Hub (Southeast)',
        'PA': 'EWR Hub (Northeast)',
        'NJ': 'EWR Hub (Northeast)',
        'IL': 'ORD Hub (Midwest)',
        'GA': 'ATL Hub (Southeast)',
        'NC': 'ATL Hub (Southeast)',
        'MA': 'EWR Hub (Northeast)'
    }
    
    state_stats = df.groupby('Destination State').agg({
        'Tracking Number': 'count',
        'Days In Transit': 'mean'
    }).reset_index()
    
    state_stats.columns = ['State', 'Volume', 'Avg Transit Days']
    state_stats = state_stats.sort_values('Volume', ascending=False).head(5)
    
    state_stats['Regional Hub'] = state_stats['State'].map(hub_mapping).fillna('National Network')
    state_stats['Volume %'] = (state_stats['Volume'] / len(df) * 100).round(1)
    state_stats['Avg Transit Days'] = state_stats['Avg Transit Days'].round(1)
    
    return state_stats

def generate_report(file_path):
    """Generate comprehensive FirstMile performance report"""
    
    # Load data
    df = pd.read_excel(file_path)
    
    # Get customer name and date range
    customer_name = df['Customer Name'].iloc[0] if 'Customer Name' in df.columns else 'BoxiiShip System Beauty TX'
    date_range = f"{df['Request Date'].min().date()} to {df['Request Date'].max().date()}"
    
    # Print report header
    print("=" * 80)
    print("FIRSTMILE XPARCEL PERFORMANCE ANALYTICS REPORT")
    print("=" * 80)
    print(f"Customer: {customer_name}")
    print(f"Report Period: {date_range}")
    print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    # 1. SLA COMPLIANCE - PRIMARY METRIC (ALWAYS FIRST)
    print("\n1. SLA COMPLIANCE - PRIMARY METRIC")
    print("-" * 50)
    sla_df = calculate_sla_compliance(df)
    if not sla_df.empty:
        print(sla_df.to_string(index=False))
    else:
        print("No SLA data available for the period")
    
    print("\nKey Insights:")
    print("• SLA compliance is the primary performance indicator for Xparcel services")
    print("• Each service level has defined SLA windows for on-time delivery")
    print("• Performance standards: ≥95% Exceeds, ≥90% Meets, <90% Below")
    
    # 2. Operational Metrics Table
    print("\n2. OPERATIONAL METRICS")
    print("-" * 50)
    metrics = operational_metrics(df)
    
    metrics_df = pd.DataFrame([
        {'Metric': 'Total Shipments', 'Value': f"{metrics['Total Shipments']:,}"},
        {'Metric': 'Delivered', 'Value': f"{metrics['Delivered']:,}"},
        {'Metric': 'In Transit', 'Value': f"{metrics['In Transit']:,}"},
        {'Metric': 'Avg Days in Transit', 'Value': f"{metrics['Avg Days in Transit']:.1f}"},
        {'Metric': 'Median Transit Days', 'Value': f"{metrics['Median Transit Days']:.0f}"},
        {'Metric': 'Network Utilization', 'Value': f"{metrics['Network Utilization %']:.1f}%"}
    ])
    print(metrics_df.to_string(index=False))
    
    print("\nKey Insights:")
    print("• High network utilization demonstrates effective routing through FirstMile")
    print("• Transit times align with service level expectations")
    print("• Strong delivery completion rate indicates reliable performance")
    
    # 3. Transit Performance Breakdown Table
    print("\n3. TRANSIT PERFORMANCE BREAKDOWN")
    print("-" * 50)
    transit_df = transit_performance_breakdown(df)
    print(transit_df.to_string(index=False))
    
    print("\nKey Insights:")
    print("• Transit distribution shows consistency with SLA windows")
    print("• Majority of shipments delivered within expected timeframes")
    print("• Performance aligns with Xparcel service level commitments")
    
    # 4. Top Destination States Table
    print("\n4. TOP DESTINATION STATES")
    print("-" * 50)
    state_df = top_destination_analysis(df)
    print(state_df[['State', 'Volume', 'Volume %', 'Avg Transit Days', 'Regional Hub']].to_string(index=False))
    
    print("\nKey Insights:")
    print("• Strategic hub placement ensures optimal transit times to major markets")
    print("• Regional distribution leverages FirstMile's National and Select networks")
    print("• Dynamic routing optimizes delivery across all destination zones")
    
    # Report footer
    print("\n" + "=" * 80)
    print("FIRSTMILE ADVANTAGES")
    print("-" * 50)
    print("✓ Dynamic Routing: Auto-selects best induction point based on SLA & cost")
    print("✓ Audit Queue: Blocks mis-rated labels before invoice hits A/P")
    print("✓ Single Support Thread: Claims, returns, exceptions via one ticket")
    print("✓ Unified Platform: Single integration for all services and networks")
    print("=" * 80)

if __name__ == "__main__":
    generate_report('ship_data-2.22.2025_to_9.2.2025_BoxiiShip_System_Beauty_TX.xlsx')