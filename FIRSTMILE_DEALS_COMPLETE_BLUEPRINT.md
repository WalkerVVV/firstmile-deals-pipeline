# FirstMile Deals - Complete System Blueprint

**System Name**: Nebuchadnezzar v2.0-v3.1.0
**Version**: 3.1.0
**Last Updated**: October 23, 2025
**Purpose**: Automated sales pipeline and customer analysis system for FirstMile shipping solutions

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Pipeline Architecture](#2-pipeline-architecture)
3. [Folder Structure & Naming Conventions](#3-folder-structure--naming-conventions)
4. [File Type Patterns](#4-file-type-patterns)
5. [Automation & Workflow Systems](#5-automation--workflow-systems)
6. [HubSpot Integration](#6-hubspot-integration)
7. [Daily Workflow Operations](#7-daily-workflow-operations)
8. [Brand Scout System](#8-brand-scout-system)
9. [Python Script Categories](#9-python-script-categories)
10. [Configuration & Dependencies](#10-configuration--dependencies)
11. [Replication Guide](#11-replication-guide)

---

## 1. System Overview

### 1.1 Core Philosophy

The FirstMile Deals system implements a **folder-based pipeline consciousness** where:
- Physical folder movement = pipeline state change
- Zero manual data entry through automation
- Real-time tracking via folder monitoring
- Bidirectional sync between local folders and HubSpot CRM

### 1.2 Key Statistics

| Metric | Count |
|--------|-------|
| Active Deal Folders | 47 |
| Python Scripts | 150+ |
| Excel Reports | 180+ |
| CSV Data Files | 80+ |
| Markdown Docs | 60+ |
| Pipeline Stages | 10 |
| HubSpot Stages | 8 |
| Documentation Files | 50+ |

### 1.3 Technology Stack

```yaml
Core:
  - Python 3.9+
  - Pandas (data analysis)
  - OpenPyXL (Excel generation)
  - Requests (API calls)

Integration:
  - HubSpot CRM (deal tracking)
  - N8N (automation engine)
  - Chrome DevTools MCP (brand research)

Infrastructure:
  - Windows 10/11
  - Local file system
  - Environment variables (.env)
```

---

## 2. Pipeline Architecture

### 2.1 10-Stage Pipeline Structure

```
┌─────────────────────────────────────────────────────────────┐
│                   NEBUCHADNEZZAR v2.0                        │
│              10-Stage Sales Pipeline                         │
└─────────────────────────────────────────────────────────────┘

[00-LEAD]                    ← Initial contact
    ↓ (Qualify)
[01-DISCOVERY-SCHEDULED]     ← Meeting booked
    ↓ (Discovery call)
[02-DISCOVERY-COMPLETE]      ← Requirements gathered
    ↓ (Rate analysis)
[03-RATE-CREATION]           ← Pricing work in progress ⚠️ BOTTLENECK
    ↓ (Proposal ready)
[04-PROPOSAL-SENT]           ← Rates delivered
    ↓ (Verbal commit)
[05-SETUP-DOCS-SENT]         ← Contracts sent
    ↓ (Integration)
[06-IMPLEMENTATION]          ← Onboarding active
    ↓ (Go-live)
[07-CLOSED-WON]              ← Active customer 🎉
    ↓ (Optional paths)
[08-CLOSED-LOST]             ← Lost deal
    ↓ (Re-engage)
[09-WIN-BACK]                ← Re-engagement campaign
```

### 2.2 Stage Definitions & Automation

| Stage | Description | HubSpot Stage ID | Auto-Actions | Follow-Up SLA |
|-------|-------------|------------------|--------------|---------------|
| **[00-LEAD]** | Initial contact | Use [01] instead | None | None |
| **[01-DISCOVERY-SCHEDULED]** | Meeting booked | `1090865183` | Stale deal reminder | 30 days |
| **[02-DISCOVERY-COMPLETE]** | Requirements gathered | `d2a08d6f-cc04-4423-9215-594fe682e538` | Task creation | 30 days |
| **[03-RATE-CREATION]** | Pricing in progress | `e1c4321e-afb6-4b29-97d4-2b2425488535` | BOTTLENECK alert | 14 days |
| **[04-PROPOSAL-SENT]** | Rates delivered | `d607df25-2c6d-4a5d-9835-6ed1e4f4020a` | Follow-up sequence | 30 days |
| **[05-SETUP-DOCS-SENT]** | Contracts sent | `4e549d01-674b-4b31-8a90-91ec03122715` | Implementation prep | 14 days |
| **[06-IMPLEMENTATION]** | Onboarding active | `08d9c411-5e1b-487b-8732-9c2bcbbd0307` | Progress tracking | 30 days |
| **[07-CLOSED-WON]** | Active customer | `3fd46d94-78b4-452b-8704-62a338a210fb` | Success handoff | Ongoing |
| **[08-CLOSED-LOST]** | Lost deal | `02d8a1d7-d0b3-41d9-adc6-44ab768a61b8` | Loss analysis | Custom |
| **[09-WIN-BACK]** | Re-engagement | Create NEW deal | Monthly check-in | Monthly |

### 2.3 Pipeline Velocity Metrics

```python
# Target metrics
AVERAGE_DAYS_IN_STAGE = {
    '[01-DISCOVERY-SCHEDULED]': 14,
    '[02-DISCOVERY-COMPLETE]': 7,
    '[03-RATE-CREATION]': 14,    # Current bottleneck
    '[04-PROPOSAL-SENT]': 30,
    '[05-SETUP-DOCS-SENT]': 14,
    '[06-IMPLEMENTATION]': 30
}

# Pipeline health indicators
HEALTHY_PIPELINE = {
    'conversion_rate_discovery_to_won': 0.30,  # 30%
    'average_deal_cycle_days': 90,
    'rate_creation_bottleneck_max': 14        # Days in stage 3
}
```

---

## 3. Folder Structure & Naming Conventions

### 3.1 Standard Folder Pattern

**Regex**: `^\[(\d{2})-([A-Z0-9\-]+)\]_(.+)$`

**Format**: `[##-STAGE-NAME]_Company_Name`

**Components**:
1. Stage prefix: `[00-09]` + descriptive name (ALL CAPS)
2. Separator: Single underscore `_`
3. Company name: Title_Case with underscores (no spaces)

**Examples**:
```
✅ [01-DISCOVERY-SCHEDULED]_Josh's_Frogs
✅ [03-RATE-CREATION]_Stackd_Logistics
✅ [04-PROPOSAL-SENT]_Team_Shipper
✅ [07-CLOSED-WON]_JM_Group_NY
✅ [09-WIN-BACK]_The_Only_Bean

❌ 01_Josh's_Frogs (missing brackets)
❌ [01-Discovery]_Company (lowercase stage)
❌ [01-DISCOVERY-SCHEDULED] Josh's Frogs (space instead of underscore)
```

### 3.2 Deal Folder Template Structure

```
[##-STAGE]_Company_Name/
│
├── CLAUDE.md                              ← AI context (required)
├── Customer_Relationship_Documentation.md ← CRM history (required)
├── README.md                              ← Deal overview (required)
│
├── PLD_Analysis/                          ← Shipping profile analysis
│   ├── raw_data/
│   │   ├── customer_pld_export.csv
│   │   ├── invoice_data.xlsx
│   │   └── carrier_invoices.pdf
│   ├── scripts/
│   │   ├── pld_analysis.py
│   │   ├── apply_firstmile_rates.py
│   │   ├── create_pricing_matrix.py
│   │   ├── revenue_calculator.py
│   │   └── invoice_audit_builder.py
│   ├── outputs/
│   │   ├── shipping_profile_report.xlsx
│   │   ├── analysis_summary.md
│   │   └── pld_discovery_report.md
│   └── README.md
│
├── Rate_Cards/                            ← Pricing matrices
│   ├── current_rates_extracted.xlsx
│   ├── firstmile_pricing_matrix.xlsx
│   ├── savings_comparison.xlsx
│   └── tier_tool_output.xlsx
│
├── Proposals/                             ← Customer-facing deliverables
│   ├── proposal_v1.xlsx
│   ├── proposal_v2_revised.xlsx
│   ├── executive_summary.pdf
│   └── presentation_deck.pptx
│
├── Communications/                        ← Email & meeting records
│   ├── EMAIL_TO_[CONTACT]_[SUBJECT].md
│   ├── MEETING_NOTES_[DATE]_[TOPIC].md
│   └── CALL_LOG_[DATE].md
│
├── Performance_Reports/                   ← Post-win reports (Stage 7+)
│   ├── firstmile_performance_report.xlsx
│   └── sla_compliance_dashboard.xlsx
│
└── Reference/                             ← Supporting documentation
    ├── competitive_analysis.md
    ├── network_coverage_analysis.md
    ├── integration_requirements.md
    ├── jira_ticket_reference.md
    ├── loss_analysis.md                   ← Stage 8+
    └── win_back_strategy.md               ← Stage 9
```

### 3.3 Root Directory Structure

```
C:\Users\BrettWalker\FirstMile_Deals\
│
├── [00-LEAD]/                             ← Stage 0 deals
├── [01-DISCOVERY-SCHEDULED]/              ← Stage 1 deals
├── [02-DISCOVERY-COMPLETE]/               ← Stage 2 deals
├── [03-RATE-CREATION]/                    ← Stage 3 deals
├── [04-PROPOSAL-SENT]/                    ← Stage 4 deals
├── [05-SETUP-DOCS-SENT]/                  ← Stage 5 deals
├── [06-IMPLEMENTATION]/                   ← Stage 6 deals
├── [07-CLOSED-WON]/                       ← Stage 7 deals (active customers)
├── [08-CLOSED-LOST]/                      ← Stage 8 deals (lost)
├── [09-WIN-BACK]/                         ← Stage 9 deals (re-engagement)
│
├── .claude/                               ← Central documentation (50+ files)
│   ├── INDEX.md
│   ├── README.md
│   ├── DOCUMENTATION_INDEX.md
│   ├── DAILY_SYNC_FLOWS_V3.md
│   ├── NEBUCHADNEZZAR_REFERENCE.md
│   ├── DEAL_FOLDER_TEMPLATE.md
│   ├── HUBSPOT_WORKFLOW_GUIDE.md
│   ├── VERIFIED_STAGE_IDS.md
│   ├── brand_scout/                       ← Brand Scout system
│   └── commands/                          ← Slash command docs
│
├── HubSpot/                               ← CRM integration
│   ├── HUBSPOT_MCP_CHEATSHEET.md
│   └── CLAUDE.md
│
├── BULK_RATE_PROCESSING/                  ← Bulk tools
│   └── RATE_CREATION_BLITZ.md
│
├── _ARCHIVE/                              ← Historical deals
│
├── config.py                              ← Main configuration
├── hubspot_config.py                      ← HubSpot configuration
├── hubspot_utils.py                       ← HubSpot API utilities
├── hubspot_realtime_updates.py            ← Real-time CRM sync
├── hubspot_batch_updates_tuesday_am.py    ← Batch processing
├── pipeline_sync_verification.py          ← Sync verification
├── daily_9am_workflow.py                  ← Morning workflow
├── daily_9am_sync.py                      ← Morning sync
├── noon_sync.py                           ← Noon check
├── temp_eod_summary.py                    ← EOD wrap
│
├── requirements.txt                       ← Python dependencies
├── .env                                   ← Environment variables (NOT committed)
└── .env.example                           ← Environment template
```

---

## 4. File Type Patterns

### 4.1 Python Scripts (150+ files)

**Categories**:

1. **PLD Analysis** (`*pld_analysis*.py`, `*_analysis.py`)
   - Comprehensive shipping profile analysis
   - Volume, carrier mix, service levels, weight distribution
   - Zone analysis, geographic distribution
   - Billable weight impact calculations

2. **Rate Calculation** (`*rate*.py`, `*pricing*.py`, `tier_tool*.py`)
   - Extract current rates from customer data
   - Apply FirstMile Xparcel pricing models
   - Calculate savings projections (target: 40%)
   - Generate comparison matrices

3. **Performance Reports** (`firstmile_orchestrator*.py`, `*performance_report*.py`)
   - 9-tab Excel reports with FirstMile branding
   - SLA compliance tracking
   - Transit performance analysis
   - Geographic and zone distribution

4. **Invoice Audits** (`invoice_audit_builder*.py`)
   - Identify carrier overcharges
   - Billable weight discrepancies
   - Refund opportunity calculations

5. **Dashboards** (`*dashboard*.py`, `*monitor*.py`)
   - Real-time performance monitoring
   - SLA compliance tracking
   - Carrier performance metrics

6. **HubSpot Integration** (`hubspot_*.py`, `daily_*.py`)
   - CRM synchronization
   - Pipeline verification
   - Task automation
   - Batch updates

### 4.2 Excel Files (180+ files)

**Types**:

1. **Performance Reports**: `*_FirstMile_Xparcel_[DATE].xlsx`
   - 9 standardized tabs
   - FirstMile branding (#366092 blue)
   - Conditional formatting for SLA compliance

2. **PLD Analysis**: `*_PLD_*.xlsx`
   - Shipping profile breakdown
   - Multi-tab workbooks
   - Volume, weight, zone analysis

3. **Rate Proposals**: `*_Savings_Analysis.xlsx`, `*_Rate_Analysis.xlsx`
   - Current vs proposed pricing
   - Savings calculations
   - Service level comparisons

4. **Invoice Audits**: `*_Audit_v*.xlsx`, `*_Detailed_Data_v*.xlsx`
   - Overcharge identification
   - Billable weight analysis
   - Refund calculations

### 4.3 CSV Data Files (80+ files)

**Types**:

1. **Original Exports**: Customer shipment data from platforms
2. **Processed Analysis**: `*_Detailed_Data*.csv`, `*_Analysis*.csv`
3. **Rate Tables**: `*_rate*.csv`, `*_matrix*.csv`, `*_pricing*.csv`
4. **Performance Data**: `*_SLA_Compliance.csv`, `*_Monthly_Breakdown.csv`

### 4.4 Markdown Documentation (60+ files)

**Types**:

1. **System Docs**: `.claude/` folder (50+ files)
2. **Deal Docs**: `CLAUDE.md`, `README.md`, `Customer_Relationship_Documentation.md`
3. **Analysis Results**: `*_Summary.md`, `*_Analysis.md`, `*_Notes.md`
4. **Communications**: `EMAIL_TO_*.md`, `MEETING_NOTES_*.md`

---

## 5. Automation & Workflow Systems

### 5.1 N8N Automation Engine

**Watch Folder**: `C:\Users\BrettWalker\FirstMile_Deals\`

**Trigger Mechanism**: Folder movement detection

**Example Flow**:
```
1. User moves folder: [03-RATE-CREATION]_Company → [04-PROPOSAL-SENT]_Company
2. N8N detects folder rename event
3. N8N extracts stage number and company name
4. N8N looks up HubSpot stage ID from mapping
5. N8N updates HubSpot deal via API
6. N8N creates follow-up EMAIL task
7. N8N logs action to _PIPELINE_TRACKER.csv
8. N8N updates AUTOMATION_MONITOR_LOCAL.html
```

**Automation Artifacts**:

| File | Location | Purpose |
|------|----------|---------|
| `_PIPELINE_TRACKER.csv` | Downloads folder | Single source of truth for all deals |
| `_DAILY_LOG.md` | Downloads folder | Daily activity log (9AM, NOON, EOD) |
| `_DAILY_LOG_FEEDBACK.md` | Downloads folder | Learning capture and improvements |
| `FOLLOW_UP_REMINDERS.txt` | Downloads folder | Manual reminder backup |
| `AUTOMATION_MONITOR_LOCAL.html` | Desktop | Visual dashboard |
| `NEBUCHADNEZZAR_CONTROL.bat` | Desktop | Control panel |

### 5.2 Daily Workflow Schedule

**9:00 AM - Priority Sync** (`daily_9am_workflow.py`)
- Fetch priority stage deals ([03], [04], [06])
- Verify EMAIL task existence
- Create missing EMAIL tasks
- Calculate urgency scores (0-100)
- Output action-oriented report

**12:00 PM - Noon Check** (`noon_sync.py`)
- Fetch afternoon priority deals
- Flag urgent items (>14d old in [03], >30d in [04])
- Display top 3 deals per stage
- Generate afternoon action plan

**4:30 PM - EOD Wrap** (`temp_eod_summary.py`)
- Query deals modified today
- Pipeline health snapshot
- Tomorrow's priorities
- Key insights
- Opening checklist for next day

**Tuesday 9:00 AM - Batch Updates** (`hubspot_batch_updates_tuesday_am.py`)
- Email-driven context integration
- Add deal notes from Superhuman email summaries
- Create action tasks
- Update properties with timestamps

**Daily - Pipeline Verification** (`pipeline_sync_verification.py`)
- Compare local folders vs HubSpot deals
- Detect discrepancies by stage
- Flag sync issues
- Trigger reconciliation if needed

### 5.3 Automation Rules by Stage

| Stage Transition | Automation Triggered |
|------------------|---------------------|
| → [01-DISCOVERY-SCHEDULED] | Stale deal reminder (30 days) |
| → [02-DISCOVERY-COMPLETE] | 30-day follow-up task |
| → [03-RATE-CREATION] | 2-week follow-up + BOTTLENECK alert |
| → [04-PROPOSAL-SENT] | 30-day follow-up + Day 7/14 reminders |
| → [05-SETUP-DOCS-SENT] | 2-week implementation prep |
| → [06-IMPLEMENTATION] | 30-day progress tracking |
| → [07-CLOSED-WON] | Hand off to customer success |
| → [08-CLOSED-LOST] | Loss analysis + custom follow-up |
| → [09-WIN-BACK] | Monthly re-engagement check-in |

---

## 6. HubSpot Integration

### 6.1 Core Configuration

```python
# Critical IDs
HUBSPOT_OWNER_ID = "699257003"              # Brett Walker
HUBSPOT_PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
HUBSPOT_PORTAL_ID = "46526832"
HUBSPOT_API_BASE = "https://api.hubapi.com"

# Stage ID Mapping (8 HubSpot stages)
STAGE_MAPPING = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-STARTED-SHIPPING]",
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[08-CLOSED-LOST]"
}

# Association Type IDs
ASSOCIATION_IDS = {
    'CONTACT_TO_COMPANY': 279,
    'LEAD_TO_CONTACT': 608,      # REQUIRED for lead creation
    'LEAD_TO_COMPANY': 610,
    'DEAL_TO_COMPANY': 341,
    'DEAL_TO_CONTACT': 3,
    'TASK_TO_DEAL': 216
}
```

### 6.2 Quick Command Reference

```bash
# Search deals
qm hubspot search-deals --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Create lead
qm hubspot create-lead --first-name "John" --last-name "Smith" \
  --email "john@company.com" --company "Acme Corp"

# Convert to deal
qm hubspot convert-to-deal --contact-id [ID] \
  --deal-name "Company - Xparcel Ground" --amount 150000

# Create task
qm hubspot create-task --deal-id [ID] \
  --title "Follow up on proposal" --type "EMAIL"

# Update stage
qm hubspot update-deal --deal-id [ID] --stage "[NEW-STAGE-UUID]"
```

### 6.3 Python Integration Functions

```python
from hubspot_realtime_updates import (
    add_deal_note,
    create_task,
    update_deal_stage,
    update_deal_property,
    log_call,
    log_email
)

# Add note
add_deal_note("Company Name", "**RATES APPROVED**\n\nDetails...")

# Create task
create_task(
    deal_name="Company Name",
    task_subject="Send meeting request",
    task_body="Meeting agenda...",
    priority="HIGH",
    due_days=0
)

# Update stage
update_deal_stage("Company Name", "[04-PROPOSAL-SENT]")

# Update property
update_deal_property("Company Name", "amount", "150000")
```

---

## 7. Daily Workflow Operations

### 7.1 Morning Workflow (9:00 AM)

**File**: `daily_9am_workflow.py`

**Steps**:
1. Fetch priority stage deals ([03], [04], [06])
2. Verify EMAIL task existence for each deal
3. Create missing EMAIL tasks with stage-specific templates
4. Calculate urgency scores (0-100 scale)
5. Output priority-ranked action report

**Urgency Scoring Algorithm**:
```python
base_score = 50

# Days in stage factor
if days_in_stage > (0.75 * sla_days):
    score += 20
elif days_in_stage > (0.50 * sla_days):
    score += 10

# Deal amount factor
if amount > 50000:
    score += 20
elif amount > 25000:
    score += 10

# Last activity factor
if days_since_activity > 14:
    score += 20
elif days_since_activity > 7:
    score += 10

# Stage proximity bonus
if stage == '[06-IMPLEMENTATION]':
    score += 15

# Max score: 100
```

**Output Format**:
```
🔥 HIGH PRIORITY (Score 80+): Action required TODAY
⚡ MEDIUM PRIORITY (Score 60-79): Action within 3 days
📌 STANDARD PRIORITY (Score <60): Monitor closely
```

### 7.2 Noon Check (12:00 PM)

**File**: `noon_sync.py`

**Steps**:
1. Fetch afternoon priority deals (3 stages)
2. Flag urgent items (>14d in [03], >30d in [04])
3. Display top 3 deals per stage
4. Generate afternoon action plan
5. Track accomplishments

### 7.3 End-of-Day Wrap (4:30 PM)

**File**: `temp_eod_summary.py`

**5-Phase Output**:
1. **Today's Activity** - Deals modified since midnight
2. **Pipeline Health** - Active deals, total value
3. **Tomorrow's Priorities** - Tasks due or overdue
4. **Key Insights** - New deals, bottleneck status
5. **Opening Checklist** - Morning execution order

---

## 8. Brand Scout System

### 8.1 Overview

**Location**: `.claude/brand_scout/`

**Purpose**: Autonomous lead research generating 9-section brand reports for eCommerce prospects.

**Key Features**:
- Chrome DevTools MCP browser automation
- 9-section standardized report format
- HubSpot-ready lead record generation
- Automatic deal folder creation
- Quality confidence scoring (HIGH/MEDIUM/LOW)

### 8.2 Report Structure

**9 Sections**:
1. **Snapshot** - Brand overview, revenue, AOV, ship volume
2. **Shipping Intelligence** - Carriers, service levels, pricing
3. **Company Overview** - Legal name, HQ, founding year
4. **Stakeholders & Contacts** - Decision makers with emails
5. **Observations & Competitors** - Strengths, complaints, benchmarks
6. **HubSpot Lead Record** - Copy/paste CRM fields
7. **CRM Contact Summary** - One-line format
8. **Technical Integration** - Platform, APIs, monitoring
9. **Methodology & Versioning** - Data sources, confidence score

### 8.3 Automation Integration

**Pipeline Flow**:
```
Brand Scout Research (25-35 min)
    ↓
Generate Report (9 sections)
    ↓
Save to .claude/brand_scout/output/
    ↓
Create [00-LEAD]_BrandName/ folder
    ↓
Trigger N8N automation
    ↓
Create HubSpot lead (optional)
    ↓
Log to _PIPELINE_TRACKER.csv
```

**Performance Targets**:
- Time per report: 25-35 minutes
- Data confidence: 80%+ target
- Verified contacts: 2+ preferred
- Weekly goal: 15-20 reports
- Conversion to Discovery: 30%

---

## 9. Python Script Categories

### 9.1 PLD Analysis Scripts

**Pattern**: `*pld_analysis*.py`, `*_analysis.py`

**Standard Workflow**:
1. Load CSV/Excel shipment data
2. Calculate volume metrics (total, daily average)
3. Analyze carrier mix (volume/spend percentages)
4. Weight distribution (with billable weight rules)
5. Zone distribution (1-8, regional vs cross-country)
6. Geographic distribution (top states)
7. Cost analysis (total spend, avg/median)
8. Billable weight impact (actual vs billable)

**Critical Billable Weight Rules**:
```python
if weight < 1 lb:
    billable = min(15.99, round_up_to_oz(weight))
elif weight == 16 oz:
    billable = 1.0 lb
else:
    billable = round_up_to_whole_pound(weight)
```

### 9.2 Rate Calculation Scripts

**Pattern**: `*rate*.py`, `*pricing*.py`, `tier_tool*.py`

**Standard Workflow**:
1. Extract current customer rates
2. Parse zone/weight pricing structure
3. Apply FirstMile Xparcel rate cards
4. Calculate zone skipping benefits
5. Project revenue and savings (40% target)
6. Generate comparison matrices
7. Create Excel workbooks

**FirstMile Rate Cards**:
```python
XPARCEL_GROUND_RATES = {
    1: 3.73, 2: 3.79, 3: 3.80, 4: 3.89,
    5: 3.94, 6: 4.02, 7: 4.09, 8: 4.24
}

XPARCEL_EXPEDITED_RATES = {
    1: 3.94, 2: 3.99, 3: 4.01, 4: 4.10,
    5: 4.15, 6: 4.24, 7: 4.31, 8: 4.48
}

XPARCEL_PRIORITY_RATES = {
    1: 4.15, 2: 4.21, 3: 4.25, 4: 4.35,
    5: 4.42, 6: 4.51, 7: 4.59, 8: 4.75
}
```

### 9.3 Performance Report Scripts

**Pattern**: `firstmile_orchestrator*.py`, `*performance_report*.py`

**9-Tab Excel Output**:
1. **Executive Summary** - High-level KPIs
2. **SLA Compliance** - Delivered-only metrics with color scale
3. **Transit Performance** - Daily distribution (0-7, 8+)
4. **Geographic Distribution** - Top 15 states with hub mapping
5. **Zone Analysis** - Zones 1-8 with regional/cross-country
6. **Operational Metrics** - Volume metrics and opportunities
7. **In-Transit Detail** - Ships not delivered with SLA status
8. **Notes & Assumptions** - Business rules
9. **Brand Style Guide** - FirstMile colors (HEX/RGB/CMYK)

**Excel Styling**:
```python
PRIMARY_BLUE = "#366092"        # FirstMile brand
LIGHT_BORDER = "#DDDDDD"

# Conditional formatting for SLA compliance
80-89%: Red (#FFC7CE)
90-94%: Yellow (#FFEB84)
95-100%: Green (#C6EFCE)
```

---

## 10. Configuration & Dependencies

### 10.1 Environment Variables

**File**: `.env` (NOT committed to git)

```bash
HUBSPOT_API_KEY=pat-na1-xxxx...
HUBSPOT_OWNER_ID=699257003
HUBSPOT_PIPELINE_ID=8bd9336b-4767-4e67-9fe2-35dfcad7c8be
HUBSPOT_PORTAL_ID=46526832
FIRSTMILE_DEALS_PATH=C:\Users\BrettWalker\FirstMile_Deals
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 10.2 Python Dependencies

**File**: `requirements.txt`

```
pandas>=2.0.0
numpy>=1.24.0
requests>=2.28.0
urllib3>=2.0.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
xlrd>=2.0.1
python-dotenv>=1.0.0
python-dateutil>=2.8.0
```

### 10.3 Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | Main configuration with validation |
| `hubspot_config.py` | HubSpot-specific configuration |
| `hubspot_utils.py` | HubSpotClient class with rate limiting |
| `hubspot_realtime_updates.py` | Real-time CRM sync functions |
| `date_utils.py` | Date parsing utilities |

---

## 11. Replication Guide

### 11.1 Prerequisites

**System Requirements**:
- Windows 10/11
- Python 3.9+
- Git (for version control)
- HubSpot account with API access
- N8N instance (or alternative automation platform)

**Access Requirements**:
- HubSpot Private App Token (API key)
- Owner ID from HubSpot
- Pipeline ID from HubSpot
- Portal ID from HubSpot

### 11.2 Installation Steps

**Step 1: Clone Repository Structure**

```bash
# Create root directory
mkdir C:\Users\[YourName]\FirstMile_Deals
cd C:\Users\[YourName]\FirstMile_Deals

# Create stage directories
mkdir "[00-LEAD]"
mkdir "[01-DISCOVERY-SCHEDULED]"
mkdir "[02-DISCOVERY-COMPLETE]"
mkdir "[03-RATE-CREATION]"
mkdir "[04-PROPOSAL-SENT]"
mkdir "[05-SETUP-DOCS-SENT]"
mkdir "[06-IMPLEMENTATION]"
mkdir "[07-CLOSED-WON]"
mkdir "[08-CLOSED-LOST]"
mkdir "[09-WIN-BACK]"

# Create support directories
mkdir .claude
mkdir HubSpot
mkdir BULK_RATE_PROCESSING
mkdir _ARCHIVE
```

**Step 2: Install Python Dependencies**

```bash
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Step 3: Configure Environment**

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your values
notepad .env
```

**Step 4: Configure HubSpot Integration**

1. Create HubSpot Private App
2. Copy API key to `.env`
3. Find your Owner ID, Pipeline ID, Portal ID
4. Update `hubspot_config.py` with your IDs
5. Test connection: `python hubspot_pipeline_verify.py`

**Step 5: Set Up N8N Automation**

1. Install N8N or use cloud instance
2. Configure file system watcher for root directory
3. Create workflows for:
   - Folder movement detection
   - HubSpot deal updates
   - Task creation
   - Email notifications
4. Test trigger: Move a test folder between stages

**Step 6: Initialize Documentation**

```bash
# Copy .claude/ documentation folder
# Update paths in configuration files
# Review and customize templates
```

**Step 7: Create First Deal Folder**

```bash
# Use template structure
mkdir "[01-DISCOVERY-SCHEDULED]_Test_Company"
cd "[01-DISCOVERY-SCHEDULED]_Test_Company"

# Copy template files
copy ..\[01-DISCOVERY-SCHEDULED]_TEMPLATE\CLAUDE.md .
copy ..\[01-DISCOVERY-SCHEDULED]_TEMPLATE\README.md .
copy ..\[01-DISCOVERY-SCHEDULED]_TEMPLATE\Customer_Relationship_Documentation.md .

# Create subdirectories
mkdir PLD_Analysis
mkdir Rate_Cards
mkdir Proposals
mkdir Communications
mkdir Reference
```

**Step 8: Test Daily Workflows**

```bash
# Test 9AM workflow
python daily_9am_workflow.py

# Test noon sync
python noon_sync.py

# Test EOD summary
python temp_eod_summary.py

# Verify outputs and logs
```

### 11.3 Customization Points

**Brand Customization**:
- Update `PRIMARY_BLUE` color in config.py
- Replace FirstMile branding with your company
- Customize Excel report templates
- Update email templates

**Pipeline Customization**:
- Modify stage names in STAGE_MAPPING
- Adjust SLA windows in SLA_WINDOWS
- Update automation rules per stage
- Customize follow-up timelines

**Rate Card Customization**:
- Update XPARCEL_*_RATES with your pricing
- Modify zone mappings (STATE_TO_ZONE)
- Adjust savings targets
- Customize hub assignments

### 11.4 Verification Checklist

```
✓ Python environment activated
✓ All dependencies installed
✓ .env file configured with valid API key
✓ HubSpot connection tested
✓ Pipeline sync verification passes
✓ N8N workflows configured and tested
✓ Daily workflow scripts execute successfully
✓ Test deal folder created and moved
✓ HubSpot deal updated via automation
✓ Documentation reviewed and paths updated
```

### 11.5 Troubleshooting

**Common Issues**:

1. **HubSpot API Authentication Failure**
   - Verify API key in .env
   - Check Private App permissions
   - Confirm Owner ID is correct

2. **Pipeline Sync Discrepancies**
   - Run `pipeline_sync_verification.py`
   - Check folder naming format
   - Verify stage ID mappings

3. **N8N Automation Not Triggering**
   - Check file system watcher configuration
   - Verify folder path is correct
   - Test with manual trigger

4. **Script Execution Errors**
   - Check Python version (3.9+)
   - Verify all dependencies installed
   - Review error logs for missing modules

---

## Appendix A: File Path Reference

**System Paths**:
```
C:\Users\BrettWalker\FirstMile_Deals\                 # Root
C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv  # Pipeline database
C:\Users\BrettWalker\Downloads\_DAILY_LOG.md          # Activity log
C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt # Action queue
C:\Users\BrettWalker\Desktop\AUTOMATION_MONITOR_LOCAL.html # Dashboard
C:\Users\BrettWalker\Desktop\NEBUCHADNEZZAR_CONTROL.bat # Control panel
```

---

## Appendix B: Quick Reference Tables

### Stage SLA Reference

| Stage | Follow-Up SLA | Max Days Before Alert |
|-------|---------------|----------------------|
| [01-DISCOVERY-SCHEDULED] | 30 days | 30 |
| [02-DISCOVERY-COMPLETE] | 30 days | 30 |
| [03-RATE-CREATION] | 14 days | **14** ⚠️ |
| [04-PROPOSAL-SENT] | 30 days | 30 |
| [05-SETUP-DOCS-SENT] | 14 days | 14 |
| [06-IMPLEMENTATION] | 30 days | 30 |

### Service Level SLA Windows

| Service | Transit Days | SLA Window |
|---------|--------------|------------|
| Xparcel Priority | 1-3 days | 3 days |
| Xparcel Expedited | 2-5 days | 5 days |
| Xparcel Ground | 3-8 days | 8 days |

### Performance Thresholds

| Threshold | Percentage | Status |
|-----------|------------|--------|
| Perfect Compliance | 100% | 🟢 |
| Exceeds Standard | ≥95% | 🟢 |
| Meets Standard | ≥90% | 🟡 |
| Below Standard | <90% | 🔴 |

---

## Appendix C: Naming Pattern Examples

### Valid Folder Names
```
✅ [01-DISCOVERY-SCHEDULED]_Josh's_Frogs
✅ [03-RATE-CREATION]_Stackd_Logistics
✅ [04-PROPOSAL-SENT]_Team_Shipper
✅ [07-CLOSED-WON]_JM_Group_NY
✅ [09-WIN-BACK]_The_Only_Bean
```

### Invalid Folder Names
```
❌ 01_Josh's_Frogs                      # Missing brackets
❌ [01-Discovery]_Company                # Lowercase stage
❌ [01-DISCOVERY-SCHEDULED] Company      # Space instead of underscore
❌ [01]_Company                          # Missing stage name
❌ DISCOVERY-SCHEDULED_Company           # Missing stage number
```

---

**End of Blueprint**

This blueprint provides complete documentation for replicating the FirstMile Deals system. For questions or updates, refer to `.claude/README.md` or the documentation index at `.claude/DOCUMENTATION_INDEX.md`.

**System Version**: Nebuchadnezzar v2.0-v3.1.0
**Last Updated**: October 23, 2025
**Maintained By**: Brett Walker (Owner ID: 699257003)
