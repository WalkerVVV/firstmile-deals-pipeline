# NEBUCHADNEZZAR v2.0 - System Reference Guide

## System Overview

The Nebuchadnezzar v3.0 is a fully automated 10-stage pipeline consciousness for FirstMile Deals management. Zero manual data entry, real-time tracking via folder movement, N8N automation, and HubSpot CRM integration.

---

## Critical System IDs

### HubSpot Configuration
```yaml
Owner ID: 699257003  # Brett Walker
Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
Portal ID: 46526832
```

### Association Type IDs (HubSpot API)
```yaml
# VERIFIED FROM HUBSPOT INTEGRATION
CONTACT→COMPANY: 279
LEAD→CONTACT: 608  # REQUIRED for all lead operations
LEAD→COMPANY: 610
DEAL→COMPANY: 341
DEAL→CONTACT: 3

# Legacy associations (verify if still needed):
Contact to Deal: 3
Deal to Contact: 4
Company to Deal: 342
Deal to Company: 341
Contact to Company: 1
Company to Contact: 2
Task to Deal: 216  # Used for creating follow-up tasks
```

### Pipeline Stage IDs
```yaml
# VERIFIED STAGE IDs - Source: HubSpot API /crm/v3/pipelines/deals/{pipeline_id}
# Last Updated: 2025-10-10
# Pipeline Name: "FM" (FirstMile)
# Total Stages: 8 (NOT 10 as previously documented)

# ACTUAL HUBSPOT PIPELINE STAGES:
[01] Discovery Scheduled:  1090865183
[02] Discovery Complete:   d2a08d6f-cc04-4423-9215-594fe682e538
[03] Rate Creation:        e1c4321e-afb6-4b29-97d4-2b2425488535
[04] Proposal Sent:        d607df25-2c6d-4a5d-9835-6ed1e4f4020a
[05] Setup Docs Sent:      4e549d01-674b-4b31-8a90-91ec03122715
[06] Implementation:       08d9c411-5e1b-487b-8732-9c2bcbbd0307
[07] Started Shipping:     3fd46d94-78b4-452b-8704-62a338a210fb  # This is "Closed Won"
[08] Closed Lost:          02d8a1d7-d0b3-41d9-adc6-44ab768a61b8

# IMPORTANT NOTES:
# - NO [00-LEAD] stage exists in HubSpot (use [01] Discovery Scheduled)
# - NO [09-WIN-BACK] stage exists (would need to be created manually)
# - Stage 7 is labeled "Started Shipping" in HubSpot (functionally "Closed Won")
# - Use stage names exactly as shown above for consistency

# Python Dictionary (for all scripts):
STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
}
```

---

## Quick Command Reference

### HubSpot Lead Management

#### Create Single Lead
```bash
qm hubspot create-lead \
  --first-name "John" \
  --last-name "Smith" \
  --email "john@company.com" \
  --company "Acme Corp" \
  --phone "555-123-4567" \
  --website "https://acme.com"
```

#### Bulk Lead Processing
```bash
# From CSV with columns: first_name, last_name, email, company, phone, website
qm hubspot bulk-leads --file leads.csv
```

#### Create Lead with Company Association
```bash
qm hubspot create-lead \
  --first-name "Jane" \
  --last-name "Doe" \
  --email "jane@startup.io" \
  --company "Startup LLC" \
  --associate-company
```

### HubSpot Deal Management

#### Convert Lead to Deal
```bash
qm hubspot convert-to-deal \
  --contact-id 12345 \
  --deal-name "Acme Corp - Xparcel Ground" \
  --amount 150000 \
  --stage "[02-DISCOVERY-COMPLETE]"
```

#### Update Deal Stage
```bash
qm hubspot update-deal \
  --deal-id 67890 \
  --stage "[04-PROPOSAL-SENT]"
```

#### Add Deal Note
```bash
qm hubspot add-note \
  --deal-id 67890 \
  --note "Sent rate card v2.1 with 40% savings projection"
```

#### Create Deal Task
```bash
qm hubspot create-task \
  --deal-id 67890 \
  --title "Follow up on rate card" \
  --due-date "2025-10-15" \
  --priority "HIGH"
```

### HubSpot Search & Reporting

