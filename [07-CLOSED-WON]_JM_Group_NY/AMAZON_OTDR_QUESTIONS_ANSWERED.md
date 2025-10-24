# Amazon OTDR Questions - Answered from Specification

**Date:** October 7, 2025
**Customer:** JM Group of NY
**Purpose:** Answer marketplace metrics questions using Amazon OTDR Specification

---

## Questions We CAN Answer from Amazon OTDR Spec

Based on the Amazon OTDR Specification, here are the answers to the questions we can provide definitively.

---

### ✅ QUESTION 1: How does Amazon define "Late Shipment" vs. "On-Time Delivery"?

**ANSWERED from OTDR Spec:**

#### Late Shipment Rate (LSR)
**Definition:** Tracking uploaded AFTER promised ship date

**Calculation:**
```
LSR = (Late shipments) / (Total orders)
```

**What counts as "late shipment":**
- Tracking confirmation uploaded to Amazon AFTER the "Promised Ship Date"
- Measured from Order Date + Handling Time
- Threshold: Must be < 4%
- Penalty: Listing deactivation

**Example:**
```
Order: Monday
Handling Time: 1 day
Promised Ship Date: Tuesday

If tracking uploaded Wednesday = ❌ LATE SHIPMENT (counts against LSR)
If tracking uploaded Tuesday = ✅ ON-TIME SHIPMENT
```

---

#### On-Time Delivery Rate (OTDR)
**Definition:** Package delivered AFTER "Deliver by" date

**Calculation:**
```
OTDR = (Units delivered on or before "Deliver by" date) / (Total tracked units shipped)
```

**What counts as "late delivery":**
- Actual delivery date is AFTER the "Deliver by" date
- "Deliver by" date = Order Date + Handling Time + Transit Time (all business days)
- Measured in Pacific Time (PST/PDT)
- Deadline: 11:59:59 PM PST on "Deliver by" date
- Threshold: Must be ≥ 90%
- Penalty: Listing restriction

**Example:**
```
Order: Monday
Handling Time: 1 day
Transit Time: 3 days
"Deliver by" Date: Thursday, 11:59:59 PM PST

If delivered Friday = ❌ LATE DELIVERY (counts against OTDR)
If delivered Thursday = ✅ ON-TIME DELIVERY
```

---

#### Key Difference
**LSR focuses on SHIPPING speed** (Did you upload tracking on time?)
**OTDR focuses on DELIVERY speed** (Did package arrive on time?)

**You can have:**
- Late shipment + On-time delivery (shipped late but delivered on time)
- On-time shipment + Late delivery (shipped on time but delivered late)
- Both late (worst case)

---

### ✅ QUESTION 2: What are the promised delivery windows by shipping speed?

**ANSWERED from OTDR Spec:**

#### Standard Shipping (Contiguous US)
**Maximum Transit Time:** 5 days (changed from 8 days on August 25, 2024)

**Allowed Transit Time Settings:**
- 2 days
- 3 days
- 4 days
- 5 days (maximum)

**Calculation:**
```
"Deliver by" Date = Order Date + Handling Time + Transit Time
(All in BUSINESS DAYS)
```

**Example for Standard Shipping:**
```
Order: Monday 10:00 AM
Handling Time: 1 day (seller's setting)
Transit Time: 5 days (seller's setting, maximum for Standard)

"Deliver by" Date = Monday + 1 + 5 = Next Monday, 11:59:59 PM PST
```

---

#### Free Economy Shipping
**Maximum Transit Time:** 8 days (changed from 10 days on August 25, 2024)

**Allowed Transit Time Settings:**
- 6 days
- 7 days
- 8 days (maximum)

**Use Case:** Slower, lower-cost shipping option

---

#### Media Exception (Books, Magazines, DVDs)
**Transit Time:** 5-day maximum does NOT apply
- Separate rules
- Different transit time options

---

#### Expedited Shipping
**Note:** Amazon OTDR spec does not define specific "Expedited Shipping" transit times as a separate category. This is a seller-configurable option that falls under Standard Shipping rules with shorter transit times (typically 2-3 days).

---

#### Two-Day Shipping
**Note:** Amazon OTDR spec does not define "Two-Day Shipping" transit time windows in the same way. This is typically a seller-configured transit time of 2 days within Standard Shipping.

---

### ✅ QUESTION 2B: Does Amazon calculate from order date or ship date?

**ANSWERED from OTDR Spec:**

**For "Deliver by" Date Calculation:**
Amazon calculates from **ORDER DATE**, not ship date.

**Formula:**
```
"Deliver by" Date = ORDER DATE + Handling Time + Transit Time
```

**NOT:**
```
❌ WRONG: Ship Date + Transit Time
```

