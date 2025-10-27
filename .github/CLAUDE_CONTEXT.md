# GitHub Claude Integration - FirstMile Deals Context

**System**: The Nebuchadnezzar v2.0
**Purpose**: Comprehensive context for GitHub Claude App (@claude mentions)
**Last Updated**: 2025-10-27
**Owner**: Brett Walker

---

## Quick Reference

**When mentioned via @claude in GitHub:**
- Issues: Analysis, troubleshooting, documentation requests
- Pull Requests: Code reviews, compliance checks, optimization suggestions
- Comments: Technical questions, workflow explanations

**Example Uses**:
- `@claude review this rate calculation script for accuracy`
- `@claude analyze the pipeline sync issues and suggest fixes`
- `@claude explain the billable weight calculation logic`
- `@claude check this PR for FirstMile brand compliance`

---

## System Overview

### What is FirstMile Deals?

FirstMile Deals is a fully automated sales pipeline management system for FirstMile shipping solutions. The system (nicknamed "Nebuchadnezzar v2.0") manages:

- **10-stage deal pipeline** with folder-based tracking
- **HubSpot CRM integration** via MCP
- **N8N automation** for workflow triggers
- **Python analytics** for shipping analysis
- **Daily sync flows** (9AM, NOON, EOD, End of Week)
- **Continuous learning** feedback loops

### Core Mission

Help FirstMile (a shipping carrier) win eCommerce customers by:
1. Analyzing their current shipping profiles (PLD analysis)
2. Creating optimized rate cards (typically 40% savings)
3. Demonstrating SLA improvements and network advantages
4. Managing the sales pipeline from discovery to closed-won

---

## Business Context

### FirstMile is a Carrier

**Not a 3PL or platform** - FirstMile is the actual shipping carrier offering:

- **Xparcel Ground**: 3-8 day economy ground service
- **Xparcel Expedited**: 2-5 day faster ground solution (1-20 lb)
- **Xparcel Priority**: 1-3 day premium option with money-back guarantee

### Key Terminology (CRITICAL)

- **"National Network"**: Nationwide induction partners covering 100% U.S. ZIPs
- **"Select Network"**: High-density metro injection points (LA, DAL, ATL, ORD, EWR, etc.)
- **Never name carriers**: Don't say "UPS, FedEx, USPS" - use "National" or "Select"
- **Spell eCommerce**: Camel-case 'C' always
- **Xparcel is a ship-method**: Under FirstMile brand, not separate company

### SLA Windows

- **Xparcel Priority**: 1-3 days (SLA: 3 days)
- **Xparcel Expedited**: 2-5 days (SLA: 5 days)
- **Xparcel Ground**: 3-8 days (SLA: 8 days)

### Brand Standards

- **Primary Color**: #366092 (FirstMile blue)
- **Lead with SLA compliance**: Never lead reports with daily delivery %
- **Plain, factual language**: No emojis or marketing slogans
- **Professional tone**: Data-driven insights with supporting metrics

---

## Pipeline Architecture

### 10-Stage Pipeline Structure

```
[00-LEAD] .......................... New prospects
[01-DISCOVERY-SCHEDULED] ........... Meeting booked
[02-DISCOVERY-COMPLETE] ............ Requirements gathered
[03-RATE-CREATION] ................. Pricing in progress ⚠️ BOTTLENECK
[04-PROPOSAL-SENT] ................. Rates delivered
[05-SETUP-DOCS-SENT] ............... Verbal commit
[06-IMPLEMENTATION] ................ Onboarding active
[07-CLOSED-WON] .................... Active customer 🎯
[08-CLOSED-LOST] ................... Lost deal (learn)
[09-WIN-BACK] ...................... Re-engagement
```

### Stage SLAs & Follow-ups

| Stage | SLA | Critical Action |
|-------|-----|-----------------|
| [01-DISCOVERY-SCHEDULED] | 14 days | Meeting prep & confirmation |
| [02-DISCOVERY-COMPLETE] | 30 days | Data collection & analysis start |
| [03-RATE-CREATION] | **14 days** | **BOTTLENECK STAGE** - Monitor closely |
| [04-PROPOSAL-SENT] | 30 days | Follow-up at 7d, 14d, 30d |
| [05-SETUP-DOCS-SENT] | 14 days | Urgent - at finish line |
| [06-IMPLEMENTATION] | 30 days | Daily check-ins until live |

### Automation System

**Folder Movement → N8N → HubSpot Updates**