#### Search Deals by Owner
```bash
qm hubspot search-deals \
  --owner-id 699257003 \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

#### Search Deals by Stage
```bash
qm hubspot search-deals \
  --stage "[03-RATE-CREATION]" \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

#### Get Deal Details
```bash
qm hubspot get-deal --deal-id 67890
```

#### List All Pipeline Stages
```bash
qm hubspot list-stages --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

---

## Daily Sync Flow Structure

### 9AM SYNC - Day Start
```yaml
Phase 0: Weekend/Previous Day Learnings
  - Load EOD learnings from previous session
  - Apply documented best practices
  - Review critical insights

Phase 1: Context from Previous Session
  - Pending customer responses (list all)
  - Active blockers (prioritize)
  - Expected deliverables due today

Phase 2: Live Pipeline Sync
  - Query HubSpot for current deal count
  - Stage breakdown summary
  - Identify deals approaching SLA thresholds

Phase 3: Priority Analysis
  Priority 1 - Immediate Actions:
    - Check email for pending responses
    - Resolve active blockers
    - Time-sensitive follow-ups

  Priority 2 - Active Deal Follow-ups:
    - Deals in [03-RATE-CREATION] > 14 days
    - Deals in [04-PROPOSAL-SENT] > 30 days
    - Win-back opportunities

Phase 4: Action Generation
  - HubSpot tasks due today
  - Recommended actions with context
  - Email templates needed

Phase 5: Pipeline Health
  - Critical deals this week
  - SLA violations
  - Stage bottlenecks

Next Sync: Specify time (typically NOON)
```

### NOON SYNC - Midday Progress
```yaml
Phase 1: Morning Execution Review
  - Completed actions from 9AM sync
  - New customer responses received
  - Updated blocker status

Phase 2: Pipeline Changes
  - Deals moved between stages
  - New leads created
  - Lost/won deals

Phase 3: Afternoon Priorities
  - Remaining actions from morning
  - New urgent items
  - Prep for EOD

Next Sync: 5PM EOD
```

### 5PM EOD SYNC - End of Day
```yaml
Phase 1: Daily Summary
  - Total actions completed
  - Customer touchpoints
  - Pipeline movements

Phase 2: Learnings & Insights
  - What worked well today
  - What to improve
  - New best practices discovered

Phase 3: Tomorrow's Setup
  - Known meetings/calls scheduled
  - Expected deliverables
  - Pending responses to monitor

Phase 4: Archive & Handoff
  - Save learnings to memory
  - Update FOLLOW_UP_REMINDERS.txt
  - Note any blockers for tomorrow
