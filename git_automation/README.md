# Git Automation - Nebuchadnezzar v3.0

Multi-agent Git orchestration system for FirstMile Deals pipeline.

## Overview

This package provides automated Git operations for the Nebuchadnezzar v3.0 Matrix Edition, enabling multi-agent (desktop, mobile, automation) collaboration with conflict prevention and automatic merge detection.

## Components

### 1. `commit_wrapper.py` - Git Commit Wrapper
Handles branch creation, commits, pushes, and merges with standardized message formatting.

**Key Features**:
- Automatic branch naming: `agent_type/deal_name_action`
- Standardized commit messages: `[AGENT] [DEAL] [ACTION]: description`
- Auto-merge safety detection (no deletions, <3 files, no scripts/config)
- One-shot `quick_commit()` function for simple operations

**Usage**:
```bash
# Create branch, commit, and push
python commit_wrapper.py "Caputron" automation pld_analysis "Completed overnight analysis"

# Returns: branch name, commit hash, auto-merge eligibility
```

**Python API**:
```python
from git_automation.commit_wrapper import GitCommitWrapper, quick_commit

# Quick one-shot commit
result = quick_commit(
    deal_name="Caputron",
    agent_type="automation",
    action="pld_analysis",
    description="Analysis completed with 42% savings"
)

# Or use the full wrapper
wrapper = GitCommitWrapper()
branch = wrapper.create_branch("automation", "Caputron", "analysis")
wrapper.commit_changes("Caputron", "automation", "analysis", "Details here")
wrapper.push_branch(branch)

# Check if auto-mergeable
if wrapper.is_auto_mergeable(branch):
    wrapper.merge_to_main(branch, auto_merge=True)
```

### 2. `branch_manager.py` - Branch Lifecycle Manager
Manages agent locks, branch cleanup, and conflict prevention.

**Key Features**:
- Exclusive deal locks (prevents simultaneous edits)
- Automatic lock expiration (default 30 minutes)
- Active branch listing and filtering
- Stale branch cleanup (>30 days merged)
- Lock status monitoring

**Usage**:
```bash
# Acquire lock for a deal
python branch_manager.py acquire "Caputron" automation 60

# Release lock
python branch_manager.py release "Caputron"

# List active branches
python branch_manager.py list

# Clean up old branches
python branch_manager.py cleanup 30

# Show lock status
python branch_manager.py locks
```

**Python API**:
```python
from git_automation.branch_manager import BranchManager

manager = BranchManager()

# Try to acquire lock
lock_result = manager.acquire_lock("Caputron", "automation", timeout_minutes=60)
if lock_result['success']:
    # Perform work
    ...
    # Release lock
    manager.release_lock("Caputron")
else:
    print(f"Deal locked by: {lock_result['locked_by']}")

# Get all active branches
branches = manager.get_active_branches()

# Cleanup old merged branches
deleted = manager.cleanup_stale_branches(days_old=30)
```

## Git Hooks

### Pre-Commit Hook (`.git/hooks/pre-commit`)
Validates commits before they're created:
- ✅ Scans for exposed secrets (API keys, tokens, passwords)
- ✅ Validates folder naming convention (`[##-STAGE]_Company_Name/`)
- ✅ Prevents `.env` file from being committed

### Post-Commit Hook (`.git/hooks/post-commit`)
Logs commits and updates tracking:
- Appends commit info to `_DAILY_LOG.md`
- Updates last commit timestamp

## Agent Types

- **automation**: Overnight scripts, N8N workflows, batch operations
- **mobile**: Quick notes, approvals, lightweight changes from phone
- **desktop**: Complex work, proposals, detailed analysis
- **sync**: Synchronization operations, scheduled tasks

## Branch Naming Convention

Format: `agent_type/deal_name_action`

Examples:
- `automation/caputron_pld_analysis`
- `mobile/otw_quick_note`
- `desktop/stackd_proposal`
- `sync/eod_sync_20251023`

## Commit Message Format

Format: `[AGENT_TYPE] [DEAL_NAME] [ACTION]: Description`

Examples:
- `[AUTOMATION] [Caputron] [PLD_ANALYSIS]: Completed overnight analysis, 42% savings identified`
- `[MOBILE] [OTW] [QUICK_NOTE]: Added pricing notes from call with CFO`
- `[DESKTOP] [Stackd] [PROPOSAL]: Final proposal v1 with 40% savings target`

## Auto-Merge Criteria

