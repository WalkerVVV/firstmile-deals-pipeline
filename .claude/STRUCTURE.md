# .claude/ Directory Structure

**Last Updated**: 2025-11-06

## Overview

Organized documentation structure with clear separation of concerns.

```
.claude/
├── README.md                    # Quick start guide
├── INDEX.md                     # Main navigation
├── DOCUMENTATION_INDEX.md       # Comprehensive doc catalog
├── CHANGELOG.md                 # Change history
├── STRUCTURE.md                 # This file
│
├── settings.json                # Base project configuration
├── settings.local.json          # User-specific settings (gitignored)
├── .claude.json                 # Claude Code metadata
│
├── docs/                        # All documentation
│   ├── workflows/              # Daily operations & sync processes
│   ├── templates/              # Deal folder & analysis templates
│   ├── guides/                 # How-to guides & quick references
│   ├── systems/                # System architecture & integration
│   ├── reference/              # IDs, mappings, & lookup tables
│   └── archive/                # Outdated documentation
│
├── commands/                    # Slash commands (project-specific)
├── skills/                      # Claude Code skills
│   └── excel-analysis/         # Excel processing skill
│
├── agents/                      # AI agent configurations
├── brand_scout/                 # Automated lead research system
│   ├── config/                 # Brand scout configuration
│   ├── input/                  # Input queue for research
│   ├── output/                 # Generated lead folders
│   └── templates/              # Lead folder templates
│
├── scripts/                     # Python utility scripts
│   └── superhuman_eod_workflow.py
│
└── data/                        # JSON databases & caches
    └── DEAL_MEMORY_DATABASE.json

```

## Directory Purposes

### Core Files (Root Level)
- **README.md**: Quick start and system overview
- **INDEX.md**: Main navigation hub
- **DOCUMENTATION_INDEX.md**: Comprehensive catalog of all documentation
- **CHANGELOG.md**: Version history and change tracking
- **settings.json**: Team-wide base configuration
- **settings.local.json**: User-specific overrides (never committed)

### docs/workflows/
Daily operations, sync processes, and recurring workflows.

**Files**:
- `DAILY_SYNC_OPERATIONS.md` - Complete 9AM, noon, 3PM, EOD sync workflows
- `DAILY_SYNC_FLOWS_V3.md` - Sync flow diagrams and logic
- `HUBSPOT_WORKFLOW_GUIDE.md` - HubSpot integration workflows
- `HUBSPOT_REALTIME_WORKFLOW.md` - Real-time HubSpot sync
- `AUTO_STORE_WORKFLOW.md` - Automated storage workflows
- `CROSS_DEVICE_WORKFLOW.md` - Multi-device sync patterns
- `SYNC_AGENT_ORCHESTRATION.md` - Agent coordination for syncs
- `TUESDAY_MORNING_STARTUP_GUIDE.md` - Weekly startup procedures
- `APPLYING_LEARNINGS_TO_DAILY_WORKFLOW.md` - Continuous improvement

### docs/templates/
Standardized templates for common operations.

**Files**:
- `DEAL_FOLDER_TEMPLATE.md` - Standard deal folder structure
- `NEW_ACCOUNT_SETUP_TEMPLATE.md` - New customer onboarding
- `FULL_XPARCEL_ANALYSIS_TEMPLATE.md` - Comprehensive analysis template
- `EXCEL_PROCESS_TEMPLATES.md` - Excel report generation
- `WORKBOOK_BLUEPRINT (1).md` - Workbook structure guide

### docs/guides/
How-to guides and quick references.

**Files**:
- `SYNC_QUICK_REFERENCE.md` - Quick sync command reference
- `SLASH_COMMANDS_GUIDE.md` - Available slash commands
- `FOLDER_STRUCTURE.md` - Project structure guide

### docs/systems/
System architecture and integration documentation.

**Files**:
- `BRAND_SCOUT_SYSTEM.md` - Automated lead generation system
- `MEMORY_AND_MCP_INTEGRATION.md` - Memory system integration
- `DOMAIN_MEMORY_INTEGRATION.md` - Domain-specific memory

### docs/reference/
IDs, mappings, lookup tables, and reference materials.

**Files**:
- `NEBUCHADNEZZAR_REFERENCE.md` - Complete system reference
- `VERIFIED_STAGE_IDS.md` - HubSpot pipeline stage mappings
- `INSTALLED_PLUGINS_REFERENCE.md` - Plugin catalog
- `OFFICIAL_ANTHROPIC_PLUGINS.md` - Official plugin list
- `HUBSPOT_MCP_STATUS.md` - MCP server status
- `DEAL_MEMORY_INDEX.md` - Deal memory database index

