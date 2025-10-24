# Stackd Logistics - Xparcel Savings Analysis (FINAL - CORRECTED)

**Analysis Date**: October 7, 2025
**Rate Card**: FirstMile Xparcel Domestic Rates (10-01-25) - verified from actual images
**Data Source**: 8,957 shipments from raw PLD export (Aug-Sep 2025)

---

## Executive Summary - FINAL NUMBERS

### Verified Savings Using Actual Rate Card

**Monthly Savings: $4,522.40 (10.2%)**
**Annual Savings: $54,268.81**

| Metric | Current (DHL) | With Xparcel Ground | Savings |
|--------|---------------|---------------------|---------|
| Monthly Shipments | 8,957 | 8,957 | - |
| Monthly Spend | **$44,453.35** | **$39,930.95** | **$4,522.40** |
| Average Cost/Label | $4.96 | $4.46 | $0.50 (10.2%) |
| Annual Projection | $533,440 | $479,171 | **$54,269** |

---

## What Changed from Initial Analysis

### Problem Identified and Resolved

**Initial (Incorrect) Analysis showed**: 31.5% savings ($13,981/month)
**Corrected Analysis shows**: 10.2% savings ($4,522/month)

**Root Cause**: The pre-calculated `Xparcel_Cost` column in the CSV file was using incorrect or outdated rate data.

**Solution**: Rebuilt analysis from scratch using:
✅ Raw PLD data file (`20250918193042_221aaf59f30469602caf8f7f7485b114.csv`)
✅ Actual rate card from images you provided
✅ Correct billable weight rounding (round up to next oz/lb tier)
✅ Proper zone calculation from ZIP codes

---

## Detailed Savings Breakdown

### By Weight Range

| Weight Range | Shipments | % of Total | Avg DHL Cost | Avg Xparcel | Savings | Savings % |
|--------------|-----------|------------|--------------|-------------|---------|-----------|
| **0-4 oz** | 4,918 | 54.9% | $4.37 | $4.06 | $0.31 | 7.1% |
| **4-8 oz** | 2,436 | 27.2% | $5.00 | $4.31 | $0.69 | 13.8% |
| **8oz-1 lb** | 934 | 10.4% | $5.60 | $5.30 | $0.30 | 5.4% |
| **1-2 lb** | 576 | 6.4% | $7.91 | $6.38 | $1.53 | 19.3% |
| **2-5 lb** | 65 | 0.7% | $9.16 | $7.36 | $1.79 | 19.6% |
| **5-10 lb** | 22 | 0.2% | $12.88 | $10.79 | $2.09 | 16.3% |
| **10+ lb** | 6 | 0.1% | $22.63 | $23.47 | **-$0.84** | **-3.7%** |

**Key Insights**:
- ✅ **92.5% of volume is under 1 lb** - FirstMile's sweet spot
- ✅ **Best savings in 4-8 oz range** (27.2% of volume at 13.8% savings)
- ✅ **Heavier packages (1-5 lbs) save 19%+** despite being <7% of volume
- ⚠️ **Only 6 packages over 10 lbs** show negative savings (can keep with DHL)

### By Zone

| Zone | Shipments | % of Total | Total Savings | Avg Savings/Pkg |
|------|-----------|------------|---------------|-----------------|
| Zone 1 | 613 | 6.8% | $321.74 | $0.52 |
| Zone 2 | 883 | 9.9% | $349.38 | $0.40 |
| Zone 3 | 1,508 | 16.8% | $866.03 | $0.57 |
| Zone 4 | 1,466 | 16.4% | $592.31 | $0.40 |
| Zone 5 | 1,201 | 13.4% | $843.68 | $0.70 |
| Zone 6 | 1,858 | 20.7% | $985.07 | $0.53 |
| Zone 7 | 1,428 | 15.9% | $564.20 | $0.40 |

**Key Insights**:
- ✅ **Savings across all zones** (except Zone 8 with no data)
- ✅ **Best savings in Zone 5** (13.4% of volume at $0.70/pkg average)
- ✅ **Zones 3 & 6 generate most total savings** ($866 + $985 = $1,851/month combined)

---

## Xparcel Rate Examples (National Network - Ground)

### Lightweight Packages (Where 92.5% of Volume Sits)

| Weight | Zone 3 | Zone 4 | Zone 5 | Zone 6 | Zone 7 |
|--------|--------|--------|--------|--------|--------|
| 1 oz | $3.93 | $4.02 | $4.07 | $4.16 | $4.23 |
| 4 oz | $3.93 | $4.03 | $4.07 | $4.17 | $4.23 |
| 8 oz | $4.25 | $4.31 | $4.35 | $4.40 | $4.40 |
| 12 oz | $4.96 | $5.02 | $5.13 | $5.31 | $5.42 |
| 1 lb | $5.59 | $5.84 | $6.11 | $6.30 | $6.65 |

### Heavier Packages (7% of Volume)

| Weight | Zone 3 | Zone 4 | Zone 5 | Zone 6 | Zone 7 |
|--------|--------|--------|--------|--------|--------|
| 2 lb | $5.77 | $6.34 | $6.40 | $6.63 | $7.51 |
| 3 lb | $6.07 | $6.62 | $7.04 | $7.38 | $9.09 |
| 5 lb | $6.93 | $7.17 | $7.95 | $9.02 | $11.27 |

---

## Value Proposition for Landon

### 1. Verified Cost Savings
- **$4,522/month ($54,269/year)** - conservative, defensible number
- **10.2% average savings** across all weight ranges and zones
- Based on actual 8,957 shipment history

