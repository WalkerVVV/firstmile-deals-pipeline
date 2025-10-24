# JOSH'S FROGS - DRY GOODS SHIPPING ANALYSIS

**Generated:** September 29, 2025
**Analysis Type:** Dry Goods Only (excludes live animal express services)
**Data Source:** Actual service volume breakdown

---

## Service Volume Breakdown (Dry Goods Only)

### Total Dry Goods Volume: **139,244 shipments/month**

| Service | Monthly Volume | % of DG Volume |
|---------|----------------|----------------|
| **USPS Ground Advantage** | 99,675 | 71.6% |
| **UPS Ground** | 12,751 | 9.2% |
| **FedEx Ground** | 10,843 | 7.8% |
| **FedEx Home Delivery** | 9,195 | 6.6% |
| **USPS Priority Mail** | 3,034 | 2.2% |
| **DHL Ground** | 2,969 | 2.1% |
| **DHL Expedited** | 448 | 0.3% |
| **UPS SurePost** | 318 | 0.2% |
| **USPS Ground** | 11 | 0.0% |
| **TOTAL** | **139,244** | **100.0%** |

---

## Carrier Family Summary

| Carrier | Volume | % of DG Volume | Services Used |
|---------|--------|----------------|---------------|
| **USPS** | 102,720 | 73.8% | Ground Advantage, Priority Mail, Ground |
| **UPS** | 13,069 | 9.4% | Ground, SurePost |
| **FedEx** | 20,038 | 14.4% | Ground, Home Delivery |
| **DHL** | 3,417 | 2.5% | Ground, Expedited |

---

## Key Characteristics of Dry Goods Shipments

### Weight Profile (Estimated)
- **60-70%** under 1 lb (small supplies, accessories)
- **25-30%** between 1-5 lbs (medium packages)
- **5-10%** between 5-15 lbs (bulk orders)

### Primary Service Types
- **USPS Ground Advantage dominates** at 71.6% of dry goods volume
- Ground services represent **97%+** of dry goods shipments
- Expedited services minimal (DHL Expedited, USPS Priority = 2.5%)

### Geographic Distribution (Typical e-Commerce)
- Zones 3-5: ~68% of volume (regional/mid-range)
- Zones 1-2: ~15% (local)
- Zones 6-8: ~17% (cross-country)

---

## FirstMile Xparcel Savings Estimates

### Current Carrier Costs (Estimated)

**USPS Ground Advantage** (99,675 pkgs @ ~$5.50 avg)
- Current monthly spend: ~$548,213
- Xparcel Ground rate: ~$4.20 avg
- Potential savings: ~$129,578/month (23.6%)

**UPS Ground** (12,751 pkgs @ ~$10.50 avg)
- Current monthly spend: ~$133,886
- Xparcel Ground rate: ~$5.00 avg
- Potential savings: ~$70,131/month (52.4%)

**FedEx Ground + Home Delivery** (20,038 pkgs @ ~$10.25 avg)
- Current monthly spend: ~$205,390
- Xparcel Ground rate: ~$5.00 avg
- Potential savings: ~$105,200/month (51.2%)

**DHL Services** (3,417 pkgs @ ~$9.50 avg)
- Current monthly spend: ~$32,462
- Xparcel Ground rate: ~$4.80 avg
- Potential savings: ~$16,060/month (49.5%)

**USPS Priority Mail** (3,034 pkgs @ ~$12.50 avg)
- Current monthly spend: ~$37,925
- Xparcel Expedited rate: ~$6.50 avg
- Potential savings: ~$18,204/month (48.0%)

---

## Total Dry Goods Savings Projection

| Metric | Current State | With FirstMile Xparcel | Savings |
|--------|---------------|------------------------|---------|
| **Monthly Spend** | ~$957,876 | ~$618,703 | **~$339,173** |
| **Annual Spend** | ~$11,494,512 | ~$7,424,436 | **~$4,070,076** |
| **Avg Cost/Pkg** | $6.88 | $4.44 | **$2.44 (35.4%)** |

### Conservative Estimate
Assuming 30% average savings (accounting for USPS GA's already competitive rates):
- **Monthly savings: ~$287,363**
- **Annual savings: ~$3,448,354**

---

## Services EXCLUDED from This Analysis

**Express/Overnight Services (Live Animals):**
- UPS Next Day Air (3,374 shipments)
- UPS 2nd Day Air (2,895 shipments)
- UPS 3-Day Select (165 shipments)
- FedEx Priority Overnight (3,704 shipments)
- FedEx Standard Overnight (1,311 shipments)
- FedEx Express Saver (2,604 shipments)
- FedEx 2-Day (16,833 shipments)
- **Total Excluded: ~30,886 shipments/month**

These services require specialized handling for live insects/animals and should be analyzed separately with temperature-controlled routing considerations.

---

## FirstMile Implementation for Dry Goods

### Recommended Service Mapping

| Current Service | FirstMile Xparcel Service | Transit Time | Rate Advantage |
|-----------------|---------------------------|--------------|----------------|
| USPS Ground Advantage | Xparcel Ground | 3-8 days | ~20-25% |
| UPS Ground | Xparcel Ground | 3-8 days | ~50-55% |
| FedEx Ground/Home | Xparcel Ground | 3-8 days | ~48-52% |
| DHL Ground | Xparcel Ground | 3-8 days | ~45-50% |
| USPS Priority Mail | Xparcel Expedited | 2-5 days | ~45-50% |
| DHL Expedited | Xparcel Expedited | 2-5 days | ~40-45% |

### Network Strategy
- **USPS Ground Advantage volume** → FirstMile National Network (all ZIPs)
- **UPS/FedEx Ground volume** → FirstMile Select Network (metro injection) for max savings
- **Priority/Expedited needs** → Xparcel Expedited (2-5 day service)

### Implementation Benefits
1. **Carrier Consolidation**: 4 carriers → 1 FirstMile relationship
2. **Single Integration**: One API for all dry goods shipments
3. **Unified Support**: Single support thread for claims/returns
4. **Simplified Billing**: One invoice vs. multiple carrier bills
5. **No Minimums**: Scale up/down seasonally without commitment

---

## Next Steps

1. **Data Validation**: Confirm average costs per service from actual invoices
2. **Weight Distribution**: Verify typical package weights for dry goods
3. **Zone Analysis**: Review destination ZIP distribution
4. **Pilot Program**: Start with UPS/FedEx Ground volume (22,789 pkgs/month)
5. **Integration**: Plan API setup with Josh's Frogs fulfillment system

---

## Files Reference

- `247bef97-8663-431e-b2f5-dd2ca243633d.csv` - Original PLD data
- `Joshs_Frogs_Complete_Audit_v3.1.xlsx` - Full analysis (includes all services)
- `DRY_GOODS_SUMMARY.md` - This document

---

**Contact:** Brett Walker
**Customer:** Josh's Frogs
**Deal Stage:** [01-DISCOVERY-SCHEDULED]