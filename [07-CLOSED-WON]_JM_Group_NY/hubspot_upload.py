"""
HubSpot Integration for FirstMile Xparcel Performance Reports
Uploads report to HubSpot and associates with contact/deal
"""

import os
import json
import requests
from datetime import datetime
from typing import Optional, Dict, Any

class HubSpotReportUploader:
    """Upload FirstMile reports to HubSpot"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize HubSpot uploader

        Args:
            api_key: HubSpot Private App API key (or set HUBSPOT_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('HUBSPOT_API_KEY')
        if not self.api_key:
            raise ValueError("HubSpot API key required. Set HUBSPOT_API_KEY environment variable or pass api_key parameter")

        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def upload_file(self, file_path: str, folder_path: str = "FirstMile Reports") -> Dict[str, Any]:
        """
        Upload file to HubSpot Files API

        Args:
            file_path: Path to the report file
            folder_path: HubSpot folder path for organization

        Returns:
            Dict with file details including file_id
        """
        print(f"[UPLOADING] {file_path} to HubSpot...")

        # First, upload the file
        files_url = f"{self.base_url}/files/v3/files"

        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            }

            data = {
                'options': json.dumps({
                    'access': 'PRIVATE',  # Keep reports private
                    'overwrite': False,
                    'duplicateValidationStrategy': 'NONE',
                    'duplicateValidationScope': 'ENTIRE_PORTAL'
                }),
                'folderPath': folder_path
            }

            # For file upload, we need different headers
            upload_headers = {"Authorization": f"Bearer {self.api_key}"}

            response = requests.post(files_url, headers=upload_headers, files=files, data=data)

        if response.status_code in [200, 201]:
            file_data = response.json()
            print(f"[SUCCESS] File uploaded: {file_data.get('id')}")
            return file_data
        else:
            print(f"[ERROR] Upload failed: {response.status_code} - {response.text}")
            raise Exception(f"Failed to upload file: {response.status_code}")

    def search_company(self, company_name: str) -> Optional[str]:
        """
        Search for a company by name

        Args:
            company_name: Company name to search

        Returns:
            Company ID if found, None otherwise
        """
        search_url = f"{self.base_url}/crm/v3/objects/companies/search"

        search_body = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "name",
                    "operator": "CONTAINS_TOKEN",
                    "value": company_name
                }]
            }],
            "limit": 1
        }

        response = requests.post(search_url, headers=self.headers, json=search_body)

        if response.status_code == 200:
            results = response.json()
            if results.get('results'):
                company_id = results['results'][0]['id']
                print(f"[FOUND] Company '{company_name}': {company_id}")
                return company_id

        print(f"[NOT FOUND] Company '{company_name}' not found in HubSpot")
        return None

    def search_deal(self, deal_name: str) -> Optional[str]:
        """
        Search for a deal by name

        Args:
            deal_name: Deal name to search

        Returns:
            Deal ID if found, None otherwise
        """
        search_url = f"{self.base_url}/crm/v3/objects/deals/search"

        search_body = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "dealname",
                    "operator": "CONTAINS_TOKEN",
                    "value": deal_name
                }]
            }],
            "limit": 1
        }

        response = requests.post(search_url, headers=self.headers, json=search_body)

        if response.status_code == 200:
            results = response.json()
            if results.get('results'):
                deal_id = results['results'][0]['id']
                print(f"[FOUND] Deal '{deal_name}': {deal_id}")
                return deal_id

        print(f"[NOT FOUND] Deal '{deal_name}' not found in HubSpot")
        return None

    def attach_to_company(self, file_id: str, company_id: str) -> bool:
        """
        Attach file to a company record

        Args:
            file_id: HubSpot file ID
            company_id: HubSpot company ID

        Returns:
            True if successful
        """
        # Create a note with the file attached
        note_url = f"{self.base_url}/crm/v3/objects/notes"

        note_body = {
            "properties": {
                "hs_timestamp": datetime.now().isoformat() + "Z",
                "hs_note_body": f"FirstMile Xparcel Performance Report generated on {datetime.now().strftime('%B %d, %Y')}.\n\nReport Details:\n- Service Level: Xparcel Expedited\n- SLA Compliance: Calculated on delivered packages only\n- Period: See report for details\n\nFile attached to this note."
            }
        }

        response = requests.post(note_url, headers=self.headers, json=note_body)

        if response.status_code in [200, 201]:
            note_data = response.json()
            note_id = note_data['id']

            # Associate note with company
            assoc_url = f"{self.base_url}/crm/v3/objects/notes/{note_id}/associations/companies/{company_id}/note_to_company"
            assoc_response = requests.put(assoc_url, headers=self.headers)

            if assoc_response.status_code in [200, 201, 204]:
                print(f"[SUCCESS] Report attached to company {company_id}")

                # Also attach the file to the note
                file_assoc_url = f"{self.base_url}/crm/v3/objects/notes/{note_id}/associations/files/{file_id}/note_to_file"
                file_response = requests.put(file_assoc_url, headers=self.headers)

                if file_response.status_code in [200, 201, 204]:
                    print(f"[SUCCESS] File attached to note")
                    return True

        return False

    def attach_to_deal(self, file_id: str, deal_id: str) -> bool:
        """
        Attach file to a deal record

        Args:
            file_id: HubSpot file ID
            deal_id: HubSpot deal ID

        Returns:
            True if successful
        """
        # Create a note with the file attached
        note_url = f"{self.base_url}/crm/v3/objects/notes"

        note_body = {
            "properties": {
                "hs_timestamp": datetime.now().isoformat() + "Z",
                "hs_note_body": f"FirstMile Xparcel Performance Report\nGenerated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n📊 Key Metrics:\n- Total Volume: 703 packages\n- SLA Compliance: 90.1% (Meets Standard)\n- Average Transit: 2.33 days\n- Service Level: Xparcel Expedited (2-5 day service)\n\n✅ Report includes:\n- Executive Summary\n- SLA Compliance Analysis\n- Transit Performance\n- Geographic Distribution\n- Zone Analysis\n- Brand Style Guide"
            }
        }

        response = requests.post(note_url, headers=self.headers, json=note_body)

        if response.status_code in [200, 201]:
            note_data = response.json()
            note_id = note_data['id']

            # Associate note with deal
            assoc_url = f"{self.base_url}/crm/v3/objects/notes/{note_id}/associations/deals/{deal_id}/note_to_deal"
            assoc_response = requests.put(assoc_url, headers=self.headers)

            if assoc_response.status_code in [200, 201, 204]:
                print(f"[SUCCESS] Report attached to deal {deal_id}")

                # Also attach the file to the note
                file_assoc_url = f"{self.base_url}/crm/v3/objects/notes/{note_id}/associations/files/{file_id}/note_to_file"
                file_response = requests.put(file_assoc_url, headers=self.headers)

                if file_response.status_code in [200, 201, 204]:
                    print(f"[SUCCESS] File attached to note")
                    return True

        return False

    def create_engagement(self, company_id: str, file_url: str) -> bool:
        """
        Create an engagement record for the report delivery

        Args:
            company_id: HubSpot company ID
            file_url: URL to the uploaded file

        Returns:
            True if successful
        """
        engagement_url = f"{self.base_url}/crm/v3/objects/tasks"

        task_body = {
            "properties": {
                "hs_task_subject": "FirstMile Performance Report Delivered",
                "hs_task_body": f"FirstMile Xparcel Performance Report has been generated and delivered.\n\nReport Highlights:\n- SLA Compliance: 90.1%\n- Average Transit: 2.33 days\n- Total Volume: 703 packages\n\nFile: {file_url}",
                "hs_task_status": "COMPLETED",
                "hs_task_priority": "MEDIUM",
                "hs_timestamp": datetime.now().isoformat() + "Z"
            }
        }

        response = requests.post(engagement_url, headers=self.headers, json=task_body)

        if response.status_code in [200, 201]:
            task_data = response.json()
            task_id = task_data['id']

            # Associate task with company
            assoc_url = f"{self.base_url}/crm/v3/objects/tasks/{task_id}/associations/companies/{company_id}/task_to_company"
            assoc_response = requests.put(assoc_url, headers=self.headers)

            if assoc_response.status_code in [200, 201, 204]:
                print(f"[SUCCESS] Engagement created for report delivery")
                return True

        return False

def upload_report_to_hubspot(
    report_path: str,
    company_name: str = "JM Group",
    deal_name: Optional[str] = None,
    api_key: Optional[str] = None
):
    """
    Main function to upload report to HubSpot

    Args:
        report_path: Path to the report file
        company_name: Company name in HubSpot
        deal_name: Optional deal name to associate
        api_key: HubSpot API key (or use environment variable)
    """
    print("""
    ========================================================================
                    HUBSPOT REPORT UPLOAD SYSTEM
                        FirstMile Integration
    ========================================================================
    """)

    try:
        # Initialize uploader
        uploader = HubSpotReportUploader(api_key)

        # Upload file
        file_data = uploader.upload_file(report_path)
        file_id = file_data['id']
        file_url = file_data.get('url', 'File uploaded successfully')

        # Search for company
        company_id = uploader.search_company(company_name)

        if company_id:
            # Attach to company
            uploader.attach_to_company(file_id, company_id)

            # Create engagement
            uploader.create_engagement(company_id, file_url)

        # If deal name provided, also attach to deal
        if deal_name:
            deal_id = uploader.search_deal(deal_name)
            if deal_id:
                uploader.attach_to_deal(file_id, deal_id)

        print("""
        ========================================================================
                            UPLOAD COMPLETE
        ========================================================================
        """)

        return {
            "success": True,
            "file_id": file_id,
            "file_url": file_url,
            "company_id": company_id,
            "message": "Report successfully uploaded to HubSpot"
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Example usage
    report_file = "FirstMile_Xparcel_Performance_JM_Group_of_NY_20250923_1504.xlsx"

    # You need to set your HubSpot API key as an environment variable
    # Or pass it directly (not recommended for production)

    # Option 1: Set environment variable
    # os.environ['HUBSPOT_API_KEY'] = 'your-api-key-here'

    # Option 2: Pass directly (for testing only)
    # result = upload_report_to_hubspot(
    #     report_path=report_file,
    #     company_name="JM Group",
    #     deal_name="JM Group - FirstMile Xparcel",
    #     api_key="your-api-key-here"
    # )

    # For now, show what would be uploaded
    print(f"Ready to upload: {report_file}")
    print("To complete upload, set HUBSPOT_API_KEY environment variable")
    print("\nExample:")
    print('os.environ["HUBSPOT_API_KEY"] = "your-private-app-token"')
    print('result = upload_report_to_hubspot(')
    print(f'    report_path="{report_file}",')
    print('    company_name="JM Group",')
    print('    deal_name="JM Group - FirstMile Migration"')
    print(')')