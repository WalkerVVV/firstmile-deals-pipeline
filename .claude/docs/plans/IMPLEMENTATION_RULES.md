# Implementation Rules & Execution Guidelines

**Purpose**: Operational rules for implementing the Action-First Sync + Automated Continuity system in the FirstMile Deals repository.

**Last Updated**: 2025-11-14

---

## Critical Rules - NEVER Violate

### 1. NO MOCK DATA, EVER
**Rule**: Never create placeholder, mock, or fake data in any component.

**Why**: Mock data causes false success reporting ("✅ SUPERHUMAN SYNCED" when no actual sync happened).

**Enforcement**:
- If a data source is unavailable, return `success: False` with clear error message
- If a system can't complete its work, report honestly: "Cannot complete this operation"
- Test with REAL data only - never fake responses for testing convenience

**Examples**:
```python
# ❌ WRONG - Mock data
def get_emails():
    return {
        "success": True,
        "emails": ["fake@example.com"]  # NO!
    }

# ✅ CORRECT - Honest failure
def get_emails():
    if not email_service_available():
        return {
            "success": False,
            "error": "Email service unavailable",
            "emails": []
        }
```

---

### 2. READ BEFORE WRITE/EDIT
**Rule**: Always use Read tool before Write or Edit operations on existing files.

**Why**: Prevents overwriting code without understanding current state.

**Enforcement**:
- Read file completely before proposing changes
- Understand context and existing patterns
- Verify changes don't break existing functionality

**Examples**:
```python
# ✅ CORRECT - Read first
1. Read unified_sync.py
2. Understand existing structure
3. Edit specific function
4. Validate changes maintain existing behavior
```

---

### 3. USE ABSOLUTE PATHS ONLY
**Rule**: All file paths must be absolute, never relative.

**Why**: Prevents path traversal issues and ensures code works from any directory.

**Enforcement**:
```python
# ❌ WRONG - Relative path
file_path = "sync_reports/report.md"

# ✅ CORRECT - Absolute path
PROJECT_ROOT = Path("C:/Users/BrettWalker/FirstMile_Deals")
file_path = PROJECT_ROOT / "sync_reports" / "report.md"
```

---

### 4. UTF-8 ENCODING EVERYWHERE
**Rule**: All Python scripts that output text must use UTF-8 encoding wrapper for Windows console emoji support.

**Why**: Windows console defaults to cp1252, which can't handle emojis used in reports.

**Enforcement**:
```python
# Add to EVERY script that prints emojis or unicode
import sys
import io

# Fix Windows console encoding for emoji support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Subprocess calls must also use UTF-8**:
```python
# ✅ CORRECT
result = subprocess.run(
    ['python', 'script.py'],
    capture_output=True,
    encoding='utf-8'  # NOT text=True
)
```

---

### 5. PRESERVE EXISTING WORKING SOLUTIONS
**Rule**: Don't rewrite working systems. Review existing code before creating new solutions.

**Why**: "We can't keep creating a new process every freaking day. It has to be the same over and over and over" - User feedback.

**Enforcement**:
1. Check git history for related commits
2. Read existing documentation in `.claude/`
3. Search codebase for similar functionality
4. Only create new solution if none exists
5. If working solution exists, use it

**Examples**:
- Email integration: Working solution existed in commit 42e3316, don't recreate
- Sync workflow: unified_sync.py works, enhance it, don't replace it
- HubSpot API: Shared functions in hubspot_sync_core.py, use them

---

### 6. VALIDATE BEFORE EXECUTION
**Rule**: All operations must validate inputs, check prerequisites, and verify conditions before execution.

**Why**: Prevents cascading failures and provides early error detection.

**Enforcement**:
```python
# ✅ CORRECT - Validate first
def update_daily_log(sync_type: str, data: dict):
    # Validate inputs
    if sync_type not in ['9am', 'noon', '3pm', 'eod']:
        raise ValueError(f"Invalid sync type: {sync_type}")

    if not data:
        raise ValueError("Sync data cannot be empty")

    # Check prerequisites
    if not self.daily_log.exists():
        self._create_from_template()

    # Verify conditions
    if sync_type != '9am':
        is_valid, error = self.validate_previous_sync(sync_type)
        if not is_valid:
            print(f"⚠️ CONTINUITY WARNING: {error}")

    # Then proceed with operation
    content = self.daily_log.read_text(encoding='utf-8')
    # ... update logic