```

---

## Automation System Components

### Core Files & Locations

#### Desktop (User Interface)
```
AUTOMATION_MONITOR_LOCAL.html    # Real-time dashboard
NEBUCHADNEZZAR_CONTROL.bat      # System control panel
```

#### Downloads Folder (Data Files)
```
_PIPELINE_TRACKER.csv           # Master pipeline database
_DAILY_LOG.md                   # Activity log
FOLLOW_UP_REMINDERS.txt         # Action queue
```

#### FirstMile_Deals Root (Deal Folders)
```
[00-LEAD]_CompanyName/
[01-DISCOVERY-SCHEDULED]_CompanyName/
[02-DISCOVERY-COMPLETE]_CompanyName/
[03-RATE-CREATION]_CompanyName/
[04-PROPOSAL-SENT]_CompanyName/
[05-SETUP-DOCS-SENT]_CompanyName/
[06-IMPLEMENTATION]_CompanyName/
[07-CLOSED-WON]_CompanyName/
[08-CLOSED-LOST]_CompanyName/
[09-WIN-BACK]_CompanyName/
```

### Watch Folder Configuration
```yaml
Root: C:\Users\BrettWalker\FirstMile_Deals\
Polling Interval: 60 seconds
Trigger: Folder rename or move
Action: Update _PIPELINE_TRACKER.csv + HubSpot sync
```

---

## Pipeline Stage Definitions

### [00-LEAD] - Initial Contact
```yaml
Entry Criteria: First contact established
Automation: None (manual only)
Follow-up SLA: No automation
Exit Criteria: Discovery call scheduled
```

### [01-DISCOVERY-SCHEDULED] - Meeting Booked
```yaml
Entry Criteria: Discovery call scheduled
Automation: Stale deal reminder (14 days)
Follow-up SLA: 14 days
Exit Criteria: Discovery call completed
```

### [02-DISCOVERY-COMPLETE] - Requirements Gathered
```yaml
Entry Criteria: Discovery call done, requirements documented
Automation: 30-day follow-up reminder
Follow-up SLA: 30 days
Exit Criteria: Data received or rate creation started
```

### [03-RATE-CREATION] - Pricing in Progress
```yaml
Entry Criteria: Data received or rate work begun
Automation: 14-day reminder (BOTTLENECK STAGE)
Follow-up SLA: 14 days (critical)
Exit Criteria: Rates completed and sent to customer
Critical: Monitor for SLA violations (>14 days)
```

### [04-PROPOSAL-SENT] - Rates Delivered
```yaml
Entry Criteria: Rate card sent to customer
Automation: 30-day follow-up reminder
Follow-up SLA: 30 days
Exit Criteria: Verbal commit or lost
```

### [05-SETUP-DOCS-SENT] - Verbal Commitment
```yaml
Entry Criteria: Customer verbal commit, docs sent
Automation: 14-day reminder
Follow-up SLA: 14 days
Exit Criteria: Customer live or implementation stalled
```

### [06-IMPLEMENTATION] - Onboarding Active
```yaml
Entry Criteria: Customer onboarding in progress
Automation: 30-day check-in
Follow-up SLA: 30 days
Exit Criteria: Customer live (move to [07-CLOSED-WON])
```

### [07-CLOSED-WON] - Active Customer
```yaml
Entry Criteria: Customer shipping live
Automation: Move to Customer Success tracking
Follow-up SLA: N/A (CS owns)
Action: Archive deal folder or move to CS system
```

### [08-CLOSED-LOST] - Lost Deal
```yaml
Entry Criteria: Customer declined or went with competitor
Automation: Optional follow-up date
Follow-up SLA: Custom (or none)
Action: Document loss reason, save for win-back
```

### [09-WIN-BACK] - Re-engagement
```yaml
Entry Criteria: Lost customer re-engaged
Automation: Monthly check-in
Follow-up SLA: 30 days
Exit Criteria: Move to [02] if re-qualified
```

---

## HubSpot API Patterns

### Search All Deals for Brett Walker
```python
import requests

url = "https://api.hubapi.com/crm/v3/objects/deals/search"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": "699257003"},
            {"propertyName": "pipeline", "operator": "EQ", "value": "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"}
        ]
    }],
    "properties": ["dealname", "dealstage", "amount", "closedate"],
    "limit": 100
}
response = requests.post(url, headers=headers, json=payload)
```

### Get Deals by Stage
```python
payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "pipeline", "operator": "EQ", "value": "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"},
            {"propertyName": "dealstage", "operator": "EQ", "value": "STAGE_ID_HERE"}
        ]
    }],
    "properties": ["dealname", "amount", "closedate", "hs_lastmodifieddate"],
    "limit": 100
}
```

### Create Deal with Associations
```python
# 1. Create the deal
deal_payload = {
    "properties": {
        "dealname": "Acme Corp - Xparcel Ground",
        "dealstage": "STAGE_ID",
        "pipeline": "8bd9336b-4767-4e67-9fe2-35dfcad7c8be",
        "amount": "150000",
        "hubspot_owner_id": "699257003"
    }
}
deal_response = requests.post(
    "https://api.hubapi.com/crm/v3/objects/deals",
    headers=headers,
    json=deal_payload
)
deal_id = deal_response.json()["id"]

# 2. Associate with contact
assoc_payload = [{
    "from": {"id": deal_id},
    "to": {"id": contact_id},
    "type": "deal_to_contact"  # Association type ID: 4
}]
requests.put(
    f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/4",
    headers=headers
)
```

---

## Sync Flow HubSpot Queries

### Query 1: Get All Active Deals
```bash
qm hubspot search-deals \
  --owner-id 699257003 \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be \
  --properties dealname,dealstage,amount,hs_lastmodifieddate
```

### Query 2: Get Stage Breakdown
```bash
# Run for each stage to get counts
for stage in "[02-DISCOVERY-COMPLETE]" "[03-RATE-CREATION]" "[04-PROPOSAL-SENT]" "[05-SETUP-DOCS-SENT]"
do
  qm hubspot search-deals --stage "$stage" --count-only
