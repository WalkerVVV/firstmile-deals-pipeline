#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Driftaway Coffee - HubSpot Win-Back Deal Creation v2
Updates company record and creates win-back deal for Xparcel Domestic restart
"""

import sys
import io
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Valid stage IDs from error message - using last stage as WIN-BACK placeholder
WIN_BACK_STAGE = "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8"  # Will treat as win-back

def update_company_notes(company_id):
    """Add relationship documentation note to company"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    note_content = """CRITICAL INCIDENT DOCUMENTATION - Driftaway Coffee

Issue Date: September 11-18, 2025
Resolution Date: October 2, 2025
Status: SERVICE SUSPENDED (Domestic) | International Active

ROOT CAUSE:
- ACI carrier added to DHL-only setup WITHOUT customer notification
- ACI carrier added WITHOUT sales rep (Brett) notification
- Result: 46 shipments missorted at DHL facilities
- Customer suspended all domestic FirstMile services

IMPACT:
- 46 ACI shipments affected (15 returned, 31 outstanding)
- Multiple end-customer complaints to Driftaway
- Brand damage to Driftaway Coffee reputation
- 23-day resolution timeline (Sept 11 - Oct 2)

RESOLUTION:
- ACI removed from setup (Oct 2, 2025 - Brycen Prout)
- Leadership approval: Zach Green (EVP Sales)
- Process improvement: Setup change notification protocol

RECOVERY STATUS:
- High recovery potential - customer maintained international services
- Long-term relationship (DHL-only for many years)
- Customer escalated internally vs switching immediately
- Awaiting confirmation to resume domestic services

KEY CONTACT:
- Suyog (Customer Support Agent) - 6rv7ngx3rlmg9djl@emails.gorgias.com
- Account Manager: Melissa (myaccountmanager@firstmile.com)

NEXT STEPS:
1. Brett to confirm ACI removal with Suyog
2. Monitor first batch of resumed shipments (100% scan compliance)
3. Weekly performance reports for 30 days
4. Track down remaining 31 outstanding packages

