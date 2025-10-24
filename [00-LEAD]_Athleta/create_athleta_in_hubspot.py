#!/usr/bin/env python3
"""
Create Athleta contacts and deal in HubSpot
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from hubspot_config import get_hubspot_config, get_api_headers, ASSOCIATION_IDS
import requests
import json

def create_company(api_headers):
    """Create Athleta company in HubSpot"""
    url = "https://api.hubapi.com/crm/v3/objects/companies"

    data = {
        "properties": {
            "name": "Athleta",
            "domain": "athleta.com",
            "industry": "Apparel",
            "annualrevenue": "1350000000",  # $1.35B
            "city": "San Francisco",
            "state": "California",
            "zip": "94105",
            "address": "2 Folsom Street",
            "country": "United States",
            "website": "https://www.athleta.com",
            "description": "Women's activewear and athleisure brand, Gap Inc. subsidiary. 259 stores nationwide, $1.35B annual revenue, ~9M packages/year."
        }
    }

    response = requests.post(url, headers=api_headers, json=data)

    if response.status_code == 201:
        company_id = response.json()['id']
        print(f"[OK] Company created: Athleta (ID: {company_id})")
        return company_id
    elif response.status_code == 409:
        # Company already exists, search for it
        print("[WARN] Company already exists, searching...")
        search_url = "https://api.hubapi.com/crm/v3/objects/companies/search"
        search_data = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "domain",
                    "operator": "EQ",
                    "value": "athleta.com"
                }]
            }]
        }
        search_response = requests.post(search_url, headers=api_headers, json=search_data)
        if search_response.status_code == 200 and search_response.json().get('results'):
            company_id = search_response.json()['results'][0]['id']
            print(f"[OK] Found existing company: Athleta (ID: {company_id})")
            return company_id

    print(f"[FAIL] Failed to create company: {response.status_code}")
    print(response.text)
    return None

def create_contact(api_headers, first_name, last_name, email, job_title, linkedin, company_id):
    """Create contact in HubSpot and associate with company"""
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    data = {
        "properties": {
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "jobtitle": job_title,
            "lifecyclestage": "lead"
        }
    }

    response = requests.post(url, headers=api_headers, json=data)

    if response.status_code == 201:
        contact_id = response.json()['id']
        print(f"[OK] Contact created: {first_name} {last_name} (ID: {contact_id})")

        # Associate contact with company
        if company_id:
            assoc_url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies/{company_id}/{ASSOCIATION_IDS['CONTACT_TO_COMPANY']}"
            assoc_response = requests.put(assoc_url, headers=api_headers)
            if assoc_response.status_code == 200:
                print(f"   [OK] Associated with Athleta company")

        return contact_id
    elif response.status_code == 409:
        print(f"[WARN] Contact already exists: {first_name} {last_name}")
        # Search for existing contact
        search_url = "https://api.hubapi.com/crm/v3/objects/contacts/search"
        search_data = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }]
        }
        search_response = requests.post(search_url, headers=api_headers, json=search_data)
        if search_response.status_code == 200 and search_response.json().get('results'):
            contact_id = search_response.json()['results'][0]['id']
            print(f"   [OK] Found existing contact (ID: {contact_id})")
            return contact_id

    print(f"[FAIL] Failed to create contact: {response.status_code}")
    print(response.text)
    return None

def create_deal(api_headers, company_id, contact_ids, config):
    """Create Athleta deal in HubSpot"""
    url = "https://api.hubapi.com/crm/v3/objects/deals"

    data = {
        "properties": {
            "dealname": "Athleta - Parcel Shipping Optimization",
            "amount": "40000000",  # $40M annual shipping spend
            "dealstage": "1090865183",  # [01-DISCOVERY-SCHEDULED] - closest to lead stage
            "pipeline": config['PIPELINE_ID'],
            "hubspot_owner_id": config['OWNER_ID'],
            "closedate": "2026-06-30",  # Q2 2026 estimated
            "dealtype": "newbusiness",
            "description": """High-value parcel shipping opportunity with Athleta, Gap Inc.'s activewear brand.

KEY METRICS:
- Annual parcel volume: ~9M packages/year
- Current shipping spend: ~$40M annually
- Potential FirstMile savings: $10-14M (25-35%)
- FirstMile Opportunity Score: 8.5/10

CURRENT PAIN POINTS:
- 50% delivery failure rate per customer reviews
- 6-carrier complexity (USPS, UPS, FedEx, LaserShip, OnTrac, UDS)
- Fulfillment errors and missing packages
- Consistent missed delivery SLAs (3-5 day promise)

VALUE PROPOSITION:
- Simplify to single Xparcel carrier solution
- Improve delivery reliability and NPS
- Zone-skipping for CA-to-nationwide optimization
- Reduce carrier management overhead from 6 to 1