done
```

### Query 3: Get SLA Violations (Deals >14 Days in Stage)
```bash
# Use hs_lastmodifieddate filter
qm hubspot search-deals \
  --stage "[03-RATE-CREATION]" \
  --modified-before "2025-09-23"  # 14 days ago from today
```

### Query 4: Get Tasks Due Today
```bash
qm hubspot search-tasks \
  --owner-id 699257003 \
  --due-date "2025-10-07" \
  --status "NOT_STARTED"
```

---

## Critical Workflows

### New Lead → Deal Conversion
```bash
# Step 1: Create lead
qm hubspot create-lead \
  --first-name "John" \
  --last-name "Smith" \
  --email "john@company.com" \
  --company "Acme Corp" \
  --phone "555-123-4567"

# Step 2: Get contact ID from response
CONTACT_ID=12345

# Step 3: Convert to deal
qm hubspot convert-to-deal \
  --contact-id $CONTACT_ID \
  --deal-name "Acme Corp - eCommerce Shipping" \
  --amount 150000 \
  --stage "[01-DISCOVERY-SCHEDULED]"

# Step 4: Create folder
mkdir "[01-DISCOVERY-SCHEDULED]_Acme_Corp"

# Step 5: Add notes/tasks in HubSpot
qm hubspot add-note \
  --deal-id $DEAL_ID \
  --note "Discovery call scheduled for 10/15/2025"
```

### Deal Stage Movement
```bash
# Step 1: Move folder
mv "[03-RATE-CREATION]_Acme_Corp" "[04-PROPOSAL-SENT]_Acme_Corp"

# Step 2: Update HubSpot (automation handles, or manual)
qm hubspot update-deal \
  --deal-id 67890 \
  --stage "[04-PROPOSAL-SENT]"

# Step 3: Create follow-up task
qm hubspot create-task \
  --deal-id 67890 \
  --title "Follow up on rate card (30 days)" \
  --due-date "2025-11-06"
```

### Rate Creation Workflow
```bash
# Step 1: Receive customer data
# Step 2: Run PLD analysis
python "[03-RATE-CREATION]_Acme_Corp/pld_analysis.py"

# Step 3: Apply FirstMile rates
python "[03-RATE-CREATION]_Acme_Corp/apply_firstmile_rates.py"

# Step 4: Generate pricing matrix
python "[03-RATE-CREATION]_Acme_Corp/create_pricing_matrix.py"

# Step 5: Create revenue projection
python "[03-RATE-CREATION]_Acme_Corp/revenue_calculator.py"

# Step 6: Send to customer
# Step 7: Move to [04-PROPOSAL-SENT]
mv "[03-RATE-CREATION]_Acme_Corp" "[04-PROPOSAL-SENT]_Acme_Corp"

# Step 8: Update HubSpot
qm hubspot update-deal --deal-id 67890 --stage "[04-PROPOSAL-SENT]"
```

---

## Pipeline Health Monitoring

### Daily Health Check
```bash
# Run at 9AM, NOON, 5PM
qm hubspot search-deals --owner-id 699257003 --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

### SLA Violation Detection
```yaml
Stage: [03-RATE-CREATION]
SLA: 14 days
Query: Deals with hs_lastmodifieddate > 14 days ago
Action: Prioritize in sync flow

Stage: [04-PROPOSAL-SENT]
SLA: 30 days
Query: Deals with hs_lastmodifieddate > 30 days ago
Action: Follow-up email or phone call
```

### Bottleneck Identification
```yaml
Monitor: Deal count by stage
Alert If:
  - [03-RATE-CREATION] > 10 deals
  - Any deal in [03] > 14 days
  - Any deal in [04] > 30 days
  - [05-SETUP-DOCS-SENT] > 14 days
```

---

## Best Practices from Field

### Email Communication
- Short, dedicated emails for critical asks (dimension requests, data needs)
- Pre-check internal dependencies before customer communication
- Use templates but personalize for context

### Deal Management
- Create Customer Relationship Docs for all qualified deals
- Ask about additional locations/brands in discovery calls
- Document loss reasons immediately in [08-CLOSED-LOST]

