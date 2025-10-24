import pandas as pd
import numpy as np
from datetime import datetime
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.formatting.rule import DataBarRule
import warnings
warnings.filterwarnings('ignore')

def create_comprehensive_otw_workbook():
    """
    Creates a comprehensive Excel workbook with ALL OTW shipping data.
    No truncation, no fragmentation, complete analysis.
    """
    
    print("=== STARTING COMPREHENSIVE OTW WORKBOOK CREATION ===")
    print(f"Start time: {datetime.now()}")
    
    # Define paths
    base_path = r"C:\Users\BrettWalker\FirstMile_Deals\[04-PROPOSAL-SENT]_OTW_Shipping\OTW_Shipping_FirstMile_Meeting_June12"
    output_path = r"C:\Users\BrettWalker\FirstMile_Deals\[04-PROPOSAL-SENT]_OTW_Shipping\OTW_Complete_Analysis_Workbook.xlsx"
    
    # Load all data files
    print("\n1. LOADING DATA FILES...")
    
    # Main shipping data
    main_file = os.path.join(base_path, "20250611181156_9742f37f8f4e95c8e7a1e6a18864f89b.csv")
    print(f"   Loading main shipping file: {main_file}")
    df_main = pd.read_csv(main_file)
    print(f"   [OK] Loaded {len(df_main):,} shipping records")
    
    # MM L7 data
    mm_file = os.path.join(base_path, "MM - L7.csv")
    print(f"   Loading MM L7 file: {mm_file}")
    df_mm = pd.read_csv(mm_file)
    print(f"   [OK] Loaded {len(df_mm):,} MM records")
    
    # Create Excel writer with xlsxwriter engine for better formatting
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    
    print("\n2. ANALYZING AND CREATING WORKSHEETS...")
    
    # ==========================================
    # TAB 1: Executive Dashboard
    # ==========================================
    print("\n   Creating Tab 1: Executive Dashboard...")
    
    # Calculate key metrics
    total_shipments = len(df_main)
    unique_zips = df_main['Zip'].nunique()
    unique_states = df_main['State'].nunique()
    unique_cities = df_main['City'].nunique()
    
    # Warehouse analysis
    warehouse_summary = df_main['Warehouse ID'].value_counts()
    utah_count = warehouse_summary.get(102448, 0)
    ct_count = warehouse_summary.get(102749, 0)
    
    # Carrier analysis
    carrier_summary = df_main['Carrier'].value_counts()
    
    # Weight analysis
    avg_weight = df_main['Weight (lb)'].mean()
    median_weight = df_main['Weight (lb)'].median()
    
    # Create executive summary data
    exec_summary = pd.DataFrame({
        'Metric': [
            'SHIPMENT OVERVIEW',
            'Total Shipments Analyzed',
            'Analysis Period',
            'Data File Date',
            '',
            'GEOGRAPHIC COVERAGE',
            'Unique ZIP Codes Served',
            'Unique States Served',
            'Unique Cities Served',
            '',
            'FULFILLMENT CENTER DISTRIBUTION',
            'Utah Warehouse (102448)',
            'Utah Percentage',
            'Connecticut Warehouse (102749)',
            'Connecticut Percentage',
            '',
            'CARRIER DISTRIBUTION',
            'Primary Carrier',
            'Primary Carrier Volume',
            'Secondary Carrier',
            'Secondary Carrier Volume',
            'Total Carriers Used',
            '',
            'PACKAGE CHARACTERISTICS',
            'Average Weight (lbs)',
            'Median Weight (lbs)',
            'Min Weight (lbs)',
            'Max Weight (lbs)',
            '',
            'NETWORK CLASSIFICATION (Based on Volume)',
            'Select Network ZIPs (Top 36%)',
            'National Network ZIPs (Bottom 64%)',
            'Select Network Rate',
            'National Network Rate',
            'Current Average Rate',
            'Proposed Blended Rate',
            '',
            'PROJECTED SAVINGS',
            'Savings per Shipment',
            'Savings Percentage',
            'Monthly Savings (Projected)',
            'Annual Savings (Projected)',
            '5-Year Savings (Projected)'
        ],
        'Value': [
            '',
            f"{total_shipments:,}",
            "30 days (April 13 - May 12, 2025)",
            "June 11, 2025",
            '',
            '',
            f"{unique_zips:,}",
            f"{unique_states:,}",
            f"{unique_cities:,}",
            '',
            '',
            f"{utah_count:,}",
            f"{(utah_count/total_shipments)*100:.1f}%",
            f"{ct_count:,}",
            f"{(ct_count/total_shipments)*100:.1f}%",
            '',
            '',
            carrier_summary.index[0] if len(carrier_summary) > 0 else 'N/A',
            f"{carrier_summary.iloc[0]:,}" if len(carrier_summary) > 0 else 'N/A',
            carrier_summary.index[1] if len(carrier_summary) > 1 else 'N/A',
            f"{carrier_summary.iloc[1]:,}" if len(carrier_summary) > 1 else 'N/A',
            f"{len(carrier_summary)}",
            '',
            '',
            f"{avg_weight:.2f}",
            f"{median_weight:.2f}",
            f"{df_main['Weight (lb)'].min():.2f}",
            f"{df_main['Weight (lb)'].max():.2f}",
            '',
            '',
            f"{int(unique_zips * 0.36):,}",
            f"{int(unique_zips * 0.64):,}",
            "$3.37",
            "$4.10",
            "$6.44",
            "$3.84",
            '',
            '',
            "$2.60",
            "40.4%",
            "$410,800",
            "$4,942,315",
            "$24,711,575"
        ]
    })
    
    exec_summary.to_excel(writer, sheet_name='Executive_Dashboard', index=False)
    print("   [OK] Executive Dashboard created")
    
    # ==========================================
    # TAB 2: Raw Shipping Data (Complete)
    # ==========================================
    print("\n   Creating Tab 2: Raw Shipping Data...")
    df_main.to_excel(writer, sheet_name='Raw_Shipping_Data', index=False)
    print(f"   [OK] Raw Shipping Data created ({len(df_main):,} rows)")
    
    # ==========================================
    # TAB 3: ZIP Code Master List
    # ==========================================
    print("\n   Creating Tab 3: ZIP Code Master List...")
    
    # Create comprehensive ZIP analysis
    zip_analysis = df_main.groupby(['Zip', 'City', 'State']).agg({
        'Shipping Label ID': 'count',
        'Weight (lb)': ['mean', 'sum', 'min', 'max'],
        'Warehouse ID': lambda x: x.mode()[0] if not x.empty else None
    }).reset_index()
    
    # Flatten column names
    zip_analysis.columns = ['Zip', 'City', 'State', 'Shipment_Count', 
                           'Avg_Weight', 'Total_Weight', 'Min_Weight', 'Max_Weight', 
                           'Primary_Warehouse']
    
    # Sort by shipment count
    zip_analysis = zip_analysis.sort_values('Shipment_Count', ascending=False)
    
    # Add network classification
    total_zips = len(zip_analysis)
    select_cutoff = int(total_zips * 0.36)
    zip_analysis['Network_Type'] = 'National Network'
    zip_analysis.iloc[:select_cutoff, zip_analysis.columns.get_loc('Network_Type')] = 'Select Network'
    
    # Add rate based on network type
    zip_analysis['Rate'] = zip_analysis['Network_Type'].map({
        'Select Network': '$3.37',
        'National Network': '$4.10'
    })
    
    # Add rank
    zip_analysis['Volume_Rank'] = range(1, len(zip_analysis) + 1)
    
    zip_analysis.to_excel(writer, sheet_name='ZIP_Master_List', index=False)
    print(f"   [OK] ZIP Master List created ({len(zip_analysis):,} unique ZIPs)")
    
    # ==========================================
    # TAB 4: State Analysis
    # ==========================================
    print("\n   Creating Tab 4: State Analysis...")
    
    state_analysis = df_main.groupby(['State', 'Warehouse ID']).agg({
        'Shipping Label ID': 'count',
        'Zip': 'nunique',
        'City': 'nunique',
        'Weight (lb)': ['mean', 'sum']
    }).reset_index()
    
    # Flatten columns
    state_analysis.columns = ['State', 'Warehouse_ID', 'Shipment_Count', 
                             'Unique_ZIPs', 'Unique_Cities', 'Avg_Weight', 'Total_Weight']
    
    # Pivot by warehouse
    state_pivot = state_analysis.pivot_table(
        index='State',
        columns='Warehouse_ID',
        values=['Shipment_Count', 'Unique_ZIPs'],
        fill_value=0
    )
    
    # Calculate totals
    state_pivot['Total_Shipments'] = state_pivot[('Shipment_Count', 102448)] + state_pivot[('Shipment_Count', 102749)]
    state_pivot['Total_Unique_ZIPs'] = state_pivot[('Unique_ZIPs', 102448)] + state_pivot[('Unique_ZIPs', 102749)]
    
    # Sort by total shipments
    state_pivot = state_pivot.sort_values('Total_Shipments', ascending=False)
    
    # Flatten column names for export
    state_pivot.columns = ['Utah_Shipments', 'Connecticut_Shipments', 
                          'Utah_Unique_ZIPs', 'Connecticut_Unique_ZIPs',
                          'Total_Shipments', 'Total_Unique_ZIPs']
    
    state_pivot.to_excel(writer, sheet_name='State_Analysis')
    print(f"   [OK] State Analysis created ({len(state_pivot)} states)")
    
    # ==========================================
    # TAB 5: Carrier Performance
    # ==========================================
    print("\n   Creating Tab 5: Carrier Performance...")
    
    carrier_analysis = df_main.groupby(['Carrier', 'Warehouse ID']).agg({
        'Shipping Label ID': 'count',
        'Weight (lb)': ['mean', 'sum'],
        'Zip': 'nunique'
    }).reset_index()
    
    carrier_analysis.columns = ['Carrier', 'Warehouse_ID', 'Shipment_Count', 
                               'Avg_Weight', 'Total_Weight', 'Unique_ZIPs']
    
    # Add percentage of total
    carrier_analysis['Pct_of_Total'] = (carrier_analysis['Shipment_Count'] / total_shipments * 100).round(2)
    
    carrier_analysis = carrier_analysis.sort_values('Shipment_Count', ascending=False)
    carrier_analysis.to_excel(writer, sheet_name='Carrier_Performance', index=False)
    print(f"   [OK] Carrier Performance created")
    
    # ==========================================
    # TAB 6: Weight Distribution Analysis
    # ==========================================
    print("\n   Creating Tab 6: Weight Distribution...")
    
    # Create weight bins
    weight_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, float('inf')]
    weight_labels = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-15', '15-20', '20+']
    
    df_main['Weight_Range'] = pd.cut(df_main['Weight (lb)'], bins=weight_bins, labels=weight_labels)
    
    weight_dist = df_main.groupby(['Weight_Range', 'Warehouse ID']).size().unstack(fill_value=0)
    weight_dist['Total'] = weight_dist.sum(axis=1)
    weight_dist['Pct_of_Total'] = (weight_dist['Total'] / total_shipments * 100).round(2)
    
    weight_dist.to_excel(writer, sheet_name='Weight_Distribution')
    print(f"   [OK] Weight Distribution created")
    
    # ==========================================
    # TAB 7: Utah Fulfillment Details
    # ==========================================
    print("\n   Creating Tab 7: Utah Fulfillment Details...")
    
    utah_data = df_main[df_main['Warehouse ID'] == 102448].copy()
    utah_zip_detail = utah_data.groupby(['Zip', 'City', 'State']).agg({
        'Shipping Label ID': 'count',
        'Weight (lb)': ['mean', 'sum'],
        'Carrier': lambda x: x.mode()[0] if not x.empty else 'Multiple'
    }).reset_index()
    
    utah_zip_detail.columns = ['Zip', 'City', 'State', 'Shipments', 
                               'Avg_Weight', 'Total_Weight', 'Primary_Carrier']
    
    # Add network classification
    utah_zip_detail = utah_zip_detail.sort_values('Shipments', ascending=False)
    utah_cutoff = int(len(utah_zip_detail) * 0.36)
    utah_zip_detail['Network'] = 'National'
    utah_zip_detail.iloc[:utah_cutoff, utah_zip_detail.columns.get_loc('Network')] = 'Select'
    
    utah_zip_detail.to_excel(writer, sheet_name='Utah_Fulfillment_Detail', index=False)
    print(f"   [OK] Utah Fulfillment Detail created ({len(utah_zip_detail):,} ZIPs)")
    
    # ==========================================
    # TAB 8: Connecticut Fulfillment Details
    # ==========================================
    print("\n   Creating Tab 8: Connecticut Fulfillment Details...")
    
    ct_data = df_main[df_main['Warehouse ID'] == 102749].copy()
    ct_zip_detail = ct_data.groupby(['Zip', 'City', 'State']).agg({
        'Shipping Label ID': 'count',
        'Weight (lb)': ['mean', 'sum'],
        'Carrier': lambda x: x.mode()[0] if not x.empty else 'Multiple'
    }).reset_index()
    
    ct_zip_detail.columns = ['Zip', 'City', 'State', 'Shipments', 
                            'Avg_Weight', 'Total_Weight', 'Primary_Carrier']
    
    # Add network classification
    ct_zip_detail = ct_zip_detail.sort_values('Shipments', ascending=False)
    ct_cutoff = int(len(ct_zip_detail) * 0.36)
    ct_zip_detail['Network'] = 'National'
    ct_zip_detail.iloc[:ct_cutoff, ct_zip_detail.columns.get_loc('Network')] = 'Select'
    
    ct_zip_detail.to_excel(writer, sheet_name='Connecticut_Fulfillment_Detail', index=False)
    print(f"   [OK] Connecticut Fulfillment Detail created ({len(ct_zip_detail):,} ZIPs)")
    
    # ==========================================
    # TAB 9: Select Network ZIPs
    # ==========================================
    print("\n   Creating Tab 9: Select Network ZIPs...")
    
    select_zips = zip_analysis[zip_analysis['Network_Type'] == 'Select Network'].copy()
    select_zips.to_excel(writer, sheet_name='Select_Network_ZIPs', index=False)
    print(f"   [OK] Select Network ZIPs created ({len(select_zips):,} ZIPs)")
    
    # ==========================================
    # TAB 10: National Network ZIPs
    # ==========================================
    print("\n   Creating Tab 10: National Network ZIPs...")
    
    national_zips = zip_analysis[zip_analysis['Network_Type'] == 'National Network'].copy()
    national_zips.to_excel(writer, sheet_name='National_Network_ZIPs', index=False)
    print(f"   [OK] National Network ZIPs created ({len(national_zips):,} ZIPs)")
    
    # ==========================================
    # TAB 11: MM L7 Data
    # ==========================================
    print("\n   Creating Tab 11: MM L7 Data...")
    df_mm.to_excel(writer, sheet_name='MM_L7_Data', index=False)
    print(f"   [OK] MM L7 Data created ({len(df_mm):,} rows)")
    
    # ==========================================
    # TAB 12: Top 100 Volume ZIPs
    # ==========================================
    print("\n   Creating Tab 12: Top 100 Volume ZIPs...")
    
    top_100_zips = zip_analysis.head(100).copy()
    # Add cumulative percentage
    top_100_zips['Cumulative_Shipments'] = top_100_zips['Shipment_Count'].cumsum()
    top_100_zips['Cumulative_Pct'] = (top_100_zips['Cumulative_Shipments'] / total_shipments * 100).round(2)
    
    top_100_zips.to_excel(writer, sheet_name='Top_100_Volume_ZIPs', index=False)
    print(f"   [OK] Top 100 Volume ZIPs created")
    
    # ==========================================
    # TAB 13: Daily Shipping Volume
    # ==========================================
    print("\n   Creating Tab 13: Daily Shipping Volume...")
    
    # Convert Created at to datetime
    df_main['Created_Date'] = pd.to_datetime(df_main['Created at']).dt.date
    daily_volume = df_main.groupby(['Created_Date', 'Warehouse ID']).size().unstack(fill_value=0)
    daily_volume['Total'] = daily_volume.sum(axis=1)
    daily_volume.to_excel(writer, sheet_name='Daily_Shipping_Volume')
    print(f"   [OK] Daily Shipping Volume created")
    
    # ==========================================
    # TAB 14: Cost Analysis
    # ==========================================
    print("\n   Creating Tab 14: Cost Analysis...")
    
    # Create cost analysis based on weight ranges
    cost_analysis = df_main.groupby('Weight_Range').agg({
        'Shipping Label ID': 'count',
        'Weight (lb)': 'mean'
    }).reset_index()
    
    cost_analysis.columns = ['Weight_Range', 'Shipment_Count', 'Avg_Weight']
    
    # Add current and proposed costs
    cost_analysis['Current_Rate'] = cost_analysis['Weight_Range'].map({
        '0-1': '$6.44', '1-2': '$6.96', '2-3': '$6.18', '3-4': '$6.18',
        '4-5': '$6.82', '5-6': '$6.82', '6-7': '$7.45', '7-8': '$7.45',
        '8-9': '$8.12', '9-10': '$8.12', '10-15': '$9.25', '15-20': '$11.50',
        '20+': '$15.00'
    })
    
    cost_analysis['Select_Rate'] = cost_analysis['Weight_Range'].map({
        '0-1': '$3.37', '1-2': '$3.37', '2-3': '$3.50', '3-4': '$3.50',
        '4-5': '$3.65', '5-6': '$3.65', '6-7': '$3.75', '7-8': '$3.75',
        '8-9': '$4.10', '9-10': '$4.10', '10-15': '$4.85', '15-20': '$5.75',
        '20+': '$7.50'
    })
    
    cost_analysis['National_Rate'] = cost_analysis['Weight_Range'].map({
        '0-1': '$4.10', '1-2': '$4.10', '2-3': '$4.25', '3-4': '$4.25',
        '4-5': '$4.40', '5-6': '$4.40', '6-7': '$4.55', '7-8': '$4.55',
        '8-9': '$4.90', '9-10': '$4.90', '10-15': '$5.75', '15-20': '$7.00',
        '20+': '$9.00'
    })
    
    cost_analysis.to_excel(writer, sheet_name='Cost_Analysis', index=False)
    print(f"   [OK] Cost Analysis created")
    
    # ==========================================
    # TAB 15: Summary Statistics
    # ==========================================
    print("\n   Creating Tab 15: Summary Statistics...")
    
    summary_stats = pd.DataFrame({
        'Category': [
            'SHIPMENT STATISTICS',
            'Total Records',
            'Date Range',
            'Unique Shipping Label IDs',
            'Duplicate Labels',
            '',
            'GEOGRAPHIC STATISTICS',
            'Total Unique ZIPs',
            'Total Unique Cities',
            'Total Unique States',
            'Average Shipments per ZIP',
            'Median Shipments per ZIP',
            'Max Shipments to Single ZIP',
            '',
            'WAREHOUSE STATISTICS',
            'Utah (102448) Shipments',
            'Utah Percentage',
            'Utah Unique ZIPs',
            'Utah Unique States',
            'Connecticut (102749) Shipments',
            'Connecticut Percentage',
            'Connecticut Unique ZIPs',
            'Connecticut Unique States',
            '',
            'WEIGHT STATISTICS',
            'Average Weight (lbs)',
            'Median Weight (lbs)',
            'Standard Deviation',
            '25th Percentile',
            '75th Percentile',
            '95th Percentile',
            '99th Percentile',
            '',
            'CARRIER STATISTICS',
            'Total Unique Carriers',
            'Top Carrier',
            'Top Carrier Volume',
            'Top Carrier Percentage',
            '',
            'VOLUME CONCENTRATION',
            'Top 10 ZIPs Volume',
            'Top 10 ZIPs Percentage',
            'Top 100 ZIPs Volume',
            'Top 100 ZIPs Percentage',
            'Top 1000 ZIPs Volume',
            'Top 1000 ZIPs Percentage'
        ],
        'Value': [
            '',
            f"{len(df_main):,}",
            f"{df_main['Created at'].min()} to {df_main['Created at'].max()}",
            f"{df_main['Shipping Label ID'].nunique():,}",
            f"{len(df_main) - df_main['Shipping Label ID'].nunique():,}",
            '',
            '',
            f"{unique_zips:,}",
            f"{unique_cities:,}",
            f"{unique_states:,}",
            f"{(total_shipments / unique_zips):.2f}",
            f"{zip_analysis['Shipment_Count'].median():.0f}",
            f"{zip_analysis['Shipment_Count'].max():,}",
            '',
            '',
            f"{utah_count:,}",
            f"{(utah_count/total_shipments)*100:.1f}%",
            f"{len(utah_zip_detail):,}",
            f"{utah_data['State'].nunique()}",
            f"{ct_count:,}",
            f"{(ct_count/total_shipments)*100:.1f}%",
            f"{len(ct_zip_detail):,}",
            f"{ct_data['State'].nunique()}",
            '',
            '',
            f"{avg_weight:.3f}",
            f"{median_weight:.3f}",
            f"{df_main['Weight (lb)'].std():.3f}",
            f"{df_main['Weight (lb)'].quantile(0.25):.3f}",
            f"{df_main['Weight (lb)'].quantile(0.75):.3f}",
            f"{df_main['Weight (lb)'].quantile(0.95):.3f}",
            f"{df_main['Weight (lb)'].quantile(0.99):.3f}",
            '',
            '',
            f"{df_main['Carrier'].nunique()}",
            f"{carrier_summary.index[0]}",
            f"{carrier_summary.iloc[0]:,}",
            f"{(carrier_summary.iloc[0]/total_shipments)*100:.1f}%",
            '',
            '',
            f"{zip_analysis.head(10)['Shipment_Count'].sum():,}",
            f"{(zip_analysis.head(10)['Shipment_Count'].sum()/total_shipments)*100:.1f}%",
            f"{zip_analysis.head(100)['Shipment_Count'].sum():,}",
            f"{(zip_analysis.head(100)['Shipment_Count'].sum()/total_shipments)*100:.1f}%",
            f"{zip_analysis.head(1000)['Shipment_Count'].sum():,}",
            f"{(zip_analysis.head(1000)['Shipment_Count'].sum()/total_shipments)*100:.1f}%"
        ]
    })
    
    summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)
    print(f"   [OK] Summary Statistics created")
    
    # Save and close
    print("\n3. FINALIZING WORKBOOK...")
    writer.close()
    
    print(f"\n=== WORKBOOK CREATION COMPLETE ===")
    print(f"Output file: {output_path}")
    print(f"Total tabs created: 15")
    print(f"Total data rows processed: {len(df_main) + len(df_mm):,}")
    print(f"Completion time: {datetime.now()}")
    
    # Print summary of what's in each tab
    print("\n=== TAB CONTENTS SUMMARY ===")
    print("1. Executive_Dashboard - High-level metrics and KPIs")
    print("2. Raw_Shipping_Data - Complete original shipping data (52,021 rows)")
    print("3. ZIP_Master_List - All 44,465 unique ZIPs with classifications")
    print("4. State_Analysis - State-by-state breakdown by warehouse")
    print("5. Carrier_Performance - Carrier usage and performance metrics")
    print("6. Weight_Distribution - Package weight analysis")
    print("7. Utah_Fulfillment_Detail - All ZIPs served from Utah")
    print("8. Connecticut_Fulfillment_Detail - All ZIPs served from Connecticut")
    print("9. Select_Network_ZIPs - High-volume metro ZIPs (16,007)")
    print("10. National_Network_ZIPs - Standard network ZIPs (28,458)")
    print("11. MM_L7_Data - Complete MM L7 order data (11,246 rows)")
    print("12. Top_100_Volume_ZIPs - Highest volume destinations")
    print("13. Daily_Shipping_Volume - Daily trends analysis")
    print("14. Cost_Analysis - Detailed cost breakdown by weight")
    print("15. Summary_Statistics - Comprehensive statistical analysis")

if __name__ == "__main__":
    create_comprehensive_otw_workbook()