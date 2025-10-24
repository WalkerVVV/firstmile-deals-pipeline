"""
SLA Performance Analysis by Xparcel Service Level
Shows what % of delivered packages met their respective SLA windows
"""

import pandas as pd

# Load data
DATA_FILE = r"C:\Users\BrettWalker\FirstMile_Deals\[07-CLOSED-WON]_JM_Group_NY\JM Group NY_FirstMile_Domestic_Tracking_9.30.25.xlsx"
df = pd.read_excel(DATA_FILE)

# SLA Windows
SLA_WINDOWS = {
    'Ground': 8,
    'Expedited': 5,
    'Direct Call': 3  # Priority
}

print("="*80)
print("SLA PERFORMANCE BY XPARCEL SERVICE LEVEL")
print("Delivered Packages Only - % Meeting Their Respective SLA Windows")
print("="*80)

# Filter for delivered only
delivered = df[df['Delivered Status'] == 'Delivered'].copy()

print(f"\nTotal Delivered Shipments: {len(delivered)}")
print(f"Total All Shipments: {len(df)}")
print(f"Delivery Rate: {(len(delivered)/len(df)*100):.1f}%")

# Group by Xparcel Type
if 'Xparcel Type' in delivered.columns:
    service_types = delivered['Xparcel Type'].unique()

    print("\n" + "="*80)
    print("SLA PERFORMANCE BREAKDOWN")
    print("="*80)

    results = []

    for service in sorted(service_types):
        service_df = delivered[delivered['Xparcel Type'] == service].copy()

        if service not in SLA_WINDOWS:
            print(f"\nWARNING: Unknown service type '{service}' - skipping")
            continue

        sla_window = SLA_WINDOWS[service]

        # Calculate SLA compliance
        within_sla = len(service_df[service_df['Days In Transit'] <= sla_window])
        total = len(service_df)
        compliance_pct = (within_sla / total * 100) if total > 0 else 0

        # Service name mapping
        service_name_map = {
            'Ground': 'Xparcel Ground',
            'Expedited': 'Xparcel Expedited',
            'Direct Call': 'Xparcel Priority'
        }

        service_name = service_name_map.get(service, service)

        results.append({
            'Service': service_name,
            'SLA Window': f'{sla_window} days',
            'Total Delivered': total,
            '% of Total': f'{(total/len(delivered)*100):.1f}%',
            'Within SLA': within_sla,
            'Outside SLA': total - within_sla,
            'SLA Compliance': f'{compliance_pct:.1f}%'
        })

        print(f"\n{service_name} ({sla_window}-day SLA)")
        print(f"  Total Delivered: {total}")
        print(f"  Within SLA: {within_sla}")
        print(f"  Outside SLA: {total - within_sla}")
        print(f"  SLA Compliance: {compliance_pct:.1f}%")

        # Transit day distribution
        print(f"\n  Transit Day Distribution:")
        for day in range(sla_window + 3):  # Show a few days beyond SLA
            count = len(service_df[service_df['Days In Transit'] == day])
            if count > 0:
                pct = (count / total * 100)
                cumulative = len(service_df[service_df['Days In Transit'] <= day])
                cum_pct = (cumulative / total * 100)
                sla_marker = " [WITHIN]" if day <= sla_window else " [OUTSIDE]"
                print(f"    Day {day}: {count:4d} ({pct:5.1f}%) | Cumulative: {cumulative:4d} ({cum_pct:5.1f}%){sla_marker}")

        # Statistics
        avg_transit = service_df['Days In Transit'].mean()
        median_transit = service_df['Days In Transit'].median()
        p90_transit = service_df['Days In Transit'].quantile(0.90)
        p95_transit = service_df['Days In Transit'].quantile(0.95)

        print(f"\n  Statistics:")
        print(f"    Average: {avg_transit:.1f} days")
        print(f"    Median: {median_transit:.1f} days")
        print(f"    90th Percentile: {p90_transit:.1f} days")
        print(f"    95th Percentile: {p95_transit:.1f} days")

    # Summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    # Overall performance
    print("\n" + "="*80)
    print("OVERALL PERFORMANCE")
    print("="*80)

    total_within_sla = sum([r['Within SLA'] for r in results])
    total_delivered = len(delivered)
    overall_compliance = (total_within_sla / total_delivered * 100) if total_delivered > 0 else 0

    print(f"\nTotal Delivered: {total_delivered}")
    print(f"Total Within SLA: {total_within_sla}")
    print(f"Overall SLA Compliance: {overall_compliance:.1f}%")

    # Performance status
    if overall_compliance >= 100.0:
        status = "Perfect Compliance"
    elif overall_compliance >= 95.0:
        status = "Exceeds Standard"
    elif overall_compliance >= 90.0:
        status = "Meets Standard"
    else:
        status = "Below Standard"

    print(f"Performance Status: {status}")

else:
    print("\nERROR: 'Xparcel Type' column not found in data")

print("\n" + "="*80)
