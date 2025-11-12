# Rules.md System Implementation Summary

**Date**: 2025-11-07
**System**: The Nebuchadnezzar v3.0
**Framework**: Solo Swift Crafter methodology adapted for Python/HubSpot/FirstMile

---

## 🎯 What We Built

A comprehensive **rules.md** system based on the Solo Swift Crafter methodology that provides:

1. **Universal `rules.md`** with agent-specific sections
2. **Agent skill files** that reference rules.md for detailed workflows
3. **Excel reporting standards** integrated into rules
4. **Common Mistakes section** with 10 violation examples and corrections
5. **Versioning strategy** with changelog
6. **Rules compliance validator** for automated enforcement

---

## 📂 File Structure Created

```
FirstMile_Deals/
├── rules.md                                    # Master rules file (NEW)
├── .claude/
│   └── skills/                                 # Agent skill files (NEW)
│       ├── README.md                           # Skills overview
│       ├── brand_scout_skill.md                # Brand Scout workflows
│       ├── prioritization_skill.md             # 9AM sync workflows
│       └── analysis_skill.md                   # Analysis & reporting workflows
├── utils/
│   └── rules_compliance_validator.py           # Compliance validator (NEW)
└── examples/
    └── sync_with_compliance_validation.py      # Integration example (NEW)
```

---

## 📋 Rules.md Contents (1,276 lines)

### Core Sections

1. **Overview** (lines 1-36)
   - Project summary and scope
   - Source of truth references
   - Engineering ethos and principles

2. **Python Best Practices** (lines 38-75)
   - Architecture patterns
   - Modularity requirements
   - Naming conventions

3. **Agent Best Practices (8 MUST-FOLLOW RULES)** (lines 77-192)
   - Rule #1: Shared Code > Duplication
   - Rule #2: Context Continuity Across Syncs
   - Rule #3: Learning Gates (Capture Before Complete)
   - Rule #4: Folder-HubSpot Consistency
   - Rule #5: Credential Security (Zero Tolerance)
   - Rule #6: Brand Scout Approval Gate
   - Rule #7: Performance Standards & Quality Gates
   - Rule #8: Ask Before Major Operations

4. **Agent-Specific Rules** (lines 194-395)
   - Brand Scout Agent
   - Prioritization Agent (9AM Sync)
   - Analysis Agent (PLD & Performance Reports)
   - Sync Coordinator Agent (HubSpot API)
   - Learning Agent (Knowledge Capture)

5. **Sync Flow Constraints** (lines 397-465)
   - Timing dependencies (9AM → Noon → 3PM → EOD → Weekly)
   - Context dependency rules
   - Output format standards
   - HubSpot consistency rules

6. **File Operations & Folder Management** (lines 467-502)
   - Folder move policy (ask first)
   - Archive/Win-Back policy
   - Script creation policy
   - Documentation auto-update policy

7. **References** (lines 504-518)
   - DOCUMENTATION_INDEX.md
   - NEBUCHADNEZZAR_REFERENCE.md
   - DAILY_SYNC_OPERATIONS.md
   - HUBSPOT_WORKFLOW_GUIDE.md
   - FIRSTMILE.md

8. **File Structure & Organization** (lines 520-538)
   - Project tree
   - Shared code location
   - Naming conventions

9. **Explicit "DO NOT" List** (lines 540-542)
   - 14 prohibited practices with explanations

10. **Excel Reporting Standards** (lines 544-739)
    - 9-tab structure (mandatory order)
    - FirstMile brand colors
    - Header/data cell styling
    - SLA calculation rules
    - Hub mapping
    - Filename convention
    - Quality validation checklist
    - Prohibited practices

11. **Additional Quality Standards** (lines 741-767)
    - Markdown formatting
    - Logging standards
    - Error handling
    - Performance optimization

12. **Common Mistakes & Corrections** (lines 770-1250)
    - **Mistake 1**: Skipping context loading in syncs
    - **Mistake 2**: Direct HubSpot API calls (bypassing rate limiter)
    - **Mistake 3**: Updating deal stage without folder verification
    - **Mistake 4**: Auto-creating HubSpot records without approval
    - **Mistake 5**: Hardcoding API keys
    - **Mistake 6**: Leading reports with daily delivery %
    - **Mistake 7**: Marking sync complete without learnings
    - **Mistake 8**: Creating new scripts instead of extending shared modules
    - **Mistake 9**: Skipping zone distribution in analysis
    - **Mistake 10**: Using carrier names in reports

