#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test new association method in hubspot_sync_core
"""

import sys
import os
import io
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    load_dotenv()

    API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not API_KEY:
        print("ERROR: HUBSPOT_API_KEY not found")
        sys.exit(1)

    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id="699257003",
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    print("\nTesting new associate_contact_to_deal method...")
    print("This should return True (association already exists)\n")

    result = sync.associate_contact_to_deal(
        contact_id="173878634555",  # Fernando
        deal_id="36470789710"        # Tinoco
    )

    if result:
        print("SUCCESS: Method works correctly!\n")
    else:
        print("WARNING: Method returned False\n")

if __name__ == "__main__":
    main()
