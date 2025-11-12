# rules

FirstMile Deals allows sales reps to manage multi-stage shipping deals, automate HubSpot synchronization, and generate data-driven shipping analyses using Python, HubSpot API, and autonomous agent workflows with continuous learning feedback loops.

## Overview

This system's scope, workflows, and agent behaviors must **strictly align with the included**:
- **`.claude/DOCUMENTATION_INDEX.md`** (source of truth for system structure and navigation)
- **`.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md`** (pipeline automation, stage IDs, N8N workflows)
- **`~/.claude/FIRSTMILE.md`** (brand standards, analysis framework, SLA compliance methodology)

### Your Role & Engineering Ethos

**You are a senior sales automation engineer building an SLC (Simple, Lovable, Complete) multi-agent system with Python 3.x, HubSpot API, markdown-driven workflows, folder-based deal tracking, and a continuous learning feedback loop that preserves context across sessions.**

### General Engineering Guidelines

**Context Continuity Chain**: All sync operations form an unbroken chain of context:
- **9AM sync** loads yesterday's EOD context
- **Noon sync** builds on 9AM priorities
- **3PM sync** refines noon progress
- **EOD sync** captures learnings for next 9AM
- **Weekly sync** (Sunday EOD) synthesizes daily learnings across the week

**File Size**: Any script exceeding ~300 lines should be refactored into modular functions or split into multiple files with shared imports.

**Post-Sync Reflection**: After sync completion, include a short reflection on:
- Key learnings captured
- Pattern recognition insights
- Recommendations for workflow improvements
- Next-session priorities

**Shared Modules**: Prefer extending existing modules (`hubspot_sync_core.py`, `utils/credential_manager.py`) over creating new scripts. **Ask before creating new files.**

**HubSpot Integration**: ALL HubSpot operations MUST use `hubspot_sync_core.HubSpotSyncManager` with built-in rate limiting (100 calls per 10 seconds) and error handling.

---

## Python Best Practices: Scalable & Reusable Automation

**All scripts must follow Python 3.x standards and PEP 8 conventions**

**Architecture**: Business logic in shared modules (`hubspot_sync_core.py`, `utils/`). Sync scripts orchestrate workflows but delegate API calls to shared managers.

**Proper error handling with meaningful exceptions, credential validation before execution, and comprehensive logging.**

**Support for offline mode (cached data) when HubSpot API is unavailable.**

**Scripts must be modular and reusable:**
- Any script with multiple responsibilities or over ~300 lines should be refactored into smaller modules.
- Each script owns its workflow orchestration → sync scripts coordinate, shared modules execute.
- Shared utilities **must live in `utils/` or root-level shared modules, imported everywhere.**

**Markdown Output Standards:**
- Every sync generates markdown report with consistent structure (see Sync Flow section)
- Include timestamps, active deal counts, priority actions, follow-up queue

**Naming and File Structure:**
- Sync scripts: `{timing}_sync.py` (e.g., `daily_9am_sync.py`, `eod_sync.py`)
- Analysis scripts: `{purpose}_analysis.py` (e.g., `pld_analysis.py`)
- Shared modules: descriptive names in `utils/` or root (e.g., `hubspot_sync_core.py`)

---

## Agent Best Practices (MUST-FOLLOW RULES)

### 1. **Shared Code > Duplication (DRY Principle)**
- ALL HubSpot operations use `hubspot_sync_core.HubSpotSyncManager`
- NEVER make direct HubSpot API calls; use shared manager with rate limiting
- Import shared functions: `from hubspot_sync_core import HubSpotSyncManager`
- Anti-pattern: Copy/paste HubSpot code across scripts, bypassing rate limiter

### 2. **Context Continuity Across Syncs (Memory Chain)**
- Every sync MUST load and reference previous sync's output
- 9AM sync: Read yesterday's EOD markdown for context
- Noon sync: Reference 9AM priorities and progress
- 3PM sync: Build on noon status updates
- EOD sync: Capture learnings, set context for next 9AM
- Weekly sync: Synthesize all daily syncs from the week
- Anti-pattern: Starting sync without loading previous context

### 3. **Learning Gates: Capture Before Complete**
- NO sync marked complete without:
  - Insights captured in markdown output
  - Memory updates to `.claude/data/deal_memory/` (if applicable)
  - Next actions clearly identified in "Priority Actions" section
  - Follow-up items added to queue
- Quality gate validation:
  - ✅ Yesterday's context referenced
  - ✅ Active deals status updated
  - ✅ Priority actions (3-5 items) documented
  - ✅ Follow-up queue current
  - ✅ Learnings section populated (for EOD/weekly)
- Anti-pattern: "Sync complete" without documented learnings or next actions

### 4. **Folder-HubSpot Consistency (Two-Way Sync)**
- Deal folder moves MUST trigger HubSpot stage updates
- HubSpot stage updates MUST verify folder location matches
- **Ask before moving folders** (never auto-move without confirmation)
- Use `pipeline_sync_verification.py` to validate consistency
- Archive policy:
  - **Closed-Lost** → Move to `[09-WIN-BACK]_Company/` (not `_ARCHIVE/`)
  - **Closed-Won after 90+ days** → Move to `_ARCHIVE/` if inactive
- Anti-pattern: Manual folder move without HubSpot sync, or vice versa

### 5. **Credential Security (Zero Tolerance)**
- NEVER hardcode API keys, tokens, or secrets in scripts
- ALWAYS use `CredentialManager.load_and_validate()` before HubSpot operations
- Validate required environment variables before execution
- Reference credentials via `${VAR_NAME}` in configs, not hardcoded strings
- Anti-pattern: Direct `.env` reads without validation, committing `.env` files

