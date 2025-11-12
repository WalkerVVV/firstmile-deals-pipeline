#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final fix for Fernando association using v3 batch API
"""

import sys
import os
import io
import requests
from dotenv import load_dotenv

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Associate Fernando with Tinoco deal using v3 API."""

    print("\nASSOCIATING FERNANDO WITH TINOCO DEAL (v3 API)...")

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
        # Use v3 associations create endpoint
        association_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{FERNANDO_CONTACT_ID}/associations/deals/{TINOCO_DEAL_ID}/3"

        # Type 3 = contact to deal
        response = requests.put(association_url, headers=headers)

        if response.status_code in [200, 201]:
            print("SUCCESS: Fernando associated with Tinoco deal!")
            print(response.json())
        elif response.status_code == 409:
            print("INFO: Association already exists!")
        else:
            print(f"Response: {response.status_code}")
            print(response.text)

        print("\nDONE!\n")

    except Exception as e:
        print(f"ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