```

---

### 7. NEVER AUTO-COMMIT WITHOUT PERMISSION
**Rule**: Only commit to git when explicitly designed to do so (EOD sync auto-commit) or user requests.

**Why**: Prevents unwanted changes being committed automatically.

**Enforcement**:
- EOD sync auto-commit: Explicitly approved in this plan
- All other commits: Manual only, never automatic
- Always show user what will be committed before pushing

---

### 8. DIVISION BY ZERO PROTECTION
**Rule**: All calculations that divide must check for zero denominators.

**Why**: Common source of crashes in analytics and reporting code.

**Enforcement**:
```python
# ❌ WRONG
success_rate = completed / total * 100

# ✅ CORRECT
success_rate = (completed / total * 100) if total > 0 else 0
```

---

## Implementation Best Practices

### Code Organization

**File Structure Rules**:
- **Utilities**: Place reusable components in `utils/` directory
- **Templates**: Place templates in `.claude/templates/` directory
- **Documentation**: Place docs in `.claude/docs/` directory
- **Tests**: Place tests in `tests/` directory (create if doesn't exist)
- **Scripts**: Main scripts in project root

**Module Design**:
- One class per file (with related helper functions)
- Clear separation of concerns
- Minimal dependencies between modules
- All imports at top of file

---

### Error Handling Patterns

**Non-Critical Errors** (warn but continue):
```python
try:
    result = non_critical_operation()
except Exception as e:
    print(f"⚠️ Non-critical error (continuing): {e}")
    result = default_fallback()
```

**Critical Errors** (fail fast):
```python
try:
    result = critical_operation()
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    raise  # Re-raise to stop execution
```

**Validation Errors** (clear messaging):
```python
if not valid:
    error_msg = f"Validation failed: {specific_reason}"
    print(f"❌ {error_msg}")
    return False, error_msg
```

---

### Testing Requirements

**Before Committing Code**:
1. Test with real data (no mocks)
2. Test error conditions (network failure, missing data, etc.)
3. Verify UTF-8 encoding works (test emojis print correctly)
4. Check file paths are absolute
5. Validate division operations have zero checks

**Manual Testing Steps**:
```bash
# Test component in isolation
python utils/action_prioritizer.py

# Test integration
python unified_sync.py 9am

# Test full day cycle
python unified_sync.py 9am
python unified_sync.py noon
python unified_sync.py 3pm
python unified_sync.py eod

# Verify git commit
git log -1
git show HEAD
```

---

### Git Workflow

**Branch Strategy**:
- Implement on feature branch (optional but recommended)
- Test thoroughly on branch before merging to main
- Commit frequently with descriptive messages

**Commit Message Format**:
```
<type>: <short summary>

<detailed description if needed>

<reference to issue/plan if applicable>
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring
- `docs:` - Documentation changes
- `test:` - Test additions/modifications

**Example**:
```
feat: implement action-first sync reports

- Add ActionPrioritizer for intelligent ranking
- Add ContinuityManager for daily log validation
- Add GitSyncManager for EOD auto-commit
- Integrate all components into unified_sync.py

Implements plan from .claude/docs/plans/action_first_sync_implementation.md
```

---

## Code Quality Standards

### Python Style

**Follow PEP 8** with these specifics:
- Indentation: 4 spaces (no tabs)
- Line length: 100 characters max
- Docstrings: Google style for all functions and classes
- Type hints: Use for function signatures