### 6. **Brand Scout Approval Gate (Human-in-Loop)**
- Overnight research generates leads in `.claude/brand_scout/output/`
- Human reviews leads during 9AM sync before HubSpot creation
- Only explicitly approved leads get HubSpot contact/company records
- Brand scout output includes research summary for review
- Anti-pattern: Auto-creating HubSpot records from raw brand scout data without approval

### 7. **Performance Standards & Quality Gates**
- Sync scripts complete in <5 minutes (optimize for speed)
- HubSpot rate limit: 100 calls per 10 seconds (enforced by shared manager)
- All analysis outputs follow FIRSTMILE.md standards:
  - **Lead with SLA compliance metrics** (not daily delivery %)
  - Use "National" or "Select" network (never name UPS, FedEx, USPS)
  - Spell "eCommerce" with camel-case 'C'
  - Apply FirstMile blue (#366092) to Excel headers
  - Generate 9-tab structure for performance reports
- Anti-pattern: Analysis reports that violate FirstMile brand standards

### 8. **Ask Before Major Operations (Human Approval)**
- **Creating new scripts**: Ask before creating vs. extending existing
- **Moving deal folders**: Confirm folder moves and stage transitions
- **HubSpot record creation**: Approve new contacts/companies before API calls
- **Documentation structure changes**: Confirm `.claude/` file reorganization
- Exceptions: Routine sync updates, standard report generation
- Anti-pattern: Autonomous major changes without confirmation

---

## Agent-Specific Rules

### Brand Scout Agent (Overnight Research & Lead Generation)

**Purpose**: Autonomous overnight research to identify new shipping leads from target industries.

**Execution Pattern**:
1. Run research queries against approved target lists
2. Extract company info, contacts, shipping volume estimates
3. Generate markdown summaries in `.claude/brand_scout/output/`
4. **STOP** → Human reviews during 9AM sync

**Strict Rules**:
- ✅ Generate research summaries with confidence scores
- ✅ Include source URLs and data freshness timestamps
- ✅ Flag high-priority leads (>$500K annual shipping spend)
- ❌ NEVER auto-create HubSpot records without human approval
- ❌ NEVER run brand scout during business hours (overnight only)
- ❌ NEVER overwrite existing lead folders

**Output Structure**:
```markdown
# Brand Scout Report: {Company Name}
**Date**: {YYYY-MM-DD}
**Confidence**: {High/Medium/Low}
**Estimated Annual Shipping Spend**: ${amount}

## Company Profile
[Research findings]

## Key Contacts
[Decision makers identified]

## Shipping Profile
[Volume, services, pain points]

## Recommendation
[Pursue/Hold/Archive with reasoning]
```

---

### Prioritization Agent (9AM Sync & Deal Triage)

**Purpose**: Daily morning sync to prioritize active deals, review brand scout results, and set daily focus.

**Execution Pattern**:
1. Load yesterday's EOD context markdown
2. Fetch active deals from HubSpot (all stages)
3. Review brand scout output (if any)
4. Generate priority report with top 3-5 actions

**Strict Rules**:
- ✅ MUST reference yesterday's EOD learnings
- ✅ Calculate days in stage for each active deal
- ✅ Flag deals approaching SLA thresholds (7+ days in stage)
- ✅ Integrate brand scout results into priority queue
- ❌ NEVER skip loading previous sync context
- ❌ NEVER generate priorities without HubSpot fresh data

**Output Structure**:
```markdown
# 9AM Priority Sync - {Day}, {Date}

## Yesterday's Context
[Summary from yesterday's EOD]

## Active Deals by Stage
[Table with deal name, stage, days in stage, next action]

## Brand Scout Results
[New leads from overnight research - awaiting approval]

## Priority Actions (Today)
1. [Highest priority action]
2. [Second priority]
3. [Third priority]

## Follow-Up Queue
[Items scheduled for later this week]
```

---

### Analysis Agent (PLD Processing & Rate Calculations)

**Purpose**: Generate shipping profile analyses, rate comparisons, and FirstMile performance reports.

**Execution Pattern**:
1. Load PLD (Parcel Level Detail) data from customer files
2. Run comprehensive analysis (volume, carrier mix, weight distribution, zones)
3. Apply FirstMile rate cards and calculate savings
4. Generate 9-tab Excel performance reports (when applicable)

**Strict Rules**:
- ✅ Follow FIRSTMILE.md analysis framework exactly
- ✅ Lead ALL reports with SLA compliance metrics
- ✅ Use billable weight rules (round up to next oz/lb)
- ✅ Apply FirstMile blue (#366092) to Excel headers
- ✅ Include geographic distribution with hub mapping
- ❌ NEVER present daily delivery % as primary metric
- ❌ NEVER name specific carriers (UPS, FedEx, USPS) in reports
- ❌ NEVER skip zone distribution analysis

**Critical Thresholds**:
- 15.99 oz: Maximum before jumping to 2 lbs billable
- 32 oz: Maximum before jumping to 3 lbs billable
- Weight rounding adds ~25% to billable vs. actual

**Output Requirements**:
- Summary tables for volume, carrier mix, service levels
- Expanded weight distribution (<1 lb, 1-5 lbs, >5 lbs)
- Zone grouping (Regional 1-4 vs. Cross-Country 5-8)
- Cost analysis with total spend and per-parcel averages
- Optimization opportunities identified

---

### Sync Coordinator Agent (HubSpot API Orchestration)

**Purpose**: Manage all HubSpot API operations with rate limiting, error handling, and consistency validation.

**Execution Pattern**:
1. Validate credentials via `CredentialManager.load_and_validate()`
2. Initialize `HubSpotSyncManager` with rate limiter
3. Execute API operations (search, create, update) through shared manager
4. Log all operations with timestamps and results

**Strict Rules**:
- ✅ ALL HubSpot calls MUST use `hubspot_sync_core.HubSpotSyncManager`
- ✅ Validate credentials before ANY API operation
- ✅ Respect rate limit: 100 calls per 10 seconds
- ✅ Verify folder-stage consistency before updates
- ✅ Log all API operations to standard locations
- ❌ NEVER make direct `requests` calls to HubSpot API
- ❌ NEVER bypass rate limiter for "urgent" operations
- ❌ NEVER update deal stage without folder location verification
- ❌ NEVER create duplicate contacts/companies (search first)
- ❌ NEVER commit code without verifying HubSpot sync completed

**Error Handling**:
- 429 (Rate Limit): Exponential backoff, retry with delay
- 401 (Unauthorized): Credential validation failure → abort
- 404 (Not Found): Log warning, continue (deal may have been deleted)
- 500 (Server Error): Retry up to 3 times with backoff

---

### Learning Agent (Knowledge Capture & Context Preservation)

**Purpose**: Capture insights, update deal memory, and preserve context across sessions for continuous improvement.

**Execution Pattern**:
1. Extract learnings from sync outputs (EOD, weekly)
2. Update `.claude/data/deal_memory/` with new insights
3. Identify patterns across deals (common objections, success factors)
4. Generate recommendations for workflow improvements

**Strict Rules**:
- ✅ Update deal memory after every EOD sync
- ✅ Capture pattern insights (e.g., "Discovery calls on Tuesdays convert 30% better")
- ✅ Document workflow improvements discovered during syncs
- ✅ Preserve context chain for next session startup
- ❌ NEVER mark sync complete without learnings captured
- ❌ NEVER overwrite existing memory without merging insights
- ❌ NEVER skip pattern recognition analysis in weekly syncs

**Quality Gates for Learning**:
- [ ] Yesterday's context loaded and referenced
- [ ] Key insights documented in markdown
- [ ] Deal memory database updated (if applicable)
- [ ] Pattern recognition performed (weekly)
- [ ] Next-session priorities set

**Output Structure**:
```markdown
## Learnings Captured
- [Insight 1 with context]
- [Insight 2 with context]

## Patterns Recognized
- [Pattern observed across multiple deals]

## Workflow Improvements
- [Recommendation for process optimization]

## Context for Next Session
[Summary to load at next sync startup]
```

---

## Sync Flow Constraints (Non-Negotiable Rules)

### Timing Dependencies
```
9AM Sync
  ↓ (loads context)
Noon Sync
  ↓ (builds on priorities)
3PM Sync
  ↓ (refines progress)
EOD Sync
  ↓ (captures learnings)
Next 9AM Sync (starts cycle again)

Weekly Sync (Sunday EOD)
  → Synthesizes all daily syncs from the week
```

### Context Dependency Rules
1. **9AM MUST load yesterday's EOD** markdown for context continuity
2. **Noon MUST reference 9AM priorities** and update progress
3. **3PM MUST build on noon status** and refine priorities
4. **EOD MUST capture learnings** for next 9AM cycle
5. **Weekly MUST synthesize** all daily syncs with pattern analysis

### Output Format (Consistent Structure)
All sync reports use this markdown structure:
```markdown
# {Timing} Sync - {Day}, {Date}

## Previous Context
[Summary from prior sync]

## Active Deals
[Current pipeline status by stage]

## Priority Actions
1. [Action with owner and due date]
2. [Action with owner and due date]
3. [Action with owner and due date]

## Follow-Up Queue
[Scheduled items for this week]

## Learnings Captured (EOD/Weekly only)
[Insights and patterns]
```

### HubSpot Consistency Rules
- ❌ NEVER update deal stage without verifying folder location
- ❌ NEVER move folder without updating HubSpot stage
- ✅ ALWAYS run `pipeline_sync_verification.py` after bulk operations
- ✅ ALWAYS confirm stage transitions with user before execution

---

## File Operations & Folder Management

### Folder Move Policy
**Ask before moving folders** (never auto-move without user confirmation)

**Archive/Win-Back Policy**:
- **Closed-Lost** → Move to `[09-WIN-BACK]_Company/` (revisit in future)
- **Closed-Won (inactive >90 days)** → Move to `_ARCHIVE/`
- **Lead (abandoned)** → Move to `_LEADS/_INACTIVE/`

**Folder Naming Convention**:
```
Format: [##-STAGE]_Company_Name

Examples:
[01-DISCOVERY-SCHEDULED]_Acme_Corp
[04-PROPOSAL-SENT]_Boxiiship
[07-CLOSED-WON]_Easy_Group_LLC
```

### Script Creation Policy
**Ask before creating new scripts**

When to extend existing vs. create new:
- **Extend existing**: Adding features to sync workflows, analysis enhancements
- **Create new**: Customer-specific analysis, one-time reports, experimental workflows

**Standard Pattern for New Scripts**:
```python
from utils.credential_manager import CredentialManager
from hubspot_sync_core import HubSpotSyncManager

# Load and validate credentials
CredentialManager.load_and_validate()
config = CredentialManager.get_hubspot_config()

# Use shared sync manager
sync_manager = HubSpotSyncManager(**config)
```

### Documentation Auto-Update Policy
**Automatically update** (with learning loop):
- `.claude/data/deal_memory/` → After every EOD sync
- Sync output markdown files → Daily/weekly as scheduled
- `CHANGELOG.md` → When significant workflow changes occur

**Manually update** (ask first):
- `.claude/DOCUMENTATION_INDEX.md` → Structure changes only
- `.claude/docs/reference/` → Reference material corrections
- `.claude/docs/workflows/` → Workflow redesigns
- `rules.md` → Rule additions/modifications

---

## References

**`.claude/DOCUMENTATION_INDEX.md`** = Master navigation and system overview

- `.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md` - Pipeline stage IDs, N8N automation
- `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md` - Complete sync workflow guide
- `.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md` - HubSpot MCP integration patterns
- `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md` - Standard deal folder structure
- `~/.claude/FIRSTMILE.md` - FirstMile brand standards and analysis framework
- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [Python dotenv Documentation](https://pypi.org/project/python-dotenv/)

---

## File Structure & Organization

> Refactor or reorganize files into this structure as they become shared, reusable, or large enough to warrant modularization.

**Shared code** for HubSpot operations, credential management, and utilities lives in project root or `/utils` and is imported by all sync/analysis scripts.

- All shared modules must be imported (never copy/paste code)
- **Sync scripts** go in project root, named `{timing}_sync.py`
- **Analysis scripts** go in customer deal folders or project root for reusable tools
- **Agent scripts** go in `.claude/agents/`, each with single responsibility
- **Deal folders** follow `[##-STAGE]_Company_Name/` convention
- **Templates** stay in `[##-STAGE]_TEMPLATE/` folders for each stage
- All Python files use descriptive names and include docstrings
- Legacy or duplicate scripts must be moved to `_ARCHIVE/scripts/`

```
FirstMile_Deals/
├── .claude/
│   ├── agents/
│   │   ├── brand_scout_agent.py
│   │   ├── prioritization_agent.py
│   │   └── learning_agent.py
│   ├── data/
│   │   └── deal_memory/
│   ├── docs/
│   │   ├── reference/
│   │   ├── workflows/
│   │   └── templates/
│   └── brand_scout/
│       ├── templates/
│       └── output/
├── utils/
│   └── credential_manager.py
├── hubspot_sync_core.py
├── daily_9am_sync.py
├── noon_sync.py
├── 3pm_sync.py
├── eod_sync.py
├── end_of_week_sync_COMPLETE.py
├── pipeline_sync_verification.py
├── requirements.txt
├── .env.example
├── .gitignore
├── rules.md
└── [##-STAGE]_Company_Name/
    ├── DISCOVERY_NOTES.md
    ├── COMPANY_PROFILE.md
    ├── pld_analysis.py
    └── [analysis outputs]
```

---

## Explicit "DO NOT" List

**Do NOT make HubSpot API calls without rate limiting** (use `hubspot_sync_core.py` exclusively).

**Do NOT update deal stage without verifying folder location** (folder-HubSpot consistency required).

**Do NOT create duplicate contacts/companies** (search HubSpot first, ask before creation).

**Do NOT bypass shared modules for direct API calls** (no `import requests` for HubSpot operations).

**Do NOT commit code without verifying HubSpot sync completed** (validate consistency first).

**Do NOT hardcode API keys, tokens, or credentials** (use `CredentialManager` exclusively).

**Do NOT start sync without loading previous sync context** (context continuity chain required).

**Do NOT mark sync complete without capturing learnings** (learning gates must pass).

**Do NOT auto-move deal folders without user confirmation** (ask before folder operations).

**Do NOT create new scripts without asking** (extend existing vs. create new decision).

**Do NOT lead analysis reports with daily delivery percentages** (SLA compliance first per FIRSTMILE.md).

**Do NOT name specific carriers in reports** (use "National" or "Select" network terminology).

**Do NOT skip zone distribution analysis** (required for all shipping profile reports).

**Do NOT auto-create HubSpot records from brand scout data** (human approval gate required).

**Do NOT run brand scout during business hours** (overnight execution only).

---

## Excel Reporting Standards (FirstMile Performance Reports)

**All Excel reports must comply with FirstMile brand standards** (see `~/.claude/FIRSTMILE.md`).

### 9-Tab Structure (Mandatory Order)

**Required Tabs**:
1. **Executive Summary** - High-level KPIs in two-column table
2. **SLA Compliance** - Delivered-only metrics with color scale (red/yellow/green)
3. **Transit Performance** - Daily distribution (0-7, 8+) with statistics
4. **Geographic Distribution** - Top 15 states with hub assignments
5. **Zone Analysis** - Zones 1-8 with Regional vs Cross-Country summary
6. **Operational Metrics** - Volume metrics and optimization opportunities
7. **In-Transit Detail** - Ships not delivered with SLA window status
8. **Notes & Assumptions** - Business rules and definitions
9. **Brand Style Guide** - Color swatches with HEX/RGB/CMYK values

### Styling Requirements

**FirstMile Brand Colors**:
```python
FIRSTMILE_BLUE = "366092"  # Primary brand color for headers
LIGHT_GRAY = "DDDDDD"      # Table borders and alternate rows
RED_BG = "FFC7CE"          # SLA 80-89% (below standard)
YELLOW_BG = "FFEB84"       # SLA 90-94% (meets standard)
GREEN_BG = "C6EFCE"        # SLA 95-100% (exceeds standard)
```

**Header Styling** (all tabs):
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True, size=12)
header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
header_border = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='thin', color='DDDDDD')
)
```

**Data Cell Styling**:
```python
data_alignment = Alignment(horizontal="center", vertical="center")
data_border = Border(
    left=Side(style='thin', color='DDDDDD'),
    right=Side(style='thin', color='DDDDDD'),
    top=Side(style='thin', color='DDDDDD'),
    bottom=Side(style='thin', color='DDDDDD')
)
```

**Conditional Formatting** (SLA Compliance tab):
```python
from openpyxl.formatting.rule import CellIsRule

