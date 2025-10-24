# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a HubSpot integration repository focused on managing FirstMile leads and deals through the HubSpot MCP (Model Context Protocol) tool. The repository contains documentation and command references for efficient HubSpot API operations.

## Key Components

### HubSpot MCP Integration

The repository uses the HubSpot MCP tool for all API interactions. All HubSpot operations should be performed using the `qm hubspot` commands rather than direct API calls.

### Critical IDs and Configuration

Always use these core IDs when working with HubSpot:
- **Owner ID**: 699257003
- **Pipeline ID**: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

### HubSpot Object Association IDs

When creating associations between HubSpot objects, use these specific IDs:
- CONTACT→COMPANY: 279
- LEAD→CONTACT: 608 (REQUIRED for all lead operations)
- LEAD→COMPANY: 610
- DEAL→COMPANY: 341
- DEAL→CONTACT: 3

### Pipeline Stage IDs

For deal progression, use these exact stage IDs:
- [00/01] Lead: 08d9c411-5e1b-487b-8732-9c2bcbbd0307
- [02] Discovery: d2a08d6f-cc04-4423-9215-594fe682e538
- [03] Rate Creation: e1c4321e-afb6-4b29-97d4-2b2425488535
- [04] Proposal: d607df25-2c6d-4a5d-9835-6ed1e4f4020a
- [05] Setup Docs: 4e549d01-674b-4b31-8a90-91ec03122715
- Closed Won: 3fd46d94-78b4-452b-8704-62a338a210fb
- Closed Lost: 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8

## Common Commands

### Lead Operations
```bash
qm hubspot lead      # Create single BrandScout lead
qm hubspot bulk      # Process multiple leads in batch
qm hubspot search    # Find existing leads
```

### Deal Operations
```bash
qm hubspot deal      # Convert lead to deal (requires existing company/contact)
qm hubspot pipeline  # Move deals through pipeline stages
```

### Engagement Operations
```bash
qm hubspot note      # Add engagement notes to records
```

## Data Input Formats

### BrandScout Lead Structure

When creating leads from BrandScout data, use this JSON structure:

```json
{
  "company": {
    "name": "Company Name",
    "domain": "company.com",  // lowercase, no http://
    "description": "Company description",
    "annual_revenue": "10000000",
    "employee_count": "45",
    "industry": "Ecommerce"
  },
  "contact": {
    "email": "email@company.com",  // lowercase
    "firstname": "First",
    "lastname": "Last",
    "jobtitle": "Title",
    "phone": "+1 XXX-XXX-XXXX"
  },
  "shipping_intel": {
    "ships_physical": true,
    "product_types": "products",
    "estimated_volume": "12000",
    "current_carriers": "UPS; USPS"
  }
}
```

For bulk operations, wrap multiple entries in an array.

## Important Operational Rules

1. **Lead→Contact Association is MANDATORY**: Every lead must have the 608 association to a contact
2. **Deduplication Strategy**: Always search for existing companies by domain and contacts by email before creating new records
3. **Use IDs not Labels**: Always use stage IDs, not stage names when updating deal stages
4. **Data Normalization**: 
   - Domains should be lowercase without protocol
   - Email addresses should be lowercase
5. **API Efficiency**: 
   - Single lead creation: 4-5 API calls
   - Bulk operations (N leads): 6-8 total calls
   - Deal creation: 1 call with inline associations
   - Pipeline updates: Batch up to 100 records

## Output Handling

All HubSpot MCP commands return raw JSON. Expected output formats:

- **Lead Creation**: `{"companyId":"123","contactId":"456","leadId":"789","ownerId":"699257003"}`
- **Bulk Creation**: Contains summary and created IDs arrays
- **Search Results**: Array of matching records with full properties

## Error Handling

Common issues and resolutions:
- Missing Lead→Contact association will cause lead creation to fail
- Duplicate domains/emails should be handled through search-first strategy
- Invalid stage IDs will cause pipeline updates to fail silently