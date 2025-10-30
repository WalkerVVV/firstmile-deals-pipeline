# FirstMile Deals - Documentation Index
**Complete Guide to Nebuchadnezzar v3.0 System**

---

## 📚 Quick Navigation

### 🚀 Start Here
1. **[README.md](README.md)** - System overview and quick start guide
2. **[NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md)** - Complete system reference with all IDs and commands
3. **[FIRSTMILE_PIPELINE_BLUEPRINT.md](FIRSTMILE_PIPELINE_BLUEPRINT.md)** - HubSpot & N8N integration architecture

### 📋 Daily Operations
4. **[DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md)** - 9AM, NOON, EOD, and weekly sync workflows
5. **agents/[README.md](agents/README.md)** - 🎯 Sales Discipline Agents (NEW: 5/2/3/1 accountability)
6. **[EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md)** - Comprehensive EOD sync automation prompt (mistake-proof)
7. **[S4_OPTIMIZATION_PATTERNS.md](S4_OPTIMIZATION_PATTERNS.md)** - Sonnet 4.5 specific optimization patterns
8. **[REPEATABLE_IMPROVEMENT_TEMPLATE.md](REPEATABLE_IMPROVEMENT_TEMPLATE.md)** - Template for capturing workflow improvements
9. **[HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot MCP integration and workflows
10. **[DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md)** - Standard deal folder structure by stage

### 🧠 Strategy & Methodology
11. **[Brett_Walker_Instructions_v4.3.md](Brett_Walker_Instructions_v4.3.md)** - Morpheus Method and positioning
12. **[APPROVED_PIPELINE_STRUCTURE.md](APPROVED_PIPELINE_STRUCTURE.md)** - Official 10-stage pipeline definition
13. **HubSpot/[HUBSPOT_MCP_CHEATSHEET.md](HubSpot/HUBSPOT_MCP_CHEATSHEET.md)** - Complete API reference
14. **[CLAUDE.md](CLAUDE.md)** - AI assistant project context

### 🔧 Specialized Guides
15. **[EXCEL_PROCESS_TEMPLATES.md](EXCEL_PROCESS_TEMPLATES.md)** - Quick reference for all Excel deliverables
16. **[FULL_XPARCEL_ANALYSIS_TEMPLATE.md](FULL_XPARCEL_ANALYSIS_TEMPLATE.md)** - Standard Full Xparcel Analysis process
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
2. Review [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md) - Get all configuration IDs
3. Verify HubSpot connection: `qm hubspot get-deal --deal-id [ANY-ID]`
4. Run pipeline sync: `python pipeline_sync_verification.py`

**Required Files**:
- Desktop: `AUTOMATION_MONITOR_LOCAL.html`, `NEBUCHADNEZZAR_CONTROL.bat`
- Downloads: `_PIPELINE_TRACKER.csv`, `_DAILY_LOG.md`, `FOLLOW_UP_REMINDERS.txt`

### Managing Daily Workflow

**Morning Routine (9AM)**:
1. Review [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#9am-sync---day-start)
2. Run: `python daily_9am_workflow.py`
3. **🎯 NEW**: `python .claude/agents/prioritization_agent.py --daily-reminder` (Top 3 priorities)
4. **🎯 NEW**: `python .claude/agents/sales_execution_agent.py` (Check stale proposals)
5. Execute P1 actions from output
6. **Optional**: Batch Brand Scout research on queued leads

**Midday Check (NOON)**:
1. Review [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#noon-sync---midday-progress-check)
2. Run: `python pipeline_sync_verification.py`
3. **Optional**: Process new web form submissions via Brand Scout

**End of Day (5PM)**:
1. Review [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture)
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
1. Reference [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#workflow-1-single-lead-creation)
2. Create lead: `qm hubspot create-lead ...`
3. Convert to deal: `qm hubspot convert-to-deal ...`
4. Create folder using [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md)

**New Lead → Deal (Brand Scout Automated)**:
1. Generate report: `"Scout brand: [URL]"` in Claude Code
2. Review output in `.claude/brand_scout/output/`
3. Copy Section 6 fields to HubSpot
4. Create `[00-LEAD]_[BRAND]` folder with report

**Moving Deal Through Pipeline**:
1. Reference [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows)
2. Move folder: `mv [OLD-STAGE]_Company [NEW-STAGE]_Company`
3. Verify sync or manual update: `qm hubspot update-deal ...`
4. Add HubSpot note documenting stage change

### Running Analysis

**Full Xparcel Analysis** (Professional Prospect Deliverable):
1. Follow [FULL_XPARCEL_ANALYSIS_TEMPLATE.md](FULL_XPARCEL_ANALYSIS_TEMPLATE.md) - Complete process
2. Use standard prompt template with customer PLD data
3. Generate 6-tab professional Excel with FirstMile branding
4. Weight profile: 1-15oz, 15.99oz, 1-10lb (matches rate card structure)
5. Output: `[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx`

**PLD Analysis Workflow**:
1. Get methodology from [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md)
2. Place data in `[STAGE]_Company/PLD_Analysis/raw_data/`
3. Run scripts from [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress):
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
1. Follow [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress) structure
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
3. Follow [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#phase-2-learnings--insights) templates

**SOP Evolution**:
1. Propose change with v# in `_DAILY_LOG_FEEDBACK.md`
2. Test for 1-2 weeks (🟡 TESTING status)
3. Validate results and mark ✅ PERMANENT or 🔴 ABANDON

---

## 🗂 File Organization

### Root Level (FirstMile_Deals/)
```
README.md                           # Start here
DOCUMENTATION_INDEX.md              # This file
NEBUCHADNEZZAR_REFERENCE.md         # Complete reference
FIRSTMILE_PIPELINE_BLUEPRINT.md     # Architecture
DAILY_SYNC_OPERATIONS.md            # Daily workflows
EOD_SYNC_MASTER_PROMPT.md           # Automated EOD sync (mistake-proof)
HUBSPOT_WORKFLOW_GUIDE.md           # HubSpot integration
DEAL_FOLDER_TEMPLATE.md             # Folder standards
APPROVED_PIPELINE_STRUCTURE.md      # Pipeline definition
Brett_Walker_Instructions_v4.3.md   # Morpheus Method
CLAUDE.md                           # AI context
PLD_DISCOVERY_ANALYSIS_PROMPT.md    # Analysis methodology
FULL_XPARCEL_ANALYSIS_TEMPLATE.md   # Standard Full Xparcel Analysis
EXCEL_PROCESS_TEMPLATES.md          # Excel deliverable quick reference
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
.claude/brand_scout/        # Autonomous lead research
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

_ARCHIVE/                   # Completed deals
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

**Configuration & IDs**:
- [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md#critical-system-ids) - All IDs
- [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md#pipeline-stage-ids) - Stage mapping

**Commands & Scripts**:
- [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md#quick-command-reference) - All commands
- [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#quick-reference-card) - Quick commands

**Daily Workflows**:
- [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#9am-sync---day-start) - Morning routine
- [EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md) - Automated EOD sync (mistake-proof)
- [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture) - EOD process

**Deal Management**:
- [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md#required-files-by-stage) - Stage requirements
- [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows) - Stage transitions

**Analysis Methodology**:
- [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md) - Shipping analysis
- [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress) - Rate creation

**Troubleshooting**:
- [README.md](README.md#troubleshooting) - Common issues
- [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#troubleshooting) - HubSpot issues
- [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#troubleshooting) - Sync problems

---

## 🎯 Common Tasks - Quick Links

### Daily Operations
- **Start Day**: [9AM Sync Process](DAILY_SYNC_OPERATIONS.md#9am-sync---day-start)
- **Check Progress**: [NOON Sync](DAILY_SYNC_OPERATIONS.md#noon-sync---midday-progress-check)
- **End Day**: [EOD Sync Master Prompt](EOD_SYNC_MASTER_PROMPT.md) - Comprehensive automation
- **EOD Manual**: [EOD Sync Operations](DAILY_SYNC_OPERATIONS.md#eod-sync---end-of-day-learning-capture)
- **Week Review**: [End of Week Sync](DAILY_SYNC_OPERATIONS.md#end-of-week-sync---friday-eod)

### Lead & Deal Management
- **Research Lead**: [Brand Scout System](brand_scout/BRAND_SCOUT_SYSTEM.md)
- **Create Lead**: [Lead Creation Workflow](HUBSPOT_WORKFLOW_GUIDE.md#workflow-1-single-lead-creation)
- **Convert to Deal**: [Lead to Deal](HUBSPOT_WORKFLOW_GUIDE.md#workflow-3-lead-to-deal-conversion)
- **Move Deal Stage**: [Stage Progression](HUBSPOT_WORKFLOW_GUIDE.md#deal-progression-workflows)
- **Create Tasks**: [Task Automation](HUBSPOT_WORKFLOW_GUIDE.md#task--follow-up-automation)

### Analysis & Proposals
- **Run PLD Analysis**: [Analysis Workflow](DEAL_FOLDER_TEMPLATE.md#03-rate-creation---pricing-in-progress)
- **Create Rate Card**: [Rate Creation](HUBSPOT_WORKFLOW_GUIDE.md#workflow-5-rate-creation--proposal-sent)
- **Generate Proposal**: [Proposal Templates](DEAL_FOLDER_TEMPLATE.md#04-proposal-sent---rates-delivered)
- **Performance Report**: [Performance Reporting](DEAL_FOLDER_TEMPLATE.md#07-closed-won---active-customer)

### System Maintenance
- **Verify Sync**: [Pipeline Sync](README.md#troubleshooting)
- **HubSpot Auth**: [Authentication](HUBSPOT_WORKFLOW_GUIDE.md#configuration--setup)
- **Daily Scripts**: [Sync Scripts](DAILY_SYNC_OPERATIONS.md#quick-reference-commands)

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
1. **Can't find something?** Use this index or Ctrl+F in documents
2. **HubSpot issues?** See [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md#troubleshooting)
3. **Sync problems?** See [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md#troubleshooting)
4. **New to system?** Start with [README.md](README.md)

### Support Resources
- **System Reference**: [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md)
- **HubSpot API**: [HubSpot/HUBSPOT_MCP_CHEATSHEET.md](HubSpot/HUBSPOT_MCP_CHEATSHEET.md)
- **Daily Workflows**: [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md)
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
2. Review [NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md) for IDs
3. Understand [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md) workflow
4. Practice with [HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md)

### For Experienced Users
1. Bookmark this index for quick reference
2. Contribute learnings to `_DAILY_LOG_FEEDBACK.md`
3. Suggest documentation improvements
4. Help maintain and update guides

---

**Last Updated**: October 7, 2025
**System Version**: Nebuchadnezzar v3.0
**Documentation Status**: Complete
**Maintained By**: Brett Walker