### docs/archive/
Outdated or superseded documentation (preserved for reference).

**Files**:
- `MISSING_STAGES_RECOMMENDATION.md` - Historical stage analysis
- `VERSION_CONSISTENCY_REPORT.md` - Version audit (completed)
- `SYSTEM_STATUS.md` - Snapshot of system state
- `SESSION_CONTEXT.md` - Session management (deprecated)
- `mobile-first-context.md` - Mobile context (archived)
- `PRIORITIZATION_AGENT_LEARNINGS.md` - Agent learnings archive
- `PRIORITIZATION_AGENT_PROMPT.md` - Agent prompt archive
- `API_KEY_SECURITY.md` - Security guide (superseded by SECURITY.md)
- `MASTER_LEARNINGS_COMPREHENSIVE.md` - Learnings archive

### commands/
Project-specific slash commands.

**Purpose**: Custom Claude Code slash commands for this project.

**Examples**:
- `/sync [time]` - Trigger sync workflows
- `/deal [action]` - Deal management operations
- `/report [type]` - Generate analysis reports
- `/scout [company]` - Run brand scout research

### skills/
Claude Code skills for specialized operations.

**Current Skills**:
- `excel-analysis/` - Excel data processing and report generation

### agents/
AI agent configurations for complex workflows.

**Purpose**: Specialized agent prompts and configurations.

### brand_scout/
Automated lead research and qualification system.

**Workflow**:
1. Input: Company names added to `input/`
2. Processing: Overnight brand research
3. Output: Generated lead folders in `output/`
4. Integration: Auto-create HubSpot leads

See `docs/systems/BRAND_SCOUT_SYSTEM.md` for details.

### scripts/
Python utility scripts for .claude/ operations.

**Files**:
- `superhuman_eod_workflow.py` - EOD workflow automation

**Note**: Main project scripts remain in root directory.

### data/
JSON databases and cached data.

**Files**:
- `DEAL_MEMORY_DATABASE.json` - Deal state and history

## File Naming Conventions

### Uppercase
- **ALL_CAPS.md**: System documentation (CHANGELOG, README, INDEX)
- **PROPER_CASE.md**: Feature/topic documentation

### Lowercase
- **lowercase.md**: Meta files (mobile-first-context)

### Scripts
- **snake_case.py**: Python scripts
- **kebab-case.json**: Configuration files

## Navigation Paths

### Finding Documentation

**Quick Start**: Start with `README.md`

**Full Catalog**: See `DOCUMENTATION_INDEX.md`

**By Topic**:
- Daily operations → `docs/workflows/DAILY_SYNC_OPERATIONS.md`
- Deal setup → `docs/templates/DEAL_FOLDER_TEMPLATE.md`
- HubSpot integration → `docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md`
- System reference → `docs/reference/NEBUCHADNEZZAR_REFERENCE.md`
- Brand scout → `docs/systems/BRAND_SCOUT_SYSTEM.md`

### Common Tasks

**Create new deal**: Use template from `docs/templates/DEAL_FOLDER_TEMPLATE.md`

**Run daily sync**: Follow `docs/workflows/DAILY_SYNC_OPERATIONS.md`

**Set up new account**: Use `docs/templates/NEW_ACCOUNT_SETUP_TEMPLATE.md`

**Research leads**: Configure `brand_scout/input/`

**Find HubSpot IDs**: Check `docs/reference/VERIFIED_STAGE_IDS.md`

## Maintenance

### Adding New Documentation

1. Determine category (workflows, templates, guides, systems, reference)
2. Create file in appropriate `docs/` subdirectory
3. Update `DOCUMENTATION_INDEX.md`
4. Update `CHANGELOG.md`
5. Commit with descriptive message

### Archiving Documentation

When documentation becomes outdated:
1. Move to `docs/archive/`
2. Add note to `DOCUMENTATION_INDEX.md`
3. Update referencing documents
4. Document reason in `CHANGELOG.md`

### Directory Hygiene

- Keep root `.claude/` directory minimal (5-10 files max)
- All new docs go into `docs/` subdirectories
- Archive outdated content promptly
- Update index files when structure changes

## Version History

- **2025-11-06**: Initial organization - moved 38 files into structured subdirectories
- **Previous**: Flat structure with all files in root `.claude/` directory