**Example**:
```python
def prioritize_actions(self,
                      hubspot_deals: List[Dict[str, Any]],
                      emails: Dict[str, List[str]],
                      sync_type: str) -> List[Action]:
    """
    Generate prioritized action list from deals and emails.

    Args:
        hubspot_deals: List of active deals from HubSpot API
        emails: Dict with 'critical', 'yesterday', 'last_week' keys
        sync_type: '9am', 'noon', '3pm', 'eod'

    Returns:
        Top 3 actions sorted by priority score
    """
    # Implementation
```

---

### Documentation Standards

**Every File Needs**:
- File-level docstring explaining purpose
- Function docstrings with Args/Returns/Raises
- Inline comments for complex logic
- Examples for public APIs

**Example File Header**:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action prioritization engine for FirstMile sync system.

This module provides intelligent scoring and ranking of actions
from HubSpot deals and Superhuman emails to determine top 3
priorities for each sync cycle.

Author: Claude Code
Created: 2025-11-14
"""
```

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Issue: UTF-8 Encoding Error
**Symptom**: `'charmap' codec can't encode character`

**Solution**:
```python
# Add to script
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Fix subprocess calls
subprocess.run([...], encoding='utf-8')  # NOT text=True
```

---

#### Issue: Import Error
**Symptom**: `ModuleNotFoundError: No module named 'utils.action_prioritizer'`

**Solution**:
1. Verify file exists: `ls utils/action_prioritizer.py`
2. Verify `__init__.py` exists: `ls utils/__init__.py` (create if missing)
3. Check PYTHONPATH includes project root
4. Run from project root: `cd C:/Users/BrettWalker/FirstMile_Deals`

---

#### Issue: Git Commit Fails
**Symptom**: `fatal: not a git repository` or merge conflict

**Solution**:
```bash
# Verify git repo
git status

# If merge conflict
git pull
# Resolve conflicts manually
git add .
git commit -m "message"
git push

# If not git repo (shouldn't happen)
cd C:/Users/BrettWalker/FirstMile_Deals
git status
```

---

#### Issue: HubSpot API Rate Limit
**Symptom**: `429 Too Many Requests`

**Solution**:
1. Check rate limits: 100 calls per 10 seconds, 150K per 24 hours
2. Add delay between calls if batching
3. Use exponential backoff for retries
4. Cache results when possible

---

#### Issue: Continuity Validation Failure
**Symptom**: `⚠️ CONTINUITY WARNING: Missing 9AM priorities for today`

**Solution**:
1. Check if previous sync actually ran: `ls sync_reports/`
2. Check if _DAILY_LOG.md was updated: `cat _DAILY_LOG.md`
3. If missing, manually run previous sync type
4. Or set `warn_only: true` in config to continue with warning

---

## Rollback Procedures

### Quick Rollback (If Implementation Fails)

**Steps**:
```bash
# 1. Restore original unified_sync.py
git checkout HEAD~1 unified_sync.py

# 2. Remove new utility files
rm utils/action_prioritizer.py
rm utils/continuity_manager.py
rm utils/git_sync_manager.py

# 3. Remove new templates
rm -r .claude/templates/

# 4. Restore original _DAILY_LOG.md format
git checkout HEAD~1 _DAILY_LOG.md

# 5. Verify original system works
python unified_sync.py 9am
```

**Data Safety**: All sync reports preserved in `sync_reports/` and on GitHub.

---

### Partial Rollback (Keep Some Components)

**Scenario**: Action prioritization works, but continuity manager doesn't.

**Steps**:
1. Keep `utils/action_prioritizer.py`
2. Remove `utils/continuity_manager.py`
3. Modify `unified_sync.py` to use only action prioritizer
4. Test modified version

---

## Safety Checks Before Each Phase

### Pre-Phase Checklist

**Before Starting Any Implementation Phase**:
- [ ] Current system is working (run test sync)
- [ ] Latest code is committed to git
- [ ] GitHub repo is up to date (`git push`)
- [ ] Have backup of critical files
- [ ] Understand what phase will modify
- [ ] Read existing code that will be changed

**Example Pre-Phase Safety Check**:
```bash
# 1. Verify current system works
python unified_sync.py 9am
# Should complete without errors

# 2. Commit current state
git status
git add .
git commit -m "Pre-implementation checkpoint"
git push

# 3. Verify backup
git log -1
# Should show recent commit

# 4. Proceed with phase
# Now safe to start implementation
```

---

## Success Validation

### After Each Phase

**Checklist**:
- [ ] New files created have correct structure
- [ ] No syntax errors (run `python -m py_compile file.py`)
- [ ] UTF-8 encoding wrapper present in all scripts
- [ ] Absolute paths used for all file operations
- [ ] Division operations have zero checks
- [ ] Error handling implemented
- [ ] Docstrings present
- [ ] Manual testing completed
- [ ] Changes committed to git

**Example Validation**:
```bash
# 1. Syntax check
python -m py_compile utils/action_prioritizer.py

# 2. Import check
python -c "from utils.action_prioritizer import ActionPrioritizer"

# 3. Basic functionality test
python -c "
from utils.action_prioritizer import ActionPrioritizer
ap = ActionPrioritizer()
print('ActionPrioritizer initialized successfully')
"

# 4. Commit if all checks pass
git add utils/action_prioritizer.py
git commit -m "feat: add action prioritization engine"
```

---

## Communication Guidelines

### Progress Reporting

**After Each Phase Completes**:
1. Report what was completed
2. Report any issues encountered
3. Report any deviations from plan
4. Report actual time vs. estimated time
5. Ask for validation before proceeding

**Example Progress Report**:
```
✅ Phase 1 Complete: Template Creation

Completed:
- Created DAILY_LOG_TEMPLATE.md (267 lines)
- Created SYNC_REPORT_TEMPLATE.md (145 lines)
- Created ACTION_PRIORITY_CONFIG.yaml (35 lines)

Issues: None

Deviations: Added extra section to daily log template for "Blocked Items"

Time: 45 minutes (estimated 1 hour)

Ready to proceed to Phase 2?
```

---

### Error Reporting

**When Errors Occur**:
1. Clearly state what failed
2. Provide full error message/traceback
3. Explain what was being attempted
4. Propose solution or ask for guidance
5. Never hide errors or "fix" silently

**Example Error Report**:
```
❌ Phase 2 Error: Import Failure

Error Message:
ModuleNotFoundError: No module named 'yaml'

Context:
- Attempting to import PyYAML in action_prioritizer.py
- Need PyYAML to load ACTION_PRIORITY_CONFIG.yaml

Root Cause:
PyYAML not installed in environment

Proposed Solution:
Install PyYAML: pip install pyyaml

Requires approval to proceed with installation.
```

---

## Final Checklist

### Before Marking Implementation Complete

- [ ] All 5 phases completed successfully
- [ ] Full day test passed (9AM, NOON, 3PM, EOD)
- [ ] Git auto-commit works (verified on GitHub)
- [ ] _DAILY_LOG.md updates correctly
- [ ] Action prioritization produces sensible rankings
- [ ] Continuity validation catches gaps
- [ ] No breaking changes to existing functionality
- [ ] All documentation updated
- [ ] CLAUDE.md updated with new system
- [ ] User validated system works as expected

---

## References

**Related Documents**:
- Implementation Plan: `.claude/docs/plans/action_first_sync_implementation.md`
- System Overview: `.claude/README.md`
- Project Instructions: `CLAUDE.md` (project root)
- Global Framework: `~/.claude/FIRSTMILE.md`

**Key Files**:
- Main Script: `unified_sync.py`
- Daily Log: `_DAILY_LOG.md`
- Sync Reports: `sync_reports/`
- Email Cache: `superhuman_emails.json`

**Git History**:
- Email Integration: Commit 42e3316
- Unified Sync System: Commit 755157f
- File Location Fix: 2025-11-14

---

**Implementation Rules Version**: 1.0
**Last Updated**: 2025-11-14
**Status**: Active - Use These Rules During Implementation