- Watch folder: `C:\Users\BrettWalker\FirstMile_Deals\`
- Pipeline database: `_PIPELINE_TRACKER.csv` (Downloads)
- Activity log: `_DAILY_LOG.md` (Downloads)
- Action queue: `FOLLOW_UP_REMINDERS.txt` (Downloads)

---

## HubSpot Integration

### Critical IDs

```yaml
Owner ID: 699257003  # Brett Walker
Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
Portal ID: 46526832
```

### Stage IDs (HubSpot API)

```yaml
[01] Discovery Scheduled:  1090865183
[02] Discovery Complete:   d2a08d6f-cc04-4423-9215-594fe682e538
[03] Rate Creation:        e1c4321e-afb6-4b29-97d4-2b2425488535
[04] Proposal Sent:        d607df25-2c6d-4a5d-9835-6ed1e4f4020a
[05] Setup Docs Sent:      4e549d01-674b-4b31-8a90-91ec03122715
[06] Implementation:       08d9c411-5e1b-487b-8732-9c2bcbbd0307
[07] Started Shipping:     3fd46d94-78b4-452b-8704-62a338a210fb
[08] Closed Lost:          02d8a1d7-d0b3-41d9-adc6-44ab768a61b8
```

**Note**: [00-LEAD] and [09-WIN-BACK] don't exist in HubSpot (use [01] for new leads)

### MCP Tool Usage

```bash
# Lead creation
qm hubspot create-lead --first-name "John" --last-name "Smith" --email "john@company.com" --company "Acme Corp"

# Deal conversion
qm hubspot convert-to-deal --contact-id 12345 --deal-name "Acme Corp - Xparcel Ground" --amount 150000

