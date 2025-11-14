# HubSpot Lead Creation Process - Brett Walker Account

**Purpose**: Automate lead intake for Brett Walker's HubSpot CRM from Brand Scout reports or structured research data.

**Owner**: Brett Walker (brett.walker@firstmile.com)
**HubSpot Owner ID**: 699257003
**Default Pipeline**: Sales Pipeline (8bd9336b-4767-4e67-9fe2-35dfcad7c8be)
**Default Stage**: Qualification (1090865183)
**Deal Type**: New Business

---

## Automation Process Overview

Given structured research data (Brand Scout report or manual research), complete these 6 steps to create properly associated HubSpot records:

1. **Extract and Normalize Data** from research
2. **Create/Upsert Contacts** (Primary + Secondary decision makers)
3. **Create/Upsert Company** (match by domain if exists)
4. **Associate Contacts to Company**
5. **Create Lead/Deal** (in Sales Pipeline, Qualification stage)
6. **Log Results and Gaps**

---

## Step 1: Extract and Normalize Data

### Parse Research Input For:

#### Contacts
- **Primary Decision Maker** (CEO, President, Founder)
  - Full Name (firstname, lastname)
  - Title (jobtitle)
  - Email (email)
  - Phone (phone, mobilephone)
  - LinkedIn (store in notes or custom field)

- **Secondary Decision Maker** (COO, VP Ops, Fulfillment Manager)
  - Same fields as above

#### Company
- Legal name (name)
- Website domain (domain)
- Corporate address (address, city, state, zip, country)
- Industry (industry - use HubSpot predefined options)
- Company size (numberofemployees - integer only)
- Description (description)
- Operational details (store in description or notes)

#### Deal/Lead
- Lead/Opportunity name (dealname - format: "Company - Xparcel [Service]")
- Pipeline (pipeline - default: Sales Pipeline)
- Deal stage (dealstage - default: Qualification)
- Type (dealtype - default: New Business)
- Amount (amount - if known, otherwise 0)
- Close date (closedate - default: today + 90 days)
- Volume data (custom fields if available)
- Fulfillment type (custom field)
- Marketplace platform (custom field)

---

## Step 2: Create/Upsert Contacts

### API Endpoint
```
POST https://api.hubapi.com/crm/v3/objects/contacts
```

### Required Fields
- `firstname` (string)
- `lastname` (string)
- `email` (string - unique identifier)

### Recommended Fields
- `jobtitle` (string)
- `phone` (string)
- `company` (string - company name)
- `hs_lead_status` (enum - default: "NEW")
- `lifecyclestage` (enum - default: "lead")
- `hubspot_owner_id` (string - Brett Walker: "699257003")

### Field Mapping Notes
- **LinkedIn**: No standard field - store in notes or description
- **Confidence Level**: Store in notes field with ✅ ⚠️ ❌ markers
- **Source**: Use `hs_analytics_source` = "OFFLINE" and `hs_analytics_source_data_1` = "Brand Scout"

### Error Handling
- **Duplicate Email**: If contact exists, update instead of create (use email as unique key)
- **Invalid Email Format**: Log error, skip contact creation
- **Missing Required Fields**: Log warning, create with available fields

---

## Step 3: Create/Upsert Company

### API Endpoint
```
POST https://api.hubapi.com/crm/v3/objects/companies
```

### Required Fields
- `name` (string)
- `domain` (string - unique identifier)

### Recommended Fields
- `city` (string)
- `state` (string)
- `zip` (string)
- `address` (string)
- `country` (string - default: "United States")
- `industry` (string - **MUST use HubSpot predefined option**)
- `website` (string)
- `description` (string)
- `numberofemployees` (integer - NOT string like "11-50")
- `hubspot_owner_id` (string - Brett Walker: "699257003")

