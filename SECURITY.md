# Security Best Practices - FirstMile Deals System

**Last Updated**: 2025-10-10
**Version**: 1.0

## Overview

This document outlines security best practices for the FirstMile Deals system, including API key management, data protection, and secure coding patterns.

---

## 🔐 API Key Management

### CRITICAL: Never Commit API Keys

**Rule**: API keys, tokens, and credentials must NEVER be committed to version control.

### Current Migration Status

**✅ COMPLETED**:
- Created secure configuration system (`config.py`)
- Created `.env.example` template
- Created `.gitignore` with security exclusions
- Created secure HubSpot client (`hubspot_utils.py`)
- Created secure 9AM sync script (`9am_sync_secure.py`)

**⚠️ IN PROGRESS**:
- Migrating remaining 26+ scripts to use secure configuration
- Need to rotate HubSpot API key after migration complete

### Setup Instructions

#### 1. Create `.env` File

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual credentials
# NEVER commit this file to git
```

#### 2. Set Environment Variables

**`.env` file**:
```bash
HUBSPOT_API_KEY=pat-na1-YOUR_ACTUAL_TOKEN_HERE
HUBSPOT_OWNER_ID=699257003
HUBSPOT_PIPELINE_ID=8bd9336b-4767-4e67-9fe2-35dfcad7c8be
HUBSPOT_PORTAL_ID=46526832
FIRSTMILE_DEALS_PATH=C:\Users\BrettWalker\FirstMile_Deals
```

#### 3. Install Dependencies

```bash
pip install python-dotenv
# OR
pip install -r requirements.txt
```

#### 4. Use Secure Configuration

**OLD (Insecure)**:
```python
API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'  # ❌ NEVER DO THIS
```

**NEW (Secure)**:
```python
from config import Config
from hubspot_utils import HubSpotClient

# Configuration validates and loads from .env automatically
client = HubSpotClient()
```

---

## 🛡️ HubSpot API Security

### API Key Permissions

**Current Key Scope**:
- CRM: Deals (read/write)
- CRM: Contacts (read)
- CRM: Notes (write)
- CRM: Pipelines (read)

**Best Practice**: Use minimum required permissions for API keys.

### Rate Limiting

HubSpot enforces rate limits:
- **Standard**: 100 requests per 10 seconds
- **Burst**: 150 requests per 10 seconds

**Implementation**: `hubspot_utils.py` includes automatic rate limiting.

```python
# Rate limiting is handled automatically
client = HubSpotClient()
client.search_deals(filters, properties)  # Rate limited internally
```

### Error Handling

**Best Practices**:
- Always catch and log API errors
- Never expose API keys in error messages
- Use retry logic with exponential backoff
- Handle 429 (rate limit) responses gracefully

**Implementation**:
```python
from hubspot_utils import HubSpotClient, HubSpotAPIError

try:
    client = HubSpotClient()
    deals = client.search_deals(filters, properties)
except HubSpotAPIError as e:
    print(f"API Error {e.status_code}: {e.message}")
    # Log error (without API key)
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

---

## 🔒 Data Protection

### Customer Data Handling

**Sensitive Data**:
- Customer shipment data (PLD files)
- Rate cards and pricing information
- Invoice data

**Protection Measures**:
1. ✅ `.gitignore` excludes `*.csv`, `*.xlsx` (except templates)
2. ✅ Customer data stored in deal-specific folders
3. ⚠️ Data transmitted over HTTPS only
4. ⚠️ No customer data in error logs

### Local File Security

**File Locations**:
- Deal folders: `C:\Users\BrettWalker\FirstMile_Deals\[##-STAGE]_CustomerName\`
- Generated reports: Excluded from git via `.gitignore`
- Logs: `_DAILY_LOG.md` excluded from git

**Best Practice**: Never commit customer-specific data files.

---

## 🔍 Code Security Patterns

### Input Validation

Always validate and sanitize inputs:

```python
# Good: Validate before use
def get_deal(deal_id: str):
    if not deal_id or not deal_id.isdigit():
        raise ValueError("Invalid deal ID")
    # ... rest of code

# Bad: No validation
def get_deal(deal_id):
    client.get_deal(deal_id)  # What if deal_id is malicious?
```

### SQL Injection Protection

**Current Status**: ✅ No direct SQL queries in codebase

If database access is added in future:
- Use parameterized queries
- Use ORM (SQLAlchemy) with bound parameters
- Never concatenate user input into SQL

### Path Traversal Protection

```python
# Good: Use absolute paths from config
from config import Config
file_path = Config.FIRSTMILE_DEALS_PATH / customer_folder / filename

# Bad: User-controlled paths
file_path = f"C:\\Users\\{user_input}\\{filename}"  # ❌ Path traversal risk
```

---

## 🚨 Incident Response

### If API Key is Compromised

**Immediate Actions**:
1. ✅ Revoke compromised key in HubSpot
2. ✅ Generate new API key
3. ✅ Update `.env` file with new key
4. ✅ Review HubSpot audit logs for unauthorized access
5. ✅ Notify team of incident

**HubSpot Key Rotation**:
1. Go to HubSpot → Settings → Integrations → Private Apps
2. Find "FirstMile Deals API" app
3. Click "Regenerate token"
4. Update `.env` file
5. Restart all running scripts

### If Customer Data is Exposed

**Immediate Actions**:
1. ✅ Remove exposed data from public location
2. ✅ Assess scope of exposure (what data, how long, who accessed)
3. ✅ Notify affected customers (if required by law/contract)
4. ✅ Review access logs
5. ✅ Implement additional controls to prevent recurrence

---

## ✅ Security Checklist

Use this checklist for new scripts:

- [ ] API credentials loaded from environment (not hardcoded)
- [ ] Uses `config.py` and `hubspot_utils.py` modules
- [ ] Proper error handling (catch exceptions)
- [ ] No sensitive data in logs or error messages
- [ ] Input validation for user-controlled data
- [ ] Proper file path handling (absolute paths from config)
- [ ] Customer data excluded from git (check `.gitignore`)
- [ ] Rate limiting respected (use HubSpotClient)
- [ ] Timeout configured for API calls
- [ ] No SQL queries (or parameterized if needed)

---

## 📚 Additional Resources

### HubSpot Security Documentation
- [HubSpot API Security](https://developers.hubspot.com/docs/api/security)
- [Private App Scopes](https://developers.hubspot.com/docs/api/private-apps)
- [Rate Limits](https://developers.hubspot.com/docs/api/usage-details)

### Python Security Best Practices
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Tools](https://github.com/pyupio/safety)

### Internal Documentation
- [config.py](config.py) - Configuration management
- [hubspot_utils.py](hubspot_utils.py) - Secure HubSpot client
- [.env.example](.env.example) - Environment template
- [CODEBASE_ANALYSIS_REPORT_2025-10-10.md](CODEBASE_ANALYSIS_REPORT_2025-10-10.md) - Security audit

---

## 📝 Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-10 | 1.0 | Initial security documentation created |
| 2025-10-10 | 1.0 | Secure configuration system implemented |
| 2025-10-10 | 1.0 | `.gitignore` and `.env.example` created |

---

## 🤝 Questions or Concerns?

If you discover a security vulnerability or have questions about security practices:

1. **DO NOT** commit security issues to git
2. **DO NOT** share API keys or sensitive data in public channels
3. **DO** create a secure note in HubSpot or contact Brett directly
4. **DO** follow the incident response procedures above

---

**Remember**: Security is everyone's responsibility. When in doubt, ask!
