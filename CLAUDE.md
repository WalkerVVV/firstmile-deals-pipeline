# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

FirstMile Deals Management System - **The Nebuchadnezzar v3.0**: A fully automated 10-stage sales pipeline with HubSpot CRM integration, Chrome MCP email extraction, and N8N automation.

**Primary Technologies**: Python 3.x, HubSpot API, Chrome MCP, N8N webhooks

**Core Principle**: All automation must "do the work they're designed to do" - no mock/placeholder data, honest failure reporting when systems unavailable.

---

## Critical Architecture

### Unified Sync System (Single Entry Point)

**Location**: `unified_sync.py`

All daily operations run through ONE script with time-specific modes:

```bash
python unified_sync.py 9am    # Morning priority report
python unified_sync.py noon   # Mid-day progress check
python unified_sync.py 3pm    # Afternoon adjustment
python unified_sync.py eod    # End of day wrap-up
python unified_sync.py weekly # Sunday comprehensive sync
python unified_sync.py monthly # Month-end analysis
```

**Architecture Pattern**:
1. Email Integration: Chrome MCP → `superhuman_emails.json` → `mcp_email_extractor.py` subprocess
2. HubSpot Live Data: Direct API calls via `hubspot_sync_core.py`
3. Report Generation: Comprehensive markdown format saved to `sync_reports/`
4. Continuity Chain: Updates `_DAILY_LOG.md` for next sync's context

**Key Files**:
- `sync_reports/` - Timestamped sync outputs (project folder, not Downloads)
- `_DAILY_LOG.md` - Continuity log (project root)
- `FOLLOW_UP_REMINDERS.txt` - Action queue (project root)
- `superhuman_emails.json` - Email cache (refreshed each sync)

### Chrome MCP Email Integration

**CRITICAL**: Two-step architecture (subprocess cannot access MCP tools directly):

**Step 1 - Claude Code extracts emails**:
```
Use Chrome MCP tools in conversation:
- mcp__chrome-mcp-server__chrome_navigate → Open Superhuman
- mcp__chrome-mcp-server__chrome_get_web_content → Extract inbox
- Write structured data to superhuman_emails.json
```

**Step 2 - Subprocess reads cached data**:
```python
# mcp_email_extractor.py reads from JSON file
# unified_sync.py calls subprocess with UTF-8 encoding:
subprocess.run(['python', 'mcp_email_extractor.py'], encoding='utf-8')
```

**Never**:
- Create mock/placeholder email data
- Return `success: True` with fake emails
- Try to access MCP tools from subprocess

**Always**:
- Use real Chrome MCP extraction in Claude Code conversation
- Save extracted data to `superhuman_emails.json`
- Return `success: False` when data unavailable/stale (>2 hours)
- Include UTF-8 stdout wrapper for emoji support

### HubSpot API Integration

**Centralized Module**: `hubspot_sync_core.py`

**Rate Limiting Architecture**:
- Burst limit: 100 requests per 10 seconds (token bucket)
- Daily limit: 150,000 requests per 24 hours
- Automatic retry with exponential backoff
- Thread-safe request queue management

**Standard Pattern**:
```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Direct API calls for scripts (when hubspot_sync_core unavailable)
response = requests.post(
    f"https://api.hubapi.com/crm/v3/objects/deals/search",
    headers=headers,
    json=payload
)
```

**Critical Field Rules**:
- Timestamps: Unix milliseconds as STRING (e.g., `"1738281600000"` for Jan 31, 2025)
- Association type IDs: 214 (Note-Deal), 216 (Task-Deal), 280 (Contact-Company), 341 (Deal-Company)
- Never hardcode API keys (use `.env` file)
- **Read-only fields**: `notes_next_activity_date` cannot be set directly - create tasks instead
- **Required filters**: Always include Owner ID (`699257003`) and Pipeline ID to avoid pulling 3,000+ deals
- **Division protection**: Always check denominators before percentage calculations
- **Custom fields**: Query API for field names, don't guess (e.g., `monthly_volume__c` not `volume_monthly_parcels`)

**Reference**: See `.claude/docs/reference/HUBSPOT_DEAL_HYGIENE_GUIDE.md` for complete API patterns

### Deal Folder Automation

**Naming Convention**: `[##-STAGE]_Company_Name`

Moving folders between stages triggers N8N webhook automation:

```
[00-LEAD] → [01-DISCOVERY-SCHEDULED] → [02-DISCOVERY-COMPLETE] →
[03-RATE-CREATION] → [04-PROPOSAL-SENT] → [05-SETUP-DOCS-SENT] →
[06-IMPLEMENTATION] → [07-CLOSED-WON] → [08-CLOSED-LOST] → [09-WIN-BACK]
```

**Pipeline ID**: `8bd9336b-4767-4e67-9fe2-35dfcad7c8be`

