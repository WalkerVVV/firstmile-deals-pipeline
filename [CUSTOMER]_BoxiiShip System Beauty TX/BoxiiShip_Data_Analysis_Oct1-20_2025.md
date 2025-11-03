# BoxiiShip System Beauty - Data Analysis
**Analysis Period:** October 1-20, 2025
**Analysis Date:** October 31, 2025
**Total Shipments:** 11,167

---

## DATASET OVERVIEW

**Date Range:** October 1-17, 2025 (17 days)
**Total Shipments:** 11,167
**Data Source:** BoxiiShip domestic tracking export

### Service Mix
- **Ground:** 5,992 (53.7%)
- **Expedited:** 4,929 (44.1%)
- **Priority:** 244 (2.2%)

### Delivery Status Summary
- **Delivered:** 10,180 (91.2%)
- **In Transit:** 827 (7.4%)
- **NTE:** 81 (0.7%)
- **Undeliverable:** 46 (0.4%)
- **Delivery Attempt:** 21 (0.2%)
- **Other:** 12 (0.1%)

---

## CRITICAL METRIC: PICKUP TO FIRST SCAN

**Target:** Same-day induction scan
**Current Performance:**

| Metric | Value |
|--------|-------|
| Average time to first scan | **67.2 hours (2.8 days)** |
| Median time to first scan | **31.1 hours (1.3 days)** |
| Maximum time to first scan | **451.6 hours (18.8 days)** |

### First Scan Distribution
- **Same day (0-24 hours):** 3,919 (35.1%)
- **Next day (24-48 hours):** 1,881 (16.8%)
- **2+ days (>48 hours):** 5,024 (45.0%)

### By Service Level
| Service | Avg Hours to Scan | Same-Day % |
|---------|-------------------|------------|
| **Expedited** | 60.7 hours (2.5 days) | 40.2% |
| **Ground** | 73.4 hours (3.1 days) | 30.8% |
| **Priority** | 55.1 hours (2.3 days) | 36.5% |

**Finding:** Only 35.1% of packages receive same-day induction scan. 45.0% wait 2+ days for first scan.

---

## DAILY VOLUME BREAKDOWN (By Request Date)

| Date | Total | Delivered | Del % | In Transit | Transit % |
|------|-------|-----------|-------|------------|-----------|
| 10/01 | 438 | 433 | 98.9% | 1 | 0.2% |
| 10/02 | 430 | 418 | 97.2% | 0 | 0.0% |
| 10/03 | 421 | 416 | 98.8% | 0 | 0.0% |
| **10/06** | **1,990** | **1,701** | **85.5%** | **287** | **14.4%** |
| 10/07 | 1,174 | 1,146 | 97.6% | 14 | 1.2% |
| 10/08 | 1,676 | 1,610 | 96.1% | 52 | 3.1% |
| 10/09 | 818 | 782 | 95.6% | 22 | 2.7% |
| 10/10 | 558 | 524 | 93.9% | 29 | 5.2% |
| 10/13 | 1,114 | 1,047 | 94.0% | 50 | 4.5% |
| 10/14 | 510 | 476 | 93.3% | 26 | 5.1% |
| 10/15 | 353 | 327 | 92.6% | 16 | 4.5% |
| 10/16 | 320 | 291 | 90.9% | 25 | 7.8% |
| **10/17** | **1,363** | **1,009** | **74.0%** | **305** | **22.4%** |

**Key Findings:**
- **October 6:** Volume spike to 1,990 (4.5x normal). 287 still in transit (14.4%).
- **October 17:** 305 in transit out of 1,363 (22.4%).
- **Pre-Oct 6 (Oct 1-3):** 0.1% in-transit rate
- **Post-Oct 6 (Oct 6-17):** 8.4% in-transit rate

---

## IN-TRANSIT INVENTORY ANALYSIS

**Total In Transit:** 827 packages (7.4% of total)

### Age Distribution
- **Average age:** 7.4 days
- **Median age:** 6.0 days
- **Oldest:** 18 days

