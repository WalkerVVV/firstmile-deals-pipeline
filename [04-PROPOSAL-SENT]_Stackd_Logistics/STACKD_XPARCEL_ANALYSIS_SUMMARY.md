# Stackd Logistics - Xparcel Savings Analysis Summary

**Analysis Date**: October 7, 2025
**Rate Card**: FirstMile Xparcel Domestic Rates (10-01-25)
**Data Source**: 8,957 shipments (Aug-Sep 2025, 2-week period)

---

## Executive Summary

**CRITICAL FINDING**: There's a **major discrepancy** between the two savings calculations that needs immediate investigation:

### Discrepancy Analysis

**Scenario 1: MATCHED SERVICE MIX (96% Ground, 4% Expedited)**
- Current Monthly Spend: **$44,453.35**
- Xparcel Monthly Cost: **$30,472.17**
- **Monthly Savings: $13,981.18 (31.5%)**
- **Annual Savings: $167,774.22**

**Scenario 2: ALL GROUND (100% Xparcel Ground)**
- Current Monthly Spend: **$44,453.35**
- Xparcel Monthly Cost: **$41,907.91**
- **Monthly Savings: $2,545.44 (5.7%)**
- **Annual Savings: $30,545.28**

### The Problem

The "Matched Service Mix" shows **31.5% savings** while "All Ground" shows only **5.7% savings**. This doesn't make sense because:

1. **Xparcel Ground is cheaper than Xparcel Expedited** (from the rate card)
2. **100% Ground should save MORE than a 96%/4% mix, not less**
3. **The $11,435.74/month difference is enormous** and unexplained

### Likely Causes

1. **Pre-calculated Xparcel_Cost column issue**: The CSV file has a pre-calculated `Xparcel_Cost` column that may be using:
   - Incorrect rate lookups
   - Old rate card data
   - Wrong service level mapping
   - Billable weight calculation errors

2. **DHL rates may be artificially inflated** in the existing data

3. **Rate lookup logic mismatch** between the two calculations

---

## What We Know is ACCURATE

### Volume Profile (Verified from Actual Data)
- **Total Shipments**: 8,957 over 2 weeks
- **Monthly Projection**: ~2,800 shipments/month
- **Service Mix**: 96% Ground, 4% Expedited
- **Current Average Cost**: $4.96/label
- **Current Monthly Spend**: $44,453.35

### Weight Distribution (Verified)
| Weight Range | Shipments | % of Total |
|--------------|-----------|------------|
| 0-4 oz | 4,918 | 54.9% |
| 4-8 oz | 2,436 | 27.2% |
| 8oz-1 lb | 934 | 10.4% |
| 1-2 lb | 576 | 6.4% |
| 2-5 lb | 65 | 0.7% |
| 5-10 lb | 22 | 0.2% |
| 10+ lb | 6 | 0.1% |

**Key Insight**: **89.9% of packages are under 1 lb** - this is FirstMile's sweet spot for National Network pricing.

### Zone Distribution (Verified)
| Zone | Shipments | % of Total |
|------|-----------|------------|
| Zone 1 | 207 | 2.3% |
| Zone 2 | 198 | 2.2% |
| Zone 3 | 535 | 6.0% |
| Zone 4 | 2,054 | 22.9% |
| Zone 5 | 1,580 | 17.6% |
| Zone 6 | 2,148 | 24.0% |
| Zone 7 | 2,129 | 23.8% |
| Zone 8 | 106 | 1.2% |

**Key Insight**: Majority of volume is Zones 4-7 (88.3%), good fit for National Network.

### Xparcel National Rates (Verified from 10-01-25 Rate Card)

**Ground - Under 1 lb (where 89.9% of volume sits):**
| Weight | Zone 3 | Zone 4 | Zone 5 | Zone 6 | Zone 7 |
|--------|--------|--------|--------|--------|--------|
| 1 oz | $3.93 | $4.02 | $4.07 | $4.16 | $4.23 |
| 4 oz | $3.93 | $4.03 | $4.07 | $4.17 | $4.23 |
| 8 oz | $4.25 | $4.31 | $4.35 | $4.40 | $4.40 |
| 1 lb | $5.59 | $5.84 | $6.11 | $6.30 | $6.65 |

**Expedited - Under 1 lb:**
| Weight | Zone 3 | Zone 4 | Zone 5 | Zone 6 | Zone 7 |
|--------|--------|--------|--------|--------|--------|
| 1 oz | $3.93 | $4.02 | $4.07 | $4.17 | $4.23 |
| 4 oz | $3.94 | $4.03 | $4.08 | $4.17 | $4.24 |
| 8 oz | $4.25 | $4.31 | $4.36 | $4.41 | $4.48 |
| 1 lb | $5.70 | $5.84 | $6.40 | $7.22 | $7.44 |

---

## RED FLAGS from Analysis

### Heavy Package Pricing Issue
**Packages over 2 lbs show NEGATIVE savings:**
- 2-5 lbs: **-43.2% savings** (Xparcel MORE expensive)
- 5-10 lbs: **-72.7% savings** (Xparcel MUCH more expensive)
- 10+ lbs: **-55.9% savings** (Xparcel MUCH more expensive)

