# FirstMile Deals - Documentation Index
**Complete Guide to Nebuchadnezzar v3.0 System**

**Last Reorganization**: 2025-11-06 - Files moved to organized subdirectories
**See Also**: [STRUCTURE.md](STRUCTURE.md) for complete directory organization | [QUICK_NAV.md](QUICK_NAV.md) for file path changes

---

## 📚 Quick Navigation

### 🚀 Start Here
1. **[README.md](README.md)** - System overview and quick start guide
2. **[docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md)** - Complete system reference with all IDs and commands
3. **[FIRSTMILE_PIPELINE_BLUEPRINT.md](FIRSTMILE_PIPELINE_BLUEPRINT.md)** - HubSpot & N8N integration architecture

### 📋 Daily Operations
4. **[docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md)** - 9AM, NOON, EOD, and weekly sync workflows
5. **agents/[README.md](agents/README.md)** - 🎯 Sales Discipline Agents (NEW: 5/2/3/1 accountability)
6. **[EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md)** - Comprehensive EOD sync automation prompt (mistake-proof)
7. **[S4_OPTIMIZATION_PATTERNS.md](S4_OPTIMIZATION_PATTERNS.md)** - Sonnet 4.5 specific optimization patterns
8. **[REPEATABLE_IMPROVEMENT_TEMPLATE.md](REPEATABLE_IMPROVEMENT_TEMPLATE.md)** - Template for capturing workflow improvements
9. **[docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot MCP integration and workflows
10. **[docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md)** - Standard deal folder structure by stage

### 🧠 Strategy & Methodology
11. **[Brett_Walker_Instructions_v4.3.md](Brett_Walker_Instructions_v4.3.md)** - Morpheus Method and positioning
12. **[APPROVED_PIPELINE_STRUCTURE.md](APPROVED_PIPELINE_STRUCTURE.md)** - Official 10-stage pipeline definition
13. **HubSpot/[HUBSPOT_MCP_CHEATSHEET.md](HubSpot/HUBSPOT_MCP_CHEATSHEET.md)** - Complete API reference
14. **[CLAUDE.md](CLAUDE.md)** - AI assistant project context

### 🔧 Specialized Guides
15. **[docs/templates/EXCEL_PROCESS_TEMPLATES.md](docs/templates/EXCEL_PROCESS_TEMPLATES.md)** - Quick reference for all Excel deliverables
16. **[docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md](docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md)** - Standard Full Xparcel Analysis process
17. **BULK_RATE_PROCESSING/[RATE_CREATION_BLITZ.md](BULK_RATE_PROCESSING/RATE_CREATION_BLITZ.md)** - Rapid rate creation workflow
18. **[PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md)** - Shipping analysis methodology
19. **brand_scout/[BRAND_SCOUT_SYSTEM.md](brand_scout/BRAND_SCOUT_SYSTEM.md)** - Autonomous lead research system
20. **_DAILY_LOG_FEEDBACK.md** (Downloads) - Continuous learning capture

### 🤖 Sales Automation Agents
21. **agents/sales_execution_agent.py** - Auto-generate urgency follow-ups for stale proposals
22. **agents/brand_scout_agent.py** - Automated brand research (on-demand + Monday 6AM)
23. **agents/weekly_metrics_tracker.py** - Track 5/2/3/1 weekly goals with coaching feedback
24. **agents/prioritization_agent.py** - Ensure enterprise deals get 10x attention

---

## 📖 Documentation by Use Case

### Setting Up the System

**First Time Setup**:
1. Read [README.md](README.md) - Understanding the system
2. Review [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md) - Get all configuration IDs
3. Verify HubSpot connection: `qm hubspot get-deal --deal-id [ANY-ID]`
4. Run pipeline sync: `python pipeline_sync_verification.py`

**Required Files**:
- Desktop: `AUTOMATION_MONITOR_LOCAL.html`, `NEBUCHADNEZZAR_CONTROL.bat`
- Downloads: `_PIPELINE_TRACKER.csv`, `_DAILY_LOG.md`, `FOLLOW_UP_REMINDERS.txt`

### Managing Daily Workflow

**Morning Routine (9AM)**:
1. Review [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#9am-sync---day-start)
2. Run: `python daily_9am_workflow.py`
3. **🎯 NEW**: `python .claude/agents/prioritization_agent.py --daily-reminder` (Top 3 priorities)
4. **🎯 NEW**: `python .claude/agents/sales_execution_agent.py` (Check stale proposals)
5. Execute P1 actions from output
6. **Optional**: Batch Brand Scout research on queued leads

**Midday Check (NOON)**:
1. Review [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#noon-sync---midday-progress-check)
2. Run: `python pipeline_sync_verification.py`
3. **Optional**: Process new web form submissions via Brand Scout

**End of Day (5PM)**:
1. Review [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture)
2. Use [EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md) for automated sync
3. Update: `_DAILY_LOG_FEEDBACK.md` in Downloads folder
4. Capture learnings in 4 categories (worked, failed, unclear, missing)
5. **Optional**: Quality check Brand Scout reports, sync to HubSpot

**Weekly Review (Friday EOD)**:
1. **🎯 NEW**: `python .claude/agents/weekly_metrics_tracker.py` (Track 5/2/3/1 goals)
2. Review weekly performance against targets
3. Identify gaps for next week

**Monday Morning (6AM - Scheduled)**:
1. **🎯 NEW**: `python .claude/agents/brand_scout_agent.py --batch 10` (Auto-generate 10 leads)

### Creating & Managing Deals

**New Lead → Deal (Manual)**:
1. Reference [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-1-single-lead-creation)
2. Create lead: `qm hubspot create-lead ...`
3. Convert to deal: `qm hubspot convert-to-deal ...`
4. Create folder using [docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md)

**New Lead → Deal (Brand Scout Automated)**:
1. Generate report: `"Scout brand: [URL]"` in Claude Code
2. Review output in `.claude/brand_scout/output/`
3. Copy Section 6 fields to HubSpot
4. Create `[00-LEAD]_[BRAND]` folder with report

**Moving Deal Through Pipeline**:
1. Reference [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows)
2. Move folder: `mv [OLD-STAGE]_Company [NEW-STAGE]_Company`
3. Verify sync or manual update: `qm hubspot update-deal ...`
4. Add HubSpot note documenting stage change

### Running Analysis

**Full Xparcel Analysis** (Professional Prospect Deliverable):
1. Follow [docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md](docs/templates/FULL_XPARCEL_ANALYSIS_TEMPLATE.md) - Complete process
2. Use standard prompt template with customer PLD data
3. Generate 6-tab professional Excel with FirstMile branding
4. Weight profile: 1-15oz, 15.99oz, 1-10lb (matches rate card structure)
5. Output: `[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx`

**PLD Analysis Workflow**:
1. Get methodology from [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md)
2. Place data in `[STAGE]_Company/PLD_Analysis/raw_data/`
3. Run scripts from [docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress):
   ```bash
   python pld_analysis.py
   python apply_firstmile_rates.py
   python create_pricing_matrix.py
   ```

**Performance Reporting** (Post-Win):
1. Use `firstmile_orchestrator.py` script
2. Follow FirstMile brand guidelines (see CLAUDE.md)
3. Output 9-tab Excel report with SLA compliance first

### Rate Creation Workflows

**Standard Rate Creation**:
1. Follow [docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress) structure
2. Reference JIRA ticket (RATE-####)
3. Run full analysis suite
4. Generate pricing matrix

**Bulk Rate Processing**:
1. Use [RATE_CREATION_BLITZ.md](BULK_RATE_PROCESSING/RATE_CREATION_BLITZ.md) template
2. Process multiple deals in parallel
3. Track in spreadsheet

### Continuous Improvement

**Capturing Learnings**:
1. Daily: Update `_DAILY_LOG_FEEDBACK.md` at EOD
2. Weekly: Review and archive to Saner.ai (Friday EOD)
3. Follow [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#phase-2-learnings--insights) templates

**SOP Evolution**:
1. Propose change with v# in `_DAILY_LOG_FEEDBACK.md`
2. Test for 1-2 weeks (🟡 TESTING status)
3. Validate results and mark ✅ PERMANENT or 🔴 ABANDON

---

## 🗂 File Organization

### .claude/ Directory (Organized Structure)
```
.claude/
├── README.md                       # System overview
├── INDEX.md                        # Main navigation
├── DOCUMENTATION_INDEX.md          # This file (comprehensive catalog)
├── STRUCTURE.md                    # Directory organization guide
├── QUICK_NAV.md                    # File path changes reference
├── CHANGELOG.md                    # Change history
├── settings.json                   # Base configuration
├── settings.local.json             # User overrides (gitignored)
│
├── docs/
│   ├── workflows/                  # 9 daily operations files
│   ├── templates/                  # 5 template files
│   ├── guides/                     # 3 how-to guides
│   ├── systems/                    # 3 system architecture docs
│   ├── reference/                  # 6 reference materials
│   └── archive/                    # 9 archived documents
│
├── commands/                       # Slash commands
├── skills/                         # Claude Code skills
├── agents/                         # AI agent configs
├── brand_scout/                    # Lead research system
├── scripts/                        # Python utilities
└── data/                          # JSON databases
```

### Root Level (FirstMile_Deals/)
```
README.md                           # Start here
CLAUDE.md                           # AI context (points to .claude/)
APPROVED_PIPELINE_STRUCTURE.md      # Pipeline definition
FIRSTMILE_PIPELINE_BLUEPRINT.md     # Architecture
Brett_Walker_Instructions_v4.3.md   # Morpheus Method
EOD_SYNC_MASTER_PROMPT.md           # Automated EOD sync
PLD_DISCOVERY_ANALYSIS_PROMPT.md    # Analysis methodology
S4_OPTIMIZATION_PATTERNS.md         # Sonnet 4.5 patterns
REPEATABLE_IMPROVEMENT_TEMPLATE.md  # Workflow improvements
```

### Deal Folders
```
[##-STAGE]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
├── Communications/
├── Performance_Reports/
└── Reference/
```

### Support Folders
```
brand_scout/                # Autonomous lead research
├── BRAND_SCOUT_INSTRUCTIONS.md
├── templates/
│   └── brand_scout_v3.7_template.md
├── output/
│   └── [Generated reports]
└── config/
    └── research_guidelines.md

HubSpot/                    # CRM integration docs
├── HUBSPOT_MCP_CHEATSHEET.md
└── CLAUDE.md

BULK_RATE_PROCESSING/       # Rapid rate creation
└── RATE_CREATION_BLITZ.md

XPARCEL_NATIONAL_SELECT/    # Network analysis tools

_ARCHIVE/                   # Completed deals + old scripts
└── scripts/sync_backups/   # Archived sync scripts (8 files)
```

### External Locations
```
Desktop/
├── AUTOMATION_MONITOR_LOCAL.html
└── NEBUCHADNEZZAR_CONTROL.bat

Downloads/
├── _PIPELINE_TRACKER.csv
├── _DAILY_LOG.md
└── _DAILY_LOG_FEEDBACK.md
```

---

## 🔍 Search Guide

### Finding Specific Information

**HubSpot API Reference** ⭐ NEW:
- [docs/reference/HUBSPOT_API_REFERENCE.md](docs/reference/HUBSPOT_API_REFERENCE.md) - Complete API guide (Gritty-Rain private app)
- Owner ID: 699257003 (Brett Walker), Portal ID: 8210927
- All scopes, endpoints, authentication, code examples

**Configuration & IDs**:
- [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md#critical-system-ids) - All IDs
- [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md#pipeline-stage-ids) - Stage mapping

**Commands & Scripts**:
- [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md#quick-command-reference) - All commands
- [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#quick-reference-card) - Quick commands

**Daily Workflows**:
- [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#9am-sync---day-start) - Morning routine
- [EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md) - Automated EOD sync (mistake-proof)
- [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture) - EOD process

**Deal Management**:
- [docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md#required-files-by-stage) - Stage requirements
- [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows) - Stage transitions

**Analysis Methodology**:
- [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md) - Shipping analysis
- [docs/templates/DEAL_FOLDER_TEMPLATE.md](docs/templates/DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress) - Rate creation

**Troubleshooting**:
- [README.md](README.md#troubleshooting) - Common issues
- [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#troubleshooting) - HubSpot issues
- [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#troubleshooting) - Sync problems

---

## 🎯 Common Tasks - Quick Links

### Daily Operations
- **Start Day**: [9AM Sync Process](docs/workflows/DAILY_SYNC_OPERATIONS.md#9am-sync---day-start)
- **Check Progress**: [NOON Sync](docs/workflows/DAILY_SYNC_OPERATIONS.md#noon-sync---midday-progress-check)
- **End Day**: [EOD Sync Master Prompt](EOD_SYNC_MASTER_PROMPT.md) - Comprehensive automation
- **EOD Manual**: [EOD Sync Operations](docs/workflows/DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture)
- **Week Review**: [End of Week Sync](docs/workflows/DAILY_SYNC_OPERATIONS.md#end-of-week-sync---friday-eod)

### Lead & Deal Management
- **Research Lead**: [Brand Scout System](brand_scout/BRAND_SCOUT_SYSTEM.md)
- **Create Lead**: [Lead Creation Workflow](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-1-single-lead-creation)
- **Convert to Deal**: [Lead to Deal](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-3-lead-to-deal-conversion)
- **Move Deal Stage**: [Stage Progression](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows)
- **Create Tasks**: [Task Automation](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#task--follow-up-automation)

### Analysis & Proposals
- **Run PLD Analysis**: [Analysis Workflow](docs/templates/DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress)
- **Create Rate Card**: [Rate Creation](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#workflow-5-rate-creation--proposal-sent)
- **Generate Proposal**: [Proposal Templates](docs/templates/DEAL_FOLDER_TEMPLATE.md#04-proposal-sent---rates-delivered)
- **Performance Report**: [Performance Reporting](docs/templates/DEAL_FOLDER_TEMPLATE.md#07-closed-won---active-customer)

### System Maintenance
- **Verify Sync**: [Pipeline Sync](README.md#troubleshooting)
- **HubSpot Auth**: [Authentication](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#configuration--setup)
- **Daily Scripts**: [Sync Scripts](docs/workflows/DAILY_SYNC_OPERATIONS.md#quick-reference-commands)

---

## 📊 Documentation Metrics

### Coverage
- **Total Documents**: 13 core files
- **Total Words**: ~50,000
- **Coverage Areas**:
  - System Architecture ✅
  - Daily Operations ✅
  - HubSpot Integration ✅
  - Deal Management ✅
  - Analysis Workflows ✅
  - Continuous Learning ✅
  - Troubleshooting ✅

### Key Achievements
- ✅ Complete system reference with all IDs
- ✅ Daily sync workflow documentation
- ✅ HubSpot MCP integration guide
- ✅ Deal folder templates by stage
- ✅ Continuous learning system
- ✅ Troubleshooting guides
- ✅ Quick reference cards

---

## 🔄 Documentation Updates

### Update Log

**November 6, 2025 - v3.0 Major Reorganization & System Enhancement**
- ✅ Reorganized .claude/ directory into structured subdirectories (docs/{workflows,templates,guides,systems,reference,archive})
- ✅ Created STRUCTURE.md documenting new organization
- ✅ Created QUICK_NAV.md for file path changes
- ✅ Updated all path references in DOCUMENTATION_INDEX.md
- ✅ Created root CLAUDE.md (400 lines) - project instructions
- ✅ Fixed .gitignore to allow .claude/ documentation in version control
- ✅ Created settings.json for team configuration
- ✅ Moved BrightData token to .env for security
- ✅ Pinned Python dependencies for reproducibility
- ✅ Archived 8 old sync scripts
- ✅ Implemented HubSpot rate limiting (hubspot_sync_core.py)
- ✅ Added scheduled GitHub Actions workflows for daily syncs

**October 8, 2025 - v2.1 EOD Sync Automation Enhancement**
- ✅ Created EOD_SYNC_MASTER_PROMPT.md - Comprehensive mistake-proof automation
- ✅ Integrated Superhuman AI email analysis via Chrome MCP
- ✅ Added error prevention patterns from production learnings
- ✅ Updated DOCUMENTATION_INDEX.md with new automation guide

**October 7, 2025 - v2.0 Complete Documentation Suite**
- ✅ Created master README.md
- ✅ Updated NEBUCHADNEZZAR_REFERENCE.md with verified stage IDs
- ✅ Created DAILY_SYNC_OPERATIONS.md
- ✅ Created HUBSPOT_WORKFLOW_GUIDE.md
- ✅ Created DEAL_FOLDER_TEMPLATE.md
- ✅ Created DOCUMENTATION_INDEX.md (this file)

### Maintenance Schedule
- **Daily**: Update `_DAILY_LOG_FEEDBACK.md` with learnings
- **Weekly**: Review and update FAQ sections
- **Monthly**: Audit for outdated information
- **Quarterly**: Major version updates

---

## 🆘 Getting Help

### Quick Help
1. **Can't find something?** Use this index, [QUICK_NAV.md](QUICK_NAV.md), or Ctrl+F in documents
2. **File moved?** Check [QUICK_NAV.md](QUICK_NAV.md) for path changes
3. **Directory structure?** See [STRUCTURE.md](STRUCTURE.md)
4. **HubSpot issues?** See [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md#troubleshooting)
5. **Sync problems?** See [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md#troubleshooting)
6. **New to system?** Start with [README.md](README.md)

### Support Resources
- **System Reference**: [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md)
- **HubSpot API**: [HubSpot/HUBSPOT_MCP_CHEATSHEET.md](HubSpot/HUBSPOT_MCP_CHEATSHEET.md)
- **Daily Workflows**: [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md)
- **Saner.ai Archive**: Check weekly learning exports

---

## 📝 Contributing to Documentation

### Adding New Content
1. Determine best location (existing doc vs new file)
2. Follow markdown formatting standards
3. Update this index with new content
4. Add cross-references in related docs
5. Update table of contents

### Documentation Standards
- **Headings**: Use ATX style (`#`, `##`, `###`)
- **Code Blocks**: Include language identifier
- **Links**: Use relative paths
- **Examples**: Include real, working examples
- **Dates**: YYYY-MM-DD format

---

## 🚀 Next Steps

### For New Users
1. Read [README.md](README.md) completely
2. Review [docs/reference/NEBUCHADNEZZAR_REFERENCE.md](docs/reference/NEBUCHADNEZZAR_REFERENCE.md) for IDs
3. Check [STRUCTURE.md](STRUCTURE.md) to understand organization
4. Understand [docs/workflows/DAILY_SYNC_OPERATIONS.md](docs/workflows/DAILY_SYNC_OPERATIONS.md) workflow
5. Practice with [docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md](docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md)

### For Experienced Users
1. Bookmark this index and [QUICK_NAV.md](QUICK_NAV.md) for quick reference
2. Contribute learnings to `_DAILY_LOG_FEEDBACK.md`
3. Suggest documentation improvements
4. Help maintain and update guides

---

**Last Updated**: November 6, 2025
**System Version**: Nebuchadnezzar v3.0
**Documentation Status**: Complete (Reorganized v3.0)
**Maintained By**: Brett Walker