**Stage IDs** (see `.claude/docs/reference/VERIFIED_STAGE_IDS.md`):
- `1090865183`: [01-DISCOVERY-SCHEDULED]
- `d2a08d6f-cc04-4423-9215-594fe682e538`: [02-DISCOVERY-COMPLETE]
- `e1c4321e-afb6-4b29-97d4-2b2425488535`: [03-RATE-CREATION]
- `d607df25-2c6d-4a5d-9835-6ed1e4f4020a`: [04-PROPOSAL-SENT]
- `4e549d01-674b-4b31-8a90-91ec03122715`: [05-SETUP-DOCS-SENT]
- `08d9c411-5e1b-487b-8732-9c2bcbbd0307`: [06-IMPLEMENTATION]
- `3fd46d94-78b4-452b-8704-62a338a210fb`: [07-STARTED-SHIPPING]

---

## Windows Console Encoding (Critical Fix Pattern)

**Problem**: Windows default encoding (cp1252) fails with emojis in output

**Solution**: Add UTF-8 wrapper to ALL Python scripts that output text:

```python
import sys
import io

# Fix Windows console encoding for emoji support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Subprocess Calls**: Use `encoding='utf-8'` parameter:

```python
result = subprocess.run(
    ['python', 'script.py'],
    capture_output=True,
    encoding='utf-8',  # NOT text=True (uses cp1252)
    timeout=30
)
```

**Applied To**:
- `mcp_email_extractor.py`
- `unified_sync.py`
- `update_boxiiship_nov12_meeting.py`
- All scripts that output to console

---

## Brand Scout Lead Generation

**Location**: `.claude/brand_scout/`

**Workflow**:
1. Overnight automated research (external trigger)
2. Generates reports in `.claude/brand_scout/output/`
3. Creates `[00-LEAD]_CompanyName` folders with research
4. 9AM sync detects new leads and prompts outreach

**Template**: `.claude/brand_scout/BRAND_SCOUT_TEMPLATE.md`
**Process**: `.claude/brand_scout/HUBSPOT_LEAD_CREATION_PROCESS.md`

**HubSpot Integration**:
```python
# 6-step automation:
# 1. Create company
# 2. Create primary contact (CEO/Founder)
# 3. Create secondary contact (COO/Operations)
# 4. Associate contacts with company
# 5. Create deal
# 6. Associate deal with company and contacts
```

---

## Common Commands

### Daily Operations

```bash
# Morning sync (9AM)
python unified_sync.py 9am

# Noon check
python unified_sync.py noon

# End of day wrap
python unified_sync.py eod

# Update specific HubSpot deal
python update_boxiiship_nov12_meeting.py  # Example deal update script
```

### Customer Analysis

```bash
# PLD (Parcel Level Detail) analysis
cd [CUSTOMER]_Folder
python pld_analysis.py

# FirstMile performance report (9-tab Excel)
python firstmile_orchestrator.py

# Rate application and savings calculation
python apply_firstmile_rates.py

# Invoice audit analysis
python invoice_audit_builder_v31.py
```

### HubSpot Operations

```bash
# Search deals by stage
qm hubspot search-deals --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Create lead with contacts
python create_[company]_lead.py  # Generated by Brand Scout

