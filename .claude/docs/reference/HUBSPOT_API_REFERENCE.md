# HubSpot API Reference - Gritty-Rain Private App

**Quick Reference Guide for FirstMile Deals HubSpot Integration**

---

## 🔑 Brett Walker Credentials

| Property | Value |
|----------|-------|
| **Name** | Brett Walker |
| **Email** | brett.walker@firstmile.com |
| **Owner/User ID** | `699257003` |
| **Portal ID** | `8210927` |

---

## 🔐 Authentication (Gritty-Rain Private App)

**Auth Method**: Bearer Token
**Header Format**: `Authorization: Bearer pat-na1-d546b...`

**CRITICAL**: Full token stored in `.env` file as `HUBSPOT_API_KEY`
**NEVER** commit the actual token to git!

### Python Usage
```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

---

## 📋 Available API Scopes

### CRM Objects (Read/Write)
✅ Deals: `crm.objects.deals.read`, `crm.objects.deals.write`, `crm.schemas.deals.read`
✅ Contacts: `crm.objects.contacts.read`, `crm.objects.contacts.write`
✅ Companies: `crm.objects.companies.read`, `crm.objects.companies.write`
✅ Owners: `crm.objects.owners.read`
✅ Leads: `crm.objects.leads.read`, `crm.objects.leads.write`
✅ Appointments: `crm.objects.appointments.read`, `crm.objects.appointments.write`

### Email & Communication
✅ Marketing Email: `marketing-email`
✅ Transactional Email: `transactional-email`
✅ Sales Email: `sales-email-read`

### Automation & Sequences
✅ Sequences: `automation.sequences.read`
✅ Sequence Enrollments: `automation.sequences.enrollments.write`
✅ Meeting Links: `scheduler.meetings.meeting-link.read`

### Other
✅ Pipelines: `crm.pipelines.orders.read`
✅ Schemas: `crm.schemas.contacts.read`, `crm.schemas.companies.read`
✅ Actions, Timeline, OAuth

---

## 🎯 Common API Patterns

### 1. Get All Deals for Brett Walker

```http
POST https://api.hubapi.com/crm/v3/objects/deals/search
Authorization: Bearer pat-na1-d546b...
Content-Type: application/json

{
  "filterGroups": [
    {
      "filters": [
        { "propertyName": "hubspot_owner_id", "operator": "EQ", "value": "699257003" }
      ]
    }
  ],
  "properties": [
    "dealname",
    "dealstage",
    "amount",
    "closedate",
    "notes_last_updated",
    "hs_lastmodifieddate",
    "hs_next_step",
    "hs_priority"
  ],
  "limit": 100
}
```

**Python Example**:
```python
import requests

payload = {
    'filterGroups': [{
        'filters': [
            {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': '699257003'}
        ]
    }],
    'properties': ['dealname', 'dealstage', 'amount', 'hs_priority'],
    'limit': 100
}

response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/deals/search',
    headers=headers,
    json=payload,
    timeout=10
)

deals = response.json().get('results', [])
```

### 2. Get Single Deal by ID

```http
GET https://api.hubapi.com/crm/v3/objects/deals/{dealId}
Authorization: Bearer pat-na1-d546b...
```

**Example**: `GET https://api.hubapi.com/crm/v3/objects/deals/43491605362`

### 3. Update Deal Properties

```http
PATCH https://api.hubapi.com/crm/v3/objects/deals/{dealId}
Authorization: Bearer pat-na1-d546b...
Content-Type: application/json

{
  "properties": {
    "dealstage": "08d9c411-5e1b-487b-8732-9c2bcbbd0307",
    "hs_priority": "high",
    "hs_next_step": "Follow up on proposal"
  }
}
```

### 4. Create New Deal

```http
POST https://api.hubapi.com/crm/v3/objects/deals
Authorization: Bearer pat-na1-d546b...
Content-Type: application/json

{
  "properties": {
    "dealname": "Company Name - Service Type",
    "dealstage": "1090865183",
    "amount": "500000",
    "hubspot_owner_id": "699257003",
    "pipeline": "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
  }
}
```