### Industry Field Options (Common for FirstMile)
- `CONSUMER_GOODS` - General consumer products
- `COSMETICS` - Beauty and cosmetics
- `FOOD_BEVERAGES` - Food and beverage
- `HEALTH_WELLNESS_AND_FITNESS` - General health/wellness
- `Nutraceuticals` - Supplements specifically
- `PHARMACEUTICALS` - Medical/pharma
- `RETAIL` - General retail
- `CONSUMER_ELECTRONICS` - Electronics/tech products
- `Apparel` - Clothing and fashion

**Important**: Always use exact HubSpot industry values. If unsure, use closest match or "Other".

### Field Validation Notes
- **numberofemployees**: Must be integer (use 30 for "11-50", 75 for "51-100", etc.)
- **Read-Only Fields**: Never set `notes_last_contacted`, `hs_lastmodifieddate`, etc.
- **Domain Matching**: If company exists with same domain, update instead of create

---

## Step 4: Associate Contacts to Company

### API Endpoint
```
PUT https://api.hubapi.com/crm/v3/objects/contacts/{contactId}/associations/companies/{companyId}/280
```

### Association Type ID
- **280**: Contact to Company (primary association)

### Process
1. For each contact created in Step 2
2. Associate to company created in Step 3
3. Use contact ID and company ID from previous API responses
4. Log success or failure for each association

### Error Handling
- **400 Error**: Association may already exist (safe to ignore)
- **404 Error**: Contact or Company ID not found (check IDs)

---

## Step 5: Create Lead/Deal

### API Endpoint
```
POST https://api.hubapi.com/crm/v3/objects/deals
```

### Required Fields
- `dealname` (string - format: "Company - Xparcel Ground")
- `pipeline` (string - "8bd9336b-4767-4e67-9fe2-35dfcad7c8be")
- `dealstage` (string - "1090865183" for Qualification)
- `hubspot_owner_id` (string - "699257003" for Brett Walker)

### Standard Fields
- `dealtype` (enum - "newbusiness" for new leads)
- `amount` (number - 0 if unknown)
- `closedate` (date - ISO format, default: today + 90 days)
- `createdate` (date - ISO format, today)

### Custom Fields (if available in HubSpot)
- `average_daily_volume` (number - shipments/day)
- `fulfillment_type` (enum - "In-House" / "3PL" / "Hybrid" / "Unknown")
- `marketplace` (enum - "Shopify" / "WooCommerce" / "BigCommerce" / "Custom")
- `original_deal_date` (date)
- `best_potential_deal_date` (date)
- `owner_assigned_date` (date - today)

### Associate Deal to Company
After deal creation, associate to company:
```
PUT https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/companies/{companyId}/341
```
Association Type ID: **341** (Deal to Company)

### Associate Deal to Contacts
Associate to all contacts:
```
PUT https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/contacts/{contactId}/3
```
Association Type ID: **3** (Deal to Contact)

---

## Step 6: Error Handling & Logging

### Log Format

**Success Log**:
```
✅ COMPANY CREATED: [Company Name] (ID: [companyId])
✅ CONTACT CREATED: [Contact Name] (ID: [contactId])
✅ DEAL CREATED: [Deal Name] (ID: [dealId])
✅ ASSOCIATIONS COMPLETE
```

**Warning Log**:
```
⚠️ FIELD MISSING: [field_name] - [reason]
⚠️ INFERRED DATA: [field_name] - [confidence level]
⚠️ ASSOCIATION WARNING: [details]
```

**Error Log**:
```
❌ API ERROR: [endpoint] - [status_code] - [error_message]
❌ VALIDATION ERROR: [field_name] - [validation_issue]
❌ MISSING REQUIRED FIELD: [field_name]
```

### Output Summary

**Return This Information**:
1. **Company Record**
   - Company Name
   - Company ID
   - HubSpot URL

2. **Contact Records**
   - Primary Contact Name, ID, HubSpot URL
   - Secondary Contact Name, ID, HubSpot URL (if applicable)

3. **Deal Record**
   - Deal Name
   - Deal ID
   - Pipeline and Stage
   - HubSpot URL

