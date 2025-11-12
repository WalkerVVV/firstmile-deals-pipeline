#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Fernando association - correct API call
"""

import sys
import os
import io
import requests
from dotenv import load_dotenv

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Associate Fernando with Tinoco deal - corrected."""

    print("\nFIXING FERNANDO ASSOCIATION...")

    # Load credentials
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')

    # Details
    FERNANDO_CONTACT_ID = "173878634555"
    TINOCO_DEAL_ID = "36470789710"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Correct API endpoint for associations
        # PUT /crm/v4/objects/contact/{contactId}/associations/deal/{dealId}
        association_url = f"https://api.hubapi.com/crm/v4/objects/contact/{FERNANDO_CONTACT_ID}/associations/deal/{TINOCO_DEAL_ID}"

        payload = [
            {
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 3  # contact_to_deal
            }
        ]

        response = requests.put(association_url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            print("SUCCESS: Fernando associated with Tinoco deal!")
        elif response.status_code == 409:
            print("INFO: Association already exists!")
        else:
            print(f"Response: {response.status_code}")
            print(response.text)

        print("\nDONE!\n")

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