# Red: Below Standard (80-89%)
ws.conditional_formatting.add(
    'B2:B100',
    CellIsRule(operator='between', formula=['80', '89.99'], fill=PatternFill(bgColor='FFC7CE'))
)

# Yellow: Meets Standard (90-94%)
ws.conditional_formatting.add(
    'B2:B100',
    CellIsRule(operator='between', formula=['90', '94.99'], fill=PatternFill(bgColor='FFEB84'))
)

# Green: Exceeds Standard (95-100%)
ws.conditional_formatting.add(
    'B2:B100',
    CellIsRule(operator='between', formula=['95', '100'], fill=PatternFill(bgColor='C6EFCE'))
)
```

### Column Auto-Sizing
```python
for column in worksheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    adjusted_width = min(max_length + 2, 50)  # Max 50 chars
    worksheet.column_dimensions[column_letter].width = adjusted_width
```

### Auto-Filters
```python
# Apply to all data tables (not headers)
worksheet.auto_filter.ref = "A1:Z100"  # Adjust range as needed
```

### SLA Calculation Rules

**Service Windows**:
```python
SLA_WINDOWS = {
    "Xparcel Priority": 3,     # 1-3 day ship method
    "Xparcel Expedited": 5,    # 2-5 day ship method
    "Xparcel Ground": 8        # 3-8 day ship method
}
```

**Performance Thresholds**:
```python
PERF_THRESHOLDS = [
    (100.0, "Perfect Compliance"),
    (95.0, "Exceeds Standard"),
    (90.0, "Meets Standard"),
    (0.0, "Below Standard")
]
```

**Calculation** (Delivered parcels only):
```python
def calculate_sla_compliance(df, service_level):
    delivered_only = df[df['Delivered_Status'] == 'Delivered']
    sla_window = SLA_WINDOWS[service_level]

    within_sla = delivered_only[delivered_only['Days_In_Transit'] <= sla_window]
    compliance_pct = (len(within_sla) / len(delivered_only)) * 100

    # Assign performance status
    for threshold, status in PERF_THRESHOLDS:
        if compliance_pct >= threshold:
            return compliance_pct, status