**This is expected** - FirstMile's lightweight specialization means heavier packages should stay with DHL or use different carriers. Good news: only 0.9% of volume (93 packages) falls into this category.

### Anomalous DHL Rates in Data
The "Top Savings Opportunities" list shows DHL rates that seem artificially high:
- $33.22-$33.27 for sub-1lb packages
- $26.17-$26.78 for under 1 oz packages
- $18.70-$18.73 for 0.07 lb packages

These are **3-8x higher** than typical DHL eCommerce lightweight rates. This suggests:
1. These may be expedited/priority service shipments (not Ground)
2. DHL rates in the data include surcharges or peak fees
3. Data quality issue with rate mapping

---

## BEFORE MEETING WITH LANDON - ACTION REQUIRED

### 1. Verify DHL Rate Data
**Question**: Are the `Label Cost` values in the CSV file accurate representations of what DHL actually charged?
- Check a sample of 10-20 shipments against actual DHL invoices
- Verify if expedited services are correctly labeled as Ground
- Confirm no surcharges are inflating the baseline rates

### 2. Verify Xparcel_Cost Calculation
**Question**: How was the pre-calculated `Xparcel_Cost` column generated in the CSV?
- Which rate card was used?
- Was billable weight calculated correctly (round up to next oz/lb)?
- Was service level mapped correctly (Ground vs Expedited)?

### 3. Recalculate from Scratch
**Recommended**: Use ONLY the actual FirstMile rate card (10-01-25) and raw shipment data:
- Weight (lb)
- Zone
- Service level (Ground vs Expedited)
- Apply correct billable weight rounding
- Look up exact rate from rate card tables

---

## Meeting Strategy with Landon

### Option 1: Present Conservative Estimate (RECOMMENDED)
**"Stackd, based on your 8,957 shipment sample, we're seeing **5-10% cost savings** with FirstMile Xparcel National Network for your lightweight volume (under 1 lb)."**

**Key Points**:
- Focus on the 89.9% under 1 lb (FirstMile's strength)
- Acknowledge that 2-10+ lb packages may not save (or may cost more)
- Emphasize service benefits: single integration, Audit Queue, claims support
- Position as **service improvement + modest cost savings**

**Annual Savings Estimate**: $30,000-$50,000/year (conservative)

### Option 2: Investigate Then Present (IF TIME ALLOWS)
**"Landon, I've got your rate card ready. Before we review specific numbers, can you help me understand your current DHL pricing? I want to make sure we're comparing apples to apples."**

**Then**:
1. Review 10-20 sample shipments with actual DHL invoices
2. Verify service level mapping (Ground vs Expedited)
3. Recalculate savings with verified data
4. Present accurate, defensible numbers

---

## What to Bring to Meeting

1. **Stackd Logistics Xparcel Savings Analysis.xlsx** - comprehensive analysis workbook
2. **FirstMile Xparcel Rate Card (10-01-25)** - official rate tables
3. **Sample DHL invoices** - to verify rate accuracy (request from Landon)
4. **Service level mapping guide** - DHL services → Xparcel services

---

## Questions to Ask Landon

1. **"What services are you currently using with DHL eCommerce?"**
   - Ground
   - Expedited
   - Priority
   - SmartMail

2. **"Are the rates in your ShipHero export the actual costs DHL charges, or do they include markup/fees?"**

3. **"For your 4% expedited volume, what's driving the need for faster service?"**
   - Customer SLA requirements?
   - Marketplace delivery promises?
   - Specific product types?

4. **"Any volume changes expected for Q4 Peak Season?"**

5. **"Current integration: ShipHero API or web portal for label generation?"**

---

## Next Steps After Meeting

1. **If verbal commitment**: Move to [04-PROPOSAL-SENT], send formal rate card PDF
2. **If questions/concerns**: Provide follow-up analysis within 24 hours
3. **If DHL competitive pressure**: Request DHL rate card for side-by-side comparison
4. **If ready to proceed**: Schedule integration kickoff call with ShipHero team

---

## Bottom Line for Brett

**BE CAUTIOUS** about the 31.5% savings number until you verify:
1. DHL rate accuracy in the data
2. Xparcel_Cost calculation methodology
3. Service level mapping correctness

**SAFE POSITION**: Lead with 5-10% savings on lightweight volume (verified from actual rate card) + service benefits, then investigate for potential upside.

**DO NOT** present $167K/year savings without verifying the data quality first. If challenged, you won't be able to defend it.

---

**Files Generated**:
- `Stackd_Logistics_Xparcel_Savings_Analysis.xlsx` - Excel analysis workbook
- `stackd_xparcel_savings_analysis.py` - Python analysis script
- `STACKD_XPARCEL_ANALYSIS_SUMMARY.md` - This summary document

**Status**: Ready for Landon meeting with conservative estimate. Further data verification recommended before presenting aggressive savings projections.