**Why this matters:**
- Handling time is part of the delivery promise
- Late shipping reduces available transit time
- Seller is accountable for entire timeline from order to delivery

**Example:**
```
Order Date: Monday
Handling Time: 2 days (seller's setting)
Transit Time: 3 days (seller's setting)

"Deliver by" Date = Monday + 2 + 3 = Next Monday

If seller ships late (Wednesday instead of Tuesday):
- Still must deliver by Monday
- Now only has 5 calendar days instead of 6
- Higher risk of late delivery
```

---

### ✅ QUESTION 2C: Does "business days" include weekends, or only Mon-Fri?

**ANSWERED from OTDR Spec:**

**Business Days = Monday through Friday ONLY**

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

**Federal Holidays Excluded:**
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

---

#### Weekend Delivery Example

**Question:** If package is delivered on Saturday, is it on time?

**Answer:** It depends on the "Deliver by" date.

**Scenario 1:**
```
"Deliver by" Date: Friday, 11:59:59 PM PST
Actual Delivery: Saturday, 10:00 AM PST

Result: ❌ LATE (Saturday is after Friday deadline)
```

**Scenario 2:**
```
"Deliver by" Date: Monday, 11:59:59 PM PST
Actual Delivery: Saturday, 10:00 AM PST

Result: ✅ ON TIME (Delivered before Monday deadline)
```

**Key Point:** The calendar date of actual delivery is compared against the "Deliver by" date, but business days are used to calculate the "Deliver by" date.

---

#### Holiday Example

```
Order: Monday (week of Thanksgiving)
Handling Time: 1 day
Transit Time: 3 days
Holiday: Thursday (Thanksgiving)

Calculation:
Monday (Day 0) - Order placed
Tuesday (Day 1) - Handling
Wednesday (Day 2) - Transit day 1
Thursday (skip) - Thanksgiving holiday
Friday (Day 3) - Transit day 2
Saturday (skip) - Weekend
Sunday (skip) - Weekend
Monday (Day 4) - Transit day 3

"Deliver by" Date: Monday (8 calendar days later, 4 business days)
```

---

### ✅ QUESTION 3: How does Amazon calculate the "promised delivery date"?

**ANSWERED from OTDR Spec:**

#### Promised Delivery Date Calculation

**Official Formula:**
```
Promised Delivery Date = Order Date + Handling Time + Transit Time
(All values in BUSINESS DAYS, measured in Pacific Time)
```

---

#### Components Explained

**1. Order Date**
- Timestamp when customer placed order on Amazon
- Starting point for all calculations
- Shown in GMT (primary) and PST/PDT (secondary)

**2. Handling Time**
- Set by seller per SKU or account default
- Common values: 1-3 business days
- Time from order receipt to shipping

**3. Transit Time**
- Set by seller in shipping template
- Seller chooses based on their carrier capability
- Standard Shipping: 2-5 days maximum
- Free Economy: 6-8 days maximum

---

#### Complete Example

```
Order Placed: Friday, 2:00 PM PST
Seller's Handling Time: 1 business day
Seller's Transit Time: 3 business days

Step-by-step calculation:
Friday (Day 0) - Order received
Saturday (skip) - Weekend
Sunday (skip) - Weekend
Monday (Day 1) - Handling day
Tuesday (Day 2) - Transit day 1
Wednesday (Day 3) - Transit day 2
Thursday (Day 4) - Transit day 3

Promised Delivery Date: Thursday, 11:59:59 PM PST
```

---

#### Who Sets These Values?

**Handling Time:**
- ✅ Seller configures in Amazon Seller Central
- Set per SKU or account default
- Cannot be changed after order is placed

**Transit Time:**
- ✅ Seller configures in shipping templates
- Chosen based on seller's shipping method
- Must not exceed Amazon maximums:
  - Standard: 5 days max
  - Economy: 8 days max

**Order Date:**
- ❌ Seller does NOT control
- Set by Amazon when customer places order

---

#### What Customer Sees vs What Seller is Judged By

**Customer View (with promise extensions):**
```
"Guaranteed delivery by Friday, Nov 15"
(May include 1-2 day promise extension for weather, carrier delays)
```

**Seller's Accountability (without promise extensions):**
```
"Deliver by" Date: Thursday, Nov 14, 11:59:59 PM PST
(Original calculation, NO extensions applied)
```

**Critical Point:**
- Customers may see a LATER date (with extensions)
- Sellers are judged by EARLIER date (without extensions)
- Promise extensions do NOT help seller's OTDR

---

### ✅ QUESTION 4: What is the "Deliver by" date time zone?

**ANSWERED from OTDR Spec:**

#### Time Zone: Pacific Time (PST/PDT)

**All "Deliver by" dates are measured in Pacific Time.**

**Deadline Format:**
```
"Deliver by" Date: [DATE], 11:59:59 PM PST/PDT
```