### Age Breakdown
| Days Old | Count | % of In-Transit |
|----------|-------|-----------------|
| 13 days | 287 | 34.7% |
| 2 days | 305 | 36.9% |
| 11 days | 52 | 6.3% |
| 6 days | 50 | 6.0% |
| 9 days | 29 | 3.5% |
| 5 days | 26 | 3.1% |
| 10 days | 22 | 2.7% |
| 12 days | 14 | 1.7% |
| 4 days | 16 | 1.9% |
| 3 days | 25 | 3.0% |
| 18 days | 1 | 0.1% |

### By Service Level
| Service | In Transit | Avg Age | Beyond SLA |
|---------|------------|---------|------------|
| **Expedited** | 210 | 4.1 days | 63 (beyond 5-day SLA) |
| **Ground** | 616 | 8.6 days | 377 (beyond 8-day SLA) |
| **Priority** | 1 | 5.0 days | 1 (beyond 3-day SLA) |

**Total Beyond SLA:** 441 packages

### By Carrier
- **aci_ws:** 527 packages (63.7%)
- **dhl:** 300 packages (36.3%)

---

## DELIVERY PERFORMANCE BY SLA WINDOW

### EXPEDITED (2-5 Day Service | Target: 95% by Day 5)
**Total Delivered:** 4,663
**Delivered within SLA (≤5 days):** 4,612 (98.9%)
**Delivered late (>5 days):** 51 (1.1%)

**Gap to 95% target:** -3.9pp (EXCEEDS TARGET)

#### Transit Day Distribution
| Day | Count | % | Cumulative % | Status |
|-----|-------|---|--------------|--------|
| 0 | 147 | 3.2% | 3.2% | Within SLA |
| 1 | 887 | 19.0% | 22.2% | Within SLA |
| 2 | 1,650 | 35.4% | 57.6% | Within SLA |
| 3 | 1,327 | 28.5% | 86.0% | Within SLA |
| 4 | 513 | 11.0% | 97.0% | Within SLA |
| 5 | 88 | 1.9% | 98.9% | Within SLA |
| 6 | 27 | 0.6% | 99.5% | Late |
| 7 | 10 | 0.2% | 99.7% | Late |
| 8 | 4 | 0.1% | 99.8% | Late |
| 9 | 7 | 0.2% | 99.9% | Late |
| 10 | 2 | 0.0% | 100.0% | Late |
| 13 | 1 | 0.0% | 100.0% | Late |

---

### GROUND (3-8 Day Service | Target: 95% by Day 8)
**Total Delivered:** 5,284
**Delivered within SLA (≤8 days):** 5,263 (99.6%)
**Delivered late (>8 days):** 21 (0.4%)

**Gap to 95% target:** -4.6pp (EXCEEDS TARGET)

#### Transit Day Distribution
| Day | Count | % | Cumulative % | Status |
|-----|-------|---|--------------|--------|
| 0 | 190 | 3.6% | 3.6% | Within SLA |
| 1 | 1,152 | 21.8% | 25.4% | Within SLA |
| 2 | 860 | 16.3% | 41.7% | Within SLA |
| 3 | 1,229 | 23.3% | 64.9% | Within SLA |
| 4 | 1,467 | 27.8% | 92.7% | Within SLA |
| 5 | 230 | 4.4% | 97.0% | Within SLA |
| 6 | 43 | 0.8% | 97.9% | Within SLA |
| 7 | 65 | 1.2% | 99.1% | Within SLA |
| 8 | 27 | 0.5% | 99.6% | Within SLA |
| 9 | 13 | 0.2% | 99.8% | Late |
| 10 | 5 | 0.1% | 99.9% | Late |
| 11 | 2 | 0.0% | 100.0% | Late |
| 12 | 1 | 0.0% | 100.0% | Late |

---

### PRIORITY (2-3 Day Service | Target: 95% by Day 3)
**Total Delivered:** 233
**Delivered within SLA (≤3 days):** 229 (98.3%)
**Delivered late (>3 days):** 4 (1.7%)

