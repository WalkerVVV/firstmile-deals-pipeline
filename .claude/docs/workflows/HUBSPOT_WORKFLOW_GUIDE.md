# HubSpot MCP Workflow Guide
**Complete Integration Reference for Nebuchadnezzar v3.0**

---

## Overview

This guide documents how to use HubSpot MCP tools within the Nebuchadnezzar pipeline system for seamless deal management, from lead creation through closed-won.

### MCP Integration Benefits
- **Direct API Access**: Native HubSpot integration via MCP protocol
- **Automation Ready**: Triggers N8N workflows automatically
- **Zero Context Switching**: Execute from command line or Claude Code
- **Real-time Sync**: Folder movements reflect instantly in HubSpot

---

## Table of Contents

1. [Configuration & Setup](#configuration--setup)
2. [Lead Management Workflows](#lead-management-workflows)
3. [Deal Progression Workflows](#deal-progression-workflows)
4. [Task & Follow-up Automation](#task--follow-up-automation)
5. [Search & Reporting](#search--reporting)
6. [Integration with Daily Syncs](#integration-with-daily-syncs)
7. [Troubleshooting](#troubleshooting)

---

## Configuration & Setup

### Core IDs
```yaml
Owner ID: 699257003  # Brett Walker
Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
Portal ID: 46526832
```

### Stage Mapping (✅ VERIFIED October 7, 2025)
**Source**: Direct HubSpot API Query | **Reference**: [VERIFIED_STAGE_IDS.md](VERIFIED_STAGE_IDS.md)

```python
# Complete verified mapping from HubSpot FM pipeline
STAGE_IDS = {
    "[01-DISCOVERY-SCHEDULED]": "1090865183",
    "[02-DISCOVERY-COMPLETE]": "d2a08d6f-cc04-4423-9215-594fe682e538",
    "[03-RATE-CREATION]": "e1c4321e-afb6-4b29-97d4-2b2425488535",
    "[04-PROPOSAL-SENT]": "d607df25-2c6d-4a5d-9835-6ed1e4f4020a",
    "[05-SETUP-DOCS-SENT]": "4e549d01-674b-4b31-8a90-91ec03122715",
    "[06-IMPLEMENTATION]": "08d9c411-5e1b-487b-8732-9c2bcbbd0307",
    "[07-CLOSED-WON]": "3fd46d94-78b4-452b-8704-62a338a210fb",
    "[08-CLOSED-LOST]": "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8"
}

# Note: [00-LEAD] and [09-WIN-BACK] are local-only (not in HubSpot)
```

### Association Type IDs (✅ VERIFIED)
```python
# Primary associations (verified from HubSpot integration)
ASSOCIATIONS = {
    "CONTACT→COMPANY": 279,
    "LEAD→CONTACT": 608,      # REQUIRED for all lead operations
    "LEAD→COMPANY": 610,
    "DEAL→COMPANY": 341,
    "DEAL→CONTACT": 3,
    "TASK→DEAL": 216          # For follow-up tasks
}

# Legacy associations (verify if still needed):
# "contact_to_deal": 3
# "deal_to_contact": 4
# "company_to_deal": 342
# "deal_to_company": 341
```

### Authentication
```bash
# Initial login (refresh OAuth token)
/login

# Verify authentication
qm hubspot get-deal --deal-id [ANY-DEAL-ID]
```

---

## Lead Management Workflows

### Workflow 1: Single Lead Creation

**Use Case**: BrandScout discovery, cold outreach, referral

**Command**:
```bash
qm hubspot create-lead \
  --first-name "Jordan" \
  --last-name "Blake" \
  --email "ops@acme.com" \
  --company "Acme Corp" \
  --phone "+1-801-555-0200" \
  --website "https://acme.com"
```

**What Happens**:
1. Creates contact record
2. Creates/updates company record
3. Automatically associates contact → company
4. Returns contact ID and company ID

**Follow-up Action**:
```bash
# Add initial note
qm hubspot add-note \
  --contact-id [CONTACT-ID] \
  --note "Source: BrandScout | Interest: High-volume DTC shipping | Next: Discovery call"
```

### Workflow 2: Bulk Lead Processing

**Use Case**: Conference leads, LinkedIn export, purchased list

**Preparation**:
Create CSV with columns:
```
first_name,last_name,email,company,phone,website
John,Smith,john@company.com,Smith LLC,555-123-4567,https://company.com
Jane,Doe,jane@startup.io,Startup Inc,555-987-6543,https://startup.io
```

**Command**:
```bash
qm hubspot bulk-leads --file leads.csv
```

**What Happens**:
1. Reads CSV file
2. Deduplicates by email and domain
3. Creates contacts and companies
4. Associates all relationships
5. Returns summary report

**Best Practices**:
- Clean data before import (lowercase emails, validate phones)
- Include website for company enrichment
- Add source tracking in follow-up notes

### Workflow 3: Lead to Deal Conversion

**Use Case**: Discovery call scheduled, qualified prospect

**Step 1: Verify Contact Exists**
```bash
qm hubspot search-contacts --email "ops@acme.com"
```

**Step 2: Convert to Deal**
```bash
qm hubspot convert-to-deal \
  --contact-id 12345678 \
  --deal-name "Acme Corp - Xparcel Ground" \
  --amount 150000 \
  --stage "[01-DISCOVERY-SCHEDULED]"
```

**Step 3: Create Deal Folder**
```bash
mkdir "[01-DISCOVERY-SCHEDULED]_Acme_Corp"
```

**Step 4: Initialize Folder Structure**
```bash
# Copy template files
cp DEAL_FOLDER_TEMPLATE/CLAUDE.md "[01-DISCOVERY-SCHEDULED]_Acme_Corp/"
cp DEAL_FOLDER_TEMPLATE/Customer_Relationship_Documentation_TEMPLATE.md "[01-DISCOVERY-SCHEDULED]_Acme_Corp/Customer_Relationship_Documentation.md"
```

**What Happens**:
- Deal created in HubSpot with [01-DISCOVERY-SCHEDULED] stage
- Contact and company automatically associated
- Folder movement triggers N8N automation
- Daily sync picks up for 9AM workflow

---

## Deal Progression Workflows

### Workflow 4: Discovery Complete → Rate Creation

**Trigger**: Discovery call done, requirements gathered, data requested

**Step 1: Update Deal Stage**
```bash
# Move folder first (triggers automation)
mv "[01-DISCOVERY-SCHEDULED]_Acme_Corp" "[02-DISCOVERY-COMPLETE]_Acme_Corp"

# Verify HubSpot sync (or update manually)
qm hubspot update-deal \
  --deal-id [DEAL-ID] \
  --stage "[02-DISCOVERY-COMPLETE]"
```

**Step 2: Add Discovery Notes**
```bash
qm hubspot add-note \
  --deal-id [DEAL-ID] \
  --note "Discovery completed. Requirements: 20K pkgs/mo, <1lb average, CA→East Coast heavy. Data requested via email."
```

**Step 3: Create Follow-up Task**
```bash
qm hubspot create-task \
  --deal-id [DEAL-ID] \
  --title "Follow up on PLD data request" \
  --due-date "2025-10-14" \
  --priority "HIGH"
```

**Step 4: Update Customer Relationship Doc**
```markdown
<!-- In Customer_Relationship_Documentation.md -->

## Discovery Call - Oct 7, 2025

**Attendees**: Jordan Blake (Ops Director), Brett Walker (FirstMile)

**Key Requirements**:
- Volume: ~20,000 packages/month
- Weight: Majority <1 lb (apparel)
- Geography: CA warehouse → East Coast heavy
- Pain Points: UPS costs, slow transit to NYC/BOS
- Timeline: Needs solution by Q4 peak

**Next Steps**:
- Data requested: 3 months PLD from current carrier
- Follow-up: Oct 14 (7 days)
```

### Workflow 5: Rate Creation → Proposal Sent

**Trigger**: Rates completed, ready to send

**Step 1: Move to Rate Creation (if not already)**
```bash
mv "[02-DISCOVERY-COMPLETE]_Acme_Corp" "[03-RATE-CREATION]_Acme_Corp"
```

**Step 2: Run Analysis Scripts**
```bash
cd "[03-RATE-CREATION]_Acme_Corp"
python pld_analysis.py
python apply_firstmile_rates.py
python create_pricing_matrix.py
```

**Step 3: Move to Proposal Sent**
```bash
# After rates sent to customer
mv "[03-RATE-CREATION]_Acme_Corp" "[04-PROPOSAL-SENT]_Acme_Corp"

qm hubspot update-deal \
  --deal-id [DEAL-ID] \
  --stage "[04-PROPOSAL-SENT]"
```

**Step 4: Add Proposal Note**
```bash
qm hubspot add-note \
  --deal-id [DEAL-ID] \
  --note "Rate card v1 sent via email. Showing 42% savings ($120K annual). Highlighted Select Network zone-skipping for East Coast. Next: Schedule review call."
```

**Step 5: Set Follow-up Sequence**
```bash
# Day 7 follow-up
qm hubspot create-task \
  --deal-id [DEAL-ID] \
  --title "Follow up on rate card review" \
  --due-date "2025-10-21" \
  --priority "MEDIUM"

# Day 14 follow-up
qm hubspot create-task \
  --deal-id [DEAL-ID] \
  --title "Second follow-up on proposal" \
  --due-date "2025-10-28" \
  --priority "HIGH"
```

### Workflow 6: Verbal Commit → Setup Docs

**Trigger**: Customer verbally commits, ready for onboarding

**Command Sequence**:
```bash
# Move folder
mv "[04-PROPOSAL-SENT]_Acme_Corp" "[05-SETUP-DOCS-SENT]_Acme_Corp"

# Update HubSpot
qm hubspot update-deal \
  --deal-id [DEAL-ID] \
  --stage "[05-SETUP-DOCS-SENT]"

# Add commitment note
qm hubspot add-note \
  --deal-id [DEAL-ID] \
  --note "Verbal commitment received! Jordan approved $150K annual. Setup docs sent to ops@acme.com and finance@acme.com. Target go-live: Nov 1."

# Create implementation tasks
qm hubspot create-task \
  --deal-id [DEAL-ID] \
  --title "Verify setup docs signed" \
  --due-date "2025-10-21" \
  --priority "HIGH"

qm hubspot create-task \
  --deal-id [DEAL-ID] \
  --title "Schedule API integration kickoff" \
  --due-date "2025-10-23" \
  --priority "MEDIUM"
```

### Workflow 7: Go Live → Closed Won

**Trigger**: Customer shipping live with FirstMile

**Command Sequence**:
```bash
# Move folder
mv "[06-IMPLEMENTATION]_Acme_Corp" "[07-CLOSED-WON]_Acme_Corp"

# Update to Closed Won
qm hubspot update-deal \
  --deal-id [DEAL-ID] \
  --stage "[07-CLOSED-WON]"

# Add win note with details
qm hubspot add-note \
  --deal-id [DEAL-ID] \
  --note "🎯 CLOSED WON! First shipments processed Oct 30. Integration complete, tracking verified. ARR: $150K. Handoff to Customer Success team for onboarding support."
```

**Post-Win Actions**:
1. Archive deal folder or move to Customer Success system
2. Update `_PIPELINE_TRACKER.csv` with win details
3. Capture learnings in EOD sync
4. Add to weekly win report

---

## Task & Follow-up Automation

### Task Creation Patterns

#### Pattern 1: Stage-Based Follow-ups
```python
# Automatic task creation based on stage
TASK_TEMPLATES = {
    "[02-DISCOVERY-COMPLETE]": {
        "subject": "Follow up on PLD data request",
        "due_days": 7,
        "priority": "HIGH"
    },
    "[03-RATE-CREATION]": {
        "subject": "Check rate creation status",
        "due_days": 14,
        "priority": "HIGH"
    },
    "[04-PROPOSAL-SENT]": {
        "subject": "Follow up on proposal",
        "due_days": 7,
        "priority": "MEDIUM"
    }
}
```

**Automated via**:
```bash
python daily_9am_sync.py  # Creates missing tasks
```

#### Pattern 2: Manual Task Creation
```bash
# Standard follow-up
qm hubspot create-task \
  --deal-id [ID] \
  --title "Call Jordan re: rate questions" \
  --due-date "2025-10-15" \
  --priority "HIGH" \
  --type "TODO"

# Email follow-up
qm hubspot create-task \
  --deal-id [ID] \
  --title "Email: Proposal review" \
  --due-date "2025-10-15" \
  --priority "MEDIUM" \
  --type "EMAIL"
```

#### Pattern 3: Bulk Task Creation (Monday Setup)
```python
# Example: Create all Monday tasks from EOD sync
tasks = [
    {"deal": "Stackd", "title": "Proposal presentation prep", "date": "2025-10-07"},
    {"deal": "Driftaway", "title": "Recovery call", "date": "2025-10-07"},
    {"deal": "DYLN", "title": "Brock data follow-up", "date": "2025-10-07"}
]

for task in tasks:
    qm hubspot create-task \
      --deal-id task["deal_id"] \
      --title task["title"] \
      --due-date task["date"] \
      --priority "HIGH"
```

### Follow-up SLA by Stage

| Stage | First Follow-up | Second Follow-up | Escalation |
|-------|----------------|------------------|------------|
| [01-DISCOVERY-SCHEDULED] | 3 days before call | 1 day before | N/A |
| [02-DISCOVERY-COMPLETE] | 7 days | 14 days | 30 days |
| [03-RATE-CREATION] | 7 days | 14 days | **Immediate** |
| [04-PROPOSAL-SENT] | 7 days | 14 days | 30 days |
| [05-SETUP-DOCS-SENT] | 7 days | 14 days | **Immediate** |
| [06-IMPLEMENTATION] | 7 days | 14 days | 21 days |

---

## Search & Reporting

### Deal Searches

#### Search by Owner (All My Deals)
```bash
qm hubspot search-deals \
  --owner-id 699257003 \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

#### Search by Stage
```bash
qm hubspot search-deals \
  --stage "[03-RATE-CREATION]" \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

#### Search by Amount (High Value Deals)
```bash
# Search deals >$500K
qm hubspot search-deals \
  --min-amount 500000 \
  --owner-id 699257003
```

#### Search by Company Name
```bash
qm hubspot search-deals \
  --company "Acme Corp"
```

### Contact Searches

#### Search by Email
```bash
qm hubspot search-contacts --email "ops@acme.com"
```

#### Search by Company
```bash
qm hubspot search-contacts --company "Acme Corp"
```

### Custom Filters (Python API)
```python
import requests

# Complex search: Deals in [03] or [04] over 14 days old
payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": "699257003"},
            {"propertyName": "dealstage", "operator": "IN", "values": ["1090865183", "d607df25-2c6d-4a5d-9835-6ed1e4f4020a"]},
            {"propertyName": "hs_lastmodifieddate", "operator": "LT", "value": "2025-09-23"}  # 14 days ago
        ]
    }],
    "properties": ["dealname", "dealstage", "amount", "hs_lastmodifieddate"],
    "limit": 100
}

response = requests.post(
    "https://api.hubapi.com/crm/v3/objects/deals/search",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json=payload
)
```

---

## Integration with Daily Syncs

### 9AM Sync Integration

**Script**: `daily_9am_workflow.py`

**HubSpot Queries**:
1. Fetch all active deals by owner + pipeline
2. Group by stage
3. Calculate urgency scores
4. Generate priority action list

**Output**: Priority-ranked deals with next steps

### NOON Sync Integration

**Manual Check**:
```bash
# Quick pipeline health
python hubspot_pipeline_verify.py

# Detailed sync verification
python pipeline_sync_verification.py
```

### EOD Sync Integration

**HubSpot Updates**:
1. Add notes for all customer touchpoints
2. Update deal properties (last contact date)
3. Create tomorrow's tasks
4. Log activities for audit trail

**Command Pattern**:
```bash
# After customer call
qm hubspot add-note \
  --deal-id [ID] \
  --note "[Call Summary] Discussed pricing concerns, Jordan needs CFO approval. Follow-up: Oct 14."

# Create next task
qm hubspot create-task \
  --deal-id [ID] \
  --title "Follow up post-CFO approval" \
  --due-date "2025-10-14"
```

### Folder Movement Triggers

**Automation Flow**:
```
1. Move folder: [03]_Acme → [04]_Acme
2. N8N detects file system change
3. N8N updates _PIPELINE_TRACKER.csv
4. N8N calls HubSpot API to update deal stage
5. HubSpot stage change triggers email sequence
6. Daily sync verifies alignment
```

**Manual Verification**:
```bash
python pipeline_sync_verification.py
```

**Output**:
```
[03-RATE-CREATION]       HubSpot: 8    Local: 8    ✅ SYNCED
[04-PROPOSAL-SENT]       HubSpot: 3    Local: 4    ⚠️ +1 LOCAL
```

---

## Troubleshooting

### Issue 1: 401 Authentication Error

**Symptoms**:
```
Error: 401 Unauthorized
OAuth token has expired
```

**Fix**:
```bash
# Refresh token
/login

# Verify authentication
qm hubspot get-deal --deal-id [ANY-ID]

# Retry operation
```

### Issue 2: Deal Not Found

**Symptoms**:
```
Error: 404 Not Found
Deal ID [12345] does not exist
```

**Fix**:
```bash
# Search for deal by name
qm hubspot search-deals --company "Acme Corp"

# Verify deal is in correct pipeline
qm hubspot get-deal --deal-id [ID]
```

### Issue 3: Folder/HubSpot Mismatch

**Symptoms**:
Pipeline sync shows discrepancies

**Fix**:
```bash
# Run detailed verification
python pipeline_sync_verification.py

# Review mismatch report
# Manually reconcile:

# Option A: Update HubSpot to match folder
qm hubspot update-deal --deal-id [ID] --stage "[CORRECT-STAGE]"

# Option B: Move folder to match HubSpot
mv "[WRONG-STAGE]_Company" "[CORRECT-STAGE]_Company"
```

### Issue 4: Missing Tasks

**Symptoms**:
Deals in priority stages without follow-up tasks

**Fix**:
```bash
# Run task verification and auto-creation
python daily_9am_sync.py

# Verify tasks created
qm hubspot search-tasks --deal-id [ID]
```

### Issue 5: Association Failures

**Symptoms**:
Task created but not linked to deal

**Fix**:
```python
# Manual association via API
import requests

task_id = "123456"
deal_id = "789012"

response = requests.put(
    f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json=[{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216  # Task to Deal
    }]
)
```

---

## Quick Reference Card

### Common Commands
```bash
# Lead Creation
qm hubspot create-lead --first-name "[NAME]" --last-name "[NAME]" --email "[EMAIL]" --company "[COMPANY]"

# Deal Conversion
qm hubspot convert-to-deal --contact-id [ID] --deal-name "[NAME]" --amount [VALUE] --stage "[STAGE]"

# Stage Update
qm hubspot update-deal --deal-id [ID] --stage "[NEW-STAGE]"

# Add Note
qm hubspot add-note --deal-id [ID] --note "[TEXT]"

# Create Task
qm hubspot create-task --deal-id [ID] --title "[TITLE]" --due-date "YYYY-MM-DD" --priority "HIGH"

# Search Deals
qm hubspot search-deals --owner-id 699257003 --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

### Daily Sync Scripts
```bash
python daily_9am_workflow.py           # Priority action list
python daily_9am_sync.py               # Task verification
python pipeline_sync_verification.py   # Folder ↔ HubSpot sync
python hubspot_pipeline_verify.py      # Pipeline health check
```

### Stage IDs (Quick Copy)
```
[01-DISCOVERY-SCHEDULED]: d2a08d6f-cc04-4423-9215-594fe682e538
[02-DISCOVERY-COMPLETE]: e1c4321e-afb6-4b29-97d4-2b2425488535
[03-RATE-CREATION]: 1090865183
[04-PROPOSAL-SENT]: d607df25-2c6d-4a5d-9835-6ed1e4f4020a
[06-IMPLEMENTATION]: 08d9c411-5e1b-487b-8732-9c2bcbbd0307
[07-CLOSED-WON]: 3fd46d94-78b4-452b-8704-62a338a210fb
[08-CLOSED-LOST]: 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8
[09-WIN-BACK]: 4e549d01-674b-4b31-8a90-91ec03122715
```

---

## Best Practices Summary

1. **Always Read Before Write**: Use `qm hubspot get-deal` before updates
2. **Folder Movement First**: Move folder, then verify HubSpot sync
3. **Note Everything**: Every customer touchpoint gets a HubSpot note
4. **Task-Driven Follow-ups**: Create tasks immediately, don't rely on memory
5. **Daily Sync Verification**: Run `pipeline_sync_verification.py` daily
6. **Stage IDs Not Labels**: Use stage IDs in automation scripts
7. **Association Type Correctness**: Verify association type IDs in API calls
8. **Error Recovery**: Log all errors, retry with fresh auth token

---

**Last Updated**: October 7, 2025
**System**: Nebuchadnezzar v3.0
**Integration**: HubSpot MCP via Claude Code