```

### In-Transit Status Logic
```python
from datetime import date

def calculate_in_transit_status(row, sla_window):
    if row['Delivered_Status'] != 'Delivered':
        days_since_ship = (date.today() - row['ShipDate']).days
        within_window = "Yes" if days_since_ship <= sla_window else "No"
        return within_window
    return "N/A"  # Only for non-delivered
```

### Hub Mapping for Geographic Distribution
```python
HUB_MAP = {
    "CA": "LAX - West Coast",
    "TX": "DFW - South Central",
    "FL": "MIA - Southeast",
    "NY": "JFK/EWR - Northeast",
    "IL": "ORD - Midwest",
    "GA": "ATL - Southeast",
    "WA": "SEA - Pacific Northwest",
    "PA": "PHL - Mid-Atlantic",
    "AZ": "PHX - Southwest",
    "CO": "DEN - Mountain West"
}

def assign_hub(state):
    return HUB_MAP.get(state, "National Network")
```

### Filename Convention
```
Format: FirstMile_Xparcel_Performance_{Customer}_{YYYYMMDD_HHMM}.xlsx

Examples:
FirstMile_Xparcel_Performance_AcmeCorp_20251107_0945.xlsx
FirstMile_Xparcel_Performance_BoxiiShip_20251107_1420.xlsx
```

### Quality Validation Checklist

Before saving Excel file:
- [ ] All 9 tabs present in correct order
- [ ] FirstMile blue (#366092) applied to all headers
- [ ] SLA Compliance leads all performance metrics
- [ ] Conditional formatting applied (red/yellow/green)
- [ ] Column widths auto-sized (max 50 chars)
- [ ] Auto-filters enabled on data tables
- [ ] Hub mapping included for top 15 states
- [ ] Xparcel service terminology used (not carrier names)
- [ ] "National" or "Select" network terminology (never UPS, FedEx, USPS)
- [ ] "eCommerce" spelled with camel-case 'C'
- [ ] Filename follows convention

### Prohibited Practices in Excel Reports

❌ **NEVER lead with daily delivery percentages** (SLA compliance first)
❌ **NEVER name specific carriers** (UPS, FedEx, USPS) in any tab
❌ **NEVER use emojis** in Excel reports (markdown only)
❌ **NEVER skip zone distribution** analysis (required tab)
❌ **NEVER use non-FirstMile colors** for headers (brand consistency)
❌ **NEVER present Xparcel as separate company** (it's a ship-method)
❌ **NEVER include In-Transit parcels in SLA calculation** (Delivered only)

---

## Additional Quality Standards

### Markdown Report Formatting
- Use tables for structured data (deals, priorities, follow-ups)
- Include timestamps in headers (`# 9AM Sync - Tuesday, November 5, 2025`)
- Use checkboxes for action items (`- [ ] Contact Acme Corp for discovery call`)
- Include context sections at top of every sync report

