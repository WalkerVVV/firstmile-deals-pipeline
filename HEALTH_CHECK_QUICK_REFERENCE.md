# Repository Health Check - Quick Reference

## One-Command Health Check
```bash
python repo_health_check.py
```

## What Gets Checked

### 🔍 Structure
- Critical directories (`.claude`, `HubSpot`, etc.)
- Deal folder organization
- GitHub workflows

### 📋 Files
- Configuration files
- Documentation
- Requirements

### 🔒 Security
- `.env` file excluded
- No hardcoded credentials
- Proper secret management

### 🐍 Code Quality
- Python syntax validation
- Module imports
- Dependencies

### 📊 Statistics
- File counts
- Repository size
- Git status
- Deal metrics

## Output

### Console Output
Real-time health check progress with color-coded results:
- ✅ Green checks: Passing
- ⚠️  Yellow warnings: Needs attention
- ❌ Red errors: Critical issues

### JSON Report
Detailed report saved to `HEALTH_CHECK_REPORT.json`:
```json
{
  "timestamp": "...",
  "status": "HEALTHY|UNHEALTHY",
  "checks": [...],
  "warnings": [...],
  "errors": [...],
  "stats": {...}
}
```

### Markdown Report
Human-readable status in `REPOSITORY_HEALTH_STATUS.md`

## Health Score Interpretation

| Score | Status | Meaning |
|-------|--------|---------|
| 100 | EXCELLENT ✨ | No errors, no warnings |
| 90 | GOOD ✅ | No errors, ≤3 warnings |
| 75 | FAIR ⚠️ | No errors, >3 warnings |
| 50 | NEEDS ATTENTION ❌ | Has errors |

## Automated Health Checks

### GitHub Actions
- **Schedule:** Daily at 9 AM UTC (3 AM CT)
- **Trigger:** Push to main, Pull requests
- **Manual:** Workflow dispatch

### Workflow File
`.github/workflows/health-check.yml`

## Common Issues & Solutions

### ⚠️ Missing .env file
**Expected in CI/CD environment**
- Local: Copy `.env.example` to `.env` and configure
- CI/CD: Set environment variables in GitHub Secrets

### ⚠️ Import warnings
**Usually configuration-related**
- Check `.env` file exists locally
- Verify all required environment variables set

### ❌ Missing directories
**Critical issue**
- Verify repository clone is complete
- Check `.gitignore` isn't excluding critical directories

### ❌ Syntax errors
**Critical issue**
- Run Python syntax check: `python -m py_compile <file>.py`
- Fix syntax before committing

## Integration with Daily Workflows

### Morning Sync (9 AM)
```bash
python daily_9am_sync.py
```
Includes integrated health status check

### Noon Sync
```bash
python noon_sync.py
```
Quick progress and health check

### EOD Sync
```bash
python eod_sync.py
```
End-of-day summary with health metrics

## Manual Verification Commands

### Python Syntax
```bash
# Check single file
python -m py_compile filename.py

# Check multiple files
for f in *.py; do python -m py_compile "$f"; done
```

### Dependencies
```bash
# Install/update dependencies
pip install -r requirements.txt

# List installed packages
pip list
```

### Git Status
```bash
# Repository status
git status

# Recent commits
git log --oneline -10

# Branch information
git branch -a
```

### Repository Stats
```bash
# File counts
find . -name "*.py" | wc -l
find . -name "*.md" | wc -l

# Repository size
du -sh .

# Deal folders
find . -maxdepth 1 -type d -name "[0-9][0-9]-*"
```

## Maintenance Schedule

### Daily
- Automated health check via GitHub Actions
- Morning sync includes health status

### Weekly
- Review health check reports
- Address any warnings

### Monthly
- Full codebase review
- Update documentation
- Dependency updates

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - All checks passed |
| 1 | Failure - Critical errors found |

## Quick Troubleshooting

### Health check won't run
1. Verify Python installation: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check file permissions: `ls -la repo_health_check.py`

### Unexpected failures
1. Read error messages carefully
2. Check recent changes: `git diff`
3. Review `HEALTH_CHECK_REPORT.json` for details

### False positives
Review the specific line mentioned - health check may flag:
- Comments containing sensitive keywords
- Regex patterns for validation
- Example code in documentation

---

**Last Updated:** 2025-11-07  
**System:** Nebuchadnezzar v3.0  
**Version:** 1.0
