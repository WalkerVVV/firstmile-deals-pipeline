# Tinoco Enterprises - Data Gaps & Sources
## November 8, 2025

**Purpose**: Identify missing data, document where to find it, and define safe assumptions when data unavailable.

---

## 🚨 CRITICAL MISSING DATA

### 1. **Xparcel Ground Rate Card** ❌ BLOCKER

**What we need**:
- Xparcel Ground rates for Zones 1-8, weights 1-5 lbs
- Specifically: Zone 5 rates at 3 lbs and 4 lbs (for DIM comparison)
- DIM policy: Is 1 cu ft rule standard or negotiable?

**Where to get it**:
- **Primary source**: Brycen (FirstMile Pricing Team)
  - Email: Request Tinoco-specific rate card
  - Timeline: Need THIS WEEK (deal idle 23 days)
- **Secondary source**: FirstMile Deals folder - check for standard rate cards
  - Location: `C:\Users\BrettWalker\FirstMile_Deals\`
  - Search for: `*rate*card*.xlsx`, `*pricing*.csv`, `*Xparcel*Ground*.pdf`
- **HubSpot**: Check Deal ID 36470789710 notes for any rate discussions
  - Search for: "rate", "pricing", "Xparcel Ground"
  - Look in: Activity timeline, attached files, notes

**Safe assumptions if unavailable**:
- ⚠️ **DO NOT ASSUME** - Cannot build accurate proposal without actual rates
- **Temporary estimate**: $8.50-$9.50 range (based on USPS GA $9.13 - FirstMile typically competitive)
- **Risk**: If rates are higher than estimated, entire business case fails
- **Alternative**: Use Xparcel Expedited as proxy ($12.30) and discount 25-30% for Ground

**Action**: Email Brycen TODAY requesting Xparcel Ground rate card for Tinoco

---

### 2. **Complete USPS Ground Advantage Rate Card** ⚠️ PARTIAL

**What we have**:
- Zone 5, 3 lbs: $9.13 ✅ (from customer email)

**What we're missing**:
- Zone 5, 4 lbs: Estimated $10.50 (need confirmation)
- Zones 1-8, 1-5 lbs: Full rate matrix

**Where to get it**:
- **Primary source**: Chase/Juan (customer contact)
  - Request: "Can you share your current USPS GA invoice or rate card?"
  - Timeline: Needed for accurate savings calculation
- **Secondary source**: Customer's shipping platform data
  - If they use ShipStation/ShipHero: Export cost data from last 60 days
  - Location: Should match PLD date range (Sept 9 - Nov 6)
- **Public source**: USPS.com retail rates
  - URL: https://www.usps.com/business/prices.htm
  - Note: May not match customer's negotiated rates (likely lower)
- **FirstMile Deals folder**: Check other customer analyses with USPS GA data
  - Search for: `*USPS*rate*.xlsx`, `*Ground*Advantage*.csv`
  - Compare rates from similar volume customers

**Safe assumptions if unavailable**:
- Use USPS retail rates as CEILING (customer likely pays less)
- Estimate 4 lb rate = 3 lb rate × 1.15 (typical 15% tier jump)
  - 3 lbs: $9.13 → 4 lbs: $10.50 (reasonable estimate)
- Zone scaling: Each zone typically +$0.50-$1.50 per tier
- **Risk level**: MEDIUM - Estimates should be close to actual

**Action**: Email Chase/Juan requesting USPS GA invoice or rate confirmation

---

### 3. **Actual Shipment Costs** ❌ HIGH PRIORITY

**What we need**:
- Actual carrier costs for each shipment in PLD files
- Breakdown by carrier, service, zone, weight

**What we have**:
- Package-level details (weight, zone, dimensions) ✅
- Service levels (USPS GA, UPS SurePost, etc.) ✅
- **NO COST DATA** in CSV files ❌

**Where to get it**:
- **Primary source**: Customer invoices
  - Request from Chase/Juan: "Can you share Sept-Nov carrier invoices?"
  - Format: PDF invoices or Excel export
- **Secondary source**: Shipping platform cost reports
  - ShipStation: Cost & Profitability Report (last 60 days)
  - ShipHero: Billing Report with carrier costs
- **Tertiary source**: Carrier-specific portals
  - USPS Business Customer Gateway
  - UPS Billing Center
  - Requires customer permission/access

**Safe assumptions if unavailable**:
- Use known rate ($9.13 for Zone 5, 3 lbs) as baseline
- Apply zone-based scaling factors:
  - Zone 4: -$0.75 from Zone 5
  - Zone 6: +$0.75 from Zone 5
  - Zone 7: +$1.50 from Zone 5
  - Zone 8: +$2.25 from Zone 5
- Weight-based scaling:
  - 1 lb: $7.50 (estimated)
  - 2 lbs: $8.30 (estimated)
  - 3 lbs: $9.13 (known)
  - 4 lbs: $10.50 (estimated)
  - 5 lbs: $11.75 (estimated)
- **Risk level**: MEDIUM-HIGH - Could be off by 10-15%

**Action**: Request carrier invoices or shipping platform cost export

---

## 🟡 SUPPORTING DATA NEEDS

### 4. **DIM Waiver Policy & Precedent** ⚠️ STRATEGIC

**What we need**:
- FirstMile's official DIM waiver policy
- Historical precedent: Has it been granted before? For whom?
- Approval process: Who decides? (Brycen, VP Pricing, CEO?)
- Conditions required: Volume threshold, margin impact, customer tier?

**Where to get it**:
- **Primary source**: Brycen (FirstMile Pricing Team)
  - Ask directly: "What's the policy on DIM waivers? Any precedent?"
  - Internal docs: Policy manual, pricing guidelines
- **Secondary source**: FirstMile sales team (leadership)
  - Ask: "Have we ever granted DIM waivers? What was the business case?"
- **Memory**: Search past similar analyses in FirstMile Deals folder
  - Search for: `*DIM*waiver*.md`, `*cubic*foot*.md`
  - Check: Other customer folders with similar product profiles

**Safe assumptions if unavailable**:
- Assume DIM waiver is NEGOTIABLE (not standard policy)
- Business case required: Show ROI (revenue gain vs margin loss)
- Likely threshold: Must be material deal ($500K+ annual revenue)
- Approval level: VP Pricing or higher (not just Brycen's call)
- **Risk level**: LOW - We can make the ask regardless of precedent

**Action**: Include DIM waiver request in email to Brycen with ROI analysis

---

### 5. **FirstMile Performance Data (Current 250 Packages)** ⚠️ CONFIDENCE

**What we need**:
- Transit time data for 250 FirstMile Expedited packages
- SLA compliance: % delivered within 2-5 day window
- Customer feedback: Any complaints or issues?
- Comparison to USPS GA performance

**Where to get it**:
- **Primary source**: Chase/Juan (FirstMile account manager)
  - Ask: "How is FirstMile performing on the 250 Expedited packages?"
  - Request: Performance dashboard or QBR metrics
- **Secondary source**: FirstMile internal systems
  - Tracking data: FirstMile shipment dashboard
  - Reporting: Customer-specific performance reports
- **HubSpot**: Check deal notes for performance discussions
  - Search for: "performance", "delivery", "issues", "complaints"

**Safe assumptions if unavailable**:
- Assume FirstMile meeting SLA (no complaints documented)
- If performance were bad, deal wouldn't be in [07-STARTED-SHIPPING] stage
- Estimate 95%+ on-time delivery (industry standard for Expedited)
- **Risk level**: LOW - Can proceed without this, but helps customer confidence

**Action**: Ask Chase/Juan about FirstMile performance on current 250 packages

---

### 6. **Destination State Breakdown** ⚠️ SELECT NETWORK FIT

**What we need**:
- Top 10 destination states by volume
- Percentage of volume going to Select Network states (CA, TX, FL, NY, IL, GA, WA)

**What we have**:
- Zone distribution ✅
- ZIP codes in PLD files ✅

**Where to get it**:
- **Generate from existing data**: Run ZIP-to-state analysis on PLD files
  - Script: Parse `destination_postal_code` column
  - Extract: First 5 digits, map to state
  - Output: State-level distribution table
- **Memory**: Check past analyses for similar zone patterns
  - Zones 4-5 concentration → CA, TX likely top states
  - Zones 7-8 concentration → NY, FL likely in top 10

**Safe assumptions if unavailable**:
- Based on zone distribution, estimate:
  - CA: 15-20% (Zone 4-5, West Coast)
  - TX: 10-15% (Zone 4-5, South Central)
  - FL: 8-12% (Zone 6-7, Southeast)
  - NY: 5-8% (Zone 7-8, Northeast)
  - IL: 5-8% (Zone 6-7, Midwest)
- Assume 50%+ volume to Select Network states
- **Risk level**: LOW - Can generate from data we have

**Action**: Run Python script to map ZIPs to states (15 min task)

---

## 🟢 NICE-TO-HAVE DATA

### 7. **Historical Trends & Seasonality** 🟢 INSIGHT

**What we need**:
- Volume trends: Growing, flat, declining?
- Seasonal patterns: Q4 peak, Q1 slow?
- Product mix changes: New SKUs, discontinued items?

**Where to get it**:
- **Primary source**: Customer (Chase/Juan)
  - Ask: "Is volume growing? Any seasonal patterns?"
- **Secondary source**: PLD files from different time periods
  - Compare: Sept-Nov 2025 vs same period 2024
  - Trend: Calculate YoY growth rate
- **HubSpot**: Deal notes may mention growth plans
  - Search for: "growth", "expansion", "forecast", "Q4"

**Safe assumptions if unavailable**:
- Assume flat to slight growth (typical eCommerce)
- Q4 peak: 20-30% higher than Q1-Q3 average
- No major changes in product mix (stable brands)
- **Risk level**: VERY LOW - Not critical for pricing decision

**Action**: Ask casually in next call with Chase/Juan

---

### 8. **Scan Data & Pickup Schedule** 🟢 OPERATIONAL

**What we need**:
- Label creation timestamps
- First scan timestamps (pickup confirmation)
- Average "label-to-scan" gap (how fast do they tender packages?)

**Where to get it**:
- **Primary source**: Full tracking export from shipping platform
  - ShipStation: Export with tracking events
  - Request from Chase/Juan if needed
- **Secondary source**: Carrier tracking APIs
  - USPS Tracking API
  - UPS Tracking API
  - Requires tracking numbers from PLD files (which we don't have)

**Safe assumptions if unavailable**:
- Assume same-day or next-day pickup (typical for eCommerce)
- Standard shipping schedule: Mon-Fri, daily pickups
- No operational red flags (if there were issues, would be documented)
- **Risk level**: VERY LOW - Not needed for pricing proposal

**Action**: Skip unless operational issues suspected

---

## 📊 DATA SOURCES SUMMARY

### Immediate Actions (Today)

1. **Email Brycen**: Request Xparcel Ground rate card + DIM waiver policy
2. **Email Chase/Juan**: Request USPS GA invoice + cost data + Expedited rationale
3. **Search FirstMile Deals folder**: Look for existing rate cards and similar analyses
4. **Run ZIP-to-state script**: Generate destination state breakdown (15 min)

### FirstMile Deals Folder Search Strategy

**Location**: `C:\Users\BrettWalker\FirstMile_Deals\`

**Search patterns**:
```bash
# Rate cards
*rate*card*.xlsx
*pricing*.csv
*Xparcel*Ground*.pdf
*zone*pricing*.xlsx

