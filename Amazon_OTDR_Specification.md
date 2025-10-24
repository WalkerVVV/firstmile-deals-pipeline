# Amazon On-Time Delivery Rate (OTDR) Specification
## Complete Reference Guide for FirstMile Operations

**Document Version:** 1.0
**Last Updated:** October 7, 2025
**Amazon Policy Effective Date:** September 25, 2024
**Source:** Amazon Seller Central Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Policy Overview](#policy-overview)
3. [OTDR Calculation Method](#otdr-calculation-method)
4. [The "Deliver By" Date](#the-deliver-by-date)
5. [Transit Time Settings](#transit-time-settings)
6. [On-Time Delivery Criteria](#on-time-delivery-criteria)
7. [Promise Extensions](#promise-extensions)
8. [Defect Report Fields](#defect-report-fields)
9. [FirstMile Tracking Requirements](#firstmile-tracking-requirements)
10. [Service Level Mapping](#service-level-mapping)
11. [OTDR vs Late Shipment Rate](#otdr-vs-late-shipment-rate)
12. [Metrics Dashboard Requirements](#metrics-dashboard-requirements)
13. [Business Days Calculation](#business-days-calculation)
14. [Exception Handling](#exception-handling)
15. [Shipper Communication Templates](#shipper-communication-templates)
16. [Report Access & Auditing](#report-access--auditing)
17. [Key Takeaways](#key-takeaways)

---

## Executive Summary

### Key Points
- **Minimum Requirement:** 90% on-time delivery rate (without promise extensions)
- **Recommended Target:** 95%+ to maintain healthy account standing
- **Measurement:** Per unit, not per order (multi-SKU orders count separately)
- **Calculation Period:** 14-day rolling window (excludes most recent 7 days)
- **Time Zone:** All dates measured in Pacific Time (PST/PDT)
- **Business Days Only:** Weekends and holidays excluded from calculations

### Critical Change (September 2024)
Amazon now measures OTDR **BEFORE** promise extensions are applied. Sellers are held to their original "Deliver by" date regardless of weather delays, carrier issues, or other extensions shown to customers.

---

## Policy Overview

### Minimum Requirements

| Metric | Threshold | Consequence |
|--------|-----------|-------------|
| **On-Time Delivery Rate** | ≥ 90% | Below 90% = Listing restriction |
| **Recommended Target** | ≥ 95% | Optimal seller standing |

### Enforcement
- **Effective Date:** September 25, 2024
- **Applies To:** Seller-fulfilled orders only (not FBA)
- **Requires:** Valid tracking information

### Consequences of Non-Compliance

**If OTDR drops below 90%:**
1. Amazon sends policy violation notification
2. Seller-fulfilled product listings may be restricted
3. Seller has 72 hours to submit appeal via Account Health dashboard
4. Appeal must include:
   - Root cause analysis
   - Corrective actions taken
   - Prevention plan for future issues

### What Orders Count

✅ **Included:**
- All seller-fulfilled orders with tracking
- Each unit counted separately (not per order)
- Standard Shipping, Premium Shipping, Seller Fulfilled Prime

❌ **Excluded:**
- FBA (Fulfillment by Amazon) orders
- Orders without tracking
- Most recent 7 days (still in transit)

---

## OTDR Calculation Method

### Formula
```
OTDR = (Units delivered on or before "Deliver by" date) / (Total tracked units shipped)
```

### Calculation Window

**14-Day Rolling Window with Exclusions:**
1. Pull data from last 21 days
2. Exclude most recent 7 days (packages still in transit)
3. Calculate percentage from remaining 14-day window

**Example:**
```
Total units in last 21 days: 130 units
Units with delivery date in last 7 days: 30 units (excluded)
Units evaluated: 100 units
Units delivered on time: 90 units
Units delivered late: 10 units

OTDR = 90 / 100 = 90.0%
```

### Critical Policy Change (September 2024)

**OLD METHOD:** OTDR measured AFTER promise extensions
**NEW METHOD:** OTDR measured BEFORE promise extensions

**What this means:**
- Customer sees: "Delivery by Friday" (with 1-day extension)
- Seller judged by: "Deliver by Thursday" (without extension)
- Late Thursday delivery = Counts against OTDR even if delivered Friday on time for customer

---

## The "Deliver By" Date

### Calculation Formula
```
Order Date + Handling Time + Transit Time = "Deliver by" Date
(All values in BUSINESS DAYS)
```

### Business Days Definition

✅ **Counts as Business Days:**
- Monday through Friday

❌ **Does NOT Count:**
- Saturdays
- Sundays
- National holidays (automatically adjusted by Amazon)

### Time Zone: Pacific Time (PST/PDT)

**Critical:** All "Deliver by" dates are measured in Pacific Time.

**Example:**
- "Deliver by" date: January 1
- Deadline: January 1, 11:59:59 PM PST/PDT
- Package delivered January 2, 12:01 AM PST = ❌ LATE

### Calculation Examples

#### Example 1: Basic Calculation
```
Order Date: Monday, 10:00 AM PST
Handling Time: 1 business day
Transit Time: 2 business days

Calculation:
Monday (Day 0 - Order received)
+ 1 day handling = Tuesday (must ship by Tuesday)
+ 2 days transit = Thursday (must deliver by Thursday)

"Deliver by" Date: Thursday, 11:59:59 PM PST
```

#### Example 2: With Weekend
```
Order Date: Friday, 2:00 PM PST
Handling Time: 1 business day
Transit Time: 2 business days

Calculation:
Friday (Day 0 - Order received)
+ 1 day handling = Monday (Sat/Sun don't count)
+ 2 days transit = Wednesday

"Deliver by" Date: Wednesday, 11:59:59 PM PST
```

#### Example 3: With Holiday
```
Order Date: Monday
Handling Time: 1 business day
Transit Time: 5 business days
Holiday: Thursday (Thanksgiving)

Calculation:
Monday (Day 0)
+ 1 day handling = Tuesday
+ 5 days transit = Tuesday next week (Thursday holiday skipped)

"Deliver by" Date: Tuesday (next week), 11:59:59 PM PST
```

---

## Transit Time Settings

### Standard Shipping (Contiguous US)

**Maximum Transit Time: 5 days** (Updated August 25, 2024)

| Previous Limit | New Limit | Effective Date |
|----------------|-----------|----------------|
| 8 days | 5 days | August 25, 2024 |

**Allowed Settings:**
- 2 days
- 3 days
- 4 days
- 5 days (maximum)

**Note:** The 5-day maximum applies to all SKUs except media (books, magazines, DVDs).

### Free Economy Shipping

**Maximum Transit Time: 8 days** (Updated August 25, 2024)

| Previous Limit | New Limit | Effective Date |
|----------------|-----------|----------------|
| 10 days | 8 days | August 25, 2024 |

**Use Case:** Slower, lower-cost shipping option for price-sensitive customers

### Media Exception

**Books, Magazines, DVDs:**
- 5-day maximum does NOT apply
- Different transit time rules
- Separate policy tracking

### Key Point for FirstMile

⚠️ **Transit time is seller-configurable**, not automatic:
- Sellers choose their transit time in shipping templates
- Amazon calculates "Deliver by" date based on seller's choice
- FirstMile must deliver within that window using appropriate carrier service

**Example Scenario:**
```
Seller sets transit time: 5 days (Standard Shipping)
FirstMile uses: Xparcel Ground (3-8 day capability)

Risk: If Xparcel takes 6-8 days, delivery will be LATE for Amazon OTDR
Solution: Use Xparcel Expedited (2-5 days) instead
```

---

## On-Time Delivery Criteria

### Option A: Delivered on Time

✅ **Package delivered on or before the seller-promised "Deliver by" date**

Simple and straightforward. No protection needed.

### Option B: OTDR Protection (Even if Late)

✅ **Package receives protection from late delivery penalties IF all conditions met:**

#### For Standard Shipping, Premium Shipping, Seller Fulfilled Prime:

**All 3 conditions required:**
1. ✅ Shipping template has **Shipping Settings Automation (SSA)** enabled
2. ✅ Account has **Automated Handling Time** enabled
3. ✅ Purchased **"on-time delivery rate Protected" shipping label** via:
   - Amazon Buy Shipping, OR
   - Veeqo

#### For Seller Fulfilled Prime & Premium Shipping Orders:

**2 conditions required:**
1. ✅ **Shipping Settings Automation (SSA)** enabled on shipping template
2. ✅ **Amazon Buy Shipping** used for label purchase

### OTDR Protection Eligibility

**Eligible Shipping Options:**
- ✅ Standard Shipping
- ✅ Premium Shipping
- ✅ Seller Fulfilled Prime

**NOT Eligible:**
- ❌ Free Economy Shipping
- ❌ Other shipping options

---

## Promise Extensions

### What Are Promise Extensions?

**Definition:** Additional days Amazon adds to the customer's delivery promise to account for logistical factors:
- Extreme weather (hurricanes, severe storms)
- Transportation network constraints
- Recent seller history of late deliveries
- Carrier network disruptions

### How They Work

**Customer View:**
```
Original "Deliver by" date: Thursday
+ Promise extension: 1 day
= Customer sees: "Guaranteed delivery by Friday"
```

**Seller Accountability:**
```
Seller's "Deliver by" date: Thursday (unchanged)
Seller judged by: Thursday delivery
Promise extension: Does NOT help seller's OTDR
```

### Critical Understanding for FirstMile

⚠️ **Promise extensions are for customer expectations, NOT seller performance measurement**

**Example:**
```
Order placed: Monday
Handling time: 1 day
Transit time: 2 days
Seller's "Deliver by" date: Thursday

Amazon adds 1-day promise extension due to weather
Customer sees: Friday delivery promise

Package delivered: Friday

Result:
✅ Customer satisfied (delivered on promised date)
❌ Seller OTDR penalized (late by 1 day from Thursday)
❌ FirstMile failed to deliver by Thursday
```

### Major Network Disruptions Exception

**Amazon MAY excuse late deliveries if:**
- Event impacts 2+ major carriers simultaneously
- Examples: Hurricane, bridge collapse, major infrastructure failure
- Amazon has sole discretion to determine what constitutes disruption

**What Amazon will NOT excuse:**
- Individual carrier delays
- Single-carrier routing issues
- "My carrier was slow"
- Normal weather delays
- Package lost/misrouted

---

## Defect Report Fields

Amazon's OTDR Defect Report includes the following fields. FirstMile should track these for accurate performance monitoring.

### Order ID
**Definition:** Unique identifier assigned to each customer order

**Key Points:**
- Same Order ID may appear multiple times in defect report
- Repetition indicates order contains multiple SKUs
- Each SKU/unit counted separately

### SKU and Unit Count
**Definition:** Stock Keeping Unit identifier and quantity shipped

**Example:**
```
Order #123-4567890
SKU-A: 5 units
SKU-B: 3 units
Total impact on OTDR: 8 units

If all 8 units delivered late = 8 late deliveries counted
```

### Order Date
**Definition:** Timestamp when customer placed the order

**Display Format:**
- Primary: Greenwich Mean Time (GMT)
- Secondary: Pacific Time (PST/PDT) in parentheses

**Critical for:**
- Starting point for all date calculations
- Determining "Deliver by" date
- Calculating handling and transit windows

### Promised Ship Date
**Definition:** Deadline by which seller must ship the order (upload tracking)

**Relationship to OTDR:**
- Primarily affects Late Shipment Rate (LSR), not OTDR
- However, late shipping often leads to late delivery

### Ship Confirmation Date
**Definition:** Timestamp when seller uploaded tracking to Amazon

**Critical for:**
- Marks transition from handling to shipping phase
- Starting point for transit time calculation

### Carrier First Scan Date
**Definition:** First time carrier's tracking system registers the package

**Critical for:**
- Amazon's actual start of transit time measurement
- Validates package was picked up/inducted

**FirstMile Responsibility:**
- Ensure Xparcel scans package promptly after pickup
- Monitor gap between ship confirmation and first scan

**Example Issue:**
```
Ship Confirmation: Tuesday 2:00 PM
Carrier First Scan: Thursday 9:00 AM
Gap: 2 days = Poor handling/induction performance
Impact: Less transit time available to deliver on time
```

### Promised Delivery Date (without promise extension)
**Definition:** The "Deliver by" date calculated from seller's settings

**🔴 THIS IS THE CRITICAL DATE FOR OTDR**

**Calculation:**
```
Order Date + Handling Time + Transit Time = Promised Delivery Date
```

**Key Points:**
- This is what FirstMile must meet
- Measured in Pacific Time (PST/PDT)
- This is the date used for OTDR calculation
- Customer may see a different (later) date

### Promised Delivery Date (with promise extension)
**Definition:** The delivery date shown to customer (includes extensions)

**Key Points:**
- Customer sees this date during checkout
- May be 1-2 days later than seller's "Deliver by" date
- Reference only for context
- **NOT used for OTDR calculation**

### Actual Delivery Date
**Definition:** Date carrier made first delivery attempt

**Source:** Carrier's official tracking record

**Time Zone Consideration:**
```
"Deliver by" date: January 15, 11:59:59 PM PST
Actual delivery: January 16, 12:01 AM PST
Result: ❌ LATE (even by 2 minutes)
```

### Delivered After Promised Date Without Extension
**Definition:** Boolean flag indicating late delivery for OTDR

**Values:**
- ❌ YES = Delivered after seller's "Deliver by" date
- ✅ NO = Delivered on time

**Impact:**
- YES = Counts against OTDR
- This is the defect that FirstMile must minimize

### Carrier Name
**Definition:** Shipping provider used for delivery

**Examples:**
- USPS
- UPS
- FedEx
- Xparcel (FirstMile)
- Amazon Logistics

### Ship Method
**Definition:** Shipping service/speed selected

**Examples:**
- Standard Shipping
- Expedited Shipping
- Two-Day Shipping
- One-Day Shipping
- Free Economy

---

## FirstMile Tracking Requirements

### Minimum Data Points to Track

For each Amazon order, FirstMile must capture and monitor:

| Data Point | Source | Purpose |
|-----------|--------|---------|
| **Order ID** | Amazon | Unique identifier |
| **Order Date** | Amazon | Calculation starting point |
| **Promised Ship Date** | Amazon | Tracking upload deadline (LSR) |
| **Handling Time** | Amazon/Seller | Days until must ship |
| **Transit Time** | Amazon/Seller | Days allowed for delivery |
| **"Deliver By" Date** | Calculated | **CRITICAL TARGET DATE** |
| **Ship Confirmation Date** | FirstMile | When tracking uploaded |
| **Carrier First Scan Date** | Xparcel | Pickup/induction timestamp |
| **Current Package Location** | Xparcel | Real-time tracking |
| **Estimated Delivery Date** | Xparcel | Predicted delivery |
| **Actual Delivery Date** | Xparcel | Final delivery timestamp |
| **On-Time Status** | Calculated | Met deadline? Yes/No |

### Real-Time Monitoring Requirements

FirstMile should monitor:

✅ Orders approaching "Deliver by" deadline (2 days out)
✅ Orders with estimated delivery after deadline
✅ Orders with no carrier scans in 24+ hours
✅ Orders stuck in transit (no movement 48+ hours)
✅ Daily OTDR percentage (rolling 14-day window)

---

## Service Level Mapping

### Xparcel Service Levels (Assumed Capabilities)

| Service Level | Transit Time | Cost | Reliability |
|--------------|-------------|------|-------------|
| Xparcel Next Day | 1 day | Highest | Highest |
| Xparcel Priority | 1-3 days | High | High |
| Xparcel Expedited | 2-5 days | Medium | Medium |
| Xparcel Ground | 3-8 days | Lowest | Variable |

### Mapping for Standard Shipping

| Seller's Transit Time | FirstMile Recommendation | Risk Level | Reason |
|----------------------|--------------------------|-----------|--------|
| 2 days | Xparcel Priority (1-3 days) | ✅ Low Risk | Priority's 3-day max aligns |
| 3 days | Xparcel Priority (1-3 days) | ✅ Low Risk | Perfect alignment |
| 4 days | Xparcel Expedited (2-5 days) | ⚠️ Medium Risk | At edge of Expedited capability |
| 5 days | Xparcel Expedited (2-5 days) | ⚠️ Medium Risk | Must deliver at Expedited's max |
| 5 days | Xparcel Ground (3-8 days) | ❌ HIGH RISK | Ground can take 6-8 days |

**Recommendation:** Use Xparcel Expedited (2-5 days) or better for all Standard Shipping orders

### Mapping for Free Economy Shipping

| Seller's Transit Time | FirstMile Recommendation | Risk Level |
|----------------------|--------------------------|-----------|
| 6-7 days | Xparcel Ground (3-8 days) | ⚠️ Medium Risk |
| 8 days | Xparcel Ground (3-8 days) | ❌ HIGH RISK |

### Recommended Default Strategy

**For Standard Shipping (5-day max transit):**
- Default to Xparcel Expedited (2-5 days)
- Upgrade to Priority for 2-3 day transit times
- Never use Ground for Standard Shipping orders

**For Free Economy (8-day max transit):**
- Use Xparcel Ground (3-8 days)
- Monitor performance closely
- Be prepared to upgrade if OTDR suffers

---

## OTDR vs Late Shipment Rate

FirstMile must track TWO separate Amazon metrics:

### Comparison Table

| Aspect | Late Shipment Rate (LSR) | On-Time Delivery Rate (OTDR) |
|--------|-------------------------|------------------------------|
| What It Measures | Tracking uploaded AFTER promised ship date | Package delivered AFTER "Deliver by" date |
| Threshold | Must be < 4% | Must be ≥ 90% |
| Calculation | (Late ships) / (Total orders) | (On-time deliveries) / (Total units) |
| Penalty | Listing deactivation | Listing restriction |
| Focus | Shipping speed | Delivery speed |
| Time Frame | Order date → Ship confirmation | Order date → Actual delivery |
| Measured By | Ship date vs Promised ship date | Delivery date vs "Deliver by" date |

### How They Interact

**Scenario 1: Late Ship, On-Time Delivery**
```
Order: Monday
Promised Ship: Tuesday
Actual Ship: Wednesday (1 day late)
"Deliver by" Date: Friday
Actual Delivery: Thursday

Result:
LSR: ❌ Late ship (counts against LSR)
OTDR: ✅ On-time delivery (arrived before Friday)
```

**Scenario 2: On-Time Ship, Late Delivery**
```
Order: Monday
Promised Ship: Tuesday
Actual Ship: Tuesday (on time)
"Deliver by" Date: Friday
Actual Delivery: Saturday

Result:
LSR: ✅ On-time ship
OTDR: ❌ Late delivery (missed Friday deadline)
```

### FirstMile Responsibility for Both Metrics

**To Maintain LSR < 4%:**
- Upload tracking by promised ship date
- Ensure prompt carrier pickup after label creation
- Process orders quickly (minimize handling time)

**To Maintain OTDR ≥ 90%:**
- Select appropriate carrier service level
- Monitor in-transit packages
- Deliver by "Deliver by" date
- Alert shippers of at-risk orders

**Key Insight:** Shipping on time (LSR) doesn't guarantee on-time delivery (OTDR). FirstMile must optimize both handling AND transit.

---

## Metrics Dashboard Requirements

### Overall OTDR Score
```
┌─────────────────────────────────────┐
│ Amazon On-Time Delivery Rate       │
│                                     │
│           94.2%                     │
│   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░             │
│                                     │
│ Target: 95%+ | Minimum: 90%        │
│ Status: ⚠️ Below Target             │
└─────────────────────────────────────┘
```

Display:
- Current OTDR percentage (large, prominent)
- Visual gauge/progress bar
- Color coding:
  - 🟢 Green: 95%+
  - 🟡 Yellow: 90-94.9%
  - 🔴 Red: < 90%
- Target line (95%)
- Minimum threshold line (90%)

### Current Period Statistics
```
┌────────────────────────────────────────────────┐
│ Calculation Period: Oct 15 - Oct 28 (14 days) │
│ (Excludes: Oct 29 - Nov 4, still in transit)  │
├────────────────────────────────────────────────┤
│ Total Units Shipped: 1,247                    │
│ Units Delivered On Time: 1,175                │
│ Units Delivered Late: 72                      │
│ OTDR: 94.2%                                   │
└────────────────────────────────────────────────┘
```

### At-Risk Orders (Real-Time)
```
┌──────────────────────────────────────────────────┐
│ ⚠️ ORDERS AT RISK OF LATE DELIVERY               │
├──────────────────────────────────────────────────┤
│ Order #111-2233445 | Deliver by: Tomorrow       │
│ Location: Phoenix  | Status: In Transit         │
│ Action: Monitor    | Est. Delivery: On time     │
├──────────────────────────────────────────────────┤
│ Order #111-6677889 | Deliver by: Today 11PM     │
│ Location: Memphis  | Status: Sorting Facility   │
│ Action: URGENT     | Est. Delivery: LATE        │
└──────────────────────────────────────────────────┘
```

### Alert Thresholds

| OTDR Level | Alert Type | Action Required |
|-----------|------------|-----------------|
| 95%+ | ✅ Good Standing | Maintain current operations |
| 92-94.9% | ⚠️ Below Target | Review operations, increase monitoring |
| 90-91.9% | 🟡 Warning | Urgent review, improve carrier selection |
| < 90% | 🔴 Critical | Immediate action, Amazon may restrict |

---

## Business Days Calculation

### Business Days Rules

✅ **Counts as Business Day:**
- Monday
- Tuesday
- Wednesday
- Thursday
- Friday

❌ **Does NOT Count:**
- Saturday
- Sunday
- Federal Holidays (US)

### Federal Holidays (US)

Amazon automatically adjusts for these holidays:
- New Year's Day (January 1)
- Martin Luther King Jr. Day (3rd Monday in January)
- Presidents' Day (3rd Monday in February)
- Memorial Day (Last Monday in May)
- Independence Day (July 4)
- Labor Day (1st Monday in September)
- Columbus Day (2nd Monday in October)
- Veterans Day (November 11)
- Thanksgiving Day (4th Thursday in November)
- Christmas Day (December 25)

### Weekend Deliveries

**Question:** If package is delivered on Saturday, is it on time?

**Answer:** It depends on the "Deliver by" date.

**Example:**
```
"Deliver by" Date: Friday
Actual Delivery: Saturday
Result: ❌ LATE (Saturday doesn't count as business day, deadline was Friday)

"Deliver by" Date: Monday
Actual Delivery: Saturday
Result: ✅ ON TIME (Delivered before Monday deadline)
```

**Key Point:** The calendar date matters for actual delivery, but business days matter for calculating the deadline.

---

## Exception Handling

### What Amazon MAY Excuse

**Major Fulfillment Network Disruptions**

Criteria:
- Event must impact 2 or more major carriers simultaneously
- Examples:
  - Hurricanes affecting entire regions
  - Major bridge collapse blocking key routes
  - Catastrophic weather (blizzards, floods)
  - Infrastructure failures affecting multiple carriers

Amazon's Process:
- Amazon identifies the disruption
- Determines affected geographic regions
- Determines length of protection period
- Automatically excludes affected late deliveries from OTDR

### What Amazon Will NOT Excuse

❌ **Individual Carrier Issues:**
- Single carrier delays
- Package misrouted by carrier
- Carrier lost package
- Carrier's driver called in sick

❌ **Seller Choices:**
- Selected too slow a shipping method
- Used unreliable carrier
- Set transit time too short for capabilities

❌ **Normal Operations:**
- Standard weather delays (rain, snow)
- Holiday shipping volume
- Weekend/holiday delivery limitations
- Distance to destination

### FirstMile's Role in Exceptions

When Disruption Occurs:

1. **Document the Event:**
   - Date and time of disruption
   - Carriers affected
   - Orders impacted
   - Root cause

2. **Notify Shippers:**
   - Alert affected sellers immediately
   - Provide documentation for potential appeals
   - Explain Amazon's potential protection

3. **Monitor Amazon Communications:**
   - Watch for Amazon's official disruption announcements
   - Check if affected orders receive automatic protection
   - Track which regions/dates are covered

4. **Prepare Appeals (if needed):**
   - Compile list of affected orders
   - Document carrier confirmation of delays
   - Screenshot tracking showing disruption
   - Prepare evidence for seller appeals

---

## Shipper Communication Templates

### Template 1: Order Received Notification

**Subject:** Amazon Order [ORDER_ID] - Ship by [DATE] | Deliver by [DATE]

```
Order Confirmation
═══════════════════════════════════════════════════════════

Order Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Order ID: [ORDER_ID]
SKUs: [SKU_LIST]
Total Units: [UNIT_COUNT]

Amazon Deadlines (Pacific Time):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Order Date: [ORDER_DATE] [ORDER_TIME] PST
Ship By Date: [PROMISED_SHIP_DATE] PST
Deliver By Date: [DELIVER_BY_DATE] 11:59:59 PM PST

Timeline:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Handling Time: [X] business days
Transit Time: [X] business days
Total Days: [X] business days

Carrier Assignment:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Carrier: Xparcel
Service Level: [SERVICE_LEVEL]
Transit Capability: [X-Y] days

⚠️ OTDR Impact:
This order counts toward your Amazon On-Time Delivery Rate.
Current OTDR: [XX.X]% | Target: 95%+

Tracking must be uploaded by [PROMISED_SHIP_DATE].
Package must be delivered by [DELIVER_BY_DATE] 11:59:59 PM PST.

Next Steps:
✓ Prepare shipment by [PROMISED_SHIP_DATE]
✓ Ensure package is ready for carrier pickup
✓ Monitor tracking after pickup

Questions? Contact FirstMile Support at [CONTACT_INFO]
```

### Template 2: At-Risk Order Alert

**Subject:** ⚠️ URGENT - Amazon Order [ORDER_ID] At Risk of Late Delivery

```
AT RISK OF LATE DELIVERY
═══════════════════════════════════════════════════════════

Order ID: [ORDER_ID]
Deliver By: [DELIVER_BY_DATE] 11:59:59 PM PST (in [X] days)

Current Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shipped: [SHIP_DATE]
Carrier First Scan: [FIRST_SCAN_DATE]
Current Location: [CITY, STATE]
Last Tracking Update: [LAST_UPDATE]
Estimated Delivery: [ESTIMATED_DELIVERY]

⚠️ RISK ASSESSMENT:
Status: AT RISK
Reason: [REASON: e.g., "Package delayed in Memphis hub"]
Days Until Deadline: [X] days
Estimated vs Required: [ESTIMATED] vs [REQUIRED] (Behind by [X] days)

Impact if Late:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This late delivery will count against your Amazon OTDR.

Current Performance:
- Current OTDR: [XX.X]%
- Late deliveries this period: [X]
- [X] more late deliveries will drop you below 90% threshold

Recommended Actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Monitor tracking closely: [TRACKING_URL]
✓ Document any carrier delays
✓ Contact carrier if no updates in 24 hours
✓ Prepare documentation for potential Amazon appeal

FirstMile is monitoring this shipment closely.
We will provide updates as tracking changes.

Questions? Contact FirstMile Support IMMEDIATELY.
```

### Template 3: Late Delivery Notification

**Subject:** ❌ Amazon Order [ORDER_ID] Delivered Late - OTDR Impact

```
LATE DELIVERY NOTIFICATION
═══════════════════════════════════════════════════════════

Delivery Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required Delivery: [DATE] 11:59:59 PM PST
Actual Delivery: [DATE] [TIME] PST
Days Late: [X]

⚠️ This delivery counts against your Amazon OTDR

Updated Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Units Delivered This Period: [X]
Late Deliveries: [X]
Current OTDR: [X]%
Target: 95%+

⚠️ [X] more late deliveries will drop you below 90% threshold

Root Cause:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[REASON: e.g., "Transit time exceeded - package routed through
secondary hub due to weather delays"]

Carrier: [CARRIER_NAME]
Service Level: [SERVICE_LEVEL]

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Review service level selection for this route
✓ Consider upgrading to faster service for this destination
✓ Document carrier delays for potential Amazon appeal

FirstMile is available to discuss service level optimization.

Questions? Contact FirstMile Support at [CONTACT_INFO]
```

---

## Report Access & Auditing

### Where to View OTDR

1. Go to **Performance** menu → **Account Health**
2. Locate **Shipping Performance** section → Select **On-time delivery rate**
3. Click **View details** → Download report

### Important Notes

**Allow 72 Hours:**
- Metrics and reports update with 72-hour delay
- Account for this when analyzing performance

**Report Fields:**
- All defect report fields listed in [Defect Report Fields](#defect-report-fields) section
- Use for root cause analysis and performance tracking

---

## Key Takeaways

### For FirstMile Operations

1. **"Deliver by" Date is King** - Everything revolves around Order Date + Handling Time + Transit Time

2. **Business Days Only** - Weekends and holidays don't count in calculations

3. **Pacific Time Zone** - All dates measured in PST/PDT, deadline is 11:59:59 PM

4. **5-Day Max for Standard** - Transit time cannot exceed 5 days for standard shipping

5. **90% Minimum / 95% Target** - Stay above 95% to avoid risk zone

6. **Per Unit, Not Per Order** - Multi-SKU orders count each unit separately

7. **Promise Extensions Don't Help** - Sellers judged by original "Deliver by" date

8. **Carrier First Scan Matters** - Amazon tracks from first scan to delivery

9. **72-Hour Reporting Delay** - Allow time for metrics to update before analysis

10. **Xparcel Service Mapping is Critical** - Match Xparcel service to seller's transit time setting

### Critical Actions for FirstMile

✅ **Track "Deliver by" date for every Amazon order**
✅ **Monitor orders approaching deadline (2 days out)**
✅ **Use Xparcel Expedited or Priority for Standard Shipping**
✅ **Alert shippers of at-risk orders immediately**
✅ **Maintain 95%+ OTDR target for healthy performance**
✅ **Document carrier delays for potential seller appeals**
✅ **Provide daily OTDR reporting to shippers**

---

**END OF SPECIFICATION**

*For questions or clarifications, contact FirstMile Operations Team*
