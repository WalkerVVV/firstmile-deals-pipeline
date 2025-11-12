#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Tinoco Enterprises Contact in HubSpot
Create Fernando Arenas as new primary contact, associate with deal, and log transition.

Date: 2025-11-10
"""

import sys
import os
import io
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Create Fernando contact and update Tinoco Enterprises deal."""

    print("\n" + "="*80)
    print("TINOCO ENTERPRISES CONTACT UPDATE")
    print("="*80 + "\n")

    # Load credentials
    print("Loading credentials...")
    load_dotenv()

    API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not API_KEY:
        print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
        sys.exit(1)

    # Initialize sync manager
    print("Initializing HubSpot connection...\n")
    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id="699257003",
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    # Deal details
    TINOCO_DEAL_ID = "36470789710"
    TINOCO_COMPANY_NAME = "Tinoco Enterprises / Juggy"

    # New contact details
    fernando_details = {
        "firstname": "Fernando",
        "lastname": "Arenas",
        "email": "fernando.arenas201101@gmail.com",
        "phone": "385-472-3886",
        "jobtitle": "Primary Contact"
    }

    try:
        # Step 1: Create Fernando as new contact
        print("Step 1: Creating new contact - Fernando Arenas...")
        print(f"  Email: {fernando_details['email']}")
        print(f"  Phone: {fernando_details['phone']}\n")

        fernando_contact = sync.create_contact(fernando_details)
        fernando_contact_id = fernando_contact.get('id')

        if fernando_contact_id:
            print(f"✅ Contact created successfully!")
            print(f"   Contact ID: {fernando_contact_id}\n")
        else:
            print("❌ Failed to create contact - no ID returned")
            return

        # Step 2: Associate Fernando with Tinoco deal
        print(f"Step 2: Associating Fernando with Tinoco deal (ID: {TINOCO_DEAL_ID})...")

        association_result = sync.associate_contact_to_deal(
            contact_id=fernando_contact_id,
            deal_id=TINOCO_DEAL_ID
        )

        if association_result:
            print(f"✅ Contact associated with deal successfully!\n")
        else:
            print(f"⚠️  Association may have failed - check HubSpot manually\n")

        # Step 3: Add activity note about transition
        print("Step 3: Adding activity note about contact transition...")

        note_content = """Contact Transition - Tinoco Enterprises

New Primary Contact: Fernando Arenas
- Email: fernando.arenas201101@gmail.com
- Phone: 385-472-3886

Previous Contact: David
- Status: Moving to Michigan
- Transition Date: November 10, 2025

Call Activity:
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
            print(f"✅ Activity note created successfully!\n")
        else:
            print(f"⚠️  Note creation may have failed - check HubSpot manually\n")

        # Summary
        print("="*80)
        print("UPDATE COMPLETE")
        print("="*80)
        print(f"\n✅ Fernando Arenas created as new contact")
        print(f"✅ Associated with {TINOCO_COMPANY_NAME}")
        print(f"✅ Transition note logged in HubSpot")
        print(f"\nContact ID: {fernando_contact_id}")
        print(f"Deal ID: {TINOCO_DEAL_ID}")
        print(f"\nNext: Update Fernando as primary contact in deal manually if needed")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Please check credentials and try again.\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