4. **Fields Not Filled**
   - List all fields that couldn't be populated
   - Reason for each (not disclosed, not available, validation error)

5. **Next Steps**
   - Recommended actions based on information gaps
   - Discovery questions to ask in first call

---

## Account-Specific Rules

### Brett Walker Account Settings
- **Owner**: Brett Walker (699257003)
- **Email**: brett.walker@firstmile.com
- **Pipeline**: Sales Pipeline (8bd9336b-4767-4e67-9fe2-35dfcad7c8be)
- **Default Stage**: [01-DISCOVERY-SCHEDULED] (1090865183)

### Stage IDs (Verified 2025-10-10)
```
1090865183                                  = [01-DISCOVERY-SCHEDULED]
d2a08d6f-cc04-4423-9215-594fe682e538        = [02-DISCOVERY-COMPLETE]
e1c4321e-afb6-4b29-97d4-2b2425488535        = [03-RATE-CREATION]
d607df25-2c6d-4a5d-9835-6ed1e4f4020a        = [04-PROPOSAL-SENT]
4e549d01-674b-4b31-8a90-91ec03122715        = [05-SETUP-DOCS-SENT]
08d9c411-5e1b-487b-8732-9c2bcbbd0307        = [06-IMPLEMENTATION]
3fd46d94-78b4-452b-8704-62a338a210fb        = [07-STARTED-SHIPPING]
02d8a1d7-d0b3-41d9-adc6-44ab768a61b8        = [08-CLOSED-LOST]
```

**Note**: For Brand Scout leads, always start at **Qualification** stage, NOT Discovery Scheduled.

### Duplicate Prevention
- **Email Matching**: Check if contact exists by email before creating
- **Domain Matching**: Check if company exists by domain before creating
- **Deal Naming**: Use "Company - Service Level" format to prevent duplicate deals

---

## API Authentication

### Environment Variables Required
```bash
HUBSPOT_API_KEY=[Private App API Key]
```

### Headers Format
```python
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

---

## Common Validation Errors and Fixes

### Error: "Property values were not valid"
**Cause**: Field value doesn't match HubSpot schema
**Fix**:
- Check industry uses predefined option
- Ensure numberofemployees is integer
- Remove read-only fields

### Error: "Property does not exist"
**Cause**: Field name doesn't exist in HubSpot
**Fix**:
- Remove linkedin_url (use notes instead)
- Remove custom fields not configured in portal
- Check exact field name spelling

### Error: "INVALID_OPTION"
**Cause**: Enum field received non-allowed value
**Fix**:
- Use exact HubSpot enum values
- Check industry, dealtype, lifecyclestage fields

### Error: "INVALID_INTEGER"
**Cause**: Integer field received string
**Fix**:
- Convert "11-50" to 30 (midpoint)
- Remove commas from numbers

### Error: "READ_ONLY_VALUE"
**Cause**: Attempting to set calculated/system field
**Fix**:
- Remove notes_last_contacted
- Remove hs_lastmodifieddate
- Remove any field ending in "_date" unless explicitly documented as writable

---

## Example Python Implementation

```python
#!/usr/bin/env python3
"""
HubSpot Lead Creation - Brett Walker Account
Implements 6-step process for Brand Scout leads
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"  # Sales Pipeline
STAGE_ID = "1090865183"  # Qualification

def create_company(company_data):
    """Step 3: Create company record"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {'properties': company_data}

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/companies',
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"❌ Company creation failed: {response.status_code}")
        print(response.text)
        return None

def create_contact(contact_data):
    """Step 2: Create contact record"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {'properties': contact_data}

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/contacts',
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"❌ Contact creation failed: {response.status_code}")
        print(response.text)
        return None

def associate_contact_company(contact_id, company_id):
    """Step 4: Associate contact to company"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}/associations/companies/{company_id}/280',
        headers=headers
    )

    return response.status_code in [200, 400]  # 400 = already associated

