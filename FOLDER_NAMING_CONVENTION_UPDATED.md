# Folder Naming Convention - Updated
**Date**: October 10, 2025, 12:06 PM
**System**: Nebuchadnezzar v2.0

---

## ✅ Confirmed Folder Structure

### Active Customer Folders
```
[CUSTOMER]_CompanyName/
├── (customer business materials)
└── Win-Back_SubfolderName/
    └── (win-back campaign materials)
```

**Example**:
```
[CUSTOMER]_BoxiiShip_AF/
├── Customer_Profile.md
├── Active_Contracts/
├── Performance_Reports/
└── Win-Back_Make_Wellness_2025/
    ├── README.md
    ├── RATE-1903_Taylar_Response.md
    └── (campaign materials)
```

---

## Complete Folder Naming System

### Pipeline Stage Folders (New Prospects/Deals)
```
[00-LEAD]                   - Initial prospect contact
[01-DISCOVERY-SCHEDULED]    - Meeting booked
[02-DISCOVERY-COMPLETE]     - Requirements gathered
[03-RATE-CREATION]          - Pricing work in progress
[04-PROPOSAL-SENT]          - Rates delivered to customer
[05-SETUP-DOCS-SENT]        - Contracts/setup documents sent
[06-IMPLEMENTATION]         - Onboarding in progress
[07-CLOSED-WON]             - Active customer (use [CUSTOMER] folder instead)
[08-CLOSED-LOST]            - Deal lost (no longer pursuing)
[09-WIN-BACK]               - NEW DEAL for re-engagement (separate prospect)
```

### Customer Folders (Active Business)
```
[CUSTOMER]_CompanyName/     - Active customers (regardless of stage)
```

---

## Key Distinction

### Pipeline Folders = Temporary (Deal Lifecycle)
Deals move through pipeline stages until closed.
Once won, move to customer folder.

### Customer Folders = Permanent (Ongoing Relationship)
Active customers stay in `[CUSTOMER]_` folders.
Win-backs for existing customers = subfolder within customer folder.

---

## When to Use Each

### Use Pipeline Stage Folder When:
- New prospect (never been customer)
- Active sales cycle
- Deal not yet closed
- Example: `[04-PROPOSAL-SENT]_NewProspect_Inc/`

### Use Customer Folder When:
- Active customer (paying, shipping)
- Closed-won deal
- Ongoing business relationship
- Example: `[CUSTOMER]_BoxiiShip_AF/`

### Use Win-Back Subfolder When:
- Customer lost volume to competitor
- Customer wants to win back their end customer
- Expansion opportunity within existing customer
- Example: `[CUSTOMER]_BoxiiShip_AF/Win-Back_Make_Wellness_2025/`

### Use Pipeline [09-WIN-BACK] Folder When:
- Former customer (now completely lost)
- Creating NEW DEAL to win them back as customer
- Example: `[09-WIN-BACK]_FormerCustomer_2025/`

---

## BoxiiShip AF Current Structure

### Confirmed Folder
```
[CUSTOMER]_BoxiiShip_AF/
```

### Next Step
Create win-back subfolder:
```
[CUSTOMER]_BoxiiShip_AF/Win-Back_Make_Wellness_2025/
```

---

## HubSpot → Local Folder Mapping

| HubSpot Stage | Local Folder Type | Example |
|---------------|-------------------|---------|
| [01-06] Any stage | Pipeline folder | `[03-RATE-CREATION]_Prospect/` |
| [07] Started Shipping | Customer folder | `[CUSTOMER]_CompanyName/` |
| [08] Closed Lost | Pipeline folder | `[08-CLOSED-LOST]_LostDeal/` |
| Customer expansion | Customer subfolder | `[CUSTOMER]_Name/Win-Back_Volume/` |

---

## Folder Organization Best Practices

### Pipeline Folders:
- Temporary - deals move through stages
- Delete or archive after closed-won (moved to customer folder)
- Delete or archive after closed-lost (unless win-back planned)

### Customer Folders:
- Permanent - keep as long as customer is active
- Organize by business function (contracts, reports, campaigns)
- Use subfolders for specific initiatives (win-backs, expansions)

### Win-Back Subfolders:
- Specific campaign materials only
- Cross-reference parent customer context
- Track campaign progress and outcomes

---

## Quick Reference

**New Prospect → Customer Journey**:
```
[01-DISCOVERY-SCHEDULED]_NewCo/
    ↓
[03-RATE-CREATION]_NewCo/
    ↓
[04-PROPOSAL-SENT]_NewCo/
    ↓
[07-CLOSED-WON]_NewCo/ (temporary)
    ↓
[CUSTOMER]_NewCo/ (permanent)
```

**Existing Customer Win-Back**:
```
[CUSTOMER]_BoxiiShip_AF/
└── Win-Back_Make_Wellness_2025/
```

**Former Customer Win-Back**:
```
[09-WIN-BACK]_FormerCustomer_2025/
```

---

*Naming Convention Confirmed: 2025-10-10 12:06 PM*
*Standard: [CUSTOMER]_ prefix for all active customers*
