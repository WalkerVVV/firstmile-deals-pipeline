#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Associate Fernando with Tinoco deal and add transition note
Fernando contact already created (ID: 173878634555)
"""

import sys
import os
import io
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Associate Fernando with Tinoco deal."""

    print("\n" + "="*80)
    print("ASSOCIATE FERNANDO WITH TINOCO DEAL")
    print("="*80 + "\n")

    # Load credentials
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not API_KEY:
        print("\nERROR: HUBSPOT_API_KEY not found")
        sys.exit(1)

    # Initialize sync manager
    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id="699257003",
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    # Details
    FERNANDO_CONTACT_ID = "173878634555"
    TINOCO_DEAL_ID = "36470789710"

    try:
        # Step 1: Associate Fernando with Tinoco deal
        print(f"Step 1: Associating Fernando (ID: {FERNANDO_CONTACT_ID}) with Tinoco deal...")

        association_result = sync.associate_contact_to_deal(
            contact_id=FERNANDO_CONTACT_ID,
            deal_id=TINOCO_DEAL_ID
        )

        if association_result:
            print("SUCCESS: Contact associated with deal!\n")
        else:
            print("WARNING: Association may have failed\n")

        # Step 2: Add activity note
        print("Step 2: Adding activity note...")

        note_content = """Contact Transition - Tinoco Enterprises

New Primary Contact: Fernando Arenas
- Email: fernando.arenas201101@gmail.com
- Phone: 385-472-3886

Previous Contact: David
- Status: Moving to Michigan
- Transition Date: November 10, 2025

Call Activity (11/10/2025):
- Spoke with David at Tinoco Enterprises
- David provided Fernando's contact information
- David confirmed he is relocating to Michigan

Next Steps:
- Reach out to Fernando for ongoing coordination
- Update all future communications to Fernando
"""

        note_result = sync.create_note(
            deal_id=TINOCO_DEAL_ID,
            note_body=note_content
        )

        if note_result:
            print("SUCCESS: Activity note created!\n")
        else:
            print("WARNING: Note creation may have failed\n")

        # Summary
        print("="*80)
        print("HUBSPOT UPDATE COMPLETE")
        print("="*80)
        print(f"\nSUCCESS: Fernando Arenas associated with Tinoco Enterprises")
        print(f"SUCCESS: Transition note logged")
        print(f"\nContact ID: {FERNANDO_CONTACT_ID}")
        print(f"Deal ID: {TINOCO_DEAL_ID}")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\nERROR: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