### Rate Creation (Bottleneck Stage)
- Start data analysis immediately upon receipt
- Flag internal blockers (missing data, JIRA delays) in HubSpot notes
- Target <7 day turnaround for competitive advantage

### Follow-up Timing
- [01-DISCOVERY-SCHEDULED]: 3 days before call, 1 day reminder
- [02-DISCOVERY-COMPLETE]: 7 days post-call if no data received
- [03-RATE-CREATION]: Daily internal check, weekly customer update
- [04-PROPOSAL-SENT]: 7 days, 14 days, 30 days cadence
- [05-SETUP-DOCS-SENT]: 7 days, 14 days (urgent)

---

## Integration Points

### N8N Workflows
```yaml
Workflow 1: Folder Movement Detection
  Trigger: File system watcher
  Action: Update _PIPELINE_TRACKER.csv
  Frequency: 60 second polling

Workflow 2: HubSpot Sync
  Trigger: _PIPELINE_TRACKER.csv change
  Action: Update deal stage in HubSpot
  Frequency: On change

Workflow 3: Follow-up Reminders
  Trigger: Daily 9AM cron
  Action: Generate FOLLOW_UP_REMINDERS.txt
  Frequency: Daily

Workflow 4: Stale Deal Alerts
  Trigger: Daily 9AM cron
  Action: Alert on SLA violations
  Frequency: Daily
```

### Slack Notifications (Optional)
```yaml
Channel: #firstmile-deals
Triggers:
  - Deal moved to [04-PROPOSAL-SENT]
  - Deal moved to [07-CLOSED-WON]
  - SLA violation detected
  - Customer response received
```

---

## Troubleshooting

### HubSpot API Issues
```bash
# Test authentication
qm hubspot get-deal --deal-id 67890

# If 401 error: Token expired
# Action: Run /login to refresh OAuth token

# If 429 error: Rate limit
# Action: Wait 10 seconds, retry with exponential backoff

# If 404 error: Object not found
# Action: Verify deal ID exists in HubSpot
```

### Folder Movement Not Syncing
```bash
# Check _PIPELINE_TRACKER.csv for manual discrepancies
# Verify folder naming follows exact format: [##-STAGE]_Company_Name
# Restart NEBUCHADNEZZAR_CONTROL.bat
# Manually trigger N8N workflow if needed
```

### Missing Deal Data
```bash
# Re-query with full properties list
qm hubspot get-deal --deal-id 67890 --properties all

# Check for custom properties not in default list
# Verify deal is in correct pipeline
```

---

## System Maintenance

### Daily Tasks
- 9AM Sync: Generate priority list
- NOON Sync: Progress check
- 5PM EOD Sync: Learnings capture

### Weekly Tasks
- Review _PIPELINE_TRACKER.csv for data integrity
- Archive [07-CLOSED-WON] deals older than 90 days
- Update FOLLOW_UP_REMINDERS.txt for next week

### Monthly Tasks
- Pipeline health report (stage distribution, SLA compliance)
- Win/loss analysis
- Update CLAUDE.md with new patterns discovered

---

## Emergency Contacts & Escalation

### Internal Blockers
```yaml
Rate Creation: Brock (technical data analysis)
JIRA Delays: Engineering team
Contract Issues: Legal team
Pricing Approval: Sales leadership
```

### Customer Escalation Path
```yaml
Level 1: Brett Walker (AE)
Level 2: Sales Manager
Level 3: VP Sales
Level 4: Executive team
```

---

## Version History

**v2.0** (Current) - October 2025
- Full HubSpot API integration
- 10-stage pipeline automation
- N8N folder movement detection
- Daily sync flow structure

**v1.0** - Initial manual pipeline tracking

---

## Quick Start Checklist

- [ ] HubSpot OAuth token active (`/login` if needed)
- [ ] `qm hubspot` commands working
- [ ] Folder structure matches 10-stage pipeline
- [ ] _PIPELINE_TRACKER.csv exists in Downloads
- [ ] NEBUCHADNEZZAR_CONTROL.bat on Desktop
- [ ] N8N workflows running (verify in N8N dashboard)
- [ ] Daily sync flows scheduled (9AM, NOON, 5PM)

---

**Last Updated**: October 7, 2025
**Maintained By**: Brett Walker
**System Status**: Active
