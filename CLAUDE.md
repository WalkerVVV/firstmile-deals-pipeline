# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📚 COMPLETE DOCUMENTATION → [.claude/](/.claude/)

**All system documentation is centralized in the `.claude` folder:**

- **[.claude/README.md](/.claude/README.md)** - Complete system overview & quick start
- **[.claude/DOCUMENTATION_INDEX.md](/.claude/DOCUMENTATION_INDEX.md)** - Master navigation guide
- **[.claude/NEBUCHADNEZZAR_REFERENCE.md](/.claude/NEBUCHADNEZZAR_REFERENCE.md)** - All IDs, commands, & reference
- **[.claude/DAILY_SYNC_OPERATIONS.md](/.claude/DAILY_SYNC_OPERATIONS.md)** - 9AM, NOON, EOD workflows
- **[.claude/HUBSPOT_WORKFLOW_GUIDE.md](/.claude/HUBSPOT_WORKFLOW_GUIDE.md)** - HubSpot MCP integration
- **[.claude/DEAL_FOLDER_TEMPLATE.md](/.claude/DEAL_FOLDER_TEMPLATE.md)** - Standard deal structure

**START HERE**: [.claude/INDEX.md](/.claude/INDEX.md)

---

## Project Overview

FirstMile Deals - Sales pipeline and customer analysis system for FirstMile shipping solutions. This codebase manages deal tracking, customer data analysis, rate calculations, and performance reporting for FirstMile's Xparcel shipping services.

The system is called "The Nebuchadnezzar v2.0" - a fully automated 10-stage pipeline consciousness with N8N automation watching deal folder movements, zero manual data entry, and real-time tracking.

## Core Business Context

FirstMile is a **carrier** (not a platform/3PL) offering Xparcel ship methods:
- **Xparcel Ground**: 3-8 day economy ground service
- **Xparcel Expedited**: 2-5 day faster ground solution (1-20 lb)
- **Xparcel Priority**: 1-3 day premium option with money-back guarantee

### Key Terminology
- "National Network": Nationwide coverage (all ZIPs)
- "Select Network": Metro-focused injection points (LA, DAL, ATL, ORD, EWR, etc.)
- Never name specific carriers (UPS, FedEx, USPS) - use "National" or "Select"
- Spell "eCommerce" with camel-case 'C'
- Xparcel is a ship-method under FirstMile, not a separate company

## High-Level Architecture

### Deal Pipeline Structure (Nebuchadnezzar v2.0)
The repository follows a 10-stage pipeline system with automated folder-based tracking:
```
[00-LEAD] → [01-DISCOVERY-SCHEDULED] → [02-DISCOVERY-COMPLETE] →
[03-RATE-CREATION] → [04-PROPOSAL-SENT] → [05-SETUP-DOCS-SENT] →
[06-IMPLEMENTATION] → [07-CLOSED-WON] → [08-CLOSED-LOST] → [09-WIN-BACK]
```

Each deal folder contains customer-specific data, analysis scripts, and reports. Moving folders between stages triggers N8N automation workflows.

### Automation System
- **Watch Folder**: `C:\Users\BrettWalker\FirstMile_Deals\`
- **Pipeline Database**: `_PIPELINE_TRACKER.csv` (downloads folder)
- **Activity Log**: `_DAILY_LOG.md` (downloads folder)
- **Action Queue**: `FOLLOW_UP_REMINDERS.txt` (downloads folder)
- **Command Center**: `AUTOMATION_MONITOR_LOCAL.html` (desktop)
- **Control Panel**: `NEBUCHADNEZZAR_CONTROL.bat` (desktop)

### HubSpot Integration
The system integrates with HubSpot CRM for lead management and deal tracking:
- **Owner ID**: 699257003 (Brett Walker)
- **Pipeline ID**: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- **Quick Commands**: Use `qm hubspot` commands for lead creation, bulk processing, deal conversion
- See `HubSpot/HUBSPOT_MCP_CHEATSHEET.md` for complete API reference

### Key Analysis Patterns

1. **PLD (Parcel Level Detail) Analysis**: Comprehensive shipping profile analysis covering carrier mix, service levels, weight distribution, dimensions, zones, and optimization opportunities. Standard flow:
   - Load shipment data (CSV/Excel)
   - Calculate volume metrics and daily averages
   - Analyze weight distribution with billable weight rules
   - Generate zone and geographic distribution
   - Create cost analysis and savings projections
   - Output Excel reports with professional formatting

2. **Performance Reporting**: Customer-facing reports following strict FirstMile brand standards:
   - SLA compliance (primary metric, always first)
   - Transit performance breakdowns
   - Geographic and zone analysis
   - In-transit status tracking
   - Excel output with 9 standard tabs

3. **Rate Calculation**: Complex multi-zone, multi-weight tier pricing matrices:
   - Extract current customer rates
   - Apply FirstMile pricing models
   - Calculate savings projections
   - Generate comparison matrices
   - Common scripts: `apply_customer_rates.py`, `create_pricing_matrix.py`, `revenue_calculator.py`

4. **Invoice Audit Analysis**: Carrier invoice auditing for overcharge identification:
   - Compare invoiced rates vs contracted rates
   - Identify billable weight discrepancies
   - Calculate refund opportunities
   - Scripts typically named `invoice_audit_builder_*.py`

## Commands

### Python Analysis Scripts
```bash
# Run PLD analysis on customer data
python [customer_folder]/pld_analysis.py

