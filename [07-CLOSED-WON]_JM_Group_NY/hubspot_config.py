"""
HubSpot Configuration and Upload Execution
For FirstMile Xparcel Performance Reports
"""

import os
from hubspot_upload import upload_report_to_hubspot

# Configuration
HUBSPOT_CONFIG = {
    # Get your Private App token from HubSpot:
    # Settings > Integrations > Private Apps > Create/Select App > Access Token
    "api_key": os.getenv("HUBSPOT_API_KEY"),  # Store in environment variable for security

    # Company mapping (FirstMile customer name -> HubSpot company name)
    "company_mapping": {
        "JM Group of NY": "JM Group",
        "JM Group": "JM Group",
        # Add more mappings as needed
    },

    # Deal naming convention
    "deal_naming": {
        "prefix": "FirstMile Migration - ",
        "suffix": " - Xparcel"
    },

    # File organization in HubSpot
    "folder_structure": {
        "root": "FirstMile Reports",
        "by_year": True,  # Creates /FirstMile Reports/2025/
        "by_customer": True  # Creates /FirstMile Reports/2025/JM Group/
    }
}

def upload_latest_report():
    """
    Upload the most recent JM Group report to HubSpot
    """
    # Find the latest report
    import glob
    import os

    pattern = "FirstMile_Xparcel_Performance_JM_Group_of_NY_*.xlsx"
    files = glob.glob(pattern)

    if not files:
        print("[ERROR] No report files found")
        return

    # Get the most recent file
    latest_file = max(files, key=os.path.getctime)
    print(f"[FOUND] Latest report: {latest_file}")

    # Check if API key is configured
    if not HUBSPOT_CONFIG["api_key"]:
        print("""
        ========================================================================
                        HUBSPOT API KEY REQUIRED
        ========================================================================

        To upload reports to HubSpot, you need to:

        1. Create a Private App in HubSpot:
           - Go to Settings > Integrations > Private Apps
           - Click "Create a private app"
           - Name it "FirstMile Report Integration"
           - In Scopes tab, select:
             ✓ crm.objects.companies.read
             ✓ crm.objects.companies.write
             ✓ crm.objects.deals.read
             ✓ crm.objects.deals.write
             ✓ crm.objects.contacts.read
             ✓ files
           - Create the app and copy the Access Token

        2. Set the environment variable:
           Windows (Command Prompt):
           set HUBSPOT_API_KEY=your-token-here

           Windows (PowerShell):
           $env:HUBSPOT_API_KEY="your-token-here"

           Or add to this file directly (not recommended for production):
           HUBSPOT_CONFIG["api_key"] = "your-token-here"

        3. Run this script again

        ========================================================================
        """)
        return

    # Upload the report
    result = upload_report_to_hubspot(
        report_path=latest_file,
        company_name="JM Group",
        deal_name="JM Group - FirstMile Migration",
        api_key=HUBSPOT_CONFIG["api_key"]
    )

    if result["success"]:
        print("""
        ========================================================================
                        SUCCESSFULLY UPLOADED TO HUBSPOT
        ========================================================================

        ✅ Report uploaded to HubSpot Files
        ✅ Attached to JM Group company record
        ✅ Note created with report details
        ✅ Engagement task marked complete

        View in HubSpot:
        - Companies > JM Group > Notes & Activities
        - Files & Templates > FirstMile Reports

        ========================================================================
        """)
    else:
        print(f"\n[ERROR] Upload failed: {result.get('error')}")

def batch_upload_reports(directory: str = "."):
    """
    Upload multiple reports to HubSpot

    Args:
        directory: Directory containing report files
    """
    import glob

    pattern = os.path.join(directory, "FirstMile_Xparcel_Performance_*.xlsx")
    files = glob.glob(pattern)

    print(f"[FOUND] {len(files)} report files")

    for file_path in files:
        # Extract customer name from filename
        filename = os.path.basename(file_path)
        # Pattern: FirstMile_Xparcel_Performance_{Customer}_{timestamp}.xlsx

        parts = filename.replace("FirstMile_Xparcel_Performance_", "").replace(".xlsx", "").rsplit("_", 2)
        if parts:
            customer_name = parts[0].replace("_", " ")

            # Look up HubSpot company name
            hubspot_company = HUBSPOT_CONFIG["company_mapping"].get(
                customer_name, customer_name
            )

            print(f"\n[UPLOADING] {filename}")
            print(f"[CUSTOMER] {customer_name} -> {hubspot_company}")

            result = upload_report_to_hubspot(
                report_path=file_path,
                company_name=hubspot_company,
                api_key=HUBSPOT_CONFIG["api_key"]
            )

            if result["success"]:
                print(f"[SUCCESS] ✅ Uploaded to HubSpot")
            else:
                print(f"[FAILED] ❌ {result.get('error')}")

if __name__ == "__main__":
    # Upload the latest JM Group report
    upload_latest_report()

    # Uncomment to batch upload all reports in directory
    # batch_upload_reports()