# Update deal stage (triggers N8N automation)
qm hubspot update-deal --deal-id [ID] --stage "[STAGE-ID]"
```

---

## Critical Business Rules

### FirstMile Service Levels

FirstMile is a **carrier** (not 3PL) offering Xparcel ship methods:
- **Xparcel Ground**: 3-8 day economy (SLA: 8 business days)
- **Xparcel Expedited**: 2-5 day faster ground (SLA: 5 business days)
- **Xparcel Priority**: 1-3 day premium (SLA: 3 business days)

**Network Terminology**:
- "National Network": Nationwide coverage (100% U.S. ZIPs)
- "Select Network": High-density metro injection points
- **Never** name specific carriers (UPS, FedEx, USPS) in reports

### Performance Reporting Standards

**SLA Compliance** (see `~/.claude/FIRSTMILE.md`):
- Always lead with SLA compliance percentages (NOT daily delivery %)
- Calculate only on delivered shipments (exclude in-transit)
- Report three separate percentages (Priority, Expedited, Ground)

**Thresholds**:
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

**Excel Report Structure** (9 tabs):
1. Executive Summary
2. SLA Compliance (delivered-only with color scale)
3. Transit Performance (daily distribution)
4. Geographic Distribution (top 15 states)
5. Zone Analysis (1-8, Regional vs Cross-Country)
6. Operational Metrics
7. In-Transit Detail (undelivered with SLA window)
8. Notes & Assumptions
9. Brand Style Guide (#366092 FirstMile blue)

### Billable Weight Rules

ALL carriers follow these rules:
- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound

---

## File Structure

```
FirstMile_Deals/
├── unified_sync.py              # Main sync orchestrator
├── mcp_email_extractor.py       # Email subprocess (reads JSON cache)
├── hubspot_sync_core.py         # Centralized HubSpot API module
├── update_[deal]_meeting.py     # Deal-specific update scripts
├── _DAILY_LOG.md                # Continuity chain
├── FOLLOW_UP_REMINDERS.txt      # Action queue
├── superhuman_emails.json       # Email cache (Chrome MCP extracted)
├── sync_reports/                # Timestamped sync outputs
├── .claude/
│   ├── brand_scout/             # Lead generation system
│   │   ├── BRAND_SCOUT_TEMPLATE.md
│   │   ├── HUBSPOT_LEAD_CREATION_PROCESS.md
│   │   └── output/              # Generated reports
│   ├── agents/
│   │   ├── prioritization_agent.py
│   │   └── sales_execution_agent.py
│   └── docs/                    # System documentation
├── [##-STAGE]_Company_Name/     # Deal folders (trigger N8N on move)
└── _ARCHIVE/                    # Closed deals
```

---

## Known Issues & Solutions

### Sync Files Were in Downloads Folder

**FIXED (2025-11-14)**: All sync files now in project folder:
- `sync_reports/` instead of `Downloads/`
- `_DAILY_LOG.md` in project root
- `FOLLOW_UP_REMINDERS.txt` in project root

### Mock Email Data

**FIXED (2025-11-14)**: Removed all placeholder/mock email data
- System honestly reports when email integration unavailable
- Uses real Chrome MCP extraction → JSON cache → subprocess pattern
- Never returns `success: True` with fake data

### Windows Emoji Encoding

**FIXED (2025-11-14)**: UTF-8 wrapper added to all scripts
- `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`
- Subprocess calls use `encoding='utf-8'` parameter

### HubSpot API Timestamp Format

**FIXED (2025-11-14)**: Use Unix milliseconds (not ISO strings)
```python
timestamp_ms = int(datetime.now().timestamp() * 1000)
properties["hs_timestamp"] = str(timestamp_ms)
```

---

## Development Guidelines

### Script Standards

**All Python scripts must**:
1. Load credentials from `.env` file (never hardcode)
2. Use direct API calls when `hubspot_sync_core` unavailable
3. Include Windows UTF-8 encoding fix
4. Generate markdown output
5. Return honest status (no mock data)

**Standard Imports**:
```python
import os
import sys
import io
from dotenv import load_dotenv
import requests

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load credentials
load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')
```

### Never Commit

- `.env` files (use `.env.example` template)
- API keys or tokens in code
- `settings.local.json`
- Mock/placeholder data
- Files in `_ARCHIVE/` or old backup scripts

### Documentation

When modifying workflows, update:
1. This CLAUDE.md file
2. Relevant `.claude/docs/` files
3. `CHANGELOG.md` with changes
4. Commit with descriptive message

---

## MCP Integration

**Active Servers**:
- `github` - PR management, commit automation
- `brightdata` - Lead research, web scraping
- `chrome-mcp-server` - Browser automation for email extraction
- `Ref` - Documentation search

**Chrome MCP Usage** (in Claude Code conversation only):
```
mcp__chrome-mcp-server__chrome_navigate
mcp__chrome-mcp-server__chrome_get_web_content
mcp__chrome-mcp-server__chrome_screenshot
```

---

## Troubleshooting

### Email Integration Fails

**Symptoms**: Sync shows "⚠️ MANUAL MODE" instead of "✅ SUPERHUMAN SYNCED"

**Check**:
1. Is `superhuman_emails.json` present and recent (<2 hours)?
2. Run Chrome MCP extraction manually in Claude Code conversation
3. Verify UTF-8 encoding in both scripts

### HubSpot API Errors

**Rate Limiting**: Check burst (100/10s) and daily (150K/24h) limits
**Auth Errors**: Verify `.env` has current `HUBSPOT_API_KEY`
**Field Errors**: Check timestamp format (Unix ms), association type IDs

### Sync Reports in Wrong Location

**Check**: `unified_sync.py` should use `SYNC_REPORTS_DIR = PROJECT_ROOT / "sync_reports"`
**Not**: `DOWNLOADS = Path.home() / "Downloads"`

---

## See Also

**Complete Documentation**: `.claude/` folder
- [.claude/README.md](./.claude/README.md) - System overview
- [.claude/DOCUMENTATION_INDEX.md](./.claude/DOCUMENTATION_INDEX.md) - Navigation guide
- [.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md](./.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md) - Detailed sync workflow
- [.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md](./.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md) - All IDs and automation

**Global Framework**: `~/.claude/FIRSTMILE.md` - Brand standards and reporting framework

---

## Version

**System**: The Nebuchadnezzar v3.0
**Last Updated**: 2025-11-14
**Claude Code**: 2.0+
**Python**: 3.x