# Generate performance report
python [customer_folder]/firstmile_orchestrator.py

# Apply FirstMile rates and calculate savings
python [customer_folder]/apply_firstmile_rates.py

# Create pricing matrix for rate proposals
python [customer_folder]/create_pricing_matrix.py

# Generate revenue projections
python [customer_folder]/revenue_calculator.py

# Invoice audit analysis
python [customer_folder]/invoice_audit_builder_v31.py
```

### Common Python Dependencies
```bash
pip install pandas numpy openpyxl xlsxwriter matplotlib seaborn plotly
```

### Daily Sync Commands
```bash
# Morning priority report (9AM sync)
python daily_9am_workflow.py

# Task verification and missing task creation
python daily_9am_sync.py

# Folder-to-HubSpot sync verification
python pipeline_sync_verification.py

# Noon progress check
python noon_sync.py
```

### Pipeline Management
```bash
# Move deal through pipeline (triggers automation)
# Simply move folder to new stage directory:
move "[03-RATE-CREATION]_CustomerName" "[04-PROPOSAL-SENT]_CustomerName"

# HubSpot deal update
qm hubspot update-deal --deal-id [ID] --stage "[NEW-STAGE]"

# Bulk rate creation workflow
# See BULK_RATE_PROCESSING/RATE_CREATION_BLITZ.md for template
```

### HubSpot Commands
```bash
# Search deals by stage
qm hubspot search-deals --pipeline-id 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Create new lead
qm hubspot create-lead --first-name "John" --last-name "Smith" --email "john@company.com" --company "Acme Corp"

# Convert lead to deal
qm hubspot convert-to-deal --contact-id [ID] --deal-name "Company - Xparcel Ground" --amount 150000

# Create follow-up task
qm hubspot create-task --deal-id [ID] --title "Follow up on proposal" --type "EMAIL"
```

## Critical Business Rules

### Billable Weight Calculation
ALL carriers follow these rules:
- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound (32, 48, 64 oz, etc.)

### SLA Windows
- Xparcel Priority: 3 days
- Xparcel Expedited: 5 days
- Xparcel Ground: 8 days

### Performance Thresholds
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

### Brand Standards
- Primary color: #366092 (FirstMile blue)
- Always lead with SLA compliance in reports (not daily delivery %)
- Use plain, factual language (no emojis or slogans)
- Maintain consistent sheet names in Excel outputs

## Data Processing Patterns

### Standard CSV/Excel Loading
```python
import pandas as pd

# Handle various date formats
date_cols = ['created', 'delivered', 'ship_date', 'Request Date']
df = pd.read_csv(file, parse_dates=date_cols, dayfirst=False)

# Handle tracking numbers in scientific notation
df['tracking'] = df['tracking'].astype(str).str.replace('.0', '', regex=False)

