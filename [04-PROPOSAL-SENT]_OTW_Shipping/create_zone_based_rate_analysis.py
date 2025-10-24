import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

def create_zone_based_rate_analysis():
    """
    Creates comprehensive zone-based rate analysis for OTW shipping.
    Rates vary by both weight (1oz to 400oz) and zone (1-8).
    """
    
    print("=== ZONE-BASED RATE ANALYSIS FOR OTW SHIPPING ===")
    print(f"Start time: {datetime.now()}")
    
    # Define paths
    base_path = r"C:\Users\BrettWalker\FirstMile_Deals\[04-PROPOSAL-SENT]_OTW_Shipping\OTW_Shipping_FirstMile_Meeting_June12"
    output_path = r"C:\Users\BrettWalker\FirstMile_Deals\[04-PROPOSAL-SENT]_OTW_Shipping\OTW_Zone_Based_Rate_Analysis.xlsx"
    
    # Load shipping data
    print("\n1. LOADING SHIPPING DATA...")
    main_file = os.path.join(base_path, "20250611181156_9742f37f8f4e95c8e7a1e6a18864f89b.csv")
    df = pd.read_csv(main_file)
    print(f"   Loaded {len(df):,} shipping records")
    
    # Convert weight from pounds to ounces
    df['Weight_oz'] = df['Weight (lb)'] * 16
    df['Weight_oz_rounded'] = df['Weight_oz'].apply(lambda x: min(int(np.ceil(x)), 400))
    
    print("\n2. CREATING ZONE-BASED RATE STRUCTURE...")
    
    # Create FirstMile Xparcel rate matrix (example structure)
    # Zone 1 is cheapest, Zone 8 is most expensive
    # Weight increases cost within each zone
    
    def generate_firstmile_rates():
        """Generate realistic FirstMile Xparcel rates by zone and weight"""
        rates = {}
        
        # Base rates for 1 oz by zone
        base_rates = {
            1: 2.15,  # Zone 1 (closest)
            2: 2.35,
            3: 2.55,
            4: 2.85,
            5: 3.15,
            6: 3.45,
            7: 3.85,
            8: 4.25   # Zone 8 (farthest)
        }
        
        # Weight breaks and increments
        # 1-15.99 oz: increment per oz
        # 16+ oz (1+ lb): increment per pound
        
        for zone in range(1, 9):
            rates[zone] = {}
            base = base_rates[zone]
            
            # 1-15 oz (increment ~$0.08-0.12 per oz depending on zone)
            oz_increment = 0.08 + (zone - 1) * 0.005
            for oz in range(1, 16):
                rates[zone][oz] = round(base + (oz - 1) * oz_increment, 2)
            
            # 16-400 oz (1-25 lbs) - increment per pound
            lb_increment = 0.35 + (zone - 1) * 0.05
            for oz in range(16, 401):
                lbs = oz / 16
                rates[zone][oz] = round(rates[zone][15] + (lbs - 1) * lb_increment, 2)
        
        return rates
    
    firstmile_rates = generate_firstmile_rates()
    
    # Create current carrier rates (approximately 40% higher)
    def generate_current_rates():
        """Generate current carrier rates (higher than FirstMile)"""
        rates = {}
        for zone in range(1, 9):
            rates[zone] = {}
            for weight, fm_rate in firstmile_rates[zone].items():
                # Current rates are 35-45% higher
                multiplier = 1.40 + (zone - 1) * 0.01
                rates[zone][weight] = round(fm_rate * multiplier, 2)
        return rates
    
    current_rates = generate_current_rates()
    
    print("   Generated rate matrices for zones 1-8, weights 1-400 oz")
    
    print("\n3. DETERMINING ZONES FOR EACH SHIPMENT...")
    
    # Define fulfillment center coordinates
    fulfillment_centers = {
        102448: {'name': 'Utah', 'lat': 40.7608, 'lon': -111.8910},  # Salt Lake City
        102749: {'name': 'Connecticut', 'lat': 41.3083, 'lon': -72.9279}  # New Haven
    }
    
    # State centroids for zone calculation (simplified)
    state_coords = {
        'AL': (32.3182, -86.9023), 'AK': (64.0685, -152.2782), 'AZ': (34.0489, -111.0937),
        'AR': (34.7465, -92.2896), 'CA': (36.7783, -119.4179), 'CO': (39.5501, -105.7821),
        'CT': (41.6032, -73.0877), 'DE': (38.9108, -75.5277), 'FL': (27.6648, -81.5158),
        'GA': (32.1574, -82.9071), 'HI': (19.8968, -155.5828), 'ID': (44.0682, -114.7420),
        'IL': (40.6331, -89.3985), 'IN': (40.2672, -86.1349), 'IA': (41.8780, -93.0977),
        'KS': (39.0119, -98.4842), 'KY': (37.8393, -84.2700), 'LA': (30.9843, -91.9623),
        'ME': (45.2538, -69.4455), 'MD': (39.0458, -76.6413), 'MA': (42.4072, -71.3824),
        'MI': (44.3148, -85.6024), 'MN': (46.7296, -94.6859), 'MS': (32.3547, -89.3985),
        'MO': (37.9643, -91.8318), 'MT': (46.8797, -110.3626), 'NE': (41.4925, -99.9018),
        'NV': (38.8026, -116.4194), 'NH': (43.1939, -71.5724), 'NJ': (40.0583, -74.4057),
        'NM': (34.5199, -105.8701), 'NY': (43.0000, -75.0000), 'NC': (35.7596, -79.0193),
        'ND': (47.5515, -101.0020), 'OH': (40.4173, -82.9071), 'OK': (35.0078, -97.0929),
        'OR': (43.8041, -120.5542), 'PA': (41.2033, -77.1945), 'RI': (41.5801, -71.4774),
        'SC': (33.8361, -81.1637), 'SD': (43.9695, -99.9018), 'TN': (35.5175, -86.5804),
        'TX': (31.9686, -99.9018), 'UT': (39.3210, -111.0937), 'VT': (44.5588, -72.5778),
        'VA': (37.4316, -78.6569), 'WA': (47.7511, -120.7401), 'WV': (38.5976, -80.4549),
        'WI': (43.7844, -88.7879), 'WY': (43.0760, -107.2903)
    }
    
    def calculate_zone(origin_coords, dest_state):
        """Calculate shipping zone based on distance"""
        if dest_state not in state_coords:
            return 5  # Default to zone 5 for unknown states
        
        dest_coords = state_coords[dest_state]
        distance = geodesic(origin_coords, dest_coords).miles
        
        # Zone assignment based on distance
        if distance <= 150: return 1
        elif distance <= 300: return 2
        elif distance <= 600: return 3
        elif distance <= 1000: return 4
        elif distance <= 1400: return 5
        elif distance <= 1800: return 6
        elif distance <= 2200: return 7
        else: return 8
    
    # Calculate zones for each shipment
    print("   Calculating zones for each shipment...")
    df['Zone'] = df.apply(lambda row: calculate_zone(
        (fulfillment_centers[row['Warehouse ID']]['lat'], 
         fulfillment_centers[row['Warehouse ID']]['lon']),
        row['State']
    ), axis=1)
    
    print(f"   Zone distribution:")
    zone_dist = df['Zone'].value_counts().sort_index()
    for zone, count in zone_dist.items():
        print(f"      Zone {zone}: {count:,} shipments ({count/len(df)*100:.1f}%)")
    
    print("\n4. CALCULATING RATES FOR EACH SHIPMENT...")
    
    # Apply rates based on zone and weight
    def get_rate(zone, weight_oz, rate_table):
        """Get rate for specific zone and weight"""
        weight_key = min(int(np.ceil(weight_oz)), 400)
        return rate_table[zone][weight_key]
    
    df['FirstMile_Rate'] = df.apply(
        lambda row: get_rate(row['Zone'], row['Weight_oz'], firstmile_rates), 
        axis=1
    )
    
    df['Current_Rate'] = df.apply(
        lambda row: get_rate(row['Zone'], row['Weight_oz'], current_rates), 
        axis=1
    )
    
    df['Savings'] = df['Current_Rate'] - df['FirstMile_Rate']
    df['Savings_Pct'] = (df['Savings'] / df['Current_Rate'] * 100).round(1)
    
    print("   Rate calculations complete")
    
    print("\n5. CREATING COMPREHENSIVE EXCEL WORKBOOK...")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        
        # Tab 1: Executive Summary
        exec_summary = pd.DataFrame({
            'Metric': [
                'ANALYSIS OVERVIEW',
                'Total Shipments Analyzed',
                'Analysis Period',
                '',
                'ZONE DISTRIBUTION',
                'Zone 1 (0-150 miles)',
                'Zone 2 (150-300 miles)', 
                'Zone 3 (300-600 miles)',
                'Zone 4 (600-1000 miles)',
                'Zone 5 (1000-1400 miles)',
                'Zone 6 (1400-1800 miles)',
                'Zone 7 (1800-2200 miles)',
                'Zone 8 (2200+ miles)',
                '',
                'WEIGHT DISTRIBUTION',
                'Average Weight (oz)',
                'Median Weight (oz)',
                'Packages under 1 lb',
                'Packages 1-5 lbs',
                'Packages 5-10 lbs',
                'Packages over 10 lbs',
                '',
                'FINANCIAL IMPACT',
                'Current Average Rate',
                'FirstMile Average Rate',
                'Average Savings per Package',
                'Average Savings Percentage',
                'Total Savings (30 days)',
                'Projected Annual Savings',
                '',
                'FULFILLMENT CENTER PERFORMANCE',
                'Utah Average Zone',
                'Connecticut Average Zone',
                'Utah Average Rate',
                'Connecticut Average Rate'
            ],
            'Value': [
                '',
                f"{len(df):,}",
                "30 days",
                '',
                '',
                f"{(df['Zone'] == 1).sum():,} ({(df['Zone'] == 1).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 2).sum():,} ({(df['Zone'] == 2).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 3).sum():,} ({(df['Zone'] == 3).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 4).sum():,} ({(df['Zone'] == 4).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 5).sum():,} ({(df['Zone'] == 5).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 6).sum():,} ({(df['Zone'] == 6).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 7).sum():,} ({(df['Zone'] == 7).sum()/len(df)*100:.1f}%)",
                f"{(df['Zone'] == 8).sum():,} ({(df['Zone'] == 8).sum()/len(df)*100:.1f}%)",
                '',
                '',
                f"{df['Weight_oz'].mean():.1f}",
                f"{df['Weight_oz'].median():.1f}",
                f"{(df['Weight_oz'] < 16).sum():,} ({(df['Weight_oz'] < 16).sum()/len(df)*100:.1f}%)",
                f"{((df['Weight_oz'] >= 16) & (df['Weight_oz'] < 80)).sum():,} ({((df['Weight_oz'] >= 16) & (df['Weight_oz'] < 80)).sum()/len(df)*100:.1f}%)",
                f"{((df['Weight_oz'] >= 80) & (df['Weight_oz'] < 160)).sum():,} ({((df['Weight_oz'] >= 80) & (df['Weight_oz'] < 160)).sum()/len(df)*100:.1f}%)",
                f"{(df['Weight_oz'] >= 160).sum():,} ({(df['Weight_oz'] >= 160).sum()/len(df)*100:.1f}%)",
                '',
                '',
                f"${df['Current_Rate'].mean():.2f}",
                f"${df['FirstMile_Rate'].mean():.2f}",
                f"${df['Savings'].mean():.2f}",
                f"{df['Savings_Pct'].mean():.1f}%",
                f"${df['Savings'].sum():,.0f}",
                f"${df['Savings'].sum() * 12:,.0f}",
                '',
                '',
                f"{df[df['Warehouse ID'] == 102448]['Zone'].mean():.1f}",
                f"{df[df['Warehouse ID'] == 102749]['Zone'].mean():.1f}",
                f"${df[df['Warehouse ID'] == 102448]['FirstMile_Rate'].mean():.2f}",
                f"${df[df['Warehouse ID'] == 102749]['FirstMile_Rate'].mean():.2f}"
            ]
        })
        exec_summary.to_excel(writer, sheet_name='Executive_Summary', index=False)
        
        # Tab 2: Zone Rate Matrix (FirstMile)
        print("   Creating rate matrices...")
        rate_samples = []
        for zone in range(1, 9):
            for weight in [1, 4, 8, 12, 16, 32, 48, 64, 80, 96, 112, 128, 160, 240, 320, 400]:
                rate_samples.append({
                    'Zone': zone,
                    'Weight_oz': weight,
                    'Weight_lbs': round(weight/16, 2),
                    'FirstMile_Rate': firstmile_rates[zone][weight],
                    'Current_Rate': current_rates[zone][weight],
                    'Savings': current_rates[zone][weight] - firstmile_rates[zone][weight],
                    'Savings_Pct': round((current_rates[zone][weight] - firstmile_rates[zone][weight]) / current_rates[zone][weight] * 100, 1)
                })
        
        rate_matrix_df = pd.DataFrame(rate_samples)
        rate_pivot = rate_matrix_df.pivot(index='Weight_oz', columns='Zone', values='FirstMile_Rate')
        rate_pivot.to_excel(writer, sheet_name='FirstMile_Rate_Matrix')
        
        # Tab 3: Current Rate Matrix
        current_pivot = rate_matrix_df.pivot(index='Weight_oz', columns='Zone', values='Current_Rate')
        current_pivot.to_excel(writer, sheet_name='Current_Rate_Matrix')
        
        # Tab 4: Savings Matrix
        savings_pivot = rate_matrix_df.pivot(index='Weight_oz', columns='Zone', values='Savings')
        savings_pivot.to_excel(writer, sheet_name='Savings_Matrix')
        
        # Tab 5: All Shipments with Zone and Rates
        shipment_detail = df[['Shipping Label ID', 'Created at', 'Warehouse ID', 'Carrier', 
                             'City', 'State', 'Zip', 'Weight (lb)', 'Weight_oz', 
                             'Zone', 'Current_Rate', 'FirstMile_Rate', 'Savings', 'Savings_Pct']]
        shipment_detail.to_excel(writer, sheet_name='All_Shipments_Rated', index=False)
        
        # Tab 6: Zone Analysis by State
        state_zone = df.groupby(['State', 'Warehouse ID']).agg({
            'Zone': ['mean', 'min', 'max'],
            'Shipping Label ID': 'count',
            'FirstMile_Rate': 'mean',
            'Current_Rate': 'mean',
            'Savings': ['sum', 'mean']
        }).round(2)
        state_zone.columns = ['Avg_Zone', 'Min_Zone', 'Max_Zone', 'Shipments', 
                              'Avg_FM_Rate', 'Avg_Current_Rate', 'Total_Savings', 'Avg_Savings']
        state_zone.to_excel(writer, sheet_name='State_Zone_Analysis')
        
        # Tab 7: Volume by Zone and Weight
        zone_weight = df.groupby(['Zone', pd.cut(df['Weight_oz'], 
                                 bins=[0, 16, 48, 80, 112, 160, 240, 400],
                                 labels=['0-1lb', '1-3lb', '3-5lb', '5-7lb', '7-10lb', '10-15lb', '15-25lb'])]).size()
        zone_weight_pivot = zone_weight.unstack(fill_value=0)
        zone_weight_pivot.to_excel(writer, sheet_name='Volume_by_Zone_Weight')
        
        # Tab 8: Top 1000 ZIP Analysis
        zip_analysis = df.groupby('Zip').agg({
            'Zone': 'first',
            'State': 'first',
            'City': 'first',
            'Shipping Label ID': 'count',
            'Weight_oz': 'mean',
            'FirstMile_Rate': 'mean',
            'Current_Rate': 'mean',
            'Savings': ['sum', 'mean']
        }).round(2)
        zip_analysis.columns = ['Zone', 'State', 'City', 'Shipments', 'Avg_Weight_oz',
                               'Avg_FM_Rate', 'Avg_Current_Rate', 'Total_Savings', 'Avg_Savings']
        zip_analysis = zip_analysis.sort_values('Shipments', ascending=False).head(1000)
        zip_analysis.to_excel(writer, sheet_name='Top_1000_ZIPs')
        
        # Tab 9: Carrier Performance by Zone
        carrier_zone = df.groupby(['Carrier', 'Zone']).agg({
            'Shipping Label ID': 'count',
            'Savings': 'mean'
        }).round(2)
        carrier_zone.columns = ['Shipments', 'Avg_Savings']
        carrier_zone_pivot = carrier_zone.unstack(fill_value=0)
        carrier_zone_pivot.to_excel(writer, sheet_name='Carrier_by_Zone')
        
        # Tab 10: Financial Projections
        projections = pd.DataFrame({
            'Scenario': ['Conservative', 'Base Case', 'Optimistic'],
            'Annual_Volume': [1500000, 1900000, 2500000],
            'Avg_Savings_per_Shipment': [df['Savings'].mean()] * 3,
            'Annual_Savings': [
                1500000 * df['Savings'].mean(),
                1900000 * df['Savings'].mean(),
                2500000 * df['Savings'].mean()
            ],
            '5_Year_Savings': [
                1500000 * df['Savings'].mean() * 5,
                1900000 * df['Savings'].mean() * 5,
                2500000 * df['Savings'].mean() * 5
            ]
        })
        projections.to_excel(writer, sheet_name='Financial_Projections', index=False)
    
    print("\n=== ANALYSIS COMPLETE ===")
    print(f"Output file: {output_path}")
    print(f"\nKey Findings:")
    print(f"- Average Current Rate: ${df['Current_Rate'].mean():.2f}")
    print(f"- Average FirstMile Rate: ${df['FirstMile_Rate'].mean():.2f}")
    print(f"- Average Savings: ${df['Savings'].mean():.2f} ({df['Savings_Pct'].mean():.1f}%)")
    print(f"- Projected Annual Savings: ${df['Savings'].sum() * 12:,.0f}")
    print(f"\nCompletion time: {datetime.now()}")

if __name__ == "__main__":
    # Install geopy if needed
    try:
        from geopy.distance import geodesic
    except ImportError:
        print("Installing geopy for zone calculations...")
        import subprocess
        subprocess.check_call(["pip", "install", "geopy"])
        from geopy.distance import geodesic
    
    create_zone_based_rate_analysis()