---

## 📊 Key Deal Properties

| Property | Description | Example |
|----------|-------------|---------|
| `dealname` | Deal name | "Stackd Logistics - 20k Monthly Shipments" |
| `dealstage` | Pipeline stage ID | "08d9c411-5e1b-487b-8732-9c2bcbbd0307" |
| `amount` | Deal value (string) | "479171" |
| `hubspot_owner_id` | Owner user ID | "699257003" (Brett Walker) |
| `pipeline` | Pipeline ID | "8bd9336b-4767-4e67-9fe2-35dfcad7c8be" (FM) |
| `hs_priority` | Priority flag | "high", "medium", "low", null |
| `hs_next_step` | Next action | "Follow up on proposal" |
| `notes_last_updated` | Last note timestamp | "2025-11-06T17:00:00Z" |
| `hs_lastmodifieddate` | Last modified | "2025-11-06T18:30:00Z" |
| `createdate` | Created date | "2025-09-17T10:00:00Z" |
| `closedate` | Expected close | "2025-12-31" |

---

## 🔗 Deal Object ID Examples

| Deal Name | Object ID | Owner ID | CRM URL |
|-----------|-----------|----------|---------|
| Logystico LLC - Skupreme | 43491605362 | 699257003 | [View](https://app.hubspot.com/contacts/8210927/record/0-3/43491605362) |
| Flat Fee Shipping | 43827801265 | 699257003 | [View](https://app.hubspot.com/contacts/8210927/record/0-3/43827801265) |
| Upstate Prep - New Deal | 42448709378 | 699257003 | [View](https://app.hubspot.com/contacts/8210927/record/0-3/42448709378) |
| Stackd Logistics - 20k Monthly | 45672180169 | 699257003 | [View](https://app.hubspot.com/contacts/8210927/record/0-3/45672180169) |

**URL Pattern**: `https://app.hubspot.com/contacts/{portal_id}/record/0-3/{deal_object_id}`

---

## 🚀 Rate Limiting

**Burst Limit**: 100 requests per 10 seconds
**Daily Limit**: 150,000 requests per 24 hours

**Implemented in**: `hubspot_sync_core.py` (TokenBucketRateLimiter)

---

## 📁 Related Files

| File | Purpose |
|------|---------|
| `.env` | Contains `HUBSPOT_API_KEY` token (never commit!) |
| `config.py` | Configuration constants and stage mappings |
| `hubspot_sync_core.py` | Shared HubSpot API utilities with rate limiting |
| `.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md` | Pipeline stage IDs and automation rules |
| `.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md` | Workflow integration guide |

---

## 🔧 Code Templates

### Basic Deal Search
```python
from hubspot_sync_core import HubSpotSyncManager

sync = HubSpotSyncManager()
deals = sync.fetch_deals(
    pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be",
    owner_id="699257003"
)
```

### Update Deal Stage
```python
sync.update_deal(
    deal_id="43491605362",
    properties={
        "dealstage": "08d9c411-5e1b-487b-8732-9c2bcbbd0307",
        "hs_priority": "high"
    }
)
```

### Create Contact
```python
contact = sync.create_contact({
    "firstname": "John",
    "lastname": "Smith",
    "email": "john@company.com",
    "company": "Acme Corp"
})
```

---

## ⚠️ Important Notes

1. **NEVER commit API tokens** - Always use `.env` file
2. **Owner ID required** - Use `699257003` for Brett's deals
3. **Deal Object ID is primary key** - Use for all updates/reads
4. **Portal ID** - `8210927` (FirstMile HubSpot account)
5. **Pipeline ID** - `8bd9336b-4767-4e67-9fe2-35dfcad7c8be` (FM pipeline)
6. **Rate limiting** - Use `hubspot_sync_core.py` for automatic rate limit handling
7. **Error handling** - Always use try/except with HubSpot API calls

---

**Last Updated**: 2025-11-06
**Private App**: Gritty-Rain
**Documentation Source**: Brett Walker
