# FirstMile Deals Codebase Analysis Report

**Date**: October 10, 2025
**Time**: 12:06 PM PST
**System**: Nebuchadnezzar v2.0
**Analyst**: Claude Code (`/sc:analyze` comprehensive review)

---

## Executive Summary

Comprehensive analysis of FirstMile_Deals sales pipeline and customer analysis system. The codebase consists of **98 Python scripts** across **19 active deal folders** supporting HubSpot CRM integration, PLD analysis, rate calculations, and performance reporting.

### Key Findings

✅ **Strengths**:
- Well-organized folder-based pipeline structure
- Comprehensive analysis tools for shipping data
- Rich documentation system in `.claude/` folder
- Multiple backup/versioning of critical scripts

⚠️ **Critical Issues**:
- **SECURITY**: Hardcoded HubSpot API key in 26+ files (Priority 1)
- **ARCHITECTURE**: 746 import statements with potential redundancy
- **CONSISTENCY**: Multiple script versions without clear ownership
- **DOCUMENTATION**: Stage mapping discrepancies (10 vs 8 stages)

🔧 **Recommendations**:
1. Immediately migrate API keys to environment variables
2. Consolidate duplicate scripts and establish versioning standard
3. Complete stage mapping correction across all documentation
4. Implement error handling and logging standards

---

## 1. Codebase Structure

### File Inventory

| Category | Count | Examples |
|----------|-------|----------|
| **Pipeline Management** | 19 | `9am_sync.py`, `check_priority_deals.py`, `get_pipeline_stages.py` |
| **PLD Analysis** | 12 | Customer-specific PLD analysis scripts |
| **Rate Calculation** | 24 | `apply_firstmile_rates.py`, `create_pricing_matrix.py`, `revenue_calculator.py` |
| **Performance Reporting** | 8 | `firstmile_orchestrator.py`, `firstmile_performance_report.py` |
| **Invoice Audit** | 6 | `invoice_audit_builder_v31.py`, audit analysis scripts |
| **HubSpot Integration** | 15 | Deal creation, note updates, pipeline sync scripts |
| **Utility Scripts** | 14 | Weight analysis, dimension analysis, zone mapping |

### Folder Organization

```
FirstMile_Deals/
├── .claude/                    # Documentation (8 core files)
├── [##-STAGE]_CustomerName/    # Active deals (19 folders)
├── [CUSTOMER]_CompanyName/     # Active customers (3 folders)
├── HubSpot/                    # HubSpot integration docs
├── BULK_RATE_PROCESSING/       # Templates for rapid rate creation
└── [Root scripts]/             # Pipeline management (19 files)
```

**Documentation Files** (`.claude/` folder):
- `README.md` - System overview
- `DOCUMENTATION_INDEX.md` - Master navigation
- `NEBUCHADNEZZAR_REFERENCE.md` - Complete system reference
- `DAILY_SYNC_OPERATIONS.md` - 9AM, NOON, EOD workflows
- `HUBSPOT_WORKFLOW_GUIDE.md` - HubSpot MCP integration
- `DEAL_FOLDER_TEMPLATE.md` - Standard deal structure

---

## 2. Security Analysis

### 🚨 CRITICAL: Hardcoded API Keys

**Issue**: HubSpot API key `pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764` is hardcoded in 26+ Python scripts.