13. **Version & Changelog** (lines 1253-1276)
    - System version
    - Last updated date
    - Changelog with future versions planned

---

## 🎓 Agent Skill Files

### Brand Scout Skill (550 lines)
**Location**: `.claude/skills/brand_scout_skill.md`

**Contents**:
- 3-phase execution workflow (Planning, Collection, Reporting)
- Output template with confidence scoring
- Strict compliance rules (✅ MUST DO / ❌ NEVER DO)
- Quality gates checklist
- Human approval workflow
- Research source priorities
- Error handling patterns
- Performance metrics

---

### Prioritization Skill (630 lines)
**Location**: `.claude/skills/prioritization_skill.md`

**Contents**:
- 4-phase execution workflow (Context, HubSpot Fetch, Scoring, Report)
- Priority score formula with stage weights
- Output template with yesterday's context reference
- Context continuity validation
- HubSpot API efficiency patterns
- Priority score tuning guidance
- Error handling (missing context, API failures)
- Integration with other agents

---

### Analysis Skill (580 lines)
**Location**: `.claude/skills/analysis_skill.md`

**Contents**:
- 4-phase execution workflow (Validation, Analysis, Opportunity ID, Reporting)
- 9 analysis components with code examples:
  1. Volume Profile
  2. Carrier Mix
  3. Expanded Weight Distribution
  4. Zone Distribution
  5. Geographic Distribution with Hub Mapping
  6-9. (Additional components)
- FIRSTMILE.md compliance requirements
- Excel report generation (9-tab structure)
- Styling requirements and brand standards
- Quality gates and error handling

---

## 🔍 Rules Compliance Validator

**Location**: `utils/rules_compliance_validator.py` (760 lines)

**Purpose**: Automated enforcement of rules.md quality gates

### Available Validations

1. **`validate_sync_operation()`**
   - Validates 9AM, noon, 3PM, EOD, weekly syncs
   - Checks context loading, HubSpot fresh data, learnings captured
   - Returns compliance report with score

2. **`validate_hubspot_operation()`**
   - Validates HubSpot API calls
   - Checks shared manager usage, credentials, rate limiter
   - Verifies folder consistency for stage updates

3. **`validate_brand_scout_operation()`**
   - Validates brand scout research
   - Checks human approval, confidence scores, source documentation
   - Prevents business-hours execution

4. **`validate_analysis_operation()`**
   - Validates PLD analysis and reports
   - Checks FIRSTMILE.md compliance, SLA leading, network terminology
   - Prohibits carrier name mentions

5. **`validate_excel_report()`**
   - Validates Excel report compliance
   - Checks 9-tab structure, FirstMile blue headers, SLA tab position
   - Verifies conditional formatting and filename convention

6. **`validate_folder_operation()`**
   - Validates folder moves, creates, archives
   - Checks user approval and HubSpot sync verification

7. **`validate_learning_capture()`**
   - Validates learning loop compliance
   - Checks insights documented, memory updated, next actions identified

### Compliance Scoring

- **Score Range**: 0-100
- **PASS**: ≥90% compliance
- **WARNING**: 70-89% compliance
- **FAIL**: <70% compliance

**Violation Weights**:
- Critical violations: -30 to -35 points
- Major violations: -20 to -25 points
- Minor violations: -10 to -15 points
- Warnings: -5 to -10 points

### Convenience Functions

```python
# Quick validators for common operations
validate_9am_sync(context_loaded, previous_eod_path, hubspot_fresh)
validate_eod_sync(context_loaded, learnings_captured, hubspot_fresh)
validate_hubspot_call(uses_shared_manager, credentials_validated)
```

---

## 💡 Integration Example

**Location**: `examples/sync_with_compliance_validation.py` (320 lines)

**Demonstrates**:
- 9-phase sync execution with validation checkpoints
- Pre-flight compliance validation (before execution)
- Credential validation before HubSpot calls
- Post-execution compliance validation
- Compliance report generation and saving

**Phases**:
1. Context Loading
2. Pre-Flight Validation
3. Credential Validation
4. HubSpot Data Fetch
5. Priority Scoring
6. Report Generation
7. Output Saving
8. Post-Execution Validation
9. Final Status

