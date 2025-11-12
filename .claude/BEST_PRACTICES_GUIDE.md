# FirstMile Deals - Best Practices Guide

**Complete navigation and usage guide for the FirstMile Deals system with SuperClaude framework**

**Last Updated**: November 6, 2025
**System Version**: Nebuchadnezzar v3.0
**Audience**: All users (new and experienced)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Daily Navigation Patterns](#daily-navigation-patterns)
3. [Documentation Discovery](#documentation-discovery)
4. [Working with Claude Code](#working-with-claude-code)
5. [HubSpot Integration](#hubspot-integration)
6. [Deal Management](#deal-management)
7. [Analysis & Reporting](#analysis--reporting)
8. [Troubleshooting](#troubleshooting)
9. [System Maintenance](#system-maintenance)
10. [Common Pitfalls](#common-pitfalls)

---

## Getting Started

### First Time Setup (30 minutes)

**Step 1: Understand the Structure**
```bash
# Navigate to project
cd ~/firstmile_deals

# Review these files IN ORDER:
1. README.md                              # System overview
2. .claude/STRUCTURE.md                   # Directory organization
3. .claude/DOCUMENTATION_INDEX.md         # Complete catalog
4. .claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md  # IDs and commands
```

**Step 2: Verify Configuration**
```bash
# Check settings exist
ls -la .claude/settings.local.json

# Verify .env file
cat .env | grep -E "HUBSPOT_API_KEY|BRIGHTDATA_API_TOKEN"

# Test HubSpot connection (if configured)
# qm hubspot get-deal --deal-id [ANY-DEAL-ID]
```

**Step 3: Understand Daily Workflow**
- Read: `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md`
- Bookmark: `EOD_SYNC_MASTER_PROMPT.md` (for end-of-day automation)
- Review: Pipeline stages in `APPROVED_PIPELINE_STRUCTURE.md`

**Step 4: Run First Sync (Test)**
```bash
# Morning sync (generates priority report)
python daily_9am_sync.py

# Review output in Downloads/_PIPELINE_TRACKER.csv
```

### Navigation Philosophy

**🎯 Golden Rule**: Start broad, drill down as needed

1. **Lost?** → `.claude/DOCUMENTATION_INDEX.md` (comprehensive catalog)
2. **File moved?** → `.claude/QUICK_NAV.md` (path changes)
3. **How is this organized?** → `.claude/STRUCTURE.md`
4. **Quick command?** → `.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md`
5. **Daily task?** → `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md`

---

## Daily Navigation Patterns

### Morning Routine (9:00 AM CT) - 15 minutes

```bash
# 1. Navigate to project
cd ~/firstmile_deals

# 2. Run morning sync
python daily_9am_sync.py

# 3. Review priorities (opens automatically or check Downloads/)
# - _PIPELINE_TRACKER.csv (all deals)
# - Console output (P1 actions)

# 4. Optional: Check for stale proposals
python .claude/agents/sales_execution_agent.py

# 5. Optional: Get top 3 priorities
python .claude/agents/prioritization_agent.py --daily-reminder
```

**What to Focus On**:
- **P1 Actions**: Time-sensitive follow-ups (proposals >3 days, discovery calls today)
- **Stage Transitions**: Deals ready to move forward
- **New Leads**: Web form submissions or inbound leads

### Midday Check (12:00 PM CT) - 5 minutes

```bash
# Run quick sync
python noon_sync.py

# Or verify pipeline manually
python pipeline_sync_verification.py
```

**What to Check**:
- New web form submissions (Brand Scout opportunity)
- Stage changes from morning activities
- Task completion status

### Afternoon Checkpoint (3:00 PM CT) - 5 minutes

```bash
# Run afternoon sync
python 3pm_sync.py
```

**What to Review**:
- Progress on P1 actions from morning
- Any new urgencies or blockers
- Prep for EOD sync

### End of Day (5:30 PM CT) - 20 minutes

**Option A: Automated (Recommended)**
```bash
# Use Claude Code with EOD_SYNC_MASTER_PROMPT.md
# Opens in Claude Code automatically or paste content
```

**Option B: Manual**
```bash
# Run EOD script
python eod_sync.py

# Update learning log
# Edit Downloads/_DAILY_LOG_FEEDBACK.md
```

**What to Capture**:
1. **What Worked**: Successful patterns, good outcomes
2. **What Failed**: Issues, blockers, errors
3. **What's Unclear**: Questions, ambiguities
4. **What's Missing**: Gaps in process, tools, or documentation

### Weekly Review (Friday 5:00 PM CT) - 30 minutes

```bash
# Track weekly metrics
python .claude/agents/weekly_metrics_tracker.py

# Review against 5/2/3/1 goals:
# - 5 discovery calls completed
# - 2 proposals sent
# - 3 follow-ups executed
# - 1 deal closed (won or lost)
```

---

## Documentation Discovery

### The Three-Tier System

**Tier 1: Quick Reference (< 5 minutes)**
- `.claude/QUICK_NAV.md` - File paths after reorganization
- `.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md` - All IDs, commands, quick reference
- `.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#quick-reference-card` - Common commands

**Tier 2: How-To Guides (5-15 minutes)**
- `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md` - Daily routines
- `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md` - Deal folder standards
- `.claude/docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md` - Analysis process

**Tier 3: Deep Dives (15-60 minutes)**
- `.claude/DOCUMENTATION_INDEX.md` - Complete catalog (395 lines)
- `.claude/STRUCTURE.md` - System architecture
- `FIRSTMILE_PIPELINE_BLUEPRINT.md` - HubSpot & N8N integration
- `Brett_Walker_Instructions_v4.3.md` - Morpheus Method philosophy

### Finding Information Fast

**Scenario: "How do I create a new lead?"**
```
1. Go to: .claude/DOCUMENTATION_INDEX.md
2. Search: Ctrl+F "Create Lead"
3. Click link: docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-1-single-lead-creation
4. Follow steps in guide
```

**Scenario: "What's the stage ID for Discovery Scheduled?"**
```
1. Go to: .claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md
2. Search: Ctrl+F "Discovery Scheduled" or "stage IDs"
3. Find: 1090865183
```

**Scenario: "How do I run a Full Xparcel Analysis?"**
```
1. Go to: .claude/DOCUMENTATION_INDEX.md
2. Search: Ctrl+F "Full Xparcel"
3. Click: docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md
4. Copy prompt template, replace [Customer] and [PLD_DATA]
5. Run in Claude Code
```

### Search Strategies

**Use Ctrl+F (Find) effectively**:
- **Broad terms first**: "analysis", "sync", "deal", "rate"
- **Then narrow**: "PLD analysis", "9am sync", "deal progression"
- **Use fragments**: "NEBUCH" finds NEBUCHADNEZZAR_REFERENCE.md

**Use Grep for multi-file search**:
```bash
# Find all mentions of "rate limiting"
grep -r "rate limiting" .claude/

# Find all Python scripts with "hubspot" in name
find . -name "*hubspot*.py"

# Find all markdown files with "discovery"
grep -r "discovery" --include="*.md" .claude/
```

---

## Working with Claude Code

### SuperClaude Framework Integration

**What is SuperClaude?**
- Enhanced Claude Code with custom commands, personas, and MCP servers
- Global configuration in `~/.claude/` (CLAUDE.md, COMMANDS.md, etc.)
- Project configuration in `~/firstmile_deals/.claude/`

**Key Files**:
- `~/.claude/CLAUDE.md` - Global SuperClaude instructions
- `~/firstmile_deals/CLAUDE.md` - Project-specific context (400 lines)
- `~/firstmile_deals/.claude/settings.local.json` - Permissions & MCP servers

### Using Slash Commands

**Available Commands** (see `~/.claude/COMMANDS.md`):
```bash
# Analysis
/sc:analyze [target]              # Multi-dimensional analysis
/sc:troubleshoot [symptoms]       # Problem investigation

# Development
/sc:build [target]                # Project builder
/sc:implement [feature]           # Feature implementation

# Quality
/sc:improve [target]              # Code enhancement
/sc:cleanup [target]              # Technical debt reduction

# Documentation
/sc:document [target]             # Generate documentation

# Planning
/sc:task [operation]              # Long-term project management
/sc:estimate [target]             # Evidence-based estimation

# Meta
/sc:load [path]                   # Load project context
/sc:spawn [mode]                  # Task orchestration
```

**Example Usage**:
```
User: "/sc:analyze hubspot_sync_core.py --focus performance"
Claude: [Analyzes file for performance bottlenecks with recommendations]

User: "/sc:document daily_9am_sync.py"
Claude: [Generates comprehensive documentation]
```

### Working with MCP Servers

**Available Servers**:
1. **github** - Repository operations, PR management
2. **brightdata** - Web scraping, SERP data
3. **Ref** - Documentation lookup (official library docs)
4. **episodic-memory** - Cross-session conversation memory
5. **domain-memory-agent** - Project knowledge base

**When to Use Each**:
- **github**: Creating issues, PRs, reviewing code
- **brightdata**: Brand Scout research, competitor analysis
- **Ref**: Looking up HubSpot API docs, Python library references
- **episodic-memory**: "What did we work on last week?"
- **domain-memory-agent**: Storing deal notes, customer insights

**Example**:
```
User: "Use Ref to look up HubSpot deal properties API"
Claude: [Uses Ref MCP to fetch official HubSpot API documentation]

User: "Search memory for when we discussed rate limiting"
Claude: [Uses episodic-memory to find previous conversations]
```

### Personas (Auto-Activated)

SuperClaude automatically activates specialized personas based on context:

- **Frontend Persona**: UI work, components, accessibility
- **Backend Persona**: APIs, databases, server-side logic
- **Security Persona**: Vulnerabilities, compliance, threat modeling
- **Analyzer Persona**: Root cause analysis, debugging
- **Scribe Persona**: Documentation, professional writing

**You don't need to request these** - they activate automatically based on keywords and context.

---

## HubSpot Integration

### Configuration

**Required Environment Variables** (`.env`):
```bash
HUBSPOT_API_KEY=pat-na1-your-token-here
HUBSPOT_OWNER_ID=699257003
HUBSPOT_PIPELINE_ID=8bd9336b-4767-4e67-9fe2-35dfcad7c8be
HUBSPOT_PORTAL_ID=46526832
```

**Test Connection**:
```bash
# Verify credentials loaded
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('HUBSPOT_API_KEY'))"

# Test API call (requires qm CLI or custom script)
# qm hubspot get-deal --deal-id [ANY-ID]
```

### Using HubSpot Sync Manager (NEW)

**Rate-Limited API Calls** (recommended):
```python
from hubspot_sync_core import HubSpotSyncManager

# Context manager (auto-cleanup)
with HubSpotSyncManager() as sync:
    # Fetch deals
    deals = sync.fetch_deals(stage_id="1090865183", limit=100)

    # Update deal
    sync.update_deal(deal_id="12345", properties={
        'dealstage': 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a'
    })

    # Create contact
    contact = sync.create_contact({
        'email': 'john@company.com',
        'firstname': 'John',
        'lastname': 'Smith'
    })

# Rate limit stats logged automatically
```

**Benefits**:
- Automatic rate limiting (100 req/10s, 150K req/day)
- Exponential backoff retry
- Thread-safe
- Request logging

### Common Operations

**Create Lead**:
```python
# See: .claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-1
# qm hubspot create-lead --email "john@company.com" --company "Acme Corp"
```

**Convert Lead to Deal**:
```python
# See: .claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-3
# qm hubspot convert-to-deal --contact-id [ID] --pipeline-id [PIPELINE]
```

**Move Deal Stage**:
```python
# Update deal stage
sync.update_deal(deal_id="12345", properties={
    'dealstage': 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a'  # Stage ID
})

# Then rename folder
# mv "[01-DISCOVERY-SCHEDULED]_Company" "[02-DISCOVERY-COMPLETE]_Company"
```

**Create HubSpot Note**:
```python
sync.create_note(
    deal_id="12345",
    note="Discovery call completed. Moving to rate creation."
)
```

---

## Deal Management

### Deal Folder Naming Convention

**Format**: `[##-STAGE]_Company_Name`

**Examples**:
- `[00-LEAD]_Acme_Corporation`
- `[01-DISCOVERY-SCHEDULED]_Acme_Corporation`
- `[03-RATE-CREATION]_Acme_Corporation`
- `[07-CLOSED-WON]_Acme_Corporation`

**Stage Codes** (see `APPROVED_PIPELINE_STRUCTURE.md`):
```
00 - LEAD
01 - DISCOVERY-SCHEDULED
02 - DISCOVERY-COMPLETE
03 - RATE-CREATION
04 - PROPOSAL-SENT
05 - SETUP-DOCS-SENT
06 - IMPLEMENTATION
07 - CLOSED-WON
08 - CLOSED-LOST
09 - WIN-BACK
```

### Creating New Deal

**Step 1: Research (Brand Scout)**
```bash
# In Claude Code
"Scout brand: https://www.acmecorp.com"

# Output saved to: .claude/brand_scout/output/[BRAND]_brand_scout_[DATE].md
```

**Step 2: Create Folder**
```bash
# Copy template
cp -r .claude/docs/templates/DEAL_FOLDER_TEMPLATE "[00-LEAD]_Acme_Corporation"

# Add Brand Scout report
mv .claude/brand_scout/output/Acme*.md "[00-LEAD]_Acme_Corporation/Reference/"
```

**Step 3: Create in HubSpot**
```bash
# Create contact first, then convert to deal
# See: .claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md
```

### Moving Deal Through Pipeline

**Best Practice Workflow**:
1. **Complete stage requirements** (see `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md`)
2. **Update HubSpot first** (via sync script or manual)
3. **Rename folder** to match new stage
4. **Add HubSpot note** documenting reason for stage change
5. **Update local tracker** (Downloads/_PIPELINE_TRACKER.csv)

**Example**:
```bash
# 1. Complete discovery call, have notes

# 2. Update in HubSpot (via script or API)
python -c "
from hubspot_sync_core import HubSpotSyncManager
with HubSpotSyncManager() as sync:
    sync.update_deal('12345', {'dealstage': '1090865183'})  # Discovery Complete
"

# 3. Rename folder
mv "[01-DISCOVERY-SCHEDULED]_Acme" "[02-DISCOVERY-COMPLETE]_Acme"

# 4. Add note in HubSpot
# (via UI or API)

# 5. Next sync will update tracker automatically
python noon_sync.py
```

### Required Files by Stage

See `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md` for complete breakdown.

**Key Requirements**:
- **01-DISCOVERY**: Discovery notes, call recording
- **03-RATE-CREATION**: PLD data, analysis results, JIRA ticket
- **04-PROPOSAL-SENT**: Proposal PDF, pricing matrix, rate card
- **06-IMPLEMENTATION**: Integration docs, testing results
- **07-CLOSED-WON**: Contract, setup confirmation, performance baseline

---

## Analysis & Reporting

### PLD (Parcel Level Detail) Analysis

**Purpose**: Understand customer shipping profile for rate optimization

**Input**: Excel/CSV with columns:
- Carrier, Service, Weight, Dimensions, Zone, Destination State, Cost

**Process** (see `PLD_DISCOVERY_ANALYSIS_PROMPT.md`):
```bash
# 1. Place data in deal folder
cp customer_data.xlsx "[03-RATE-CREATION]_Acme/PLD_Analysis/raw_data/"

# 2. Run analysis scripts
cd "[03-RATE-CREATION]_Acme/PLD_Analysis"
python ../../pld_analysis.py
python ../../apply_firstmile_rates.py
python ../../create_pricing_matrix.py

# 3. Review outputs in analysis_results/
```

**Key Metrics to Extract**:
- Annual volume (total parcels)
- Service mix (% Ground vs Expedited vs Priority)
- Weight profile (< 1 lb, 1-5 lb, 5+ lb)
- Zone distribution (Regional 1-4 vs Cross-Country 5-8)
- Top 10 destination states
- Average cost per parcel

### Full Xparcel Analysis

**Purpose**: Professional prospect deliverable showing savings opportunity

**Template**: `.claude/docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md`

**Process**:
```
1. Open template in Claude Code
2. Replace [Customer] with company name
3. Replace [PLD_DATA] with actual data
4. Run prompt
5. Output: 6-tab Excel workbook
```

**Output Tabs**:
1. **Executive Summary** - High-level KPIs
2. **Current State Analysis** - Volume, weight, service mix
3. **FirstMile Solution** - Xparcel service mapping
4. **Cost Comparison** - Current vs FirstMile rates
5. **Savings Summary** - Annual savings projection
6. **Implementation Plan** - Next steps

**Deliverable Naming**: `[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx`

### Performance Reporting (Post-Win)

**Purpose**: Monthly performance reports for active customers

**Tool**: `firstmile_orchestrator.py` script

**Process**:
```bash
# Run orchestrator
python firstmile_orchestrator.py \
  --customer "Acme Corporation" \
  --data-file "[07-CLOSED-WON]_Acme/Performance_Reports/raw_data/acme_shipments.xlsx" \
  --report-period "November 1-30, 2025" \
  --service-level "Xparcel Priority"

# Output: 9-tab Excel report
```

**Report Tabs**:
1. **Executive Summary**
2. **SLA Compliance** (primary metric - delivered only)
3. **Transit Performance**
4. **Geographic Distribution**
5. **Zone Analysis**
6. **Operational Metrics**
7. **In-Transit Detail**
8. **Notes & Assumptions**
9. **Brand Style Guide**

**Key Rule**: **SLA compliance always comes first** (not daily delivery %)

---

## Troubleshooting

### Common Issues

#### Issue: MCP Servers Not Working
**Symptoms**: "mcp__github__* not found", plugins not loading

**Solution**:
```bash
# Check project settings
cat .claude/settings.local.json

# Should have permissions for MCP servers
# If missing, merge from global:
# See: .claude/settings.local.json (should have 73 permissions)

# Restart Claude Code
```

#### Issue: HubSpot API 401 Unauthorized
**Symptoms**: "Authentication failed", 401 errors

**Solution**:
```bash
# Check .env file
cat .env | grep HUBSPOT_API_KEY

# Verify token is valid (not expired)
# Generate new token: HubSpot → Settings → Integrations → Private Apps

# Update .env
echo "HUBSPOT_API_KEY=pat-na1-NEW-TOKEN" >> .env

# Restart scripts
```

#### Issue: Rate Limit Errors (429)
**Symptoms**: "Rate limit exceeded", 429 errors

**Solution**:
```bash
# Use new HubSpotSyncManager (auto rate limiting)
# See: hubspot_sync_core.py

# Check current rate limit stats
python -c "
from hubspot_sync_core import HubSpotSyncManager
with HubSpotSyncManager() as sync:
    stats = sync.get_rate_limit_stats()
    print(stats)
"

# Wait if daily limit exhausted (resets at midnight UTC)
```

#### Issue: Sync Script Fails
**Symptoms**: Script errors, incomplete sync

**Solution**:
```bash
# Check logs
python daily_9am_sync.py 2>&1 | tee sync_debug.log

# Common fixes:
# 1. Missing dependencies
pip install -r requirements.txt

# 2. Wrong directory
cd ~/firstmile_deals

# 3. Missing .env
cp .env.example .env
# Then edit .env with actual values

# 4. Python version
python --version  # Should be 3.11+
```

#### Issue: Can't Find Documentation
**Symptoms**: "Where is [file]?", "Link broken"

**Solution**:
```bash
# Files were reorganized on 2025-11-06
# Check: .claude/QUICK_NAV.md for old → new paths

# Or search:
find .claude -name "*[KEYWORD]*"

# Or check comprehensive index:
# .claude/DOCUMENTATION_INDEX.md
```

### Getting Help

**Tier 1: Self-Service** (< 5 min)
1. Check `.claude/DOCUMENTATION_INDEX.md` → Search for topic
2. Check `.claude/QUICK_NAV.md` → Find file paths
3. Check troubleshooting section in relevant guide

**Tier 2: Claude Code** (5-15 min)
1. Ask Claude Code: "How do I [task]?"
2. Reference documentation: "See DAILY_SYNC_OPERATIONS.md"
3. Use slash commands: "/sc:troubleshoot [issue]"

**Tier 3: System Review** (15-30 min)
1. Review `.claude/STRUCTURE.md` → Understand organization
2. Review `README.md` → System overview
3. Review relevant workflow guides

---

## System Maintenance

### Daily Maintenance (5 minutes)

**What to Do**:
1. Run scheduled syncs (9AM, Noon, 3PM, EOD)
2. Update `_DAILY_LOG_FEEDBACK.md` with learnings
3. Archive completed deals to `_ARCHIVE/`

**Automated (GitHub Actions)**:
- Syncs run automatically on weekdays (if configured)
- Check: `.github/workflows/scheduled-syncs.yml`
- View logs: GitHub → Actions tab

### Weekly Maintenance (30 minutes)

**Friday EOD Checklist**:
1. Run weekly metrics tracker
2. Review and update FAQ sections in docs
3. Archive daily logs to Saner.ai
4. Clean up Downloads folder (old CSVs, logs)
5. Review pipeline health (stage distribution, velocity)

### Monthly Maintenance (2 hours)

**First Friday of Month**:
1. Audit documentation for outdated information
2. Update version numbers and dates
3. Review and update requirements.txt
4. Clean up old sync script backups
5. Performance review: sync times, error rates

### Quarterly Maintenance (4 hours)

**Major Reviews**:
1. System architecture review
2. Major documentation updates
3. Workflow optimization review
4. Tool and dependency upgrades
5. Training materials update

---

## Common Pitfalls

### Pitfall 1: Ignoring Daily Syncs
**Problem**: Manual HubSpot updates, outdated local state

**Solution**:
- Set up automated syncs (GitHub Actions)
- Run at least 9AM and EOD syncs daily
- Use `_PIPELINE_TRACKER.csv` as single source of truth

### Pitfall 2: Inconsistent Deal Naming
**Problem**: Folders don't match HubSpot, hard to find deals

**Solution**:
- Always use format: `[##-STAGE]_Company_Name`
- Rename folder when moving stages
- Use exact company name from HubSpot

### Pitfall 3: Skipping Documentation
**Problem**: Lost context, repeated mistakes, unclear processes

**Solution**:
- Update `_DAILY_LOG_FEEDBACK.md` at EOD
- Capture learnings in 4 categories (worked, failed, unclear, missing)
- Archive weekly to Saner.ai

### Pitfall 4: Direct HubSpot API Calls Without Rate Limiting
**Problem**: 429 errors, API timeouts, account suspension risk

**Solution**:
- Use `hubspot_sync_core.py` for all API calls
- Implements automatic rate limiting
- See: `HUBSPOT_SYNC_CORE_USAGE.md`

### Pitfall 5: Not Using Templates
**Problem**: Inconsistent deliverables, missing information

**Solution**:
- Use `.claude/docs/templates/` for all standard outputs
- Full Xparcel Analysis Template
- Deal Folder Template
- Excel Process Templates

### Pitfall 6: Hardcoding Credentials
**Problem**: Security risks, tokens in version control

**Solution**:
- Always use `.env` for credentials
- Never commit `.env` to git
- Use `CredentialManager` in scripts (if available)

### Pitfall 7: Bypassing Stage Requirements
**Problem**: Incomplete deals, missing data, blocked transitions

**Solution**:
- Review stage requirements: `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md`
- Complete checklist before moving stages
- Add HubSpot note documenting completion

### Pitfall 8: Not Backing Up Work
**Problem**: Lost data, can't recover from mistakes

**Solution**:
- Git commit regularly
- Archive completed deals
- Backup Downloads folder weekly
- Use version control for all scripts

---

## Quick Reference Cards

### File Navigation Cheat Sheet

```
LOST? START HERE:
.claude/DOCUMENTATION_INDEX.md     → Complete catalog
.claude/QUICK_NAV.md               → File path changes
.claude/STRUCTURE.md               → Directory organization

DAILY TASKS:
.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md  → Morning/noon/EOD
EOD_SYNC_MASTER_PROMPT.md                        → Automated EOD

DEAL MANAGEMENT:
.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md   → Folder structure
.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md → HubSpot operations

ANALYSIS:
.claude/docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md  → Prospect deliverable
PLD_DISCOVERY_ANALYSIS_PROMPT.md                          → PLD analysis

REFERENCE:
.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md  → All IDs, commands
APPROVED_PIPELINE_STRUCTURE.md                      → Stage definitions
```

### Command Cheat Sheet

```bash
# DAILY OPERATIONS
python daily_9am_sync.py          # Morning priority report
python noon_sync.py               # Midday progress check
python 3pm_sync.py                # Afternoon checkpoint
python eod_sync.py                # End of day summary

# AGENTS
python .claude/agents/sales_execution_agent.py     # Stale proposals
python .claude/agents/prioritization_agent.py      # Top 3 priorities
python .claude/agents/brand_scout_agent.py         # Lead research
python .claude/agents/weekly_metrics_tracker.py    # 5/2/3/1 goals

# HUBSPOT (via Python)
from hubspot_sync_core import HubSpotSyncManager
with HubSpotSyncManager() as sync:
    sync.fetch_deals(stage_id="1090865183")
    sync.update_deal(deal_id="123", properties={...})
    sync.create_contact({...})

# ANALYSIS
python pld_analysis.py                    # PLD analysis
python apply_firstmile_rates.py           # Rate application
python create_pricing_matrix.py           # Pricing matrix
python firstmile_orchestrator.py          # Performance reports

# SYSTEM
git status                                # Check git state
git add . && git commit -m "msg"          # Commit changes
pip install -r requirements.txt           # Install dependencies
python -m pytest tests/                   # Run tests
```

### Stage ID Quick Reference

```
PIPELINE: FirstMile Sales Pipeline
ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

STAGES:
00 LEAD                    → 1090865169
01 DISCOVERY-SCHEDULED     → 1090865183
02 DISCOVERY-COMPLETE      → 1090865197
03 RATE-CREATION          → d607df25-2c6d-4a5d-9835-6ed1e4f4020a
04 PROPOSAL-SENT          → 1090865211
05 SETUP-DOCS-SENT        → 1090865225
06 IMPLEMENTATION         → 1090865239
07 CLOSED-WON             → closedwon
08 CLOSED-LOST            → closedlost
09 WIN-BACK               → 1090865253

See: .claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md
```

---

## Summary: The First Mile Deals Navigation Pattern

1. **Start Your Day**: Run `daily_9am_sync.py` → Review priorities
2. **Need Info?**: Check `.claude/DOCUMENTATION_INDEX.md` → Find guide
3. **Working Deal?**: Follow `.claude/docs/templates/DEAL_FOLDER_TEMPLATE.md` → Complete stage requirements
4. **Need Analysis?**: Use templates in `.claude/docs/templates/` → Generate deliverable
5. **End Your Day**: Run EOD sync → Update `_DAILY_LOG_FEEDBACK.md`
6. **Lost?**: Check `.claude/QUICK_NAV.md` or `.claude/STRUCTURE.md`

**Remember**:
- Documentation is organized (not scattered)
- Templates exist for common tasks
- Syncs keep everything aligned
- Learning logs prevent repeated mistakes

---

**Last Updated**: November 6, 2025
**Maintained By**: Brett Walker
**System Version**: Nebuchadnezzar v3.0
