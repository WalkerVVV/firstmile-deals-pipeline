# .claude Folder - Central Operations Manual
**Nebuchadnezzar v2.0 System Documentation**

This folder contains ALL system documentation, templates, and operational guides used across every deal in the FirstMile_Deals pipeline.

---

## 📚 Core Documentation (START HERE)

1. **[README.md](README.md)** - Complete system overview & quick start
2. **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Master navigation guide
3. **[NEBUCHADNEZZAR_REFERENCE.md](NEBUCHADNEZZAR_REFERENCE.md)** - Complete system reference with all IDs & commands
4. **[CHANGELOG.md](CHANGELOG.md)** - Version history, changes, migrations, and roadmap

---

## 📋 Operational Guides

### Daily Operations
- **[DAILY_SYNC_FLOWS_V3.md](DAILY_SYNC_FLOWS_V3.md)** - ⭐ v3.0 Daily sync prompts (9AM, NOON, 3PM, EOD, Weekly) with continuous improvement
- **[SYNC_QUICK_REFERENCE.md](SYNC_QUICK_REFERENCE.md)** - One-page quick reference card for syncs
- **[DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md)** - Legacy sync workflow documentation
- **[HUBSPOT_WORKFLOW_GUIDE.md](HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot MCP integration & workflows

### Deal Management
- **[DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md)** - Standard folder structure for all deals

### System Status & Reference
- **[VERIFIED_STAGE_IDS.md](VERIFIED_STAGE_IDS.md)** - ⭐ Authoritative stage ID mapping (verified October 7, 2025)
- **[SYSTEM_STATUS.md](SYSTEM_STATUS.md)** - Current status, verification checklist, known issues
- **[HUBSPOT_MCP_STATUS.md](HUBSPOT_MCP_STATUS.md)** - MCP connection status and workarounds
- **[MISSING_STAGES_RECOMMENDATION.md](MISSING_STAGES_RECOMMENDATION.md)** - Analysis of [00-LEAD] and [09-WIN-BACK]

---

## 🏗️ System Architecture (Legacy)

These files are maintained for historical reference:

- **[WORKBOOK_BLUEPRINT (1).md](WORKBOOK_BLUEPRINT (1).md)** - Original workbook design
- **settings.local.json** - Local configuration

---

## 📁 How to Use This Folder

### For Individual Deals
Every deal folder should reference this central documentation:

```markdown
# In [STAGE]_Company/CLAUDE.md:

See central documentation:
- Operations: /.claude/README.md
- Daily Workflow: /.claude/DAILY_SYNC_OPERATIONS.md
- Templates: /.claude/DEAL_FOLDER_TEMPLATE.md
```

### For System Maintenance
Update documentation here, NOT in individual deal folders. All deals automatically benefit from centralized updates.

### For New Team Members
Start with:
1. [README.md](README.md) - System overview
2. [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md) - Daily workflow
3. [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Find everything

---

## 🔄 Documentation Update Process

1. **Make changes in `.claude` folder only**
2. Individual deals reference centralized docs
3. No duplication across deal folders
4. Version control via git (FirstMile_Deals root)

---

**Last Updated**: October 7, 2025
**Location**: `C:\Users\BrettWalker\FirstMile_Deals\.claude\`
**Purpose**: Centralized operations manual for all pipeline activities
