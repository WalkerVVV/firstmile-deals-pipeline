import pandas as pd
import numpy as np
import os

def examine_rate_sheets():
    """Examine the structure of FirstMile rate sheets to understand how to parse them"""
    
    base_path = r"C:\Users\BrettWalker\FirstMile_Deals\[04-PROPOSAL-SENT]_OTW_Shipping"
    utah_rates_path = os.path.join(base_path, "OTW Shipping - UT_FirstMile_Xparcel_07-15-25.xlsx")
    ct_rates_path = os.path.join(base_path, "OTW Shipping - CT_FirstMile_Xparcel_07-15-25.xlsx")
    
    print("=== EXAMINING FIRSTMILE RATE SHEET STRUCTURE ===\n")
    
    # Load Utah rate sheets
    print("1. UTAH RATE SHEETS:")
    utah_sheets = pd.read_excel(utah_rates_path, sheet_name=None)
    
    # Examine Expedited sheet
    print("\n   Xparcel Expedited SLT_NATL Sheet:")
    expedited = utah_sheets['Xparcel Expedited SLT_NATL']
    print(f"   Shape: {expedited.shape}")
    print("\n   First 20 rows preview:")
    print(expedited.head(20).to_string())
    
    # Examine Ground sheet
    print("\n\n   Xparcel Ground SLT_NATL Sheet:")
    ground = utah_sheets['Xparcel Ground SLT_NATL']
    print(f"   Shape: {ground.shape}")
    print("\n   First 20 rows preview:")
    print(ground.head(20).to_string())
    
    # Save samples for manual inspection
    with pd.ExcelWriter(os.path.join(base_path, 'Rate_Sheet_Samples.xlsx')) as writer:
        expedited.head(30).to_excel(writer, sheet_name='Utah_Expedited_Sample', index=False)
        ground.head(30).to_excel(writer, sheet_name='Utah_Ground_Sample', index=False)
        
        # Also check Connecticut
        ct_sheets = pd.read_excel(ct_rates_path, sheet_name=None)
        ct_expedited = ct_sheets['Xparcel Expedited SLT_NATL']
        ct_expedited.head(30).to_excel(writer, sheet_name='CT_Expedited_Sample', index=False)
    
    print("\n\nRate sheet samples saved to: Rate_Sheet_Samples.xlsx")
    print("Please review to understand the structure for proper parsing.")

if __name__ == "__main__":
    examine_rate_sheets()