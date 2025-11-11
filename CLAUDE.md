# FirstMile Deals Management System

Multi-stage sales pipeline management for FirstMile shipping deals with HubSpot CRM integration and automated workflow synchronization.

## 📚 Complete Documentation

**All system documentation is centralized in the `.claude` folder:**

- **[.claude/README.md](./.claude/README.md)** - Complete system overview & quick start
- **[.claude/DOCUMENTATION_INDEX.md](./.claude/DOCUMENTATION_INDEX.md)** - Master navigation guide
- **[.claude/STRUCTURE.md](./.claude/STRUCTURE.md)** - Directory organization guide
- **[.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md](./.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md)** - All IDs, commands, & reference
- **[.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md](./.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md)** - 9AM, NOON, EOD workflows
- **[.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](./.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot MCP integration
- **[.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md](./.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md)** - Standard deal structure

**START HERE**: [.claude/INDEX.md](./.claude/INDEX.md)

---

## Project Context

**The Nebuchadnezzar v3.0** - A fully automated 10-stage pipeline consciousness with N8N automation watching deal folder movements, zero manual data entry, and real-time tracking.

FirstMile is a **carrier** (not a platform/3PL) offering Xparcel ship methods:
- **Xparcel Ground**: 3-8 day economy ground service
- **Xparcel Expedited**: 2-5 day faster ground solution (1-20 lb)
- **Xparcel Priority**: 1-3 day premium option with money-back guarantee

---

## Core Workflows

### 1. Daily Sync Operations

**Unified Sync System v1.0** - Single script for all sync times:
```bash
# Morning priority report (9AM sync)
python unified_sync.py 9am

# Noon progress check
python unified_sync.py noon

# Afternoon update (3PM sync)
python unified_sync.py 3pm

# End of day summary
python unified_sync.py eod

# Weekly rollup (Sunday EOD)
python unified_sync.py weekly

# Monthly review (End of month)
python unified_sync.py monthly
```

**Important**:
- All syncs use comprehensive format with email integration, HubSpot live data, and execution plans
- Automatic continuity chain: Each sync writes to `_DAILY_LOG.md` for next sync's context
- See `UNIFIED_SYNC_GUIDE.md` for complete usage documentation

### 2. HubSpot Deal Management
```bash
# Search deals by stage
qm hubspot search-deals --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Create new lead
qm hubspot create-lead --first-name "John" --last-name "Smith" --email "john@company.com" --company "Acme Corp"

# Convert lead to deal
qm hubspot convert-to-deal --contact-id [ID] --deal-name "Company - Xparcel Ground" --amount 150000

# Update deal stage (triggers automation)
qm hubspot update-deal --deal-id [ID] --stage "[NEW-STAGE]"
```

### 3. Brand Scout Lead Generation

**Location**: `.claude/brand_scout/` folder

Automated brand research runs overnight:
- Company info, contacts, shipping data extraction
- Auto-creates HubSpot leads with contacts and companies
- Generates `[00-LEAD]_BrandName` folders with relationship docs
- Review new leads during 9AM sync in `.claude/brand_scout/output/`

See [.claude/docs/systems/BRAND_SCOUT_SYSTEM.md](./.claude/docs/systems/BRAND_SCOUT_SYSTEM.md) for complete workflow.

### 4. Analysis & Reporting

**PLD (Parcel Level Detail) Analysis**:
```bash
# Run comprehensive shipping profile analysis
python [customer_folder]/pld_analysis.py

# Generate FirstMile performance report (9-tab Excel)
python [customer_folder]/firstmile_orchestrator.py

# Apply rates and calculate savings
python [customer_folder]/apply_firstmile_rates.py

# Create pricing matrix
python [customer_folder]/create_pricing_matrix.py

# Invoice audit analysis
python [customer_folder]/invoice_audit_builder_v31.py
```

---

## Key Commands

### Claude Code Integration

```bash
# Load deal context
/load @deal_folder

# Analyze shipping data
/analyze @pld_file

# Generate documentation
/document

# Commit sync reports
/git
```

### Slash Commands (Project-Specific)

Located in `.claude/commands/`:
- `/sync [time]` - Trigger sync workflows
- `/deal [action]` - Deal management operations
- `/report [type]` - Generate analysis reports
- `/scout [company]` - Run brand scout research

---

## Important Conventions

### Deal Folder Naming
```
Format: [##-STAGE]_Company_Name

Examples:
[01-DISCOVERY-SCHEDULED]_Acme_Corp
[04-PROPOSAL-SENT]_Boxiiship
[07-CLOSED-WON]_Easy_Group_LLC
```

Moving folders between stages triggers N8N automation workflows.

### Pipeline Stages
```
[00-LEAD] → [01-DISCOVERY-SCHEDULED] → [02-DISCOVERY-COMPLETE] →
[03-RATE-CREATION] → [04-PROPOSAL-SENT] → [05-SETUP-DOCS-SENT] →
[06-IMPLEMENTATION] → [07-CLOSED-WON] → [08-CLOSED-LOST] → [09-WIN-BACK]
```

See [.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md](./.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md) for stage IDs and automation rules.

### Script Standards

**All Python scripts must**:
1. Use `CredentialManager` for API keys (never hardcode)
2. Import shared functions from `hubspot_sync_core.py`
3. Generate output in markdown format
4. Update deal memory database (`DEAL_MEMORY_DATABASE.json`)
5. Log to standard locations

**Standard Pattern**:
```python
from utils.credential_manager import CredentialManager
from hubspot_sync_core import HubSpotSyncManager

# Load and validate credentials
CredentialManager.load_and_validate()
config = CredentialManager.get_hubspot_config()

# Use shared sync manager
sync_manager = HubSpotSyncManager(**config)
deals = sync_manager.fetch_active_deals()
```

### Credential Management

**Never commit**:
- `.env` files (use `.env.example` as template)
- API keys or tokens in code
- `settings.local.json` files

**Always**:
- Use `python-dotenv` to load environment variables
- Validate required vars before execution
- Reference tokens via `${VAR_NAME}` in configs

### Documentation Updates

When adding/modifying workflows:
1. Update relevant `.claude/` documentation
2. Add entry to `DOCUMENTATION_INDEX.md`
3. Update `CHANGELOG.md` with changes
4. Commit docs with descriptive messages

---

## MCP Integration

### Configured Servers

**Active**:
- `github` - PR management, commit automation, issue tracking
- `brightdata` - Lead research, competitive intelligence, web scraping
- `Ref` - Documentation search and reference

**Available** (add to `.mcp.json` if needed):
- `notion` - Knowledge management (currently configured)
- Custom HubSpot MCP (evaluation in progress)

### Usage Examples

```bash
# GitHub operations
mcp__github__list_pull_requests
mcp__github__create_issue
mcp__github__search_code

# BrightData research
mcp__brightdata__search_engine
mcp__brightdata__scrape_as_markdown

# Documentation search
mcp__Ref__ref_search_documentation
mcp__Ref__ref_read_url
```

---

## Quality Standards

### Code Quality

- **DRY Principle**: Use shared modules, no duplicate code
- **Error Handling**: Try/except with meaningful messages
- **Rate Limiting**: All HubSpot calls through rate-limited manager
- **Testing**: Validate credentials before API calls
- **Logging**: Consistent logging format with timestamps

### Reporting Standards

**Follow global FirstMile framework** (see `~/.claude/FIRSTMILE.md`):
- Always lead with SLA compliance metrics (not daily delivery %)
- Use "National" or "Select" network (never name UPS, FedEx, USPS)
- Spell "eCommerce" with camel-case 'C'
- Apply FirstMile blue (#366092) to Excel headers
- Generate 9-tab structure for performance reports

### Sync Report Format

All daily sync reports must include:
1. **Yesterday's Context**: Activities and learnings from previous day
2. **Active Deals**: Current pipeline status by stage
3. **Priority Actions**: Top 3-5 actions for today
4. **Follow-Up Queue**: Upcoming tasks with due dates
5. **Brand Scout Results**: New leads from overnight research

---

## System File Locations

### Configuration
- **Project Root**: `/c/Users/BrettWalker/firstmile_deals/`
- **Python Config**: `config.py`, `hubspot_config.py`, `hubspot_utils.py`
- **Environment**: `.env` (never commit), `.env.example` (template)
- **Dependencies**: `requirements.txt`, `requirements-dev.txt`

### Automation & Tracking
- **Pipeline DB**: `C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv`
- **Activity Log**: `C:\Users\BrettWalker\Downloads\_DAILY_LOG.md`
- **Action Queue**: `C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt`
- **Dashboard**: `C:\Users\BrettWalker\Desktop\AUTOMATION_MONITOR_LOCAL.html`

### Deal Folders
- **Active Deals**: `[##-STAGE]_Company_Name/` directories
- **Archive**: `_ARCHIVE/` folder
- **Leads**: `_LEADS/` folder
- **Templates**: `[##-STAGE]_Template/` folders

---

## Critical Business Rules

### Billable Weight Calculation
ALL carriers follow these rules:
- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound (32, 48, 64 oz, etc.)

### SLA Windows
- Xparcel Priority: 3 days
- Xparcel Expedited: 5 days
- Xparcel Ground: 8 days

### Performance Thresholds
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

---

## Common Operations

### Create New Deal Folder
```bash
# Use template based on stage
cp -r "[01-DISCOVERY-SCHEDULED]_TEMPLATE" "[01-DISCOVERY-SCHEDULED]_NewCompany"

# Customize files
cd "[01-DISCOVERY-SCHEDULED]_NewCompany"
# Edit DISCOVERY_NOTES.md, COMPANY_PROFILE.md, etc.
```

### Run Daily Sync Cycle
```bash
# Morning (9 AM CT)
python unified_sync.py 9am
# Review output, update priorities

# Noon (12 PM CT)
python unified_sync.py noon
# Check progress, adjust actions

# Afternoon (3 PM CT)
python unified_sync.py 3pm
# Final priorities, prepare EOD

# End of Day (before 6 PM CT)
python unified_sync.py eod
# Capture learnings, plan tomorrow
```

### Move Deal Through Pipeline
```bash
# Move folder to trigger automation
mv "[03-RATE-CREATION]_Company" "[04-PROPOSAL-SENT]_Company"

# Update HubSpot (if not auto-synced)
python pipeline_sync_verification.py
```

---

## Troubleshooting

### Sync Script Fails
1. Check `.env` file has all required variables
2. Validate HubSpot API key is current
3. Review `logs/` directory for error messages
4. Run with `--debug` flag for verbose output

### HubSpot API Errors
1. Check rate limiting (100 calls per 10 seconds)
2. Verify API key permissions (Private App)
3. Confirm stage IDs match pipeline
4. Review `hubspot_sync_core.py` error logs

### Missing Deal Data
1. Check folder naming matches convention
2. Verify `DEAL_MEMORY_DATABASE.json` is updated
3. Run `pipeline_sync_verification.py`
4. Review N8N automation logs

### Git Issues
1. Ensure `.gitignore` excludes `.env` and `settings.local.json`
2. Commit `.claude/` documentation files
3. Use descriptive commit messages
4. Push after major sync completions

---

## See Also

### Essential Documentation
- [.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md](./.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md) - Complete sync workflow
- [.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](./.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md) - HubSpot integration
- [.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md](./.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md) - Deal folder structure
- [.claude/docs/systems/BRAND_SCOUT_SYSTEM.md](./.claude/docs/systems/BRAND_SCOUT_SYSTEM.md) - Automated lead generation

### Reference Materials
- [.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md](./.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md) - IDs and automation
- [.claude/docs/reference/VERIFIED_STAGE_IDS.md](./.claude/docs/reference/VERIFIED_STAGE_IDS.md) - Stage mapping
- [.claude/docs/templates/EXCEL_PROCESS_TEMPLATES.md](./.claude/docs/templates/EXCEL_PROCESS_TEMPLATES.md) - Analysis templates

### Global Framework
- `~/.claude/FIRSTMILE.md` - FirstMile brand standards and analysis framework
- `~/.claude/PRINCIPLES.md` - Development principles and standards
- `~/.claude/ORCHESTRATOR.md` - SuperClaude framework orchestration

---

## Version

**System**: The Nebuchadnezzar v3.0
**Last Updated**: 2025-11-06
**Claude Code**: 2.0.34
**Python**: 3.x
**Node**: For MCP servers