---

## 🚀 How to Use

### 1. Load Rules at Session Start

```bash
# In Claude Code
/load @rules.md
```

### 2. Reference Agent Skills

```bash
# Load specific skill for context
/load @.claude/skills/brand_scout_skill.md
```

### 3. Integrate Validator in Sync Scripts

```python
from utils.rules_compliance_validator import RulesComplianceValidator

validator = RulesComplianceValidator()

# Validate before execution
report = validator.validate_sync_operation(
    sync_type='9am',
    context_loaded=True,
    hubspot_data_fresh=True,
    previous_sync_path='/path/to/eod.md',
    priorities_documented=True
)

validator.print_report(report)

if report['status'] == 'FAIL':
    print("Fix violations before continuing")
    sys.exit(1)
```

### 4. Run Example Integration

```bash
python examples/sync_with_compliance_validation.py
```

---

## 📊 Benefits

### For AI Agents
1. **Clear Behavioral Constraints**: Know exactly what's allowed/prohibited
2. **Context Preservation**: Rules enforce context continuity chain
3. **Quality Gates**: Automated validation prevents rule violations
4. **Learning Loop**: Mandatory capture-before-complete gates

### For Development
1. **Consistency**: All agents follow same standards
2. **Maintainability**: Single source of truth for rules
3. **Debugging**: Common Mistakes section shows anti-patterns
4. **Automation**: Validator enforces rules automatically

### For Operations
1. **Audit Trail**: Compliance reports for every operation
2. **Quality Assurance**: >90% compliance required to pass
3. **Learning**: Changelog tracks rule evolution
4. **Onboarding**: New team members learn from rules.md

---

## 🔄 Maintenance

### When to Update Rules.md

1. **AI Makes Mistakes**: Add to Common Mistakes section
2. **New Patterns Discovered**: Update Agent Best Practices
3. **Workflow Changes**: Update Sync Flow Constraints
4. **Tool Changes**: Update tool references and integrations

### Versioning

Update `## Changelog` section in rules.md:
```markdown
### YYYY-MM-DD - Version Description
- Change 1
- Change 2
- Change 3
```

Increment version number in `## Version` section.

---

## 📖 Documentation Hierarchy

```
rules.md (Master Rules)
    ↓ references
.claude/skills/ (Agent Workflows)
    ↓ validates with
utils/rules_compliance_validator.py (Automated Enforcement)
    ↓ demonstrates in
examples/sync_with_compliance_validation.py (Integration Example)
```

---

## ✅ Completion Checklist

- [x] Created universal rules.md with agent-specific sections
- [x] Defined sync flow constraints and context continuity chain
- [x] Established HubSpot integration prohibitions
- [x] Added file operations policy
- [x] Created Excel reporting standards section
- [x] Added Common Mistakes section (10 examples)
- [x] Integrated versioning strategy with changelog
- [x] Created Brand Scout agent skill file
- [x] Created Prioritization agent skill file
- [x] Created Analysis agent skill file
- [x] Created rules_compliance_validator.py
- [x] Created integration example script
- [x] Created skills README.md

---

## 🎓 Next Steps

### Immediate
1. **Test validator in daily syncs**: Integrate into `daily_9am_sync.py`
2. **Collect violation data**: Run validator for 1 week, track common issues
3. **Refine scoring**: Adjust violation weights based on impact

### Short-Term (1-2 weeks)
1. **Expand Common Mistakes**: Add examples from real violations
2. **Create Sync Coordinator skill**: Complete agent skill set
3. **Create Learning Agent skill**: Document knowledge capture workflows

### Long-Term (1+ month)
1. **Automated compliance reporting**: Daily/weekly compliance dashboards
2. **Pattern recognition**: ML-based violation prediction
3. **Rule evolution tracking**: Measure rule effectiveness over time

---

## 📚 Related Documentation

- [rules.md](./rules.md) - Master rules file
- [.claude/skills/README.md](./.claude/skills/README.md) - Skills overview
- [.claude/DOCUMENTATION_INDEX.md](./.claude/DOCUMENTATION_INDEX.md) - Master navigation
- [CLAUDE.md](./CLAUDE.md) - Project context and workflows

---

**System**: The Nebuchadnezzar v3.0
**Framework**: SuperClaude (SLC methodology)
**Last Updated**: 2025-11-07