TIMING OPPORTUNITY:
- New CEO (Maggie Gauger) started Aug 2025
- Turnaround mandate = operational review
- Perfect timing for vendor evaluation in Q4 2025 or Q1 2026"""
        }
    }

    response = requests.post(url, headers=api_headers, json=data)

    if response.status_code == 201:
        deal_id = response.json()['id']
        print(f"[OK] Deal created: Athleta - Parcel Shipping Optimization (ID: {deal_id})")

        # Associate deal with company
        if company_id:
            assoc_url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/companies/{company_id}/{ASSOCIATION_IDS['DEAL_TO_COMPANY']}"
            assoc_response = requests.put(assoc_url, headers=api_headers)
            if assoc_response.status_code == 200:
                print(f"   [OK] Associated with Athleta company")

        # Associate deal with contacts
        for contact_id in contact_ids:
            if contact_id:
                assoc_url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/{ASSOCIATION_IDS['DEAL_TO_CONTACT']}"
                assoc_response = requests.put(assoc_url, headers=api_headers)
                if assoc_response.status_code == 200:
                    print(f"   [OK] Associated with contact ID {contact_id}")

        # Create initial follow-up task
        create_initial_task(api_headers, deal_id, config)

        return deal_id

    print(f"[FAIL] Failed to create deal: {response.status_code}")
    print(response.text)
    return None

def create_initial_task(api_headers, deal_id, config):
    """Create initial follow-up task for Athleta deal"""
    url = "https://api.hubapi.com/crm/v3/objects/tasks"

    data = {
        "properties": {
            "hs_task_subject": "LinkedIn research - Gap Inc. Supply Chain leadership",
            "hs_task_body": """Research Gap Inc. supply chain org chart on LinkedIn:
1. Identify VP/Director of Supply Chain Operations
2. Map reporting structure (Athleta → Gap Inc. corporate)
3. Find mutual connections for warm introduction
4. Prepare outreach materials (email, pitch deck)""",
            "hs_task_priority": "HIGH",
            "hs_task_status": "NOT_STARTED",
            "hs_task_type": "TODO",
            "hubspot_owner_id": config['OWNER_ID'],
            "hs_timestamp": "1728950400000"  # Oct 15, 2025 (1 week out)
        }
    }

    response = requests.post(url, headers=api_headers, json=data)

    if response.status_code == 201:
        task_id = response.json()['id']
        print(f"[OK] Task created (ID: {task_id})")

        # Associate task with deal
        assoc_url = f"https://api.hubapi.com/crm/v3/objects/tasks/{task_id}/associations/deals/{deal_id}/{ASSOCIATION_IDS['TASK_TO_DEAL']}"
        assoc_response = requests.put(assoc_url, headers=api_headers)
        if assoc_response.status_code == 200:
            print(f"   [OK] Task associated with deal")
    else:
        print(f"[WARN] Failed to create task: {response.status_code}")

def main():
    print("Creating Athleta in HubSpot...")
    print("=" * 60)

    # Get configuration
    config = get_hubspot_config()
    api_headers = get_api_headers(config['API_KEY'])

    # Step 1: Create Company
    print("\n[1] Creating Company...")
    company_id = create_company(api_headers)
    if not company_id:
        print("[X] Failed to create company. Aborting.")
        return

    # Step 2: Create Contacts
    print("\n[2] Creating Contacts...")

    # Contact 1: Maggie Gauger (CEO)
    maggie_id = create_contact(
        api_headers,
        "Maggie",
        "Gauger",
        "maggiegauger@athleta.com",  # Note: Email TBD
        "President & CEO",
        "https://www.linkedin.com/in/maggiegauger",
        company_id
    )

    # Contact 2: Chris Blakeslee (Former CEO)
    chris_id = create_contact(
        api_headers,
        "Chris",
        "Blakeslee",
        "chrisblakeslee@gap.com",  # Note: Email TBD
        "Former President & CEO",
        "https://www.linkedin.com/in/chrisblakeslee",
        company_id
    )

    contact_ids = [maggie_id, chris_id]

    # Step 3: Create Deal
    print("\n[3] Creating Deal...")
    deal_id = create_deal(api_headers, company_id, contact_ids, config)

    print("\n" + "=" * 60)
    print("[OK] COMPLETE! Athleta added to HubSpot")
    print(f"   Company ID: {company_id}")
    print(f"   Contact IDs: {contact_ids}")
    print(f"   Deal ID: {deal_id}")
    print("\nNext steps:")
    print("  1. Verify in HubSpot: https://app.hubspot.com/contacts/8210927")
    print("  2. Update contact emails when obtained")
    print("  3. Complete LinkedIn research task (due Oct 15)")

if __name__ == "__main__":
    main()
