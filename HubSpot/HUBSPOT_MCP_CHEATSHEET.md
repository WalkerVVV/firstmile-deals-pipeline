# 🚀 HUBSPOT MCP QUICK COMMAND CHEAT SHEET

## CORE IDS (Always Used)
```
Owner: 699257003
Pipeline: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

## QUICK COMMANDS
```bash
qm hubspot lead      # Single BrandScout → Lead creation
qm hubspot bulk      # Multiple leads batch processing  
qm hubspot deal      # Convert to Deal (needs company/contact)
qm hubspot note      # Add engagement note to records
qm hubspot pipeline  # Move deals through stages
qm hubspot search    # Find existing leads
```

## ASSOCIATION IDS
```javascript
CONTACT→COMPANY: 279
LEAD→CONTACT: 608 (required)
LEAD→COMPANY: 610
DEAL→COMPANY: 341
DEAL→CONTACT: 3
```

## STAGE IDS
```javascript
[00/01] Lead:         08d9c411-5e1b-487b-8732-9c2bcbbd0307
[02] Discovery:       d2a08d6f-cc04-4423-9215-594fe682e538
[03] Rate Creation:   e1c4321e-afb6-4b29-97d4-2b2425488535
[04] Proposal:        d607df25-2c6d-4a5d-9835-6ed1e4f4020a
[05] Setup Docs:      4e549d01-674b-4b31-8a90-91ec03122715
Closed Won:           3fd46d94-78b4-452b-8704-62a338a210fb
Closed Lost:          02d8a1d7-d0b3-41d9-adc6-44ab768a61b8
```

## INPUT FORMATS

### BRANDSCOUT (Single):
```json
{
  "company": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "description": "Leading widget manufacturer",
    "annual_revenue": "10000000",
    "employee_count": "45",
    "industry": "Ecommerce"
  },
  "contact": {
    "email": "ops@acme.com",
    "firstname": "Jordan",
    "lastname": "Blake",
    "jobtitle": "Director of Ops",
    "phone": "+1 801-555-0200"
  },
  "shipping_intel": {
    "ships_physical": true,
    "product_types": "widgets",
    "estimated_volume": "12000",
    "current_carriers": "UPS; USPS"
  }
}
```

### BRANDSCOUT_LIST (Bulk):
```json
[
  {/* same structure as above */},
  {/* another entry */}
]
```

## OUTPUT FORMATS

### Lead Creation:
```json
{"companyId":"123","contactId":"456","leadId":"789","ownerId":"699257003"}
```

### Bulk Creation:
```json
{"summary":{"companiesCreated":2,"contactsCreated":2,"leadsCreated":2},"created":{"companyIds":["123","124"],"contactIds":["456","457"],"leadIds":["789","790"]}}
```

## API CALL EFFICIENCY
- **Single Lead**: 4-5 calls
- **Bulk (N leads)**: 6-8 calls total
- **Deal Creation**: 1 call with inline associations
- **Note Creation**: 1 call (legacy engagement API)
- **Pipeline Update**: 1 call (batch up to 100)

## DEDUPLICATION STRATEGY
1. Search company by domain
2. Search contact by email  
3. Create only if not found
4. Associate if existing

## CRITICAL RULES
- ✅ Lead→Contact association (608) is REQUIRED
- ✅ Use IDs not labels for stages
- ✅ Domain = lowercase, no http://
- ✅ Email = lowercase
- ✅ All commands return raw JSON only