**Gap to 95% target:** -3.3pp (EXCEEDS TARGET)

#### Transit Day Distribution
| Day | Count | % | Cumulative % | Status |
|-----|-------|---|--------------|--------|
| 1 | 12 | 5.2% | 5.2% | Within SLA |
| 2 | 195 | 83.7% | 88.8% | Within SLA |
| 3 | 22 | 9.4% | 98.3% | Within SLA |
| 4 | 4 | 1.7% | 100.0% | Late |

---

## SLA PERFORMANCE SUMMARY

| Service | Delivered | Within SLA | On-Time % | Target | Status |
|---------|-----------|------------|-----------|--------|--------|
| **Expedited** | 4,663 | 4,612 | 98.9% | 95% | MEETS |
| **Ground** | 5,284 | 5,263 | 99.6% | 95% | MEETS |
| **Priority** | 233 | 229 | 98.3% | 95% | MEETS |

**Note:** SLA performance is for DELIVERED packages only. Does not include 827 in-transit packages, 441 of which are beyond their SLA window.

---

## CRITICAL ISSUES IDENTIFIED

### 1. Pickup to First Scan Delays
- **Target:** Same-day induction scan
- **Actual:** 67.2 hour (2.8 day) average
- **Only 35.1%** receiving same-day scan
- **45.0%** waiting 2+ days for first scan

### 2. October 6 Volume Spike Impact
- **Volume:** 1,990 shipments (4.5x normal)
- **Still in transit:** 287 packages (13 days later)
- **In-transit rate:** Jumped from 0.1% to 14.4%

### 3. October 17 Recent Volume
- **1,363 shipments requested**
- **305 still in transit** (22.4%)
- Only **74.0% delivered** (vs 95%+ on earlier dates)

### 4. Packages Beyond SLA Still In Transit
- **Expedited:** 63 packages beyond 5-day SLA
- **Ground:** 377 packages beyond 8-day SLA
- **Priority:** 1 package beyond 3-day SLA
- **Total:** 441 packages beyond SLA and still undelivered

### 5. Oldest Stuck Packages
- **18 days:** 1 package (Ground to OR)
- **13 days:** 287 packages (Ground, all from Oct 6)
- Most showing "Electronic Manifest transmitted" as last scan

---

## IN-TRANSIT TRACKING LIST

**Total packages requiring status update:** 827

**Exported to:** `In_Transit_Tracking_List_Oct20_2025.csv`

**File contains:**
- Tracking Number
- Carrier
- Product
- Xparcel Type
- Calculated Zone
- Destination State/Zip
- Request Date
- Start Date
- Most Recent Scan Date
- Most Recent Scan
- Days Since Request
- Days Since Last Scan

**Sorted by:** Days Since Request (oldest first)

**Use for:** Batch tracking status updates to provide current delivery status for each package.

---

## DATA FOR FIRSTMILE TEAM

### Improvement Focus Areas

**1. Pickup to First Scan (Induction)**
- Current: 67.2 hour average (2.8 days)
- Target: Same-day (24 hours)
- Gap: 43.2 hours improvement needed

**2. Network Capacity**
- October 6: System unable to handle 1,990 shipment day
- 287 packages from that day still in transit 13 days later

**3. Tracking Visibility**
- Many packages showing only "Electronic Manifest transmitted"
- Indicates packages not being physically inducted/scanned

**4. In-Transit Inventory Management**
- 827 packages in transit (7.4% of total volume)
- 441 beyond their SLA window
- Average age: 7.4 days

---

## DATA NOTES

- Analysis based on data exported October 20, 2025
- "In Transit" status is as of data export date
- Delivered packages show strong SLA performance (98-99%)
- Issue is primarily with in-transit inventory and scan delays
- Customer processes 32,000 shipments/month total volume
- Additional locations: American Fork (15,000/week), Magna (3-4K/week)

---

**Report Generated:** October 31, 2025
**Next Step:** Track all 827 in-transit packages for current status updates
