# Credential Security Solution Guide

## Summary: How to Keep API Keys Safe

### ✅ Current Status
- **GitHub Actions**: Secure (uses GitHub Secrets)
- **Local Scripts**: 16 files with hardcoded credentials need updating

### 🎯 The Goal
**NEVER** have `pat-na1-` tokens visible in any Python files

---

## Two Environments, Two Solutions

### 1. GitHub Actions (Cloud) - ✅ ALREADY SECURE

**How it works:**
- Token stored in: **GitHub Repository Secrets** (encrypted)
- Accessed via: `${{ secrets.HUBSPOT_API_KEY }}`
- Visible in: **NOWHERE** (GitHub auto-masks it in all logs)

**Your working token** (only for GitHub Secrets):
```
${HUBSPOT_API_KEY}
```

This token:
- ✅ Works perfectly in GitHub Actions
- ✅ Is encrypted in GitHub's vault
- ✅ Never appears in logs or git history
- ❌ **Does NOT work** when used directly in local Python scripts

**Location:** Settings → Secrets and variables → Actions → `HUBSPOT_API_KEY`

---

### 2. Local Scripts (Your Windows PC) - NEEDS UPDATING

**Current problem:**
```python
# ❌ BAD - Hardcoded in 16 files
API_KEY = "${HUBSPOT_API_KEY}"
```

**Secure solution:**
```python
# ✅ GOOD - Load from environment
import os
from dotenv import load_dotenv

load_dotenv()  # Reads from .env file
API_KEY = os.environ.get('HUBSPOT_API_KEY')

if not API_KEY:
    raise ValueError("HUBSPOT_API_KEY not found in .env file")
```

---

## Step-by-Step: Securing Local Scripts

### Step 1: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 2: Create/Update .env File

Your `.env` file is already set up at:
```
C:\Users\BrettWalker\FirstMile_Deals\.env
```

**Current content:**
```bash
# HubSpot Private App Token
HUBSPOT_API_KEY=${HUBSPOT_API_KEY}
```

**Status:** ✅ This file is already in `.gitignore` - safe from git

### Step 3: Update Python Scripts

**Files that need updating (16 total):**
- `9am_sync.py`
- `daily_9am_workflow.py`
- `noon_sync.py`
- `check_priority_deals.py`
- `create_boxiiship_tasks.py`
- `create_boxiiship_winback_deal.py`
- `create_morning_tasks_oct27.py`
- `fix_boxiiship_correct_structure.py`
- `get_pipeline_stages.py`
- `get_task_details.py`
- `mark_boxiiship_winback.py`
- `update_boxiiship_winback.py`
- `update_team_shipper.py`
- `add_winback_note.py`
- `[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback.py`
- `[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback_v2.py`

**Template for secure script:**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Description
"""

import os
import sys
import io
from dotenv import load_dotenv
import requests
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Get API key from environment (SECURE PATTERN)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)

# Other constants
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Your script code continues here...
```

---

## Why The GitHub Token Doesn't Work Locally

The token `${HUBSPOT_API_KEY}` shows authentication errors when used in local scripts. This might be because:

1. **Token was created specifically for GitHub Actions** (some PATs have IP restrictions)
2. **Token permissions** might require GitHub's infrastructure
3. **Token might need regeneration** for local + cloud use

### Solution Options:

**Option A: Generate Two Separate Tokens**
- Token 1: For GitHub Actions (current one - keep it)
- Token 2: For local scripts (generate new one)

**Option B: Verify Current Token Permissions**
- Go to HubSpot → Settings → Integrations → Private Apps
- Verify all required scopes are enabled
- Try regenerating the token

**Option C: Use GitHub Token Works Locally**
- Keep using the older token for local scripts temporarily
- Use new token only in GitHub Secrets
- Migrate when you have a working token for both

---

## Quick Fix: Update One Script as Example

Let's update `daily_9am_sync.py` as a template:

**Before:**
```python
# Configuration
API_KEY = "${HUBSPOT_API_KEY}"
```

**After:**
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    raise ValueError("HUBSPOT_API_KEY not found. Check .env file.")
```

---

## Security Checklist

### Before Every Git Commit:

```bash
# 1. Scan for exposed credentials
python secure_credentials.py

# 2. Check what you're about to commit
git diff

# 3. Verify no tokens in staged files
git diff --cached | grep "pat-na1-"

# 4. If clean, commit
git add .
git commit -m "Secure credentials - use environment variables"
git push
```

### Monthly Security Audit:

- [ ] Rotate HubSpot API tokens (generate new ones)
- [ ] Update `.env` file with new tokens
- [ ] Update GitHub Secrets with new tokens
- [ ] Run `python secure_credentials.py` to verify no hardcoded credentials
- [ ] Check git log for any accidentally committed credentials

---

## Emergency: Credential Exposed in Git

If you accidentally commit a credential:

1. **IMMEDIATELY revoke the token** in HubSpot
2. **Generate a new token**
3. **Update .env and GitHub Secrets**
4. **Clean git history** (advanced - requires force push)

---

## Best Practices Summary

### ✅ DO:
- Store tokens in `.env` file (local)
- Store tokens in GitHub Secrets (cloud)
- Use `os.environ.get()` to load them
- Add `.env` to `.gitignore`
- Rotate tokens every 90 days
- Run security audits before commits

### ❌ DON'T:
- Hardcode tokens in Python files
- Commit `.env` file to git
- Share tokens in chat/email
- Use same token for dev and production
- Leave old tokens active after rotation

---

## Quick Commands Reference

```bash
# Install dependencies
pip install python-dotenv requests

# Run security audit
python secure_credentials.py

# Check .env is ignored by git
git check-ignore .env  # Should output: .env

# Verify no credentials in staged changes
git diff --cached | grep "pat-na1-"

# Search all Python files for hardcoded tokens
grep -r "pat-na1-" . --include="*.py" | grep -v ".git/"
```

---

## Next Steps

1. **Immediate:** Run `python secure_credentials.py` to identify all files with hardcoded credentials
2. **Priority:** Update `daily_9am_sync.py` (9AM workflow needs this)
3. **This week:** Update remaining 15 files with secure pattern
4. **Before next commit:** Run security audit to verify everything is clean
5. **Monthly:** Rotate tokens and re-run security audit

---

**Remember:** Credentials are like house keys. The `.env` file is your safe - it stays at home (local machine). The code files are your blueprints - they can be shared publicly without risk.