---

#### Critical Time Zone Examples

**Example 1: East Coast Delivery**
```
"Deliver by" Date: January 15, 11:59:59 PM PST

Package delivered in New York:
- January 15, 11:00 PM EST = ✅ ON TIME (8:00 PM PST, before deadline)
- January 16, 2:00 AM EST = ❌ LATE (11:00 PM PST, after deadline)
```

**Example 2: Midnight Crossing**
```
"Deliver by" Date: January 15, 11:59:59 PM PST

Package delivered:
- January 15, 11:59:58 PM PST = ✅ ON TIME (1 second before deadline)
- January 16, 12:00:01 AM PST = ❌ LATE (2 seconds after deadline)
```

---

#### Why This Matters for FirstMile

**Scenario:**
```
Package delivered in Florida: January 15, 11:30 PM EST
"Deliver by" Date: January 15, 11:59:59 PM PST

Florida time: 11:30 PM EST
Pacific time: 8:30 PM PST

Result: ✅ ON TIME (delivered 3.5 hours before PST deadline)
```

**FirstMile Tracking Must:**
- Convert all delivery timestamps to Pacific Time
- Compare against PST/PDT deadline
- Account for time zone differences

---

### ✅ QUESTION 5: When does the 14-day calculation window apply?

**ANSWERED from OTDR Spec:**

#### OTDR Calculation Window

**14-Day Rolling Window with Exclusions:**

**Step 1:** Pull data from last 21 days
**Step 2:** Exclude most recent 7 days (packages still in transit)
**Step 3:** Calculate OTDR from remaining 14-day window

---

#### Example Calculation

```
Today's Date: November 4, 2025

Step 1: Pull last 21 days
- Start: October 14, 2025
- End: November 3, 2025
- Total shipments in this period: 130 units

Step 2: Exclude most recent 7 days
- Exclude: October 28 - November 3 (still in transit)
- Excluded shipments: 30 units

Step 3: Calculate from 14-day window
- Evaluated period: October 14 - October 27 (14 days)
- Units evaluated: 100 units
- Units delivered on time: 90 units
- Units delivered late: 10 units

OTDR = 90 / 100 = 90.0%
```

---

#### Why 7-Day Exclusion?

**Reason:** Many packages are still in transit during this period

**Example:**
```
Package shipped: November 1
Transit time: 5 days
Expected delivery: November 6 (still 2 days away)

This package is excluded from OTDR calculation until November 8
(72 hours after delivery to allow for tracking updates)
```

---

#### When Does OTDR Update?

**Update Frequency:** Daily

**Data Lag:** 72 hours after delivery

**Example:**
```
Package delivered: November 1
Amazon's tracking receives update: November 2
OTDR calculation includes this delivery: November 4 (72 hours later)
```

**Why 72-hour lag:**
- Allows carrier tracking systems to update
- Gives time for delivery confirmations
- Accounts for weekend/holiday processing delays

---

#### Impact on Real-Time Monitoring

**For FirstMile:**
```
Today: November 4
Most recent OTDR data: Deliveries through October 28

At-Risk Orders to Monitor:
- Shipped October 29 - November 3 (in transit, not yet counted)
- "Deliver by" dates: November 1 - November 8
- These will impact OTDR starting November 8-11
```

**Key Point:** FirstMile must monitor in-transit orders NOW to prevent OTDR impact LATER (7-10 days from ship date).

---

## Questions We CANNOT Answer (Need JM Group Input)

The following questions require JM Group's specific configuration and data:

---

### ❌ QUESTION 6: What shipping speeds do your customers select?

**Why we can't answer:**
- This is unique to JM Group's customer base
- Varies by product, price point, and customer preferences
- Not defined in Amazon OTDR spec (seller-specific)

**What we need from JM Group:**
```
% of orders: Standard Shipping
% of orders: Expedited Shipping
% of orders: Two-Day Shipping
% of orders: One-Day Shipping
% of orders: Free Economy
```

**Where to find:**
- Amazon Seller Central → Reports → Shipping Performance
- ShipStation → Reports → Shipping Method breakdown

---

### ❌ QUESTION 7: What transit times have you set in your shipping templates?

**Why we can't answer:**
- Seller-configurable setting in Amazon Seller Central
- Not visible to FirstMile without access to JM Group's account

**What we need from JM Group:**
```
For Standard Shipping: [2, 3, 4, or 5 days?]
For Free Economy: [6, 7, or 8 days?]
For other shipping speeds: [?]
```

**Where to find:**
- Amazon Seller Central → Settings → Shipping Settings
- Shipping Templates → Transit Time column

