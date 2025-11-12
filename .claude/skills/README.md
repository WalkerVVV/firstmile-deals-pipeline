# Agent Skills Reference

Agent-specific skill documentation that references [rules.md](../../rules.md) for complete system compliance.

## Available Skills

### 1. [Brand Scout Agent](./brand_scout_skill.md)
**Purpose**: Autonomous overnight research to identify new shipping leads

**Key Rules**:
- Human approval gate before HubSpot creation
- Confidence scoring (High/Medium/Low) required
- Source attribution mandatory
- Overnight execution only (never during business hours)

**Output**: Research summaries in `.claude/brand_scout/output/YYYY-MM-DD/`

**Quality Gates**:
- [ ] Confidence scores calculated
- [ ] Sources documented
- [ ] Output saved for 9AM review
- [ ] Human approval received before HubSpot creation

---

### 2. [Prioritization Agent](./prioritization_skill.md)
**Purpose**: Daily morning sync to prioritize active deals and set daily focus

**Key Rules**:
- MUST load yesterday's EOD context before HubSpot fetch
- Calculate days in stage for all deals
- Flag deals >7 days with warnings
- Document top 3-5 priority actions

**Output**: 9AM priority report with context reference

**Quality Gates**:
- [ ] Yesterday's context loaded
- [ ] Fresh HubSpot data fetched
- [ ] Priority scores calculated
- [ ] Top 3-5 actions documented
- [ ] Follow-up queue updated

---

### 3. [Analysis Agent](./analysis_skill.md)
**Purpose**: Generate shipping profile analyses and FirstMile performance reports

**Key Rules**:
- Follow FIRSTMILE.md framework exactly
- Lead ALL reports with SLA compliance (not daily %)
- Use "National" or "Select" network terminology
- NEVER name carriers (UPS, FedEx, USPS)
- Include zone distribution and hub mapping

**Output**: PLD analysis, rate comparisons, 9-tab Excel performance reports

**Quality Gates**:
- [ ] FIRSTMILE.md compliance validated
- [ ] SLA compliance leads metrics
- [ ] Network terminology used correctly
- [ ] Zone distribution included
- [ ] Hub mapping for top states

---

## How to Use Agent Skills

### 1. Load Skill at Session Start
```bash
# In Claude Code
/load @.claude/skills/brand_scout_skill.md

# Or reference in your code
from pathlib import Path
skill_path = Path('.claude/skills/prioritization_skill.md')
```

### 2. Follow Execution Workflow
Each skill file contains:
- Phase-by-phase execution steps
- Quality gate checklists
- Code examples and templates
- Error handling guidance

### 3. Validate Against Rules
All skills reference [rules.md](../../rules.md) for compliance. Use the Rules Compliance Validator:

```python
from utils.rules_compliance_validator import RulesComplianceValidator

validator = RulesComplianceValidator()

# Validate Brand Scout operation
report = validator.validate_brand_scout_operation(
    human_approval_received=True,
    confidence_scores_calculated=True,
    sources_documented=True,
    output_saved=True,
    is_business_hours=False
)

validator.print_report(report)
```

---

## Rules Compliance Validator

**Location**: `utils/rules_compliance_validator.py`

**Purpose**: Automated enforcement of rules.md quality gates

**Available Validations**:
- `validate_sync_operation()` - 9AM, noon, 3PM, EOD, weekly syncs
- `validate_hubspot_operation()` - HubSpot API calls
- `validate_brand_scout_operation()` - Brand scout research
- `validate_analysis_operation()` - PLD analysis and reports
- `validate_excel_report()` - Excel report compliance
- `validate_folder_operation()` - Deal folder moves
- `validate_learning_capture()` - Learning loop compliance

**Example Integration**:
```python
# In your sync script
from utils.rules_compliance_validator import validate_9am_sync

# Before execution
report = validate_9am_sync(
    context_loaded=True,
    previous_eod_path='/path/to/eod_sync.md',
    hubspot_fresh=True
)

if report['status'] == 'FAIL':
    print("Violations detected - address before continuing")
    sys.exit(1)
```

**See**: `examples/sync_with_compliance_validation.py` for full integration example

---

## Quality Gates Reference

### Sync Operations
- [ ] Previous context loaded before HubSpot fetch
- [ ] Fresh HubSpot data fetched
- [ ] Priority actions documented (3-5 items)
- [ ] Learnings captured (EOD/weekly only)
- [ ] Context saved for next sync

### HubSpot Operations
- [ ] Uses `hubspot_sync_core.HubSpotSyncManager`
- [ ] Credentials validated via `CredentialManager`
- [ ] Rate limiter enabled (100 calls per 10 seconds)
- [ ] Folder verified (for stage updates)

### Brand Scout Operations
- [ ] Human approval received before HubSpot creation
- [ ] Confidence scores calculated (High/Medium/Low)
- [ ] Research sources documented
- [ ] Output saved to `.claude/brand_scout/output/`
- [ ] Overnight execution only (not business hours)

### Analysis Operations
- [ ] Follows FIRSTMILE.md framework
- [ ] SLA compliance leads metrics (not daily %)
- [ ] Uses "National" or "Select" network terminology
- [ ] NO carrier names mentioned (UPS, FedEx, USPS)
- [ ] Zone distribution included
- [ ] Hub mapping for top states

### Excel Reports
- [ ] 9 tabs in correct order
- [ ] FirstMile blue (#366092) on all headers
- [ ] SLA Compliance tab #2 (leads metrics)
- [ ] Conditional formatting (red/yellow/green)
- [ ] Auto-filters enabled
- [ ] Filename follows convention

---

## Related Documentation

- **[rules.md](../../rules.md)** - Complete system rules and agent-specific sections
- **[DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md)** - Master navigation
- **[NEBUCHADNEZZAR_REFERENCE.md](../docs/reference/NEBUCHADNEZZAR_REFERENCE.md)** - Stage IDs and automation
- **[DAILY_SYNC_OPERATIONS.md](../docs/workflows/DAILY_SYNC_OPERATIONS.md)** - Sync workflows
- **[FIRSTMILE.md](~/.claude/FIRSTMILE.md)** - FirstMile brand framework

---

## Version

**Created**: 2025-11-07
**Skills**: Brand Scout, Prioritization, Analysis
**Validator**: rules_compliance_validator.py v1.0
**Framework**: The Nebuchadnezzar v3.0