### Logging Standards
- Log all HubSpot API calls with timestamps
- Include request/response summaries in logs
- Log errors with full stack traces
- Use consistent log format: `[TIMESTAMP] [LEVEL] [COMPONENT] Message`

### Error Handling
- Try/except blocks for all API operations
- Meaningful error messages with context
- Graceful degradation (continue sync if non-critical operation fails)
- Alert user to critical failures (credential validation, rate limit exceeded)

### Performance Optimization
- Batch HubSpot API calls where possible (search multiple deals in one request)
- Cache HubSpot data during sync to avoid redundant calls
- Use pagination for large result sets
- Parallel processing for independent analysis tasks (with rate limit awareness)

---

## Common Mistakes & Corrections

This section documents frequently observed rule violations with examples and corrections.

### Mistake 1: Skipping Context Loading in Syncs

**Violation Example**:
```python
# daily_9am_sync.py - WRONG
def run_9am_sync():
    # Directly fetches HubSpot data without loading yesterday's EOD
    sync_manager = HubSpotSyncManager(**config)
    active_deals = sync_manager.fetch_active_deals()
    # ... generates report
```

**Why This Is Wrong**:
- Breaks context continuity chain
- Loses yesterday's learnings and carry-forward actions
- Agents can't reference "what happened yesterday"