**Why this is CRITICAL:**
```
If JM Group set transit time to 5 days:
- FirstMile must use Xparcel Expedited (2-5 days)
- Xparcel Ground (3-8 days) = HIGH RISK of late delivery

If JM Group set transit time to 3 days:
- FirstMile must use Xparcel Priority (1-3 days)
- Xparcel Expedited or Ground = GUARANTEED late delivery
```

---

### ❌ QUESTION 8: What is your handling time setting?

**Why we can't answer:**
- Seller-configurable setting
- Can be set per SKU or account default

**What we need from JM Group:**
```
Handling Time: [1, 2, or 3 days?]
```

**Why this matters:**
```
Example with 5-day transit time setting:

Handling Time: 1 day
"Deliver by" = Order Date + 1 + 5 = 6 business days total
FirstMile has 5 days for transit

Handling Time: 3 days
"Deliver by" = Order Date + 3 + 5 = 8 business days total
FirstMile still has only 5 days for transit (same constraint)
```

**Impact:** Handling time doesn't change FirstMile's transit window, but it does affect when package enters FirstMile's system.

---

### ❌ QUESTION 9: Can you share 10-20 tracking numbers Amazon flagged as "late"?

**Why we can't answer:**
- Requires access to JM Group's Amazon OTDR Defect Report
- Only visible in their Seller Central account

**What we need from JM Group:**
```
Tracking numbers for packages Amazon counted as:
- Late shipment (LSR violation)
- Late delivery (OTDR violation)

Plus for each:
- Order ID
- "Deliver by" date
- Actual delivery date
- Ship method
- Destination state
```

**Where to find:**
- Amazon Seller Central → Performance → Account Health
- Shipping Performance → On-time delivery rate → View details → Download report

**Why we need this:**
```
With actual tracking numbers, FirstMile can:
✓ Trace exact route through Xparcel network
✓ Identify carrier-specific delays
✓ Determine if issue is zone-specific
✓ Check if service level was appropriate
✓ Provide root cause analysis
✓ Recommend specific fixes
```

---

### ❌ QUESTION 10: What is your current ShipStation automation setup?

**Why we can't answer:**
- Unique to JM Group's ShipStation configuration
- Requires access to their account

**What we need from JM Group:**
```
Current service level selection method:
□ Manual selection for each order
□ ShipStation automation rules
□ Default to one service level for all orders

If using automation rules:
- Rule 1: [Condition] → [Xparcel Service]
- Rule 2: [Condition] → [Xparcel Service]
- etc.
```

**Example automation rules we might recommend:**
```
IF marketplace = "Amazon" AND shipping_method = "Standard" AND zone <= 4
  THEN use Xparcel Ground

IF marketplace = "Amazon" AND shipping_method = "Standard" AND zone >= 5
  THEN use Xparcel Expedited

IF marketplace = "Walmart"
  THEN use Xparcel Expedited (to protect 92.8% OTDR)
```

---

## Summary: What We Know vs. What We Need

### ✅ WE CAN ANSWER (From Amazon OTDR Spec):

1. ✅ How Amazon defines "Late Shipment" vs "On-Time Delivery"
2. ✅ Maximum transit times by shipping speed (5 days Standard, 8 days Economy)
3. ✅ "Deliver by" date calculation formula (Order Date + Handling + Transit)
4. ✅ Business days definition (Mon-Fri only, excludes weekends/holidays)
5. ✅ Time zone (Pacific Time, 11:59:59 PM PST/PDT deadline)
6. ✅ OTDR calculation window (14-day rolling, excludes most recent 7 days)
7. ✅ How promise extensions work (help customer, don't help seller)
8. ✅ What Amazon excuses (major disruptions) and doesn't (individual delays)

---

### ❌ WE NEED FROM JM GROUP:

1. ❌ What % of orders are Standard vs Expedited vs Two-Day shipping?
2. ❌ What transit times have you set in your Amazon shipping templates?
3. ❌ What is your handling time setting?
4. ❌ Can you provide 10-20 tracking numbers Amazon flagged as late?
5. ❌ What's your current ShipStation automation setup for service level selection?
6. ❌ What are your top destination states by marketplace (Amazon vs Walmart)?
7. ❌ When did you start using FirstMile? (To compare performance before/after)

---

## Next Steps

**With this information, we can now:**

1. **Explain the disconnect** between FirstMile's 99.9% SLA (8-day window) and JM Group's marketplace metrics (likely using 4-5 day transit time settings)

2. **Provide educated recommendations** based on Amazon's Standard Shipping 5-day maximum:
   - Recommend Xparcel Expedited (2-5 days) as default for Standard Shipping
   - Recommend Xparcel Priority (1-3 days) for 2-3 day transit settings

3. **Wait for JM Group's answers** to the remaining questions to provide exact, tailored optimization

---

**Status:** Partial answers provided from Amazon OTDR Specification
**Next:** Send meeting request with remaining questions to JM Group