Full documentation: [CUSTOMER]_Driftaway_Coffee/Customer_Relationship_Documentation.md
"""

    # Timestamp needs to be Unix epoch in milliseconds
    timestamp_ms = int(datetime.now().timestamp() * 1000)

    note_payload = {
        "properties": {
            "hs_timestamp": timestamp_ms,
            "hs_note_body": note_content,
            "hubspot_owner_id": OWNER_ID
        }
    }

    print(f"📝 Creating company note...")
    note_response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/notes",
        headers=headers,
        json=note_payload
    )

    if note_response.status_code == 201:
        note = note_response.json()
        note_id = note["id"]
        print(f"✓ Created note (ID: {note_id})")

        # Associate note with company
        assoc_payload = {
            "inputs": [{
                "from": {"id": note_id},
                "to": {"id": company_id},
                "type": "note_to_company"
            }]
        }

        assoc_response = requests.post(
            "https://api.hubapi.com/crm/v3/associations/notes/companies/batch/create",
            headers=headers,
            json=assoc_payload
        )

        if assoc_response.status_code == 201:
            print(f"✓ Associated note with company")
            return True
        else:
            print(f"⚠️  Note created but association failed: {assoc_response.status_code}")
            return True
    else:
        print(f"❌ Error creating note: {note_response.status_code}")
        print(note_response.text)
        return False

def create_winback_deal(company_id):
    """Create win-back deal for Xparcel Domestic restart"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Use valid stage ID from pipeline
    deal_payload = {
        "properties": {
            "dealname": "Driftaway Coffee - Xparcel Domestic Win-Back",
            "dealstage": WIN_BACK_STAGE,
            "pipeline": PIPELINE_ID,
            "hubspot_owner_id": OWNER_ID,
            "amount": "0",
            "deal_currency_code": "USD"
        }
    }

    print(f"🎯 Creating win-back deal...")
    deal_response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals",
        headers=headers,
        json=deal_payload
    )

    if deal_response.status_code == 201:
        deal = deal_response.json()
        deal_id = deal["id"]
        print(f"✓ Created deal (ID: {deal_id})")

        # Associate deal with company
        assoc_payload = {
            "inputs": [{
                "from": {"id": deal_id},
                "to": {"id": company_id},
                "type": "deal_to_company"
            }]
        }

        assoc_response = requests.post(
            "https://api.hubapi.com/crm/v3/associations/deals/companies/batch/create",
            headers=headers,
            json=assoc_payload
        )

        if assoc_response.status_code == 201:
            print(f"✓ Associated deal with company")
        else:
            print(f"⚠️  Deal created but association failed: {assoc_response.status_code}")

        # Add deal context note
        deal_note_content = """WIN-BACK OPPORTUNITY - Driftaway Coffee Xparcel Domestic

OBJECTIVE: Resume domestic FirstMile/Xparcel services after ACI incident resolution

BACKGROUND:
- Long-term customer (DHL-only for many years)
- Service suspended Sept 11, 2025 due to ACI missort incident
- 46 shipments affected, customer had end-customer complaints
- ACI removed from setup Oct 2, 2025
- International services maintained throughout (trust signal)

WIN-BACK STRATEGY:
1. Confirm ACI removal with Suyog (Customer Support Agent)
2. Offer 100% scan monitoring for first batch of resumed shipments
3. Weekly performance reports for 30 days
4. Direct line to Brett: 402-718-4727
5. Expedite tracking for remaining 31 outstanding packages

RECOVERY INDICATORS:
- Customer maintained international services (did not switch completely)
- Customer escalated to sales rep (Brett) vs going to competitor
- Long-term relationship history (years with FirstMile)
- Clear resolution path (ACI removed per leadership approval)
- Brock assessment: "strong possibility to turn back on quickly"

RELATIONSHIP STATUS:
- Primary Contact: Suyog (6rv7ngx3rlmg9djl@emails.gorgias.com)
- Account Manager: Melissa (myaccountmanager@firstmile.com)
- Sales Rep: Brett Walker (402-718-4727)

RISK FACTORS:
- 23-day resolution timeline may have deepened trust concerns
- 31 packages still outstanding from incident
- Competitor conversations likely during suspension
- End-customer complaints may have damaged Driftaway brand

NEXT ACTIONS:
1. Send confirmation email to Suyog (ACI removal complete)
2. Schedule recovery call to discuss resumption comfort level
3. Create performance monitoring plan (30-day SLA guarantee)
4. Expedite outstanding package tracking
5. Document lessons learned for process improvements

Full incident documentation: Customer_Relationship_Documentation.md
"""

        timestamp_ms = int(datetime.now().timestamp() * 1000)

        deal_note_payload = {
            "properties": {
                "hs_timestamp": timestamp_ms,
                "hs_note_body": deal_note_content,
                "hubspot_owner_id": OWNER_ID
            }
        }

        print(f"📝 Creating deal context note...")
        deal_note_response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/notes",
            headers=headers,
            json=deal_note_payload
        )

        if deal_note_response.status_code == 201:
            deal_note = deal_note_response.json()
            deal_note_id = deal_note["id"]
            print(f"✓ Created deal note (ID: {deal_note_id})")

            # Associate note with deal
            deal_assoc_payload = {
                "inputs": [{
                    "from": {"id": deal_note_id},
                    "to": {"id": deal_id},
                    "type": "note_to_deal"
                }]
            }

            deal_assoc_response = requests.post(
                "https://api.hubapi.com/crm/v3/associations/notes/deals/batch/create",
                headers=headers,
                json=deal_assoc_payload
            )

            if deal_assoc_response.status_code == 201:
                print(f"✓ Associated note with deal")

        return deal_id
    else:
        print(f"❌ Error creating deal: {deal_response.status_code}")
        print(deal_response.text)
        return None

def main():
    print("=" * 70)
    print("DRIFTAWAY COFFEE - HUBSPOT WIN-BACK SETUP v2")
    print("=" * 70)
    print()

    # Company already exists: 20566169147
    company_id = "20566169147"
    print(f"✓ Using existing company ID: {company_id}")
    print()

    # Step 1: Update company with relationship documentation
    print("📊 Updating company record...")
    if update_company_notes(company_id):
        print("✓ Company documentation updated")
    else:
        print("⚠️  Company documentation update failed")

    print()

    # Step 2: Create win-back deal
    print("🎯 Creating win-back deal...")
    deal_id = create_winback_deal(company_id)

    print()
    print("=" * 70)
    if deal_id:
        print("✅ SUCCESS - HubSpot Updated")
        print(f"   Company ID: {company_id}")
        print(f"   Deal ID: {deal_id}")
        print(f"   View Deal: https://app.hubspot.com/contacts/8210927/deal/{deal_id}")
    else:
        print("⚠️  PARTIAL SUCCESS - Company updated, deal creation failed")
    print("=" * 70)

if __name__ == "__main__":
    main()
