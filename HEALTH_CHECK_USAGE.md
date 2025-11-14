# Repository Health Check - Usage Guide

## Quick Start

Run the health check anytime with a single command:

```bash
python repo_health_check.py
```

## Sample Output

```
🚀 Starting Nebuchadnezzar v3.0 Health Check...

🔍 Checking repository structure...
  ✅ .claude
  ✅ HubSpot
  ✅ BULK_RATE_PROCESSING
  ✅ XPARCEL_NATIONAL_SELECT
  ✅ .github/workflows

📋 Checking critical files...
  ✅ .gitignore
  ✅ .env.example
  ✅ CLAUDE.md
  ✅ requirements.txt
  ✅ .claude/README.md
  ✅ .claude/DOCUMENTATION_INDEX.md
  ✅ .claude/NEBUCHADNEZZAR_REFERENCE.md

🔒 Checking security...
  ✅ .env file properly excluded
  🔍 Scanning for hardcoded credentials...
  ✅ No hardcoded credentials detected

🐍 Checking Python syntax...
  ✅ config.py
  ✅ hubspot_config.py
  ✅ hubspot_utils.py
  ✅ date_utils.py
  ✅ daily_9am_sync.py
  ✅ noon_sync.py
  ✅ eod_sync.py
  ✅ pipeline_sync_verification.py

📦 Checking core module imports...
  ✅ config
  ✅ hubspot_config
  ✅ hubspot_utils
  ✅ date_utils

📚 Checking dependencies...
  📦 Found 9 dependencies
  ✅ pandas 2.3.3
  ✅ numpy 2.3.4
  ✅ openpyxl 3.1.5
  ✅ requests 2.31.0

📊 Gathering statistics...
  📝 Python files: 191
  📄 Markdown files: 514
  📁 Deal folders: 41
  💾 Repository size: 709M
  ✅ No uncommitted changes
  🔖 Last commit: 11127ae - Add comprehensive repository health check system

======================================================================
📊 NEBUCHADNEZZAR v3.0 HEALTH CHECK REPORT
======================================================================
Timestamp: 2025-11-07T19:38:06.262984
Status: HEALTHY

✅ Checks Passed:
  - Repository structure verified
  - Critical files verified
  - Security scan completed
  - Python syntax validated
  - Core modules import check completed
  - Dependencies checked

📊 Statistics:
  - Python Files: 191
  - Markdown Files: 514
  - Deal Folders: 41
  - Repo Size: 709M
  - Uncommitted Changes: 0
  - Last Commit: 11127ae - Add comprehensive repository health check system

🎯 Overall Health Score: 100/100 - EXCELLENT ✨
======================================================================

💾 Report saved to: HEALTH_CHECK_REPORT.json
```

## What's Included

### 1. Repository Health Check Script
**File:** `repo_health_check.py`

Comprehensive Python script that checks:
- ✅ Repository structure (critical directories)
- ✅ Critical files (configuration, documentation)
- ✅ Security (no credentials in repo)
- ✅ Python code quality (syntax validation)
- ✅ Module imports (core modules)
- ✅ Dependencies (installed packages)
- ✅ Statistics (file counts, repo size, git status)

### 2. Health Status Report
**File:** `REPOSITORY_HEALTH_STATUS.md`

Detailed markdown report with:
- Executive summary
- Complete check results
- System architecture overview
- Documentation status
- Recommendations
- Version information

### 3. Quick Reference Guide
**File:** `HEALTH_CHECK_QUICK_REFERENCE.md`

Quick reference with:
- One-command usage
- Output interpretation
- Health score meanings
- Troubleshooting guide
- Integration with workflows
- Manual verification commands

### 4. JSON Report
**File:** `HEALTH_CHECK_REPORT.json` (auto-generated)

Machine-readable report with:
```json
{
  "timestamp": "2025-11-07T19:38:06.262984",
  "status": "HEALTHY",
  "checks": [...],
  "warnings": [...],
  "errors": [...],
  "stats": {...}
}
```

## When to Use

### Daily
- Part of morning sync workflow
- Automated via GitHub Actions (9 AM UTC)

### Before Commits
- Verify code quality before pushing
- Ensure no security issues

### After Updates
- Check after dependency updates
- Verify after major changes

### Troubleshooting
- Diagnose repository issues
- Verify configuration

## Health Score Guide

| Score | Status | Action |
|-------|--------|--------|
| 100 | EXCELLENT ✨ | Keep up the great work! |
| 90 | GOOD ✅ | Review warnings if any |
| 75 | FAIR ⚠️ | Address warnings soon |
| 50 | NEEDS ATTENTION ❌ | Fix errors immediately |

## Current Status: EXCELLENT ✨

Your repository is in excellent health with a score of **100/100**:
- ✅ All critical systems operational
- ✅ No security issues
- ✅ All dependencies installed
- ✅ Code quality validated
- ✅ 191 Python files, 514 documentation files
- ✅ 41 active deal folders
- ✅ Comprehensive documentation

## Next Steps

1. **Bookmark this file** for quick reference
2. **Run health checks regularly** (already automated)
3. **Review reports** when issues arise
4. **Keep dependencies updated** (check monthly)

## Support

For issues or questions:
1. Review `HEALTH_CHECK_QUICK_REFERENCE.md`
2. Check `REPOSITORY_HEALTH_STATUS.md` for detailed info
3. Review `HEALTH_CHECK_REPORT.json` for technical details
4. Consult `.claude/README.md` for system documentation

---

**System:** Nebuchadnezzar v3.0  
**Version:** 1.0  
**Last Updated:** 2025-11-07