# Pipeline search
qm hubspot search-deals --owner-id 699257003 --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Update deal stage
qm hubspot update-deal --deal-id 67890 --stage "[04-PROPOSAL-SENT]"
```

---

## Core Analysis Workflows

### 1. PLD (Parcel Level Detail) Analysis

**Purpose**: Comprehensive shipping profile analysis for rate creation

**Standard Flow**:
1. Load customer shipment data (CSV/Excel)
2. Calculate volume metrics (total, daily average, marketplace mix)
3. Analyze carrier mix (current carriers vs FirstMile opportunity)
4. Weight distribution with billable weight rules
5. Zone distribution (Regional 1-4 vs Cross-Country 5-8)
6. Geographic analysis (top states, hub mapping)
7. Cost analysis (current spend vs FirstMile savings projection)

**Scripts**: `pld_analysis.py`, `[customer]_pld_analysis.py`

**Output**: Excel report with professional FirstMile branding

### 2. Rate Calculation & Pricing

**Purpose**: Create competitive FirstMile rate cards with savings projections

**Workflow**:
1. Extract current customer rates from invoices/data
2. Apply FirstMile pricing models (National/Select networks)
3. Calculate zone/weight tier matrices
4. Generate savings comparison (target: 40% savings)
5. Create revenue projections based on volume

**Scripts**: `apply_customer_rates.py`, `create_pricing_matrix.py`, `revenue_calculator.py`

**Critical Rule**: Rate creation is bottleneck stage - target <7 day turnaround

### 3. Performance Reporting

**Purpose**: Customer-facing reports with SLA compliance and transit performance

**9-Tab Structure**:
1. Executive Summary
2. **SLA Compliance** (ALWAYS FIRST METRIC)
3. Transit Performance
4. Geographic Distribution
5. Zone Analysis
6. Operational Metrics
7. In-Transit Detail
8. Notes & Assumptions
9. Brand Style Guide

**Script**: `firstmile_orchestrator.py`

**Brand Requirements**:
- Lead with SLA compliance (not daily delivery %)
- FirstMile blue (#366092) headers
- Auto-sized columns, conditional formatting
- Plain factual language

### 4. Invoice Audit Analysis

**Purpose**: Identify carrier overcharges and refund opportunities

**Analysis**:
- Compare invoiced rates vs contracted rates
- Billable weight discrepancies
- Service level mismatches
- Zone errors

**Scripts**: `invoice_audit_builder_v31.py`, `invoice_audit_builder_DRY_GOODS_ONLY.py`

---

## Critical Business Rules

### Billable Weight Calculation

**ALL carriers** follow these rules:
- **Under 1 lb**: Round UP to next whole oz, MAX 15.99 oz
- **16 oz exactly**: Bills as 1 lb (16 oz)
- **Over 1 lb**: Round UP to next whole pound (32, 48, 64 oz, etc.)

**Example**:
- 15.5 oz → Bills as 16 oz (still under 1 lb)
- 15.99 oz → Bills as 15.99 oz (maximum before jump)
- 16.0 oz → Bills as 1 lb (2 lbs billable if over 1.0 lb actual)
- 17.0 oz → Bills as 2 lbs
- 31.5 oz → Bills as 32 oz (2 lbs)
- 32.1 oz → Bills as 3 lbs

### Hub Mapping

```python
HUB_MAP = {
    "CA": "LAX - West Coast",
    "TX": "DFW - South Central",
    "FL": "MIA - Southeast",
    "NY": "JFK/EWR - Northeast",
    "IL": "ORD - Midwest",
    "GA": "ATL - Southeast"
}
```

### Performance Thresholds

```yaml
Perfect Compliance: 100%
Exceeds Standard: ≥95%
Meets Standard: ≥90%
Below Standard: <90%
```

---

## Daily Sync Operations

### 9AM Sync - Day Start

**Purpose**: Generate priority-ranked action list

**Process**:
1. Load previous day learnings from `_DAILY_LOG_FEEDBACK.md`
2. Check overnight email responses (automated via Superhuman AI)
3. Live HubSpot pipeline sync
4. Priority analysis (P1 immediate, P2 active)
5. Action generation with context
6. Pipeline health check

**Script**: `daily_9am_workflow.py`

**Output**: Priority list with urgency scoring

### NOON Sync - Midday Check

**Purpose**: Progress check and afternoon planning

**Process**:
1. Review morning execution completion
2. Process new customer responses
3. Update blocker status
4. Identify afternoon priorities

**Script**: `pipeline_sync_verification.py`

### EOD Sync - End of Day

**Purpose**: Capture learnings and setup tomorrow

**Process**:
1. Daily summary (touchpoints, movements, actions completed)
2. Learnings capture (What worked ✅, What failed ❌, What's unclear ❓, What's missing 🔧)
3. Tomorrow's setup (meetings, deliverables, pending responses)
4. Archive to `_DAILY_LOG_FEEDBACK.md`

**Automated**: Uses Chrome MCP + Superhuman AI for email intelligence

### End of Week Sync - Friday EOD

**Purpose**: Weekly reflection and next week planning

**Process**:
1. Week summary metrics
2. SOP evolution tracking (PERMANENT ✅, TESTING 🟡, PROPOSED 🔴)
3. Pipeline velocity analysis
4. Next week priorities
5. Archive learnings to Saner.ai

---

## Repository Structure

### Deal Folders

```
[##-STAGE]_Company_Name/
├── CLAUDE.md                    # AI context
├── Customer_Relationship_Documentation.md  # Complete history
├── PLD_Analysis/
│   ├── raw_data.csv
│   ├── pld_analysis.py
│   ├── shipping_profile_report.xlsx
│   └── analysis_summary.md
├── Rate_Cards/
│   ├── current_rates_extracted.xlsx
│   ├── firstmile_pricing_matrix.xlsx
│   └── savings_comparison.xlsx
├── Proposals/
│   ├── proposal_v1.xlsx
│   └── executive_summary.pdf
├── Communications/
│   ├── EMAIL_TO_[CONTACT]_[SUBJECT].md
│   └── MEETING_NOTES_[DATE].md
└── Analysis_Scripts/
    ├── apply_firstmile_rates.py
    ├── create_pricing_matrix.py
    └── revenue_calculator.py
```

### Key Directories

```
FirstMile_Deals/
├── [Deal Folders]/              # Active pipeline (10 stages)
├── _ARCHIVE/                    # Completed/archived deals
├── .claude/                     # System documentation
│   ├── README.md
│   ├── DOCUMENTATION_INDEX.md
│   ├── NEBUCHADNEZZAR_REFERENCE.md
│   ├── DAILY_SYNC_OPERATIONS.md
│   ├── HUBSPOT_WORKFLOW_GUIDE.md
│   └── DEAL_FOLDER_TEMPLATE.md
├── HubSpot/                     # CRM integration docs
│   ├── HUBSPOT_MCP_CHEATSHEET.md
│   └── CLAUDE.md
├── BULK_RATE_PROCESSING/        # Rate creation templates
│   └── RATE_CREATION_BLITZ.md
├── XPARCEL_NATIONAL_SELECT/     # Network analysis tools
├── .github/                     # GitHub integration
│   ├── workflows/
│   │   └── claude.yml
│   └── CLAUDE_CONTEXT.md (this file)
├── config.py                    # Python configuration
├── hubspot_config.py            # HubSpot integration
├── date_utils.py                # Date handling utilities
└── requirements.txt             # Python dependencies
```

### External Locations

```
Desktop/
├── AUTOMATION_MONITOR_LOCAL.html  # Dashboard
└── NEBUCHADNEZZAR_CONTROL.bat     # Control panel

Downloads/
├── _PIPELINE_TRACKER.csv          # Master database
├── _DAILY_LOG.md                  # Activity log
├── _DAILY_LOG_FEEDBACK.md         # Learning capture
└── FOLLOW_UP_REMINDERS.txt        # Action queue
```

---

## Common Data Processing Patterns

### CSV/Excel Loading

```python
import pandas as pd

# Handle various date formats
date_cols = ['created', 'delivered', 'ship_date', 'Request Date']
df = pd.read_csv(file, parse_dates=date_cols, dayfirst=False)

# Handle tracking numbers in scientific notation
df['tracking'] = df['tracking'].astype(str).str.replace('.0', '', regex=False)

# Standardize service level names
service_map = {
    'Ground': 'Xparcel Ground',
    'Expedited': 'Xparcel Expedited',
    'Priority': 'Xparcel Priority',
    'Direct Call': 'Xparcel Priority'  # Data mapping
}
```

### Zone Analysis Pattern

**Critical for pricing**: Zones 1-8 with Regional (1-4) vs Cross-Country (5-8) grouping

```python
def categorize_zone(zone):
    if zone in [1, 2, 3, 4]:
        return 'Regional'
    elif zone in [5, 6, 7, 8]:
        return 'Cross-Country'
    else:
        return 'Unknown'
```

### Excel Report Generation

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# FirstMile branding
FIRSTMILE_BLUE = '366092'
header_fill = PatternFill(start_color=FIRSTMILE_BLUE, end_color=FIRSTMILE_BLUE, fill_type='solid')
header_font = Font(color='FFFFFF', bold=True)

# Apply to headers
for cell in ws[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center')
```

---

## Python Scripts & Tools

### Daily Workflow Scripts

```bash
# Morning priority report
python daily_9am_workflow.py

# Task verification
python daily_9am_sync.py

# Pipeline sync check
python pipeline_sync_verification.py

# HubSpot verification
python hubspot_pipeline_verify.py
```

### Analysis Scripts

```bash
# PLD analysis
python pld_analysis.py

# Performance reporting
python firstmile_orchestrator.py

# Rate application
python apply_firstmile_rates.py

# Pricing matrix
python create_pricing_matrix.py

# Revenue calculator
python revenue_calculator.py

# Invoice audit
python invoice_audit_builder_v31.py
```

### Dependencies

```bash
pip install pandas numpy openpyxl xlsxwriter matplotlib seaborn plotly
```

---

## Troubleshooting Guide

### Sync Issues

**Folder not syncing to HubSpot**:
```bash
python pipeline_sync_verification.py
```

**Missing tasks in HubSpot**:
```bash
python daily_9am_sync.py
```

**Stage ID errors**:
- Check `.claude/NEBUCHADNEZZAR_REFERENCE.md` for correct UUID format
- Verify stage IDs match HubSpot pipeline (8 stages, not 10)

### Script Errors

**Import errors**:
```bash
pip install -r requirements.txt
```

**API authentication**:
- Verify HubSpot API key in `.env` file
- Check Owner ID: 699257003
- Confirm Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

**Date parsing issues**:
- Use `date_utils.py` functions for consistency
- Check for timezone handling

**Encoding errors**:
- Scripts use UTF-8 encoding
- Check Windows console encoding settings

### Data Quality

**Tracking numbers as scientific notation**:
```python
df['tracking'] = df['tracking'].astype(str).str.replace('.0', '', regex=False)
```

**Service level inconsistencies**:
- Apply `service_map` standardization
- Watch for "Direct Call" → "Xparcel Priority" mapping

**Billable weight discrepancies**:
- Verify calculations match carrier rules (see Critical Business Rules)
- Check for rounding errors in weight conversions

---

## Common Pitfalls & Anti-Patterns

### ❌ What NOT to Do

1. **Never lead reports with daily delivery %** → Always SLA compliance first
2. **Don't name specific carriers** → Use "National" or "Select" network
3. **Don't use [00-LEAD] or [09-WIN-BACK] in HubSpot** → Only 8 stages exist
4. **Don't use simple numbers for stage IDs** → Must use full UUIDs
5. **Don't assume folder name = HubSpot stage** → Always verify sync
6. **Don't skip billable weight validation** → Critical for accurate pricing
7. **Don't use emojis in customer reports** → Professional tone only
8. **Don't skip Read before Write/Edit** → File operations security

### ✅ Best Practices

1. **Pre-check internal dependencies** before customer communications
2. **Create Customer Relationship Docs** for all [01-QUALIFIED]+ deals
3. **Ask about additional locations/brands** in every discovery call
4. **Use dedicated emails** for critical asks (dimensions, data)
5. **Document loss reasons immediately** in [08-CLOSED-LOST]
6. **Target <7 day turnaround** for rate creation (competitive edge)
7. **Follow 7d, 14d, 30d cadence** for proposal follow-ups
8. **Run tests before marking complete** → `lint`, `typecheck`, validation

---

## GitHub Claude Use Cases

### Code Reviews

**When to mention @claude**:
- Pull requests with rate calculation changes
- Performance report script updates
- HubSpot integration modifications
- Pipeline automation changes
- Data processing script reviews

**What Claude checks**:
- FirstMile brand compliance
- Billable weight calculation accuracy
- SLA reporting standards
- HubSpot API usage correctness
- Python best practices

**Example**:
```
@claude review this PR for:
1. Billable weight calculation accuracy
2. FirstMile brand standards (SLA first, no carrier names)
3. HubSpot stage ID correctness
4. Data quality handling (tracking numbers, dates)
```

### Bug Analysis

**When to mention @claude**:
- Pipeline sync failures
- HubSpot API errors
- Data processing issues
- Report generation bugs
- Automation workflow problems

**Example**:
```
@claude investigate this pipeline sync failure:
- Folder: [03-RATE-CREATION]_Acme_Corp
- HubSpot shows deal in [02-DISCOVERY-COMPLETE]
- _PIPELINE_TRACKER.csv shows [03-RATE-CREATION]
- Logs attached in issue description
```

### Documentation Requests

**When to mention @claude**:
- New script documentation
- Workflow explanation
- Business rule clarification
- Integration guide updates

**Example**:
```
@claude document this new invoice audit script:
- Purpose and use cases
- Input requirements
- Output format
- Integration with deal folder structure
```

### Optimization Suggestions

**When to mention @claude**:
- Script performance improvements
- Data processing efficiency
- Report generation optimization
- Workflow automation enhancements

**Example**:
```
@claude suggest optimizations for this PLD analysis script:
- Currently processes 100K rows in 45 seconds
- Memory usage spikes at 2GB
- Looking for pandas/numpy optimizations
```

---

## Quick Reference Card

### Essential Commands

```bash
# HubSpot
qm hubspot search-deals --owner-id 699257003
qm hubspot update-deal --deal-id [ID] --stage "[STAGE]"
qm hubspot create-task --deal-id [ID] --title "[TITLE]"

# Daily Sync
python daily_9am_workflow.py
python pipeline_sync_verification.py

# Analysis
python pld_analysis.py
python firstmile_orchestrator.py
python apply_firstmile_rates.py
```

### Critical IDs

```
Owner: 699257003
Pipeline: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
Portal: 46526832
```

### File Locations

```
Docs: .claude/
Deals: [##-STAGE]_Company_Name/
Database: Downloads/_PIPELINE_TRACKER.csv
Logs: Downloads/_DAILY_LOG.md
```

### Brand Standards

```
Color: #366092 (FirstMile blue)
Lead with: SLA compliance
Avoid: Carrier names, emojis, marketing language
Services: Xparcel Ground (3-8d), Expedited (2-5d), Priority (1-3d)
```

---

## Documentation Links

**Complete System Documentation**: `.claude/` folder

- **[README.md](.claude/README.md)** - System overview & quick start
- **[DOCUMENTATION_INDEX.md](.claude/DOCUMENTATION_INDEX.md)** - Navigation guide
- **[NEBUCHADNEZZAR_REFERENCE.md](.claude/NEBUCHADNEZZAR_REFERENCE.md)** - All IDs & commands
- **[DAILY_SYNC_OPERATIONS.md](.claude/DAILY_SYNC_OPERATIONS.md)** - 9AM, NOON, EOD workflows
- **[HUBSPOT_WORKFLOW_GUIDE.md](.claude/HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot integration
- **[DEAL_FOLDER_TEMPLATE.md](.claude/DEAL_FOLDER_TEMPLATE.md)** - Standard structure

**START HERE**: [.claude/README.md](.claude/README.md)

---

## System Status

**Version**: Nebuchadnezzar v2.0
**Status**: Production Active
**Pipeline Value**: $81.7M across 87 deals
**Automation**: Zero manual data entry
**Integration**: Folder ↔ HubSpot ↔ N8N
**Target**: 40% savings for customers, 2-day nationwide delivery

---

**"Free your mind from manual processes. The system sees all movements."**

*— The Nebuchadnezzar v2.0*