A branch qualifies for automatic merge if ALL of the following are true:
- ✅ No file deletions (only additions/modifications)
- ✅ Changes affect 3 or fewer files
- ✅ No Python scripts (`.py`) modified
- ✅ No configuration files (`.json`, `.yml`, `.yaml`, `.env`) modified
- ✅ Simple text additions (markdown, txt, csv, xlsx)

## Lock System

### Why Locks?
Prevents multiple agents from editing the same deal simultaneously, avoiding Git conflicts.

### Lock Lifecycle
1. Agent acquires lock before starting work (30 min timeout)
2. Lock file created: `.git/agent_locks/DealName.lock`
3. Agent performs work (branch, commit, push)
4. Agent releases lock when done
5. Expired locks auto-removed on next acquire attempt

### Lock File Format
```json
{
  "deal_name": "Caputron",
  "agent_type": "automation",
  "locked_at": "2025-10-23T22:30:00",
  "expires_at": "2025-10-23T23:00:00",
  "pid": 12345
}
```

## N8N Integration

See `N8N_INTEGRATION_GUIDE.md` for complete N8N workflow setup.

**Quick Summary**:
- N8N watches for folder movements
- Triggers Python `commit_wrapper.py` on change
- Creates Git commit automatically
- Updates HubSpot deal stage
- Logs action to `_DAILY_LOG.md`

## Testing

### Manual Test Workflow
```bash
# 1. Acquire lock
python git_automation/branch_manager.py acquire "Test_Company" automation 30

# 2. Create commit
python git_automation/commit_wrapper.py "Test_Company" automation test "Testing automation"

# 3. Check results
git branch | grep automation
git log --oneline -1

# 4. Release lock
python git_automation/branch_manager.py release "Test_Company"

# 5. Verify auto-merge eligibility
# (Check branch was created and is ready for review)
```

### Automated Test Suite
```bash
# Run unit tests (when implemented)
python -m pytest git_automation/tests/

# Integration tests with real Git operations
python git_automation/tests/integration_test.py
```

## Troubleshooting

### Issue: "Lock already acquired"
```bash
# Check lock status
python git_automation/branch_manager.py locks

# Force release if needed (use carefully)
python git_automation/branch_manager.py release "DealName"
```

### Issue: "Pre-commit hook failed - secrets detected"
- Review the file that triggered the error
- Remove any hardcoded API keys, tokens, or passwords
- Use `.env` file for sensitive data
- Add sensitive files to `.gitignore`

### Issue: "Branch not auto-mergeable"
This is expected for complex changes. Branches requiring manual review will be flagged. Review them via:
- GitHub web interface
- Mobile review dashboard
- Desktop Git client

### Issue: "Python command not found in N8N"
- Set Python path in N8N settings
- Use full path: `C:\Python\python.exe`
- Or add Python to system PATH

## Security

### Protected Data
- `.env` file (pre-commit hook blocks this)
- API keys (pattern matching in pre-commit)
- Passwords (pattern matching in pre-commit)
- Tokens (pattern matching in pre-commit)

### Secret Patterns Detected
- `api_key = "xxx"`
- `password = "xxx"`
- `secret = "xxx"`
- `token = "xxx"`
- `ghp_` (GitHub PAT)
- `pat-na1-` (HubSpot API key)

## Configuration

### Environment Variables
Set in `.env` file:
```env
FIRSTMILE_DEALS_PATH=C:\Users\BrettWalker\FirstMile_Deals
GITHUB_PAT=ghp_your_token_here
AUTO_MERGE_ENABLED=true
CONFLICT_STRATEGY=prefer_manual
```

### Git Configuration
```bash
# Verify Git hooks path
git config core.hooksPath

# Set if needed
git config core.hooksPath .git/hooks
```

## Performance

### Typical Operation Times
- Lock acquisition: <50ms
- Branch creation: <500ms
- Commit creation: <200ms
- Push to GitHub: 1-3s (network dependent)
- Auto-merge check: <100ms
- Merge to main: 1-2s

### Resource Usage
- Disk: ~1KB per lock file
- Memory: <10MB per Python process
- Network: 100-500KB per push (file count dependent)

## Future Enhancements

- [ ] AI-powered commit message generation
- [ ] Predictive branch creation
- [ ] Advanced conflict resolution
- [ ] Multi-user support
- [ ] Real-time collaboration
- [ ] Analytics dashboard

## Support

**Documentation**: See `.claude/` folder for complete system docs
**Issues**: Create GitHub issue with error logs
**Questions**: Review `N8N_INTEGRATION_GUIDE.md` for workflow setup

**Version**: 3.0.0
**Last Updated**: October 23, 2025
**License**: Proprietary (FirstMile Internal)