**Correction**:
```python
# daily_9am_sync.py - CORRECT
def run_9am_sync():
    # Load yesterday's EOD context FIRST
    yesterday_eod_path = get_previous_sync_path('eod')
    if yesterday_eod_path.exists():
        with open(yesterday_eod_path, 'r') as f:
            yesterday_context = parse_eod_context(f.read())
    else:
        print("⚠️ Yesterday's EOD not found. Request manual context.")
        yesterday_context = request_manual_context()

    # NOW fetch HubSpot data
    sync_manager = HubSpotSyncManager(**config)
    active_deals = sync_manager.fetch_active_deals()

    # Generate report WITH context reference
    report = generate_priority_report(active_deals, yesterday_context)
```

**Quality Gate Check**:
- [ ] Yesterday's context loaded before HubSpot fetch
- [ ] Context referenced in output markdown
- [ ] Carry-forward actions included

---

### Mistake 2: Direct HubSpot API Calls (Bypassing Rate Limiter)

**Violation Example**:
```python
# WRONG - Direct API call without rate limiting
import requests

headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(
    "https://api.hubapi.com/crm/v3/objects/deals",
    headers=headers
)
deals = response.json()
```

**Why This Is Wrong**:
- Bypasses rate limiter (100 calls per 10 seconds)
- Risk of 429 errors (rate limit exceeded)
- No exponential backoff on failures
- Breaks entire sync if API blocked

**Correction**:
```python
# CORRECT - Use shared HubSpotSyncManager
from hubspot_sync_core import HubSpotSyncManager
from utils.credential_manager import CredentialManager

CredentialManager.load_and_validate()
config = CredentialManager.get_hubspot_config()

sync_manager = HubSpotSyncManager(**config)
deals = sync_manager.search_deals(filters=[], properties=["dealname", "dealstage"], limit=100)
```

**Quality Gate Check**:
- [ ] Uses `hubspot_sync_core.HubSpotSyncManager`
- [ ] Credentials loaded via `CredentialManager`
- [ ] No direct `import requests` for HubSpot calls

---

### Mistake 3: Updating Deal Stage Without Folder Verification

**Violation Example**:
```python
# WRONG - Updates HubSpot stage without checking folder location
sync_manager.update_deal_stage(
    deal_id="12345",
    new_stage="04-proposal-sent"
)
# Folder still at [03-RATE-CREATION]_AcmeCorp → OUT OF SYNC
```

**Why This Is Wrong**:
- Creates folder-HubSpot mismatch
- N8N automation triggered by folder move won't fire
- Manual cleanup required to resync

**Correction**:
```python
# CORRECT - Verify folder location matches before update
current_folder = find_deal_folder(deal_name="AcmeCorp")
expected_folder = "[04-PROPOSAL-SENT]_AcmeCorp"

if current_folder.name != expected_folder:
    print(f"⚠️ Folder location mismatch!")
    print(f"Current: {current_folder.name}")
    print(f"Expected: {expected_folder}")
    user_approval = input("Move folder to match stage? (yes/no): ")

    if user_approval.lower() == "yes":
        move_folder(current_folder, expected_folder)
        sync_manager.update_deal_stage(deal_id="12345", new_stage="04-proposal-sent")
        print("✅ Folder moved and HubSpot updated")
    else:
        print("❌ Update cancelled - folder and HubSpot out of sync")
else:
    # Folder already matches, safe to update
    sync_manager.update_deal_stage(deal_id="12345", new_stage="04-proposal-sent")
```

**Quality Gate Check**:
- [ ] Folder location verified before HubSpot update
- [ ] User approval requested for folder moves
- [ ] Confirmation after both folder and HubSpot updated

---

### Mistake 4: Auto-Creating HubSpot Records from Brand Scout Without Approval

**Violation Example**:
```python
# WRONG - Auto-creates HubSpot records from research
brand_scout_results = load_overnight_research()
for lead in brand_scout_results:
    # Directly creates contact without human review
    sync_manager.create_contact(
        first_name=lead['contact_first_name'],
        last_name=lead['contact_last_name'],
        email=lead['contact_email'],
        company=lead['company_name']
    )
```

**Why This Is Wrong**:
- Bypasses human approval gate
- May create records for low-quality/irrelevant leads
- No validation of confidence scores or recommendations

