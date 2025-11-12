# Security & Credentials Management Guide

## 🚨 CRITICAL: Never Hardcode Credentials

**NEVER** put API keys, tokens, or passwords directly in code files.

## Proper Credential Storage

### 1. Environment Variables (Preferred Method)

Store credentials in `.env` file (already in `.gitignore`):

```bash
# .env file (NEVER commit this)
HUBSPOT_API_KEY=your-token-here
GITHUB_TOKEN=your-github-token
```

### 2. Python Script Pattern (Secure)

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment (no fallback to hardcoded value)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    raise ValueError("HUBSPOT_API_KEY not found in environment variables")

# Use the API key
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

### 3. BAD PATTERN (Never Do This)

```python
# ❌ NEVER DO THIS - Hardcoded token
API_KEY = "pat-na1-1234567890abcdef"

# ❌ NEVER DO THIS - Fallback to hardcoded
API_KEY = os.environ.get('HUBSPOT_API_KEY', 'pat-na1-hardcoded-token')
```

## Security Checklist

### Before Committing Code

- [ ] No `pat-na1-` strings in any code files
- [ ] No `ghp_` strings (GitHub tokens) in any code files
- [ ] All credentials loaded from environment variables
- [ ] `.env` file listed in `.gitignore`
- [ ] Run security scan: `grep -r "pat-na1-" . --include="*.py"`

### Git Repository Security

```bash
# Check .gitignore includes sensitive files
cat .gitignore | grep -E "^\.env$|^config\.py$"

# Verify no credentials in staged files
git diff --cached | grep -E "pat-na1-|ghp_"

# Search all tracked files for credentials
git ls-files | xargs grep -l "pat-na1-" 2>/dev/null
```

### Emergency: Credentials Exposed in Git History

If credentials were committed to git:

1. **Immediately revoke the exposed token** in HubSpot/GitHub
2. **Generate new credentials**
3. **Clean git history** (complex - see Git documentation)
4. **Force push** (if private repo and safe to do)

## Recommended Tools

### Python dotenv Package

```bash
pip install python-dotenv
```

Usage in scripts:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file into environment
API_KEY = os.environ.get('HUBSPOT_API_KEY')
```

### Environment Variable Verification Script

Create `verify_credentials.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    'HUBSPOT_API_KEY',
    'GITHUB_TOKEN',
]

print("Credential Check:")
for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var}: {'*' * 20}{value[-8:]}")
    else:
        print(f"❌ {var}: NOT SET")
```

## Current .env File Structure

```bash
# Nebuchadnezzar v3.0 - System Credentials
# ⚠️ NEVER COMMIT THIS FILE TO GIT - Already in .gitignore

# HubSpot Private App Token
HUBSPOT_API_KEY=pat-na1-YOUR-TOKEN-HERE

# GitHub Personal Access Token
GITHUB_TOKEN=ghp_YOUR-TOKEN-HERE

# GitHub Repository Information
GITHUB_USERNAME=WalkerVVV
GITHUB_REPO=firstmile-deals-pipeline
GITHUB_REPO_URL=https://github.com/WalkerVVV/firstmile-deals-pipeline

# System Configuration
SYSTEM_NAME=Nebuchadnezzar_v3.0
BACKUP_LOCATION=C:\\Users\\BrettWalker\\Desktop\\NEBUCHADNEZZAR_BACKUPS
LOCAL_REPO=C:\\Users\\BrettWalker\\FirstMile_Deals
```

## GitHub Secrets (For Actions/Workflows)

For automated workflows:

1. Go to GitHub repo → Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `HUBSPOT_API_KEY`
   - Other sensitive values

Access in GitHub Actions:

```yaml
- name: Run sync
  env:
    HUBSPOT_API_KEY: ${{ secrets.HUBSPOT_API_KEY }}
  run: python daily_9am_sync.py
```

## Best Practices Summary

1. **Use `.env` file** for local development (never commit)
2. **Use environment variables** in all scripts (no fallbacks)
3. **Use GitHub Secrets** for automated workflows
4. **Audit regularly** for exposed credentials
5. **Rotate tokens** periodically (every 90 days)
6. **Minimal permissions** - only grant scopes actually needed
7. **Separate tokens** for dev vs production if possible

## Audit Commands

```bash
# Find all hardcoded tokens in Python files
grep -r "pat-na1-" . --include="*.py" | grep -v ".git/"

# Find all hardcoded GitHub tokens
grep -r "ghp_" . --include="*.py" --include="*.sh" | grep -v ".git/"

# Check what's being tracked by git
git ls-files | xargs grep -l "pat-na1-" 2>/dev/null

# Verify .env is ignored
git check-ignore .env
```

## Token Scopes Reference

### HubSpot Private App Required Scopes

```
crm.objects.deals.read
crm.objects.deals.write
crm.objects.contacts.read
crm.objects.contacts.write
crm.objects.companies.read
crm.objects.companies.write
crm.schemas.deals.read
crm.objects.tasks.read
crm.objects.tasks.write
```

### GitHub Token Required Scopes

```
repo (full repository access)
workflow (update GitHub Actions workflows)
```

---

**Remember**: Credentials are like house keys - never leave them in the lock, never write them down where others can see them.