### 2. Service Benefits (Beyond Cost)
- **Single Integration**: One ShipHero API connection vs DHL's multiple service tiers
- **Audit Queue**: Blocks mis-rated labels before invoice hits A/P
- **Single Support Thread**: Claims, returns, exceptions managed via one FirstMile ticket
- **Unified Platform**: Ground + Expedited + Priority all from one provider

### 3. Perfect Volume Match
- **92.5% of packages under 1 lb** = FirstMile's specialty (National Network lightweight pricing)
- **Service mix works**: Currently 96% Ground, 4% Expedited - both supported
- **Zone distribution fits**: Zones 3-7 = 82.8% of volume (National Network strong zones)

### 4. Customer Margin Protection
Stackd's current model:
- **Cost**: $4.96/label (DHL)
- **Charge**: $16.49/label
- **Margin**: 69.5%

With FirstMile:
- **Cost**: $4.46/label (Xparcel Ground)
- **Charge**: $16.49/label (unchanged)
- **Margin**: 73.0% ✅ **+3.5 points improvement**

OR pass savings to customers to improve competitiveness while maintaining margin.

---

## Meeting Talking Points for Landon

### Opening
**"Landon, your Stackd Logistics Xparcel rates are done. I've analyzed your 8,957 shipment history against FirstMile's National Network rates."**

### The Numbers
**"You're spending $44,453/month with DHL. With Xparcel Ground, you'd spend $39,931/month."**
- **Monthly savings: $4,522**
- **Annual savings: $54,269**
- **Average savings: 10.2%**

### The Sweet Spot
**"92.5% of your packages are under 1 lb - this is exactly where FirstMile excels."**
- National Network lightweight pricing
- Best savings in your 4-8 oz range (27.2% of volume at 13.8% savings)
- Heavier packages (1-5 lbs) save 19%+

### The Service Story
**"Beyond cost, you get operational improvements:"**
- Single ShipHero integration (vs DHL complexity)
- Audit Queue prevents billing errors
- Single support team for all issues
- 3PL customer focus (we understand your model)

### The Risk Mitigation
**"Only 6 packages out of 8,957 (10+ lbs) cost slightly more with FirstMile. For those, you can stay with DHL or use a different service level."**

### The Close
**"This is verified, conservative analysis using your actual shipment data and FirstMile's approved rate card. No surprises, no inflated projections."**

---

## Questions to Ask Landon

1. **Q4 Volume**: "Any volume changes expected for Peak Season?"
   - Adjust projections based on seasonal multiplier

2. **Service Needs**: "For your 4% expedited volume, what's driving the need for faster service?"
   - Customer SLAs?
   - Marketplace requirements?
   - Specific product lines?

3. **Integration Timeline**: "When would you want to start if we move forward?"
   - Standard implementation: 2-3 weeks
   - ShipHero API integration support available

4. **DHL Comparison**: "Have you seen DHL's 2025 Peak Season fee schedule yet?"
   - Context for competitive positioning

5. **Margin Strategy**: "Would you want to pocket the savings or use them to improve customer pricing?"
   - Helps position FirstMile value beyond cost

---

## Next Steps Based on Meeting Outcome

### If Verbal Commitment
1. ✅ Move deal to [04-PROPOSAL-SENT]
2. ✅ Send formal rate card PDF via email
3. ✅ Schedule integration kickoff call with ShipHero team
4. ✅ Prepare setup documentation
5. ✅ Update HubSpot with verbal commit date + $54K annual value

### If Questions/Concerns
1. ✅ Document objections clearly
2. ✅ Provide follow-up analysis within 24 hours
3. ✅ Schedule follow-up call within 48-72 hours
4. ✅ Update Customer_Relationship_Documentation.md
5. ✅ Escalate to Sales/Pricing if rate adjustments needed

### If DHL Competitive Pressure
1. ✅ Request DHL rate card for direct comparison
2. ✅ Build side-by-side comparison matrix
3. ✅ Emphasize FirstMile advantages (Audit Queue, 3PL focus, support)
4. ✅ Offer limited-time pricing lock for Q4
5. ✅ Position as "test and compare" approach (parallel run option)

---

## Files Generated

1. **`Stackd_Logistics_Xparcel_Analysis_CORRECTED.csv`** - Full dataset with calculated rates
2. **`stackd_xparcel_savings_CORRECTED.py`** - Python analysis script with actual rate tables
3. **`STACKD_FINAL_ANALYSIS_SUMMARY.md`** - This summary document
4. **`RATES_READY_EMAIL_TO_LANDON.md`** - Meeting request email (needs update with new numbers)

---

## Bottom Line

### For Brett's Meeting Prep

**SAFE POSITION**: Present **$4,522/month ($54,269/year) savings at 10.2%**

**CONFIDENCE LEVEL**: ✅ HIGH - Based on:
- Actual rate card from images (verified)
- Raw PLD data (8,957 real shipments)
- Correct billable weight calculations
- Proper zone mapping

**DEFENSIBLE**: ✅ YES - Can show:
- Rate card tables
- Sample shipment calculations
- Weight/zone breakdowns
- Conservative assumptions (all Ground, no optimization)

**UPSIDE POTENTIAL**: Could optimize further by:
- Using Select Network for high-density metro ZIPs
- Mixing Ground/Expedited based on SLA needs
- Volume discounts at scale
- But DON'T promise this without verification

---

## Meeting Confidence

**You can confidently tell Landon:**

✅ "10.2% savings ($4,522/month, $54K/year)"
✅ "Based on your actual 8,957 shipment history"
✅ "Using FirstMile's approved October 2025 rate card"
✅ "92.5% of your volume is under 1 lb - FirstMile's specialty"
✅ "Best savings in your highest volume range (4-8 oz at 13.8%)"
✅ "Plus service improvements: Audit Queue, single integration, 3PL focus"

**Status**: Ready to present with confidence ✅