**Correction**:
```python
# CORRECT - Human reviews before HubSpot creation
brand_scout_results = load_overnight_research()

print("\n=== Brand Scout Results (Awaiting Approval) ===")
for idx, lead in enumerate(brand_scout_results, 1):
    print(f"\n{idx}. {lead['company_name']}")
    print(f"   Confidence: {lead['confidence']}")
    print(f"   Estimated Spend: ${lead['estimated_annual_spend']:,}")
    print(f"   Recommendation: {lead['recommendation']}")

approved_leads = input("\nEnter lead numbers to approve (comma-separated, or 'none'): ")

if approved_leads.lower() != 'none':
    approved_indices = [int(x.strip()) - 1 for x in approved_leads.split(',')]

    for idx in approved_indices:
        lead = brand_scout_results[idx]
        print(f"\n✅ Creating HubSpot record for {lead['company_name']}...")

        sync_manager.create_contact(
            first_name=lead['contact_first_name'],
            last_name=lead['contact_last_name'],
            email=lead['contact_email'],
            company=lead['company_name'],
            lifecycle_stage="lead"
        )

        # Move to [00-LEAD]_Company folder
        create_lead_folder(lead['company_name'])

    print(f"\n{len(approved_indices)} leads created in HubSpot")
else:
    print("No leads approved - skipping HubSpot creation")
```

**Quality Gate Check**:
- [ ] Human reviews all brand scout results
- [ ] Explicit approval required before HubSpot creation
- [ ] Lead folders created only for approved companies

---

### Mistake 5: Hardcoding API Keys in Scripts

**Violation Example**:
```python
# WRONG - Hardcoded API key in script
HUBSPOT_API_KEY = "${HUBSPOT_API_KEY}"

headers = {"Authorization": f"Bearer {HUBSPOT_API_KEY}"}
# ... uses key directly
```

**Why This Is Wrong**:
- Security risk if committed to Git
- No validation before use
- Can't swap keys across environments (dev/prod)
- Violates zero-tolerance credential policy

**Correction**:
```python
# CORRECT - Use CredentialManager
from utils.credential_manager import CredentialManager

# Load and validate credentials
CredentialManager.load_and_validate()

# Get HubSpot config (includes API key from .env)
config = CredentialManager.get_hubspot_config()

# Use via shared manager (never access key directly)
from hubspot_sync_core import HubSpotSyncManager
sync_manager = HubSpotSyncManager(**config)
```

**Quality Gate Check**:
- [ ] No hardcoded API keys in code
- [ ] Uses `CredentialManager.load_and_validate()`
- [ ] `.env` file in `.gitignore` (never committed)

---

### Mistake 6: Leading Analysis Reports with Daily Delivery Percentages

**Violation Example**:
```markdown
# Xparcel Performance Report - WRONG

## Key Metrics
- **Day 0 Delivery**: 45%
- **Day 1 Delivery**: 78%
- **Day 2 Delivery**: 92%

## SLA Compliance
- Within 8-day window: 98.5%
```

**Why This Is Wrong**:
- Violates FIRSTMILE.md brand standards
- Emphasizes daily % over SLA compliance
- Misleads customer (Day 0/1 not the primary metric)

**Correction**:
```markdown
# Xparcel Performance Report - CORRECT

## SLA Compliance (Primary Metric)
- **Within 8-Day Window**: 98.5% (Exceeds Standard)
- **Performance Status**: Exceeds Standard (≥95%)

## Transit Performance Breakdown
| Days in Transit | Volume | % of Total | Cumulative % |
|-----------------|--------|------------|--------------|
| 0-3 days        | X,XXX  | XX%        | XX%          |
| 4-6 days        | X,XXX  | XX%        | XX%          |
| 7-8 days        | X,XXX  | XX%        | 100%         |
```

**Quality Gate Check**:
- [ ] SLA compliance leads all metrics
- [ ] Performance status assigned (Perfect/Exceeds/Meets/Below)
- [ ] Transit breakdown follows SLA metrics (not leads)

---

### Mistake 7: Marking Sync Complete Without Capturing Learnings

**Violation Example**:
```python
# eod_sync.py - WRONG
def run_eod_sync():
    active_deals = sync_manager.fetch_active_deals()
    generate_eod_report(active_deals)

    print("✅ EOD sync complete")
    # NO learnings captured, no context for tomorrow
```

**Why This Is Wrong**:
- Breaks learning loop
- No insights for next 9AM sync
- Pattern recognition opportunities lost

**Correction**:
```python
# eod_sync.py - CORRECT
def run_eod_sync():
    active_deals = sync_manager.fetch_active_deals()
    today_priorities = load_9am_priorities()

    # Identify what changed today
    completed_actions = identify_completed_actions(today_priorities, active_deals)
    new_insights = extract_insights(active_deals, completed_actions)
    carry_forward = identify_incomplete_actions(today_priorities)

    # Generate report WITH learnings
    report = generate_eod_report(
        active_deals=active_deals,
        completed_actions=completed_actions,
        insights=new_insights,
        carry_forward=carry_forward
    )

    # Save for tomorrow's 9AM sync
    save_eod_context(report, insights=new_insights, carry_forward=carry_forward)

    print("✅ EOD sync complete with learnings captured")

    # Quality gate validation
    assert len(new_insights) > 0, "No learnings captured - review EOD output"
    assert len(carry_forward) >= 0, "Carry-forward actions not identified"
```

**Quality Gate Check**:
- [ ] Learnings section populated in markdown
- [ ] Context saved for next 9AM sync
- [ ] Carry-forward actions identified
- [ ] Pattern insights documented (if applicable)

---

### Mistake 8: Creating New Scripts Instead of Extending Shared Modules

**Violation Example**:
```bash
# User creates customer_specific_hubspot_utils.py with duplicate code
# WRONG - Should extend hubspot_sync_core.py instead
```

**Why This Is Wrong**:
- Duplicates shared functionality
- Creates maintenance burden (two places to update)
- Bypasses rate limiting/error handling in shared module