# Standardize service level names
service_map = {
    'Ground': 'Xparcel Ground',
    'Expedited': 'Xparcel Expedited',
    'Priority': 'Xparcel Priority',
    'Direct Call': 'Xparcel Priority'  # Data mapping
}
```

### Hub Mapping
```python
HUB_MAP = {
    "CA": "LAX - West Coast",
    "TX": "DFW - South Central",
    "FL": "MIA - Southeast",
    "NY": "JFK/EWR - Northeast",
    "IL": "ORD - Midwest",
    "GA": "ATL - Southeast"
}
```

### Zone Analysis
Zones 1-8 with Regional (1-4) vs Cross-Country (5-8) grouping is a critical pattern for rate calculations and network optimization.

### Excel Report Generation
Professional Excel outputs use openpyxl with:
- FirstMile blue (#366092) headers with white text
- Auto-sized columns (max 50 chars)
- Conditional formatting for SLA compliance
- Standard 9-tab structure for performance reports
- See `firstmile_orchestrator.py` for complete implementation

## Important File Locations

- **Customer Data**: `[stage-number]_[customer-name]/` folders
- **Rate Sheets**: Usually Excel files with zone/weight matrices in customer folders
- **Analysis Scripts**: Python files in customer folders
- **Reports**: Generated Excel/PDF files in customer folders
- **Templates**: `Brett_Walker_Instructions_v4.3.md` contains system instructions and Morpheus Method guidance
- **Pipeline Structure**: `APPROVED_PIPELINE_STRUCTURE.md` has official stage definitions
- **HubSpot Integration**: `HubSpot/` folder contains API reference and MCP cheatsheet
- **Bulk Tools**: `BULK_RATE_PROCESSING/` contains templates for rapid rate creation
- **Network Analysis**: `XPARCEL_NATIONAL_SELECT/` contains Select Network ZIP analysis tools

## Analysis Workflow

1. **Data Ingestion**: Load customer shipment data (CSV/Excel)
2. **Standardization**: Map service levels, clean tracking numbers, parse dates
3. **Analysis**: Run PLD analysis, calculate metrics, identify patterns
4. **Rate Application**: Apply FirstMile pricing, calculate savings (typically 40% savings target)
5. **Report Generation**: Create professional Excel deliverables
6. **Pipeline Update**: Move deal folder to appropriate stage (triggers automation)
7. **HubSpot Sync**: Update CRM records via `qm hubspot` commands if needed

## Key Metrics to Track

- **Volume**: Total shipments, daily average, monthly trends
- **Service Mix**: Distribution across Ground/Expedited/Priority
- **Weight Profile**: Packages by weight tier (critical for pricing)
- **Geographic Coverage**: Top states, zone distribution, hub assignment
- **Performance**: SLA compliance, transit times
- **Cost**: Current spend vs FirstMile savings projections (target 40% savings)
- **Network Fit**: National vs Select network allocation

## Common Pitfalls to Avoid

- Never lead reports with daily delivery percentages (SLA compliance first)
- Don't name specific carriers - use "National" or "Select" network
- Always validate billable weight calculations match carrier rules
- Ensure date parsing handles both US and international formats
- Check for tracking numbers in scientific notation
- Verify service level mapping is consistent (watch for "Direct Call" -> "Xparcel Priority")
- When moving folders between stages, automation expects exact naming format `[##-STAGE]_Company_Name`
- HubSpot API calls require correct association type IDs (see cheatsheet)
- Never use [00-LEAD] or [09-WIN-BACK] stage IDs in HubSpot (they don't exist - use [01-DISCOVERY-SCHEDULED] instead)
- Stage IDs in HubSpot API are long UUIDs (e.g., `d607df25-2c6d-4a5d-9835-6ed1e4f4020a`), not simple numbers


## Common Script Patterns

### PLD Analysis Scripts
- `pld_analysis.py`: Standard comprehensive shipping profile
- `[customer]_pld_analysis.py`: Customer-specific analysis
- Volume, carrier mix, service levels, weight distribution, zones, geography

### Rate Calculation Scripts
- `apply_customer_rates.py`: Apply specific customer rate cards
- `create_pricing_matrix.py`: Generate zone/weight pricing matrices
- `revenue_calculator.py`: Project revenue based on volume assumptions
- `volume_assumptions_generator.py`: Create volume distribution models
- `tier_tool_*.py`: Multi-tier rate calculators (41-tier matrices)

### Performance Report Scripts
- `firstmile_orchestrator.py`: Main 9-tab branded report generator
- `firstmile_performance_report.py`: Alternative performance reporting
- `enterprise_performance_report.py`: Large customer reporting

### Invoice Audit Scripts
- `invoice_audit_builder_v31.py`: Full audit analysis
- `invoice_audit_builder_DRY_GOODS_ONLY.py`: Filtered analysis
- Identifies overcharges, billable weight issues, refund opportunities

## Pipeline Stage Definitions

Each stage has specific automation triggers and follow-up timelines:

- **[00-LEAD]**: Initial contact, no automation
- **[01-DISCOVERY-SCHEDULED]**: Meeting booked, stale deal reminders active
- **[02-DISCOVERY-COMPLETE]**: Requirements gathered, 30-day follow-up
- **[03-RATE-CREATION]**: Pricing work in progress, 2-week follow-up (bottleneck stage)
- **[04-PROPOSAL-SENT]**: Rates delivered, 30-day follow-up
- **[05-SETUP-DOCS-SENT]**: Verbal commit, docs sent, 2-week follow-up
- **[06-IMPLEMENTATION]**: Onboarding active, 30-day follow-up
- **[07-CLOSED-WON]**: Active customer, move to customer success tracking
- **[08-CLOSED-LOST]**: Lost deal, optional follow-up date
- **[09-WIN-BACK]**: Re-engagement, monthly check-ins

See `APPROVED_PIPELINE_STRUCTURE.md` for complete stage requirements and automation rules.

## System File Locations

### Configuration Files
- **System Root**: `C:\Users\BrettWalker\FirstMile_Deals\`
- **Documentation**: `.claude/` folder (comprehensive system docs)
- **Python Config**: `config.py`, `hubspot_config.py`, `hubspot_utils.py`, `date_utils.py`
- **Security**: `.env.example` (template for API keys - never commit actual .env)
- **Requirements**: `requirements.txt` (Python dependencies)

### Automation & Tracking
- **Pipeline Database**: `C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv`
- **Activity Log**: `C:\Users\BrettWalker\Downloads\_DAILY_LOG.md`
- **Learning Capture**: `C:\Users\BrettWalker\Downloads\_DAILY_LOG_FEEDBACK.md`
- **Action Queue**: `C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt`
- **Dashboard**: `C:\Users\BrettWalker\Desktop\AUTOMATION_MONITOR_LOCAL.html`
- **Control Panel**: `C:\Users\BrettWalker\Desktop\NEBUCHADNEZZAR_CONTROL.bat`

### Key Scripts
- **Daily Workflows**: `daily_9am_workflow.py`, `daily_9am_sync.py`, `noon_sync.py`
- **Pipeline Sync**: `pipeline_sync_verification.py`, `hubspot_pipeline_verify.py`
- **Batch Operations**: `hubspot_batch_updates_tuesday_am.py`, `hubspot_realtime_updates.py`

## Brand Scout Integration

The system includes automated brand research and lead generation via Brand Scout:
- **Location**: `.claude/brand_scout/` folder
- **Automated Research**: Overnight brand analysis with company info, contacts, shipping data
- **HubSpot Integration**: Auto-creates leads with associated contacts and companies
- **Deal Folders**: Auto-generates `[00-LEAD]_BrandName` folders with relationship docs
- **Review Process**: Check `.claude/brand_scout/output/` during 9AM sync for new leads

See `.claude/brand_scout/README.md` and `.claude/BRAND_SCOUT_SYSTEM.md` for complete workflow.

## Troubleshooting Quick Reference

### Sync Issues
- **Folder not syncing to HubSpot**: Run `pipeline_sync_verification.py` to identify mismatches
- **Missing tasks in HubSpot**: Run `daily_9am_sync.py` to create missing EMAIL tasks
- **Stage ID errors**: Check `.claude/NEBUCHADNEZZAR_REFERENCE.md` for correct UUID format

### Script Errors
- **Import errors**: Check `requirements.txt` and install missing packages with `pip install -r requirements.txt`
- **API authentication**: Verify API key in script matches valid HubSpot PAT
- **Date parsing issues**: Use `date_utils.py` functions for consistent date handling
- **Encoding errors**: Scripts use UTF-8 encoding; check Windows console encoding

### Data Quality
- **Tracking numbers showing as scientific notation**: Use `.astype(str).str.replace('.0', '', regex=False)`
- **Service level inconsistencies**: Apply service_map standardization from Data Processing Patterns
- **Billable weight discrepancies**: Verify calculations match carrier rules (see Critical Business Rules)