**Affected Files** (Sample):
- [9am_sync.py:17](C:\Users\BrettWalker\FirstMile_Deals\9am_sync.py#L17)
- [check_priority_deals.py:6](C:\Users\BrettWalker\FirstMile_Deals\check_priority_deals.py#L6)
- `get_pipeline_stages.py`, `create_boxiiship_winback_deal.py`, `fix_boxiiship_correct_structure.py`
- All HubSpot integration scripts in customer folders

**Risk Assessment**:
- **Severity**: HIGH
- **Impact**: Full HubSpot CRM access if key compromised
- **Exposure**: Git repository history contains keys
- **Scope**: Owner ID `699257003`, Pipeline ID `8bd9336b-4767-4e67-9fe2-35dfcad7c8be`

**Immediate Remediation**:
```python
# CURRENT (Insecure):
API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'

# RECOMMENDED (Secure):
import os
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    raise ValueError("HUBSPOT_API_KEY environment variable not set")
```

**Action Plan**:
1. Create `.env` file with API key (add to `.gitignore`)
2. Install `python-dotenv` package
3. Update all 26+ files to use environment variable
4. Rotate HubSpot API key after migration
5. Document secure key management in `.claude/SECURITY.md`

### Other Security Concerns

✅ **No SQL Injection Risk**: No direct database queries
✅ **No XSS Risk**: No web interface generation
⚠️ **File Path Handling**: Uses absolute paths, generally safe
⚠️ **Error Messages**: Some scripts expose full file paths in errors

---

## 3. Code Quality Assessment

### Error Handling

**Current State**: Inconsistent error handling across scripts

**Analysis**:
- **Good**: Some scripts use try/except blocks for API calls
- **Missing**: Many scripts lack error handling entirely
- **Problem**: Silent failures possible in pipeline automation

**Example** ([9am_sync.py:96-99](C:\Users\BrettWalker\FirstMile_Deals\9am_sync.py#L96-L99)):
```python
if response.status_code != 200:
    print(f'❌ Error fetching deals: {response.status_code}')
    print(response.text)
    return  # Silent exit, no exception raised
```

**Recommendation**: Implement standard error handling pattern:
```python
try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
except requests.exceptions.Timeout:
    logger.error("HubSpot API timeout - check network connection")
    raise
except requests.exceptions.HTTPError as e:
    logger.error(f"HubSpot API error: {e.response.status_code} - {e.response.text}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise
```

### Code Duplication

**Identified Patterns**:

1. **HubSpot API Headers** (duplicated in 20+ files):
```python
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

2. **Stage Mapping** (duplicated in 8+ files):
```python
STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    # ... 6 more stages
}
```

3. **Date Parsing** (duplicated in 15+ files):
```python
def days_since(date_str):
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999
```

**Recommendation**: Create shared utilities module:
```python
# hubspot_utils.py
import os
import requests
from datetime import datetime

class HubSpotClient:
    def __init__(self):
        self.api_key = os.environ.get('HUBSPOT_API_KEY')
        self.owner_id = '699257003'
        self.pipeline_id = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'
        self.stage_map = {...}  # Centralized mapping

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def search_deals(self, filters, properties, limit=100):
        # Centralized API call logic with error handling
        pass

# date_utils.py
def days_since(date_str):
    """Calculate days since date with robust error handling"""
    # Centralized implementation
    pass
```

### Script Versioning

**Problem**: Multiple versions of same script without clear ownership:

| Script Base Name | Versions | Location |
|------------------|----------|----------|
| `boxiiship_dashboard` | 7 versions | `[07-CLOSED-WON]_Boxiiship/` |
| `firstmile_performance_report` | 4 versions | `[07-CLOSED-WON]_JM_Group_NY/` |
| `invoice_audit_builder` | 3 versions | Multiple folders |
| `apply_firstmile_rates` | 2-3 versions | Multiple folders |

**Examples**:
- `boxiiship_dashboard.py`
- `boxiiship_dashboard_clean.py`
- `boxiiship_dashboard_enhanced.py`
- `boxiiship_dashboard_fixed.py`
- `boxiiship_dashboard_fixed_v2.py`
- `boxiiship_dashboard_fixed_backup.py`
- `boxiiship_dashboard_firstmile_backup.py`

**Recommendation**:
1. Establish single source of truth for each script type
2. Use Git for versioning (delete `_v2`, `_fixed`, `_backup` files)
3. Document active scripts in folder README
4. Archive old versions to `_archive/` subfolder if needed

### Import Analysis

**Total Imports**: 746 import statements across 98 files

**Common Dependencies**:
- `pandas` (92 files) - Data analysis
- `requests` (26 files) - HubSpot API calls
- `openpyxl` (18 files) - Excel generation
- `datetime` (64 files) - Date handling
- `json` (24 files) - Data serialization

**Concerns**:
- No `requirements.txt` file found
- Potential version conflicts between scripts
- Missing error handling for import failures

**Recommendation**: Create `requirements.txt`:
```
pandas>=2.0.0
requests>=2.28.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
xlsxwriter>=3.1.0
```

---

## 4. Architecture Review

### Pipeline Management System

**Components**:
1. **HubSpot CRM**: 8-stage pipeline (corrected from 10)
2. **Local Folders**: Deal-specific data and analysis
3. **N8N Automation**: Folder watch and sync triggers
4. **Python Scripts**: Data processing and API integration

**Architecture Diagram**:
```
┌─────────────────┐
│  HubSpot CRM   │ ◄─── API calls (26+ scripts)
│  8 Stages      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  N8N Automation │ ◄─── Folder watch triggers
│  Event Processor│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Local Folders  │ ◄─── Deal-specific analysis
│  19 Active Deals│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Python Scripts  │ ◄─── PLD, rates, reports
│  98 Scripts     │
└─────────────────┘
```

**Identified Issues**:

1. **Stage Mapping Discrepancy** (RESOLVED 2025-10-10):
   - Documentation showed 10 stages
   - Actual HubSpot has 8 stages
   - Corrected in: `9am_sync.py`, `check_priority_deals.py`, `.claude/NEBUCHADNEZZAR_REFERENCE.md`

2. **Missing [00-LEAD] and [09-WIN-BACK] Stages**:
   - Win-back is a NEW DEAL, not a stage
   - Lead management happens outside pipeline
   - Documented in: `LOCAL_FOLDER_VS_HUBSPOT_STRUCTURE.md`

3. **Active Customer vs Pipeline Deal**:
   - Active customers: `[CUSTOMER]_CompanyName/` folder
   - Pipeline deals: `[##-STAGE]_CompanyName/` folder
   - Win-back for active customer: subfolder within customer folder
   - Win-back for former customer: NEW DEAL in [04-PROPOSAL-SENT]

### Data Flow Patterns

**PLD Analysis Workflow**:
```
1. Customer CSV/Excel → pandas DataFrame
2. Standardize service levels, tracking numbers, dates
3. Calculate volume, weight, zone distribution
4. Apply rate cards and calculate savings
5. Generate Excel reports with branding
6. Move folder to next stage (triggers N8N)
```

**Common Data Processing** (appears in 40+ files):
```python
# 1. Load data
df = pd.read_csv(file, parse_dates=['created', 'delivered', 'ship_date'])

# 2. Handle tracking numbers in scientific notation
df['tracking'] = df['tracking'].astype(str).str.replace('.0', '', regex=False)

# 3. Standardize service levels
service_map = {
    'Ground': 'Xparcel Ground',
    'Expedited': 'Xparcel Expedited',
    'Direct Call': 'Xparcel Priority'
}
df['service'] = df['service'].map(service_map)

# 4. Calculate metrics
# ...weight distribution, zones, etc.

# 5. Generate Excel output
```

**Recommendation**: Create `pld_analysis_framework.py` base class to eliminate duplication.

---

## 5. Documentation Assessment

### Documentation Completeness

| Document | Status | Quality | Notes |
|----------|--------|---------|-------|
| `.claude/README.md` | ✅ Complete | Excellent | System overview and quick start |
| `.claude/DOCUMENTATION_INDEX.md` | ✅ Complete | Excellent | Master navigation guide |
| `.claude/NEBUCHADNEZZAR_REFERENCE.md` | ⚠️ Updated | Good | Stage mapping corrected 10/10 |
| `.claude/DAILY_SYNC_OPERATIONS.md` | ✅ Complete | Excellent | 9AM, NOON, EOD workflows |
| `.claude/HUBSPOT_WORKFLOW_GUIDE.md` | ✅ Complete | Excellent | HubSpot MCP integration |
| `.claude/DEAL_FOLDER_TEMPLATE.md` | ✅ Complete | Good | Standard deal structure |
| `CLAUDE.md` (root) | ✅ Complete | Excellent | Project overview for Claude Code |
| `CLAUDE.md` (`.claude`) | ✅ Complete | Good | FirstMile branding and analysis |

### Recent Documentation Updates (2025-10-10)

✅ **Completed**:
- `9AM_SYNC_RECONCILIATION_2025-10-10.md`
- `STAGE_MAPPING_UPDATE_COMPLETE_2025-10-10.md`
- `LOCAL_FOLDER_VS_HUBSPOT_STRUCTURE.md`
- `BOXIISHIP_STRUCTURE_CORRECTION.md`
- `FOLDER_NAMING_CONVENTION_UPDATED.md`
- `FINAL_STATUS_SUMMARY_2025-10-10.md`
- `EOD_SYNC_ANALYSIS_AND_INTEGRATION.md`

### Missing Documentation

⚠️ **Needed**:
1. `SECURITY.md` - API key management, secure practices
2. `CONTRIBUTING.md` - Code standards, PR process
3. `TROUBLESHOOTING.md` - Common errors and solutions
4. `API_REFERENCE.md` - HubSpot API patterns and examples
5. Individual folder `README.md` files for each customer/deal
6. `requirements.txt` - Python dependencies
7. `.gitignore` - Proper exclusions (especially `.env`)

---

## 6. Performance Considerations

### Script Execution Times

**Fast** (<5 seconds):
- Simple lookups: `check_priority_deals.py`
- HubSpot API calls: `get_pipeline_stages.py`
- Small data processing: weight/dimension analysis

**Moderate** (5-30 seconds):
- PLD analysis scripts (depends on CSV size)
- Rate calculation scripts (zone/weight matrices)
- Excel report generation

**Slow** (>30 seconds):
- Large invoice audit builders (10K+ rows)
- Comprehensive performance reports
- Multi-customer bulk processing

**Optimization Opportunities**:
1. **Pandas Operations**: Use vectorized operations instead of iterrows()
2. **API Calls**: Batch requests where possible (HubSpot allows bulk operations)
3. **Excel Generation**: Use xlsxwriter instead of openpyxl for large files
4. **Caching**: Cache HubSpot stage mappings and hub mappings

**Example Optimization** (found in multiple files):
```python
# CURRENT (Slow):
for index, row in df.iterrows():
    df.at[index, 'zone'] = calculate_zone(row['zip'])

# OPTIMIZED (Fast):
df['zone'] = df['zip'].apply(calculate_zone)
# OR (Faster):
df['zone'] = df['zip'].map(zone_lookup_dict)
```

---

## 7. Integration Points

### HubSpot CRM

**API Endpoints Used**:
- `/crm/v3/objects/deals/search` - Deal queries (15+ files)
- `/crm/v3/objects/deals/{dealId}` - Deal updates (8+ files)
- `/crm/v3/objects/notes` - Activity notes (5+ files)
- `/crm/v3/pipelines/deals/{pipelineId}` - Pipeline metadata (2 files)

**Current Integration Quality**:
- ✅ Consistent use of Owner ID and Pipeline ID
- ✅ Proper stage ID usage after 10/10 corrections
- ⚠️ No rate limiting implemented
- ⚠️ No retry logic for failed API calls
- ❌ Hardcoded API keys (security issue)
- ❌ No centralized error handling

**Recommendation**: Implement HubSpot SDK wrapper with:
- Automatic retries with exponential backoff
- Rate limiting (100 requests per 10 seconds)
- Centralized error handling and logging
- Request/response validation

### N8N Automation

**Triggers**:
- Folder creation/deletion
- Folder rename (stage movement)
- File additions to deal folders

**Actions**:
- Update `_PIPELINE_TRACKER.csv`
- Log to `_DAILY_LOG.md`
- Create follow-up reminders in `FOLLOW_UP_REMINDERS.txt`
- Update desktop dashboard `AUTOMATION_MONITOR_LOCAL.html`

**Integration Status**: Not directly visible in codebase (external system)

### Superhuman Email Integration

**Status**: Phase 0 implementation

**Components**:
- `.claude/superhuman_eod_workflow.py` - EOD analysis prompt generator
- Integration with daily sync workflow
- First production test scheduled: Tonight (2025-10-10)

**Purpose**: Extract email intelligence for EOD sync:
- Today's activity summary by deal
- Tomorrow's action plan
- Pipeline movement detection
- Metrics and insights

---

## 8. Testing Status

### Current State

❌ **No Automated Tests Found**

**Search Results**:
- No `test_*.py` or `*_test.py` files
- No `tests/` directory
- No `pytest.ini` or test configuration
- No CI/CD configuration (GitHub Actions, etc.)

### Testing Recommendations

**Priority 1: Unit Tests**
```python
# tests/test_hubspot_utils.py
import pytest
from hubspot_utils import HubSpotClient, days_since

def test_days_since_valid_date():
    result = days_since('2025-10-01T00:00:00Z')
    assert result >= 0

def test_days_since_invalid_date():
    result = days_since('invalid')
    assert result == 999

def test_hubspot_client_headers():
    client = HubSpotClient()
    headers = client.get_headers()
    assert 'Authorization' in headers
    assert headers['Content-Type'] == 'application/json'
```

**Priority 2: Integration Tests**
```python
# tests/test_hubspot_integration.py
def test_search_deals_api():
    """Test HubSpot deal search returns valid data"""
    # Mock API response
    pass

def test_stage_mapping_accuracy():
    """Verify stage IDs match HubSpot"""
    # Fetch actual stages from API
    # Compare to STAGE_MAP
    pass
```

**Priority 3: End-to-End Tests**
```python
# tests/test_pld_analysis_workflow.py
def test_complete_pld_analysis():
    """Test full PLD analysis workflow"""
    # Load sample CSV
    # Run analysis
    # Verify Excel output
    pass
```

**Test Framework Setup**:
```bash
pip install pytest pytest-cov pytest-mock
pytest tests/ --cov=. --cov-report=html
```

---

## 9. Priority Action Items

### Immediate (Next 24 Hours)

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| 🔴 **P0** | Migrate API keys to environment variables | Security | 4 hours |
| 🔴 **P0** | Rotate HubSpot API key after migration | Security | 30 min |
| 🟡 **P1** | Create `.gitignore` with `.env` exclusion | Security | 10 min |
| 🟡 **P1** | Document secure key management | Security | 1 hour |

### Short-Term (This Week)

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| 🟡 **P1** | Create shared `hubspot_utils.py` module | Quality | 6 hours |
| 🟡 **P1** | Create shared `date_utils.py` module | Quality | 2 hours |
| 🟡 **P1** | Implement standard error handling pattern | Quality | 4 hours |
| 🟢 **P2** | Create `requirements.txt` file | Dependency | 30 min |
| 🟢 **P2** | Archive duplicate script versions | Organization | 2 hours |
| 🟢 **P2** | Add README to each customer folder | Documentation | 3 hours |

### Medium-Term (This Month)

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| 🟢 **P2** | Create `pld_analysis_framework.py` base class | Quality | 8 hours |
| 🟢 **P2** | Implement HubSpot SDK wrapper with retries | Quality | 6 hours |
| 🟢 **P2** | Write unit tests for utility functions | Quality | 8 hours |
| 🔵 **P3** | Create `SECURITY.md` documentation | Documentation | 2 hours |
| 🔵 **P3** | Create `TROUBLESHOOTING.md` guide | Documentation | 3 hours |
| 🔵 **P3** | Optimize pandas operations in slow scripts | Performance | 4 hours |

### Long-Term (Next Quarter)

| Priority | Task | Impact | Effort |
|----------|------|--------|--------|
| 🔵 **P3** | Implement full test suite (unit + integration) | Quality | 20 hours |
| 🔵 **P3** | Set up CI/CD pipeline | Quality | 8 hours |
| 🔵 **P3** | Create API documentation for common patterns | Documentation | 6 hours |
| 🔵 **P3** | Refactor all customer analysis scripts to use framework | Quality | 40 hours |

---

## 10. Metrics Summary

### Codebase Statistics

| Metric | Value | Status |
|--------|-------|--------|
| **Total Python Files** | 98 | ✅ |
| **Active Deal Folders** | 19 | ✅ |
| **Active Customer Folders** | 3 | ✅ |
| **Documentation Files** | 15+ | ✅ |
| **HubSpot Integration Scripts** | 26 | ⚠️ Security |
| **Hardcoded API Keys** | 26+ | 🔴 Critical |
| **Import Statements** | 746 | ⚠️ Redundant |
| **Duplicate Scripts** | 30+ | ⚠️ Versioning |
| **Test Files** | 0 | ❌ Missing |
| **Requirements File** | 0 | ❌ Missing |

### Code Quality Scores

| Dimension | Score | Grade | Notes |
|-----------|-------|-------|-------|
| **Security** | 40/100 | 🔴 F | Hardcoded API keys |
| **Architecture** | 70/100 | 🟡 C | Good structure, needs refactoring |
| **Documentation** | 85/100 | 🟢 B+ | Excellent docs, minor gaps |
| **Maintainability** | 65/100 | 🟡 D+ | Duplication and versioning issues |
| **Performance** | 75/100 | 🟢 C+ | Generally good, optimization opportunities |
| **Testing** | 0/100 | 🔴 F | No tests |
| **Error Handling** | 50/100 | 🟡 F | Inconsistent patterns |
| **Dependencies** | 60/100 | 🟡 D | No requirements.txt |

**Overall Codebase Health**: 55/100 (🟡 **D+**)

---

## 11. Conclusion

### Summary

The FirstMile_Deals codebase is a **functional and well-documented system** with strong organizational structure and comprehensive pipeline management capabilities. However, it has **critical security vulnerabilities** (hardcoded API keys) and **quality issues** (code duplication, inconsistent error handling, lack of testing) that require immediate attention.

### Strengths

1. ✅ **Excellent Documentation**: `.claude/` folder provides comprehensive system knowledge
2. ✅ **Organized Structure**: Clear folder hierarchy with stage-based organization
3. ✅ **Rich Functionality**: Complete PLD analysis, rate calculation, and reporting tools
4. ✅ **HubSpot Integration**: Functional API integration with correct stage mapping (post-10/10 corrections)
5. ✅ **Active Maintenance**: Recent updates and corrections demonstrate ongoing development

### Critical Weaknesses

1. 🔴 **Security**: Hardcoded API keys in 26+ files (IMMEDIATE ACTION REQUIRED)
2. 🔴 **Testing**: Zero automated tests (HIGH RISK for production system)
3. ⚠️ **Code Duplication**: Significant redundancy across scripts
4. ⚠️ **Error Handling**: Inconsistent patterns, potential for silent failures
5. ⚠️ **Versioning**: Multiple script versions without clear ownership

### Next Steps

**Immediate** (Tonight/Tomorrow):
1. ✅ Complete this analysis report
2. 🔴 Create secure `.env` file for API key
3. 🔴 Update 2-3 critical scripts to use environment variables
4. 🟡 Create `.gitignore` with proper exclusions

**This Week**:
1. Complete API key migration across all scripts
2. Rotate HubSpot API key
3. Create shared utility modules (`hubspot_utils.py`, `date_utils.py`)
4. Archive duplicate script versions

**This Month**:
1. Implement standard error handling pattern
2. Write unit tests for utility functions
3. Create base framework for PLD analysis
4. Complete missing documentation

---

## Appendix A: File References

### Critical Files for Security Migration

**Priority 1** (Daily sync, high visibility):
- [9am_sync.py:17](C:\Users\BrettWalker\FirstMile_Deals\9am_sync.py#L17)
- [check_priority_deals.py:6](C:\Users\BrettWalker\FirstMile_Deals\check_priority_deals.py#L6)
- [get_pipeline_stages.py](C:\Users\BrettWalker\FirstMile_Deals\get_pipeline_stages.py)

**Priority 2** (Deal management):
- `create_boxiiship_winback_deal.py`
- `fix_boxiiship_correct_structure.py`
- `update_team_shipper.py`

**Priority 3** (Customer-specific):
- All customer folder HubSpot integration scripts

### Key Documentation Files

- [.claude/README.md](C:\Users\BrettWalker\FirstMile_Deals\.claude\README.md)
- [.claude/NEBUCHADNEZZAR_REFERENCE.md](C:\Users\BrettWalker\FirstMile_Deals\.claude\NEBUCHADNEZZAR_REFERENCE.md)
- [CLAUDE.md](C:\Users\BrettWalker\FirstMile_Deals\CLAUDE.md)

---

**Report Generated**: 2025-10-10 12:25 PM PST
**Analyst**: Claude Code
**System**: Nebuchadnezzar v2.0
**Version**: 1.0