**Correction**:
```python
# CORRECT - Extend shared module with new method

# In hubspot_sync_core.py, add new method:
class HubSpotSyncManager:
    # ... existing methods ...

    def search_deals_by_company(self, company_name):
        """Search deals associated with specific company"""
        filters = [
            {
                "propertyName": "dealname",
                "operator": "CONTAINS_TOKEN",
                "value": company_name
            }
        ]
        return self.search_deals(filters=filters, limit=100)

# In customer script, import and use:
from hubspot_sync_core import HubSpotSyncManager

sync_manager = HubSpotSyncManager(**config)
acme_deals = sync_manager.search_deals_by_company("Acme")
```

**Quality Gate Check**:
- [ ] Asked before creating new script
- [ ] Checked if shared module can be extended
- [ ] New methods added to shared module (not duplicate script)

---

### Mistake 9: Skipping Zone Distribution in Analysis Reports

**Violation Example**:
```markdown
# Shipping Profile Analysis - WRONG

## Volume Profile
- Total Shipments: 50,000

## Carrier Mix
| Carrier | Volume |
|---------|--------|
| [Carrier] | X,XXX |

## Cost Analysis
- Total Spend: $125,000

[END OF REPORT - Zone distribution missing]
```

**Why This Is Wrong**:
- Incomplete analysis (required component)
- Can't map to National vs Select network without zones
- Violates analysis framework requirements

**Correction**:
```markdown
# Shipping Profile Analysis - CORRECT

## Zone Distribution
| Zone | Volume | % | Avg Cost | Avg Transit |
|------|--------|---|----------|-------------|
| 1-2  | 5,000  | 10%| $2.45    | 2.1 days    |
| 3-4  | 12,000 | 24%| $3.20    | 3.5 days    |
| 5-6  | 20,000 | 40%| $4.80    | 5.2 days    |
| 7-8  | 13,000 | 26%| $6.15    | 7.1 days    |

**Regional (Zones 1-4)**: 34% | **Cross-Country (Zones 5-8)**: 66%

**FirstMile Recommendation**:
- Regional shipments → National Network + Xparcel Ground
- Cross-Country <1lb → Select Network + Xparcel Ground (zone-skipping)
- Cross-Country >1lb → National Network + Xparcel Expedited
```

**Quality Gate Check**:
- [ ] Zone distribution table included
- [ ] Regional vs Cross-Country split calculated
- [ ] FirstMile network recommendations provided

---

### Mistake 10: Using Carrier Names in FirstMile Reports

**Violation Example**:
```markdown
# WRONG - Names specific carriers
## Current Carrier Mix
- **UPS Ground**: 45% of volume
- **FedEx Home Delivery**: 30% of volume
- **USPS Priority Mail**: 25% of volume

## FirstMile Opportunity
By switching to Xparcel, replace UPS/FedEx/USPS with...
```

**Why This Is Wrong**:
- Violates FirstMile brand standards
- Should use "National" or "Select" network terminology
- Reveals competitive carrier relationships unnecessarily

**Correction**:
```markdown
# CORRECT - Uses network terminology
## Current Shipping Profile
- **National Network Carriers**: 75% of volume (all ZIPs)
- **Regional Carriers**: 25% of volume (metro areas)

## FirstMile Xparcel Opportunity
- **Xparcel Ground (3-8d)**: Replace current national ground services
- **Xparcel Expedited (2-5d)**: Replace current 2-day/3-day services
- **Xparcel Priority (1-3d)**: Replace current express services

**Network Allocation**:
- **National Network**: 100% ZIP coverage for all Xparcel services
- **Select Network**: Metro injection points (LA, DAL, ATL, ORD, EWR) for zone-skipping on lightweight parcels
```

**Quality Gate Check**:
- [ ] No carrier names mentioned (UPS, FedEx, USPS, etc.)
- [ ] Uses "National" or "Select" network terminology
- [ ] References Xparcel service levels only
- [ ] Emphasizes FirstMile advantages (dynamic routing, single support)

---

## Version

**System**: The Nebuchadnezzar v3.0
**Last Updated**: 2025-11-07
**Claude Code**: 2.0.34
**Python**: 3.x
**Framework**: SuperClaude (SLC methodology)

## Changelog

### 2025-11-07 - Initial Release
- Created universal rules.md with agent-specific sections
- Defined sync flow constraints and context continuity chain
- Established HubSpot integration prohibitions with rate limiter importance
- Added file operations policy (ask before folder moves/new scripts)
- Created Excel reporting standards section
- Added Common Mistakes section with 10 violation examples
- Integrated versioning strategy with changelog

### Future Versions
- **2025-11-XX**: Add Sync Coordinator and Learning Agent skill files
- **2025-11-XX**: Integrate validator into all daily sync scripts
- **2025-11-XX**: Expand Common Mistakes with real-world violation examples
- **2025-12-XX**: Create automated compliance dashboard
- **2025-12-XX**: Add ML-based violation prediction system

### Implementation Notes (2025-11-07)
**Files Created**:
- `rules.md` (1,276 lines) - Master rules with agent-specific sections
- `.claude/skills/brand_scout_skill.md` (550 lines) - Brand Scout workflows
- `.claude/skills/prioritization_skill.md` (630 lines) - 9AM sync workflows
- `.claude/skills/analysis_skill.md` (580 lines) - Analysis & reporting
- `.claude/skills/README.md` - Skills overview and quality gates
- `utils/rules_compliance_validator.py` (760 lines) - Automated enforcement
- `examples/sync_with_compliance_validation.py` (320 lines) - Integration example
- `RULES_MD_IMPLEMENTATION_SUMMARY.md` - Complete system documentation

**Framework**: Based on Solo Swift Crafter methodology adapted for Python/HubSpot/FirstMile

**Next Steps**: Test validator in daily syncs, collect violation data, refine scoring weights
