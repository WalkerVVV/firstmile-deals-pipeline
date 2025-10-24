# FirstMile Deals - Proper Folder Structure
**Centralized Documentation in .claude Folder**

---

## ✅ CORRECT Structure (Current)

```
FirstMile_Deals/
│
├── .claude/                                    ← CENTRAL OPERATIONS MANUAL
│   ├── INDEX.md                               ← START HERE
│   ├── README.md                              ← System overview
│   ├── DOCUMENTATION_INDEX.md                 ← Master navigation
│   ├── NEBUCHADNEZZAR_REFERENCE.md            ← All IDs & commands
│   ├── DAILY_SYNC_OPERATIONS.md               ← Daily workflows
│   ├── HUBSPOT_WORKFLOW_GUIDE.md              ← HubSpot integration
│   ├── DEAL_FOLDER_TEMPLATE.md                ← Standard templates
│   └── FOLDER_STRUCTURE.md                    ← This file
│
├── CLAUDE.md                                   ← Points to .claude/ docs
├── FIRSTMILE_PIPELINE_BLUEPRINT.md            ← Historical architecture
├── APPROVED_PIPELINE_STRUCTURE.md             ← Pipeline definition
├── Brett_Walker_Instructions_v4.3.md          ← Morpheus Method
│
├── [00-LEAD]_Template/                        ← Stage templates
├── [01-DISCOVERY-SCHEDULED]_Template/
├── [01-DISCOVERY-SCHEDULED]_Josh's_Frogs/     ← Active deals
├── [01-DISCOVERY-SCHEDULED]_Logystico LLC/
├── [01-QUALIFIED]_DYLN/
├── [02-DISCOVERY-COMPLETE]_FEE_Solutions/
├── [03-RATE-CREATION]_Stackd_Logistics/
│   ├── CLAUDE.md                              ← References /.claude/ docs
│   ├── Customer_Relationship_Documentation.md
│   ├── PLD_Analysis/
│   └── ...
│
├── HubSpot/
│   └── HUBSPOT_MCP_CHEATSHEET.md
│
├── BULK_RATE_PROCESSING/
│   └── RATE_CREATION_BLITZ.md
│
├── Python Scripts/
│   ├── daily_9am_workflow.py
│   ├── daily_9am_sync.py
│   └── pipeline_sync_verification.py
│
└── _ARCHIVE/
    └── [Completed deals]
```

---

## 🎯 Key Principles

### 1. Centralized Documentation
**ALL system documentation lives in `.claude/` folder**

✅ **DO**:
- Store all guides, templates, and references in `.claude/`
- Update documentation in ONE place
- Reference centralized docs from deal folders

❌ **DON'T**:
- Duplicate documentation in deal folders
- Create README.md in individual deals
- Scatter system guides across folders

### 2. Deal Folder References

**In each [STAGE]_Company/CLAUDE.md**:
```markdown
# [Company Name] Deal Context

## System Documentation
See centralized operations manual:
- **Overview**: /.claude/README.md
- **Daily Workflow**: /.claude/DAILY_SYNC_OPERATIONS.md
- **HubSpot Guide**: /.claude/HUBSPOT_WORKFLOW_GUIDE.md
- **Templates**: /.claude/DEAL_FOLDER_TEMPLATE.md

## Deal-Specific Context
[Company-specific information here]
```

### 3. Update Workflow

**To update system documentation**:
1. Edit files in `.claude/` folder ONLY
2. All deals automatically benefit from updates
3. No need to touch individual deal folders
4. Version control via git tracks all changes

---

## 📁 What Goes Where

### `.claude/` Folder (Central Ops Manual)
✅ System documentation
✅ Operational guides
✅ HubSpot workflows
✅ Standard templates
✅ Daily sync procedures
✅ Reference materials

### Individual Deal Folders
✅ Customer-specific data
✅ PLD analysis & scripts
✅ Rate cards & proposals
✅ Communications log
✅ Deal-specific CLAUDE.md (references central docs)

### Project Root
✅ CLAUDE.md (points to .claude/)
✅ Historical architecture docs
✅ Morpheus Method instructions
✅ Python automation scripts

---

## 🔄 Migration Complete

**What was moved**:
- ✅ README.md → .claude/README.md
- ✅ NEBUCHADNEZZAR_REFERENCE.md → .claude/
- ✅ DAILY_SYNC_OPERATIONS.md → .claude/
- ✅ HUBSPOT_WORKFLOW_GUIDE.md → .claude/
- ✅ DEAL_FOLDER_TEMPLATE.md → .claude/
- ✅ DOCUMENTATION_INDEX.md → .claude/

**What was created**:
- ✅ .claude/INDEX.md (navigation hub)
- ✅ .claude/FOLDER_STRUCTURE.md (this file)
- ✅ Updated CLAUDE.md to reference .claude/

---

## 🚀 How to Use

### For Daily Work
1. Open `.claude/INDEX.md` to navigate
2. Reference specific guides as needed
3. Work in individual deal folders
4. Updates automatically apply to all deals

### For New Team Members
1. Start with `.claude/README.md`
2. Review `.claude/DAILY_SYNC_OPERATIONS.md`
3. Use `.claude/DOCUMENTATION_INDEX.md` to find everything

### For System Updates
1. Edit documentation in `.claude/` only
2. Commit changes via git
3. All deals benefit immediately
4. No duplication or sync issues

---

## 🔍 Finding Documentation

**From anywhere in the project**:
```bash
# View central docs index
cat .claude/INDEX.md

# Access specific guide
code .claude/DAILY_SYNC_OPERATIONS.md

# See all available docs
ls .claude/*.md
```

**From a deal folder**:
```bash
# Reference relative path
cat ../../.claude/README.md

# Or use absolute path
cat C:/Users/BrettWalker/FirstMile_Deals/.claude/README.md
```

---

## ✨ Benefits of This Structure

1. **Single Source of Truth**: All docs in one place
2. **Easy Updates**: Change once, applies everywhere
3. **No Duplication**: Eliminates sync issues
4. **Clear Separation**: System docs vs deal-specific data
5. **Scalable**: Add new deals without doc duplication
6. **Version Control**: Git tracks all doc changes

---

**Last Updated**: October 7, 2025
**System**: Nebuchadnezzar v2.0
**Purpose**: Centralized operations manual for all pipeline activities