def create_deal(deal_data):
    """Step 5: Create deal record"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {'properties': deal_data}

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals',
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"❌ Deal creation failed: {response.status_code}")
        print(response.text)
        return None

def associate_deal_company(deal_id, company_id):
    """Associate deal to company"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/companies/{company_id}/341',
        headers=headers
    )

    return response.status_code in [200, 400]

def create_lead_from_research(research_data):
    """
    Main function: Create HubSpot lead from Brand Scout research

    Args:
        research_data (dict): Structured research data with company, contacts, deal info

    Returns:
        dict: Created record IDs and URLs
    """

    print("="*80)
    print("HUBSPOT LEAD CREATION - Brett Walker Account")
    print("="*80)

    # Step 1: Extract data (already done via research_data param)

    # Step 3: Create company (before contacts for cleaner associations)
    print("\n1. Creating company record...")
    company_id = create_company(research_data['company'])
    if not company_id:
        return {"error": "Failed to create company"}
    print(f"   ✅ Company created: {company_id}")

    # Step 2: Create contacts
    print("\n2. Creating contact records...")
    contact_ids = []
    for contact in research_data['contacts']:
        contact_id = create_contact(contact)
        if contact_id:
            contact_ids.append(contact_id)
            print(f"   ✅ Contact created: {contact['firstname']} {contact['lastname']} ({contact_id})")

            # Step 4: Associate to company
            associate_contact_company(contact_id, company_id)

    # Step 5: Create deal
    print("\n3. Creating deal record...")
    deal_id = create_deal(research_data['deal'])
    if not deal_id:
        return {"error": "Failed to create deal"}
    print(f"   ✅ Deal created: {deal_id}")

    # Associate deal
    associate_deal_company(deal_id, company_id)
    for contact_id in contact_ids:
        # Associate deal to contacts (association type 3)
        pass  # Implement if needed

    # Step 6: Log results
    print("\n" + "="*80)
    print("LEAD CREATION COMPLETE")
    print("="*80)

    return {
        "company_id": company_id,
        "contact_ids": contact_ids,
        "deal_id": deal_id,
        "hubspot_urls": {
            "company": f"https://app.hubspot.com/contacts/8210927/company/{company_id}",
            "deal": f"https://app.hubspot.com/contacts/8210927/deal/{deal_id}"
        }
    }
```

---

## Workflow Integration

### Brand Scout → HubSpot Flow
1. **Brand Scout Report** generated (5-section format)
2. **Parse Report** into structured data
3. **Run HubSpot Script** with parsed data
4. **Create Deal Folder** `[00-LEAD]_CompanyName`
5. **Save Brand Scout Report** to deal folder
6. **Update Documentation** (Customer_Relationship.md, README.md)

### Manual Research → HubSpot Flow
1. **Gather Research** (LinkedIn, website, etc.)
2. **Format Data** using Brand Scout template structure
3. **Run HubSpot Script** with formatted data
4. **Create Deal Folder** with standard structure
5. **Document Findings** in deal folder files

---

## Best Practices

### Data Quality
- ✅ Always verify email formats before submission
- ✅ Use company domain for matching (prevents duplicates)
- ✅ Store confidence levels in notes field
- ✅ Document information gaps for discovery

### Field Validation
- ✅ Test industry values against HubSpot list
- ✅ Convert employee ranges to integers (midpoint)
- ✅ Remove read-only fields before API calls
- ✅ Use ISO date format (YYYY-MM-DD)

### Error Recovery
- ✅ Log all API responses for debugging
- ✅ Implement retry logic for rate limits
- ✅ Save raw research data before processing
- ✅ Don't fail entire process for one field error

### Audit Trail
- ✅ Log source of each data point (Brand Scout, manual, etc.)
- ✅ Timestamp all record creations
- ✅ Store research report in deal folder
- ✅ Document confidence levels for inferred data

---

*Process Version 1.0*
*Last Updated: November 13, 2025*
*Owner: Brett Walker (brett.walker@firstmile.com)*
