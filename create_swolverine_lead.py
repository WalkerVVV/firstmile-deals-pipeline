#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create SWOLVERINE lead in HubSpot with complete company and contact records.

Brand Scout Lead Generation - November 13, 2025
"""

import sys
import io
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    sys.exit(1)

OWNER_ID = "699257003"  # Brett Walker

def create_company(company_data):
    """Create company in HubSpot."""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'properties': company_data
    }

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/companies',
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"   ❌ Error creating company: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def create_contact(contact_data):
    """Create contact in HubSpot."""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'properties': contact_data
    }

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/contacts',
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"   ❌ Error creating contact: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def associate_contact_with_company(contact_id, company_id):
    """Associate contact with company in HubSpot."""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies/{company_id}/280',
        headers=headers
    )

    if response.status_code == 200:
        return True
    else:
        print(f"   ⚠️ Warning: Association may have failed: {response.status_code}")
        return False

def create_swolverine_lead():
    """Create SWOLVERINE lead with company and contacts."""

    print("=" * 80)
    print("SWOLVERINE LEAD CREATION - Brand Scout Output")
    print("=" * 80)
    print()

    # Company information
    company_data = {
        "name": "SWOLVERINE",
        "domain": "swolverine.com",
        "city": "Reno",
        "state": "Nevada",
        "zip": "89521",
        "address": "9005 Double Diamond Parkway, STE 10",
        "country": "United States",
        "industry": "Nutraceuticals",  # HubSpot predefined option
        "website": "https://swolverine.com",
        "description": "Sports nutrition and supplement company founded by certified fitness professionals. Known for clean, science-backed supplements for athletes. Multi-carrier shipping (USPS, FedEx, DHL, UPS) with $99+ free shipping threshold.",
        "numberofemployees": 30,  # Estimated mid-range
        "hs_lead_status": "NEW",
        "hubspot_owner_id": OWNER_ID
    }

    print("\n1. Creating SWOLVERINE company record...")
    print(f"   Company: {company_data['name']}")
    print(f"   Domain: {company_data['domain']}")
    print(f"   Location: {company_data['city']}, {company_data['state']}")

    # Create company
    company_id = create_company(company_data)

    if company_id:
        print(f"   ✅ Company created: {company_id}")
    else:
        print("   ❌ Failed to create company")
        return

    # Contact 1: Walter Hinchman (CEO)
    walter_data = {
        "firstname": "Walter",
        "lastname": "Hinchman",
        "email": "whinchman1@sbcglobal.net",
        "jobtitle": "CEO & Founder",
        "company": "SWOLVERINE",
        "hs_lead_status": "NEW",
        "lifecyclestage": "lead",
        "hubspot_owner_id": OWNER_ID
    }

    print("\n2. Creating Walter Hinchman contact record...")
    print(f"   Name: {walter_data['firstname']} {walter_data['lastname']}")
    print(f"   Title: {walter_data['jobtitle']}")
    print(f"   Email: {walter_data['email']}")

    walter_id = create_contact(walter_data)

    if walter_id:
        print(f"   ✅ Contact created: {walter_id}")
        # Associate with company
        associate_contact_with_company(walter_id, company_id)
        print(f"   ✅ Associated with company")
    else:
        print("   ❌ Failed to create Walter contact")

    # Contact 2: Alexandria Best (COO)
    alexandria_data = {
        "firstname": "Alexandria",
        "lastname": "Best",
        "email": "alexandria@swolverine.com",
        "jobtitle": "Co-Founder & COO",
        "company": "SWOLVERINE",
        "hs_lead_status": "NEW",
        "lifecyclestage": "lead",
        "hubspot_owner_id": OWNER_ID
    }

    print("\n3. Creating Alexandria Best contact record...")
    print(f"   Name: {alexandria_data['firstname']} {alexandria_data['lastname']}")
    print(f"   Title: {alexandria_data['jobtitle']}")
    print(f"   Email: {alexandria_data['email']}")

    alexandria_id = create_contact(alexandria_data)

    if alexandria_id:
        print(f"   ✅ Contact created: {alexandria_id}")
        # Associate with company
        associate_contact_with_company(alexandria_id, company_id)
        print(f"   ✅ Associated with company")
    else:
        print("   ❌ Failed to create Alexandria contact")

    # Summary
    print("\n" + "=" * 80)
    print("SWOLVERINE LEAD CREATION COMPLETE")
    print("=" * 80)
    print(f"\n✅ Company ID: {company_id}")
    print(f"✅ Walter Hinchman ID: {walter_id}")
    print(f"✅ Alexandria Best ID: {alexandria_id}")
    print()
    print("Next Steps:")
    print("1. Create [00-LEAD]_Swolverine deal folder")
    print("2. Save brand research report")
    print("3. Create relationship documentation")
    print("4. Plan outreach strategy")
    print()

    return {
        "company_id": company_id,
        "walter_id": walter_id,
        "alexandria_id": alexandria_id
    }

if __name__ == "__main__":
    result = create_swolverine_lead()
