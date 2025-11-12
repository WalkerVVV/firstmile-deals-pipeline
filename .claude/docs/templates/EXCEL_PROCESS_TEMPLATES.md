# EXCEL PROCESS TEMPLATES

**Quick Reference Guide for All Standard Excel Deliverables**

---

## Overview

This document provides quick links and standard prompts for all Excel-based deliverables in the FirstMile Deals pipeline. Each template follows professional FirstMile branding (#366092 blue) and is prospect-ready.

---

## 1. Full Xparcel Analysis

**Purpose**: Professional savings analysis for prospects showing FirstMile Xparcel cost savings potential

**Use Case**: [03-RATE-CREATION] stage - Primary prospect deliverable

**Template**: [FULL_XPARCEL_ANALYSIS_TEMPLATE.md](FULL_XPARCEL_ANALYSIS_TEMPLATE.md)

**Output File**: `[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx`

**Standard Prompt**:
```
Create a professional FirstMile Xparcel Savings Analysis for [CUSTOMER NAME].

DATA FILE: [path/to/customer_pld_data.csv]
DATA PERIOD: [e.g., "6 months (February - August 2025)"]

Follow .claude/FULL_XPARCEL_ANALYSIS_TEMPLATE.md for complete specifications.

REQUIREMENTS:
- 6 Excel tabs (Executive Summary, Weight Analysis, Zone Analysis, Rate Cards, Carrier Breakdown, FirstMile Advantages)
- FirstMile blue branding (#366092)
- Weight profile: 1-15oz, 15.99oz, 1-10lb, 11-15lb, 16-20lb, 21+lb
- Zone × Weight matrices for top services
- 12% savings projection (adjust based on data)

OUTPUT: Professional, prospect-ready deliverable
```

**Key Requirements**:
- ✅ 6 tabs with FirstMile branding
- ✅ Correct weight tier structure (29 tiers matching rate card)
- ✅ Zone × Weight matrices for incumbent carriers
- ✅ Green-highlighted savings (#00B050)
- ✅ Professional formatting (centered headers, right-aligned currency)

**Reference Example**: `[03-RATE-CREATION]_Stackd_Logistics/Stackd_Logistics_FirstMile_Xparcel_Savings_Analysis_*.xlsx`

---

## 2. Performance Report (Post-Win)

**Purpose**: Monthly/quarterly performance analysis for active customers

**Use Case**: [07-CLOSED-WON] stage - Customer success reporting

**Template**: See CLAUDE.md Performance Reporting section

**Output File**: `FirstMile_Xparcel_Performance_[Customer]_[YYYYMMDD_HHMM].xlsx`

**Standard Prompt**:
```
Create a FirstMile Xparcel Performance Report for [CUSTOMER NAME].

DATA FILE: [path/to/performance_data.csv]
REPORT PERIOD: [e.g., "August 7 - September 19, 2025"]
SERVICE LEVEL: [Xparcel Priority | Xparcel Expedited | Xparcel Ground]

REQUIREMENTS:
- 9 Excel tabs (Executive Summary, SLA Compliance, Transit Performance, Geographic Distribution, Zone Analysis, Operational Metrics, In-Transit Detail, Notes & Assumptions, Brand Style Guide)
- SLA compliance FIRST (primary metric)
- Color-coded SLA compliance (red/yellow/green)
- FirstMile blue branding (#366092)
- In-transit status tracking

OUTPUT: Customer-facing performance deliverable
```

**Key Requirements**:
- ✅ SLA compliance is PRIMARY metric (always first)
- ✅ 9 tabs with performance data
- ✅ Color-coded performance thresholds
- ✅ In-transit tracking with SLA window indicator
- ✅ Geographic hub mapping

**SLA Windows**:
- Xparcel Priority: 3 days (1-3 day service)
- Xparcel Expedited: 5 days (2-5 day service)
- Xparcel Ground: 8 days (3-8 day service)

---

## 3. Invoice Audit Analysis

**Purpose**: Carrier invoice auditing to identify overcharges and refund opportunities

**Use Case**: [02-DISCOVERY-COMPLETE] or [03-RATE-CREATION] - Value demonstration

**Output File**: `[Customer]_Invoice_Audit_Analysis_v[X.X].xlsx`

**Standard Prompt**:
```
Create an Invoice Audit Analysis for [CUSTOMER NAME].

DATA FILES:
- Invoice data: [path/to/invoice_data.csv]
- Contracted rates: [path/to/rate_card.xlsx]

REQUIREMENTS:
- Compare invoiced rates vs contracted rates
- Identify billable weight discrepancies
- Calculate refund opportunities by carrier/service
- Flag unauthorized surcharges
- Generate dispute documentation

OUTPUT: 5-tab audit report (Summary, Overcharges, Weight Issues, Unauthorized Charges, Dispute Documentation)
```

**Key Requirements**:
- ✅ Rate variance analysis
- ✅ Billable weight validation
- ✅ Surcharge identification
- ✅ Refund opportunity calculation
- ✅ Dispute-ready documentation

**Common Scripts**: `invoice_audit_builder_v*.py`

---

## 4. Rate Card / Pricing Matrix

**Purpose**: Visual rate card showing zone × weight pricing for customer proposals

**Use Case**: [03-RATE-CREATION] - Pricing deliverable for prospects

**Output File**: `[Customer]_FirstMile_Xparcel_Rate_Card_[YYYYMMDD].xlsx`

**Standard Prompt**:
```
Create a FirstMile Xparcel Rate Card for [CUSTOMER NAME].

REQUIREMENTS:
- Zone × Weight matrix (Zones 1-8 columns, Weight tiers rows)
- Separate tabs for each service level (Ground, Expedited, Priority)
- FirstMile blue branding
- Weight structure: 1-15oz, 15.99oz, 1-10lb, 11-15lb, 16-20lb, 21+lb
- Clear rate display with currency formatting

OUTPUT: Clean, easy-to-read rate card for customer reference
```

**Key Requirements**:
- ✅ Zone × Weight matrix format
- ✅ Correct weight tier structure
- ✅ Clean, simple formatting
- ✅ Service level tabs
- ✅ Currency formatting ($#,##0.00)

**Common Scripts**: `create_pricing_matrix.py`, `tier_tool_*.py`

---

## 5. Volume Assumptions / Revenue Projection

**Purpose**: Revenue modeling based on volume assumptions for internal forecasting

**Use Case**: [03-RATE-CREATION] or [04-PROPOSAL-SENT] - Internal planning

**Output File**: `[Customer]_Revenue_Projections_[YYYYMMDD].xlsx`

**Standard Prompt**:
```
Create a Revenue Projection Model for [CUSTOMER NAME].

HISTORICAL DATA: [path/to/historical_volume.csv]
RATE CARD: [path/to/firstmile_rates.xlsx]

REQUIREMENTS:
- Historical volume analysis (by service, zone, weight)
- Volume assumptions (conservative, realistic, aggressive)
- Revenue calculations by scenario
- Monthly/annual projections
- Service mix breakdown

OUTPUT: 4-tab revenue model (Historical, Assumptions, Projections, Summary)
```

**Key Requirements**:
- ✅ Historical volume breakdown
- ✅ 3 scenario projections
- ✅ Monthly/annual totals
- ✅ Service mix analysis
- ✅ Growth assumptions

**Common Scripts**: `revenue_calculator.py`, `volume_assumptions_generator.py`

---

## 6. PLD Analysis (Internal)

**Purpose**: Comprehensive parcel-level detail analysis for internal understanding

**Use Case**: [02-DISCOVERY-COMPLETE] or [03-RATE-CREATION] - Internal analysis

**Output File**: `[Customer]_PLD_Analysis_Summary_[YYYYMMDD].xlsx`

**Standard Prompt**:
```
Perform comprehensive PLD analysis for [CUSTOMER NAME].

DATA FILE: [path/to/pld_data.csv]

REQUIREMENTS:
- Volume profile (total, daily avg, marketplace mix)
- Carrier mix (volume/spend by carrier)
- Service level distribution
- Expanded weight distribution (see CLAUDE.md for billable weight rules)
- Dimensional analysis (avg dims, cubic volume)
- Zone distribution (1-8, Regional vs Cross-Country)
- Geographic distribution (top 10 states)
- Cost analysis (total, avg, median)
- Billable weight impact analysis

OUTPUT: Multi-tab analysis workbook (10+ tabs)
```

**Key Requirements**:
- ✅ Comprehensive volume breakdown
- ✅ Billable weight rules applied
- ✅ Geographic distribution
- ✅ Cost analysis
- ✅ Optimization opportunities

**Reference**: [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md)

**Common Scripts**: `pld_analysis.py`, `weight_analysis.py`, `dimension_analysis.py`

---

## Common Formatting Standards (All Excel Deliverables)

### FirstMile Brand Colors
```python
FM_BLUE = "366092"        # Primary brand color
FM_WHITE = "FFFFFF"       # Header text
FM_GREEN = "00B050"       # Savings/positive highlights
FM_RED = "FFC7CE"         # Alerts/negative (80-89%)
FM_YELLOW = "FFEB84"      # Warnings (90-94%)
FM_LIGHT_GREEN = "C6EFCE" # Success (95-100%)
FM_LIGHT_GRAY = "F2F2F2"  # Alternating rows
```

### Font Standards
- **Main Headers**: Calibri 18pt Bold, White on Blue
- **Section Headers**: Calibri 14pt Bold, White on Blue
- **Table Headers**: Calibri 12pt Bold, White on Blue
- **Body Text**: Calibri 11pt
- **Emphasis**: Calibri 12pt Bold (green for savings)

### Cell Formatting
```python
# Currency
cell.number_format = '$#,##0.00'

# Percentage
cell.number_format = '0.0%'

# Number with commas
cell.number_format = '#,##0'

# Date
cell.number_format = 'mmmm dd, yyyy'
```

### Alignment
- **Text**: Left aligned
- **Numbers**: Right aligned
- **Currency**: Right aligned
- **Percentages**: Center aligned
- **Headers**: Center aligned (horizontal and vertical)

### Column Widths
- **Text**: 16-20 characters
- **Numbers**: 12-16 characters
- **Currency**: 15-18 characters
- **Description**: 80+ characters

---

## Quality Checklist (All Excel Deliverables)

### Before Sending to Prospect/Customer:
- [ ] Customer name in title/header
- [ ] Correct date and data period
- [ ] FirstMile blue branding (#366092)
- [ ] All currency formatted ($#,##0.00)
- [ ] All percentages formatted (0.0%)
- [ ] Column widths appropriate
- [ ] No merged cells except headers
- [ ] No internal notes or debugging content
- [ ] Professional tab names
- [ ] File saved with descriptive name
- [ ] File size <5MB for email delivery
- [ ] Spell check completed
- [ ] Numbers validated (no negatives, realistic values)
- [ ] Formulas hidden (values only for prospect deliverables)

---

## File Naming Conventions

### Prospect Deliverables
```
[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx
[Customer]_FirstMile_Xparcel_Rate_Card_YYYYMMDD.xlsx
[Customer]_Invoice_Audit_Analysis_vX.X.xlsx
```

### Customer Deliverables
```
FirstMile_Xparcel_Performance_[Customer]_YYYYMMDD_HHMM.xlsx
```

### Internal Analysis
```
[Customer]_PLD_Analysis_Summary_YYYYMMDD.xlsx
[Customer]_Revenue_Projections_YYYYMMDD.xlsx
[Customer]_Volume_Assumptions_vX.X.xlsx
```

---

## Quick Command Reference

### Generate Full Xparcel Analysis
```bash
cd "[STAGE]_Customer_Name"
python full_xparcel_analysis.py --customer "Customer Name" --data "pld_data.csv" --period "6 months"
```

### Generate Performance Report
```bash
cd "[07-CLOSED-WON]_Customer_Name"
python firstmile_orchestrator.py --customer "Customer Name" --data "performance_data.csv" --service "Xparcel Ground"
```

### Generate Invoice Audit
```bash
cd "[STAGE]_Customer_Name"
python invoice_audit_builder_v31.py --invoices "invoice_data.csv" --rates "rate_card.xlsx"
```

### Generate Rate Card
```bash
cd "[03-RATE-CREATION]_Customer_Name"
python create_pricing_matrix.py --zones 8 --weights "1oz-10lb" --output "rate_card.xlsx"
```

---

## Troubleshooting

### Common Issues

**Issue**: Weight tiers don't match FirstMile rate card
**Solution**: Use [FULL_XPARCEL_ANALYSIS_TEMPLATE.md](FULL_XPARCEL_ANALYSIS_TEMPLATE.md) weight tier function (1-15oz, 15.99oz, 1-10lb structure)

**Issue**: Excel formatting is broken/unprofessional
**Solution**: Use openpyxl with explicit Font, Fill, Alignment objects (see template)

**Issue**: Numbers don't add up / data validation errors
**Solution**: Check for NaN values, validate sum totals, ensure consistent time periods

**Issue**: File too large for email
**Solution**: Remove unnecessary tabs, compress images, save as .xlsx (not .xls)

**Issue**: Customer name/date is wrong
**Solution**: Use template prompt with correct parameters, validate before saving

---

## Related Documentation

- [FULL_XPARCEL_ANALYSIS_TEMPLATE.md](FULL_XPARCEL_ANALYSIS_TEMPLATE.md) - Complete Full Xparcel process
- [PLD_DISCOVERY_ANALYSIS_PROMPT.md](PLD_DISCOVERY_ANALYSIS_PROMPT.md) - PLD analysis methodology
- [FIRSTMILE.md](FIRSTMILE.md) - FirstMile brand standards
- [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md) - Deal folder structure

---

**Last Updated**: October 8, 2025
**Maintained By**: Brett Walker
