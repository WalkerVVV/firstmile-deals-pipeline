# FirstMile Deals - The Nebuchadnezzar System v3.0

**Complete Sales Execution & Pipeline Management System**

> "The system sees all movements. Zero manual data entry. Pure revenue generation."

---

## 📋 Table of Contents

- [System Overview](#system-overview)
- [Quick Start](#quick-start)
- [Daily Workflow](#daily-workflow)
- [Pipeline Architecture](#pipeline-architecture)
- [HubSpot Integration](#hubspot-integration)
- [Deal Folder Structure](#deal-folder-structure)
- [Analysis & Tools](#analysis--tools)
- [Continuous Learning System](#continuous-learning-system)
- [Troubleshooting](#troubleshooting)

---

## System Overview

The Nebuchadnezzar v3.0 is a fully automated sales pipeline system integrating:

- **10-Stage Pipeline** with folder-based tracking
- **HubSpot CRM** via MCP integration
- **N8N Automation** for workflow triggers
- **Daily Sync Flows** (9AM, NOON, EOD, End of Week)
- **Continuous Learning** feedback loops
- **Python Analytics** for shipping analysis

### Core Statistics
- **Pipeline Value**: $81.7M across 87 deals
- **Automation**: Zero manual data entry
- **Integration**: Folder structure ↔ HubSpot ↔ N8N
- **Target**: 40% savings for customers, 2-day nationwide delivery

---

## Quick Start

### 1. System Location
```
📁 Root: C:\Users\BrettWalker\FirstMile_Deals\
📊 Dashboard: AUTOMATION_MONITOR_LOCAL.html (Desktop)
⚙️ Control: NEBUCHADNEZZAR_CONTROL.bat (Desktop)
```

### 2. Essential Files
```
NEBUCHADNEZZAR_REFERENCE.md .... Complete system reference
FIRSTMILE_PIPELINE_BLUEPRINT.md . HubSpot & N8N integration
Brett_Walker_Instructions_v4.3.md  Morpheus Method & positioning
CLAUDE.md ....................... AI assistant project context
```

### 3. Core Commands
```bash
# HubSpot MCP Operations
qm hubspot create-lead        # Create new lead
qm hubspot convert-to-deal    # Convert lead → deal
qm hubspot search-deals       # Search pipeline
qm hubspot update-deal        # Move deal stages

# Daily Sync Scripts
python daily_9am_workflow.py       # Morning priority report
python daily_9am_sync.py          # Task verification
python pipeline_sync_verification.py  # Folder ↔ HubSpot sync

# 🎯 NEW: Sales Discipline Agents
python .claude/agents/prioritization_agent.py --daily-reminder  # Top 3 priorities
python .claude/agents/sales_execution_agent.py                  # Stale proposal check
python .claude/agents/weekly_metrics_tracker.py                 # 5/2/3/1 goals (Friday)
python .claude/agents/brand_scout_agent.py --batch 10           # 10 leads (Monday 6AM)
```

---

## Daily Workflow

### 9AM Sync - Day Start
**Script**: `daily_9am_workflow.py`

**Purpose**: Generate priority action list with urgency scoring

**Process**:
1. **Phase 0**: Load EOD learnings from previous day
2. **Phase 1**: Review pending customer responses and blockers
3. **Phase 2**: Live pipeline sync from HubSpot
4. **Phase 3**: Priority analysis (P1 immediate, P2 active)
5. **Phase 4**: Generate action items and tasks
6. **Phase 5**: Pipeline health check and SLA violations

**Output**: Priority-ranked action list with next steps

**🎯 NEW - Sales Discipline Integration**:
```bash
# Run after main sync
python .claude/agents/prioritization_agent.py --daily-reminder  # Top 3 priorities
python .claude/agents/sales_execution_agent.py                  # Stale proposals
```
**Output**: Daily priority reminder + urgency follow-up emails

### NOON Sync - Midday Check
**Purpose**: Progress check and afternoon planning

**Process**:
1. Review morning execution completion
2. Process new customer responses
3. Update blocker status
4. Identify afternoon priorities
5. Prep for EOD sync

### EOD Sync - End of Day
**Purpose**: Capture learnings and setup tomorrow

**Process**:
1. **Daily Summary**: Actions completed, touchpoints, movements
2. **Learnings & Insights**: What worked, what failed, what's unclear
3. **Tomorrow's Setup**: Known meetings, deliverables, responses to monitor
4. **Archive**: Save to `_DAILY_LOG_FEEDBACK.md`

**See**: [Continuous Learning System](#continuous-learning-system)

### End of Week Sync - Friday EOD
**Purpose**: Weekly reflection and next week planning

**Process**:
1. Week summary metrics
2. SOP evolution tracking
3. Pipeline velocity analysis
4. Next week priorities
5. Archive learnings to Saner.ai

**🎯 NEW - Weekly Metrics Accountability**:
```bash
python .claude/agents/weekly_metrics_tracker.py
```
**Output**: `~/Downloads/WEEKLY_METRICS_YYYY-MM-DD_to_YYYY-MM-DD.md`
**Tracks**: 5 new leads, 2 discoveries, 3 proposals, 1 close per week
**Coaching**: 4/4 goals = Excellent, 3/4 = Strong, 2/4 = Average, 1/4 = Below, 0/4 = Critical

### Monday 6AM - Weekly Lead Generation
**Purpose**: Automated brand research for 10 new wellness/D2C leads

**🎯 NEW - Brand Scout Automation** (Scheduled):
```bash
python .claude/agents/brand_scout_agent.py --batch 10
```
**Output**: Brand profiles + `[00-LEAD]_BrandName` folders
**Setup**: Windows Task Scheduler, Monday 6:00 AM weekly trigger

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

### Stage Definitions & SLAs

| Stage | Entry Criteria | Follow-up SLA | Exit Criteria | Automation |
|-------|---------------|---------------|---------------|------------|
| [00-LEAD] | First contact | None | Discovery scheduled | Manual |
| [01-DISCOVERY-SCHEDULED] | Call booked | 14 days | Call completed | Stale alert |
| [02-DISCOVERY-COMPLETE] | Requirements doc | 30 days | Data received | Follow-up |
| [03-RATE-CREATION] | Data received | **14 days** | Rates sent | **Critical SLA** |
| [04-PROPOSAL-SENT] | Rates delivered | 30 days | Verbal commit | Follow-up |
| [05-SETUP-DOCS-SENT] | Docs sent | 14 days | Implementation | Urgent |
| [06-IMPLEMENTATION] | Onboarding | 30 days | Go live | Check-in |
| [07-CLOSED-WON] | Shipping live | N/A (CS) | Archive | Success |
| [08-CLOSED-LOST] | Lost | Custom | Win-back | Optional |
| [09-WIN-BACK] | Re-engaged | 30 days | Re-qualified | Monthly |

### Critical Success Metrics
- **[03-RATE-CREATION]**: Bottleneck stage - monitor >14 days
- **[04-PROPOSAL-SENT]**: Revenue at risk - follow up at 7, 14, 30 days
- **[06-IMPLEMENTATION]**: At finish line - daily check-ins

---

## HubSpot Integration

### Configuration
```yaml
Owner ID: 699257003          # Brett Walker
Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
Portal ID: 46526832
```

### Stage IDs (Verified)
```python
STAGE_MAPPING = {
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[01-DISCOVERY-SCHEDULED]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[02-DISCOVERY-COMPLETE]",
    "1090865183": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-CLOSED-WON]",
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[08-CLOSED-LOST]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[09-WIN-BACK]"
}
```

### MCP Tool Usage

**See**: `HubSpot/HUBSPOT_MCP_CHEATSHEET.md` for complete API reference

#### Lead Creation
```bash
qm hubspot create-lead \
  --first-name "John" \
  --last-name "Smith" \
  --email "john@company.com" \
  --company "Acme Corp" \
  --phone "555-123-4567"
```

#### Deal Conversion
```bash
qm hubspot convert-to-deal \
  --contact-id 12345 \
  --deal-name "Acme Corp - Xparcel Ground" \
  --amount 150000 \
  --stage "[02-DISCOVERY-COMPLETE]"
```

#### Pipeline Search
```bash
qm hubspot search-deals \
  --owner-id 699257003 \
  --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

### Workflow Integration
1. **Folder Movement** → Triggers N8N automation
2. **N8N Automation** → Updates HubSpot deal stage
3. **HubSpot Update** → Logs to `_PIPELINE_TRACKER.csv`
4. **Daily Sync** → Verifies alignment

---

## Deal Folder Structure

### Standard Folder Template

```
[##-STAGE]_Company_Name/
├── CLAUDE.md                    # AI context & instructions
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

### Required Files by Stage

**[01-DISCOVERY-SCHEDULED]**:
- Discovery agenda
- Company research

**[02-DISCOVERY-COMPLETE]**:
- Discovery notes
- Requirements doc
- Data request email

**[03-RATE-CREATION]**:
- PLD analysis
- Rate calculations
- JIRA ticket reference

**[04-PROPOSAL-SENT]**:
- Rate card
- Proposal deck
- Follow-up schedule

**[05-SETUP-DOCS-SENT]**:
- Contract
- Implementation plan

**[06-IMPLEMENTATION]**:
- Integration docs
- Test results

**[07-CLOSED-WON]**:
- Performance reports
- Customer success handoff

---

## Analysis & Tools

### PLD (Parcel Level Detail) Analysis

**Standard Workflow**:
```python
# 1. Load shipment data
python pld_analysis.py

# 2. Apply FirstMile rates
python apply_firstmile_rates.py

# 3. Generate pricing matrix
python create_pricing_matrix.py

# 4. Calculate revenue projections
python revenue_calculator.py
```

**Output**: Professional Excel reports with:
- Volume profile (total, daily avg, marketplace mix)
- Carrier mix (current vs FirstMile)
- Service level distribution
- Weight analysis (billable weight rules)
- Zone distribution (Regional vs Cross-Country)
- Geographic coverage (top states, hub mapping)
- Cost analysis (current vs FirstMile savings)

### Performance Reporting

**Script**: `firstmile_orchestrator.py`

**Output**: 9-tab Excel report with:
1. Executive Summary
2. SLA Compliance (primary metric)
3. Transit Performance
4. Geographic Distribution
5. Zone Analysis
6. Operational Metrics
7. In-Transit Detail
8. Notes & Assumptions
9. Brand Style Guide

**Key Rules**:
- **Always lead with SLA compliance** (not daily delivery %)
- Service windows: Priority (3d), Expedited (5d), Ground (8d)
- FirstMile blue (#366092) for branding
- Plain, factual language - no emojis

### Invoice Audit Analysis

**Script**: `invoice_audit_builder_*.py`

**Purpose**: Identify overcharges and refund opportunities
- Compare invoiced vs contracted rates
- Billable weight discrepancies
- Service level mismatches

---

## Continuous Learning System

### Feedback Loop Structure

**Daily Cycle**:
```
9AM Sync → Execution → NOON Check → Execution → EOD Sync → Learning Capture
```

**Weekly Cycle**:
```
Monday 9AM → Daily Syncs → Friday EOD → Weekly Reflection → Archive to Saner.ai
```

### EOD Sync Template

**File**: `_DAILY_LOG_FEEDBACK.md` (Downloads folder)

**Sections**:
1. **What Worked ✅**: Keep and replicate
2. **What Failed ❌**: Fix immediately
3. **What's Unclear ❓**: Need decisions
4. **What's Missing 🔧**: Build or acquire

### SOP Evolution Tracking

**Version Control**:
```yaml
v3.1 - Customer Relationship Docs: ✅ PERMANENT
v3.2 - Automated Stale Alerts: 🟡 TESTING
v3.3 - Multi-Location Discovery: 🟡 PROPOSED
```

**Process**:
1. Identify pattern/problem in EOD sync
2. Propose solution with test date
3. Validate over 1 week
4. Mark PERMANENT or iterate

### Learning Archive

**Daily**: `_DAILY_LOG_FEEDBACK.md`
**Weekly**: Export to Saner.ai notes system
**Monthly**: Pipeline velocity & win/loss analysis
**Quarterly**: System optimization review

---

## Troubleshooting

### Common Issues

#### 1. Folder Movement Not Syncing to HubSpot
**Symptoms**: Folder moved but HubSpot stage unchanged

**Fix**:
```bash
# Verify automation is running
# Check NEBUCHADNEZZAR_CONTROL.bat status

# Manual sync verification
python pipeline_sync_verification.py

# Manual HubSpot update
qm hubspot update-deal --deal-id [ID] --stage "[NEW-STAGE]"
```

#### 2. Missing EMAIL Tasks
**Symptoms**: Deals in priority stages without tasks

**Fix**:
```bash
# Run task verification script
python daily_9am_sync.py

# Creates missing EMAIL tasks automatically
```

#### 3. HubSpot API Authentication
**Symptoms**: 401 errors from MCP tools

**Fix**:
```bash
# Refresh OAuth token
/login

# Verify credentials
qm hubspot get-deal --deal-id [ANY-ID]
```

#### 4. Stage ID Mismatches
**Symptoms**: Deals show in wrong stage

**Fix**:
```bash
# Verify stage IDs
python hubspot_pipeline_verify.py

# Update STAGE_MAPPING in NEBUCHADNEZZAR_REFERENCE.md
```

### Emergency Procedures

**Pipeline Lock Failure**:
1. Check `_PIPELINE_TRACKER.csv` for discrepancies
2. Run `pipeline_sync_verification.py` for detailed mismatch analysis
3. Manually reconcile folders vs HubSpot
4. Restart N8N automation

**Data Loss Prevention**:
- All deal folders auto-backup to `_ARCHIVE/`
- HubSpot is source of truth for deal stages
- Daily logs archived in Downloads folder
- Weekly export to Saner.ai

---

## Project Organization

### Key Directories

```
FirstMile_Deals/
├── [Deal Folders]/              # Active pipeline (10 stages)
├── _ARCHIVE/                    # Completed/archived deals
├── HubSpot/                     # CRM integration docs
│   ├── HUBSPOT_MCP_CHEATSHEET.md
│   └── CLAUDE.md
├── BULK_RATE_PROCESSING/        # Rate creation templates
│   └── RATE_CREATION_BLITZ.md
├── XPARCEL_NATIONAL_SELECT/     # Network analysis tools
├── Python Scripts/              # Automation & sync
│   ├── daily_9am_workflow.py
│   ├── daily_9am_sync.py
│   ├── pipeline_sync_verification.py
│   └── hubspot_pipeline_verify.py
└── Documentation/               # System guides
    ├── README.md (this file)
    ├── NEBUCHADNEZZAR_REFERENCE.md
    ├── FIRSTMILE_PIPELINE_BLUEPRINT.md
    └── Brett_Walker_Instructions_v4.3.md
```

### Related Systems

**Desktop**:
- `AUTOMATION_MONITOR_LOCAL.html` - Real-time dashboard
- `NEBUCHADNEZZAR_CONTROL.bat` - System control

**Downloads**:
- `_PIPELINE_TRACKER.csv` - Master database
- `_DAILY_LOG.md` - Activity log
- `_DAILY_LOG_FEEDBACK.md` - Learning capture
- `FOLLOW_UP_REMINDERS.txt` - Action queue

**Saner.ai**:
- Weekly learning archives
- Strategic insights
- Long-term pattern recognition

---

## Best Practices

### Deal Management
1. **Create Customer Relationship Doc** for all [01-QUALIFIED]+ deals
2. **Ask about additional locations/brands** in every discovery
3. **Pre-check internal dependencies** before customer communications
4. **Use dedicated emails** for critical asks (dimensions, data)
5. **Document loss reasons immediately** in [08-CLOSED-LOST]

### Rate Creation (Bottleneck Stage)
1. Start analysis **immediately** upon data receipt
2. Flag internal blockers in HubSpot notes
3. Target **<7 day turnaround** for competitive edge
4. Alert on deals **>14 days** in stage

### Communication Patterns
- **[01-DISCOVERY-SCHEDULED]**: 3 days before, 1 day reminder
- **[02-DISCOVERY-COMPLETE]**: 7 days if no data
- **[03-RATE-CREATION]**: Daily internal, weekly customer
- **[04-PROPOSAL-SENT]**: 7d, 14d, 30d cadence
- **[05-SETUP-DOCS-SENT]**: 7d, 14d (urgent)

### Automation Rules
- Folder naming: `[##-STAGE]_Company_Name` (exact format)
- HubSpot updates: Use stage IDs not labels
- Task creation: EMAIL type for follow-ups
- Pipeline sync: Run verification weekly

---

## Support & Resources

### Documentation
- [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md) - Complete system reference
- [FIRSTMILE_PIPELINE_BLUEPRINT.md](FIRSTMILE_PIPELINE_BLUEPRINT.md) - Integration guide
- [HubSpot/HUBSPOT_MCP_CHEATSHEET.md](HubSpot/HUBSPOT_MCP_CHEATSHEET.md) - API reference
- [Brett_Walker_Instructions_v4.3.md](Brett_Walker_Instructions_v4.3.md) - Morpheus Method

### Scripts
- `daily_9am_workflow.py` - Priority action generator
- `daily_9am_sync.py` - Task verification
- `pipeline_sync_verification.py` - Sync health check
- `firstmile_orchestrator.py` - Performance reporting

### Contact
**Owner**: Brett Walker
**System**: Nebuchadnezzar v3.0
**Status**: Production (Live)
**Last Updated**: October 7, 2025

---

**"Free your mind from manual processes. The system sees all movements."**

*— The Nebuchadnezzar v3.0*