# Similar customer analyses
*DIM*weight*.md
*cubic*foot*.md
*tumbler*.md
*1-5*lb*.md

# USPS comparisons
*USPS*Ground*Advantage*.xlsx
*USPS*vs*FirstMile*.csv
```

**Target folders**:
- `[CUSTOMER]_*` folders with similar profiles (1-5 lb, high zone, economy ground)
- `_ARCHIVE/` for historical rate cards
- Root folder for standard pricing templates

### HubSpot Search Strategy

**Deal ID**: 36470789710 (Juggy / Tinoco)

**Search terms**:
- "rate" OR "pricing" OR "quote"
- "Xparcel Ground" OR "XPG"
- "DIM" OR "dimensional weight"
- "Zone 5" OR "zones"
- "Juan" (key contact)
- "2024" (related to "Creating 2024 for them" note)

**Check**:
- Activity timeline (emails, notes, calls)
- Attached files (proposals, rate cards, invoices)
- Deal properties (custom fields for pricing)

### Memory / Past Analyses Search

**Look for customers with similar profiles**:
- **Product type**: Small parcels, 1-5 lb range, uniform dimensions
- **Volume**: 3,000-5,000 packages/month (similar scale)
- **Geography**: High zones 5-8 concentration
- **Service**: USPS GA dominant, considering Xparcel Ground
- **Issue**: DIM weight concern

**Likely candidates** (search deal folders):
- Drink/beverage companies (bottles, tumblers)
- Apparel brands (consistent box sizes)
- Consumer packaged goods (CPG)

---

## 🎯 ASSUMPTIONS FRAMEWORK

### When Data is Missing: Decision Matrix

| Data Type | Can Assume? | Risk Level | Action |
|-----------|-------------|------------|--------|
| **Xparcel Ground rates** | ❌ NO | CRITICAL | Must get from Brycen - cannot proceed without |
| **USPS GA rates (partial)** | ⚠️ YES | MEDIUM | Use estimates, validate with customer invoice |
| **Actual shipment costs** | ⚠️ YES | MEDIUM | Use rate card estimates, note as assumption |
| **DIM waiver policy** | ✅ YES | LOW | Make business case regardless of precedent |
| **Performance data** | ✅ YES | LOW | Assume meeting SLA (no complaints documented) |
| **Destination states** | ✅ YES | VERY LOW | Generate from ZIP codes we have |
| **Historical trends** | ✅ YES | VERY LOW | Assume flat to slight growth |
| **Scan data** | ✅ YES | VERY LOW | Not needed for pricing proposal |

### Safe Estimation Methodology

**Rate Card Estimation** (when actual rates missing):
1. Use known anchor points (e.g., Zone 5, 3 lbs = $9.13)
2. Apply industry-standard scaling factors:
   - Zone scaling: ±$0.50-$1.50 per zone tier
   - Weight scaling: ~15% per pound tier
3. Cross-check with competitive intelligence:
   - FirstMile typically 5-10% below USPS retail
   - Xparcel Ground typically 25-30% below Xparcel Expedited
4. Document assumptions clearly in analysis
5. Present as "estimated" with range (conservative to optimistic)

**Business Case Approach** (when precise data unavailable):
- **Conservative scenario**: Use higher cost estimates (worst case)
- **Expected scenario**: Use mid-range estimates (most likely)
- **Optimistic scenario**: Use lower cost estimates (best case)
- Show Brycen all three scenarios
- Make decision based on conservative case (if that works, we're safe)

---

## 📋 DATA COLLECTION CHECKLIST

### Critical (Must Have - Blocks Proposal)

- [ ] **Xparcel Ground rate card** (Brycen) - BLOCKER
  - Priority: 🔴 CRITICAL
  - Timeline: Need THIS WEEK
  - Action: Email Brycen TODAY

### High Priority (Improves Accuracy)

- [ ] **USPS GA rate card** (Chase/Juan) - HIGH
  - Priority: 🔴 HIGH
  - Timeline: Need by next week
  - Action: Request invoice or rate confirmation

- [ ] **Actual shipment costs** (Chase/Juan) - HIGH
  - Priority: 🔴 HIGH
  - Timeline: Nice to have by next week
  - Action: Request carrier invoices or platform export

- [ ] **DIM waiver policy** (Brycen) - STRATEGIC
  - Priority: 🟡 MEDIUM
  - Timeline: Include in Brycen email
  - Action: Ask about policy and precedent

### Medium Priority (Supporting Detail)

- [ ] **FirstMile performance data** (Chase/Juan) - CONFIDENCE
  - Priority: 🟡 MEDIUM
  - Timeline: Before customer presentation
  - Action: Ask about current 250 package performance

- [ ] **Destination state breakdown** (Generate internally) - SELECT NETWORK
  - Priority: 🟡 MEDIUM
  - Timeline: Can do TODAY (15 min script)
  - Action: Run ZIP-to-state analysis

### Low Priority (Nice to Have)

- [ ] **Historical trends** (Chase/Juan) - INSIGHT
  - Priority: 🟢 LOW
  - Timeline: Casual question in next call
  - Action: Ask about growth and seasonality

- [ ] **Scan data** (Chase/Juan) - OPERATIONAL
  - Priority: 🟢 LOW
  - Timeline: Only if operational issues suspected
  - Action: Skip for now

---

## 🎬 IMMEDIATE NEXT STEPS

### Email Template: Brycen Request

**Subject**: Tinoco Enterprises - Xparcel Ground Rate Request ($930K Opportunity)

Brycen,

I'm working on Tinoco Enterprises (Juggy/MexiStuff brands) - they're currently a SMALL FirstMile customer (250 packages/month on Xparcel Expedited) with BIG expansion potential.

**The Opportunity**:
- Current FirstMile: 250 packages/month ($37K annually)
- Target FirstMile: 9,249 packages/month ($967K annually)
- **Incremental revenue: $930K annually** (37x growth)

**The Blocker**:
- They have 8,962 USPS GA packages/month we're not getting
- Customer needs Xparcel Ground pricing to justify switch
- USPS GA current rate: $9.13 (Zone 5, 3 lbs)
- DIM weight concern: 83% of volume DIMs up by 1 lb

**What I Need**:
1. Xparcel Ground rate card (Zones 1-8, 1-5 lbs)
2. DIM waiver policy: Can we waive for packages <1 cu ft?
   - Cost: $43K annually (margin hit from DIM)
   - Benefit: $930K revenue (20:1 ROI)
3. Timeline: Need this week to keep deal moving (idle 23 days)

Can we get Xparcel Ground pricing approved for Tinoco?

Brett

---

### Email Template: Chase/Juan Request

**Subject**: Tinoco - Rate Confirmation for Savings Analysis

Chase/Juan,

I'm building the savings analysis for moving USPS volume to FirstMile Xparcel Ground. To make this accurate, I need:

1. **USPS GA rate confirmation**:
   - Zone 5, 3 lbs: $9.13 ✓ (confirmed)
   - Zone 5, 4 lbs: $? (please confirm)
   - If possible: Full rate card or recent invoice

2. **Cost data** (if available):
   - Last 60 days carrier invoices (Sept-Nov)
   - Or: Cost export from ShipStation/shipping platform

3. **Quick questions**:
   - Why are 250 packages on FirstMile Expedited? (customer requirement or no Ground option?)
   - How is FirstMile performing on those 250? (any issues or complaints?)

This will help me show exact savings vs USPS and build the business case for switching.

Thanks,
Brett

---

**Document Created**: November 8, 2025
**Purpose**: Data gap analysis and collection strategy
**Critical Path**: Get Xparcel Ground rates from Brycen → Calculate savings → Build proposal
**Timeline**: Need rates THIS WEEK to maintain deal momentum
