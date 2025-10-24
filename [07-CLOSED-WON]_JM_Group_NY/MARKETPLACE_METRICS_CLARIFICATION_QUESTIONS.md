# Marketplace Metrics Clarification Questions for JM Group

**Purpose**: Understand exact marketplace performance requirements to optimize Xparcel configuration
**Date**: October 7, 2025
**From**: Brett Walker, FirstMile
**To**: Yehoshua & Daniel, JM Group of NY

---

## 🎯 OBJECTIVE

Before we can properly optimize your Xparcel setup, I need to understand the **exact marketplace performance calculation rules** for Amazon and Walmart. The screenshots you shared showed headline metrics, but I need the details behind them to configure your shipping correctly.

---

## 📊 MARKETPLACE METRICS FROM YOUR SCREENSHOTS (Sep 30, 2025)

### Amazon Account 1 (Primary)
- **Late Shipment Rate**: 1.44% (Target: <4%)
- **On-Time Delivery Rate**: 95.69% (Target: >90%)
- **Valid Tracking Rate**: 99.34% (Target: >95%)
- **Time Period**: Last 30 days
- **Volume**: 57 of 5,960 orders (30 days), 2,000 of 2,090 units (14 days)

### Amazon Account 2
- **On-Time Delivery Rate**: 94.84% (Target: >90%)
- **Time Period**: 14 days
- **Volume**: 1,562 of 1,647 units

### Walmart Account
- **On-Time Delivery Rate**: 92.8% (Target: >90%)
- **Time Period**: Last 30 days

---

## ❓ CRITICAL QUESTIONS I NEED ANSWERED

### 1. Amazon Late Shipment Rate (1.44%)

**Question**: How does Amazon define "Late Shipment"?

**What I need to know**:
- Is this based on **ship date vs. promised ship date**?
- Or is this based on **delivery date vs. promised delivery date**?
- What is the **promised ship date** typically? (Same day? Next day? 2 days after order?)
- Does the promise vary by SKU, fulfillment method, or Prime status?

**Why this matters**:
- If "Late Shipment" = shipped after promised ship date → I need to optimize pickup times and induction speed
- If "Late Shipment" = delivered after promised delivery date → I need to optimize transit times and service level selection

**Example scenario I need clarification on**:
```
Customer orders on Monday 10am
Promised ship date: Tuesday (next business day)
Actual ship date: Wednesday (1 day late)
Delivery date: Friday (still arrives on time for promised delivery)

Question: Is this counted as a "late shipment" because it shipped late,
even though it delivered on time?
```

---

### 2. Amazon On-Time Delivery Rate (95.69%)

**Question**: How does Amazon calculate the "promised delivery date"?

**What I need to know**:
- Is the promised delivery date shown to the customer at checkout?
- Is it based on **shipping speed selected** (Standard, Expedited, 2-Day, 1-Day)?
- What are the typical delivery windows by shipping speed?
  - Standard Shipping: ___ business days?
  - Expedited Shipping: ___ business days?
  - Two-Day Shipping: ___ business days?
  - One-Day Shipping: ___ business days?
- Does Amazon calculate from **order date** or **ship date**?
- Does "business days" include weekends, or only Mon-Fri?

**Why this matters**:
- I need to map your Amazon shipping speed promises to the correct Xparcel service level
- Standard Shipping → Xparcel Ground (3-8 days)? Or Xparcel Expedited (2-5 days)?
- Expedited Shipping → Xparcel Expedited (2-5 days)? Or Xparcel Priority (1-3 days)?

**Example scenario I need clarification on**:
```
Customer orders Standard Shipping on Monday 10am
Amazon shows promised delivery: Friday (5 business days)
Package ships Tuesday, delivers Saturday (4 calendar days, but 5 business days)

Question: Is Saturday delivery counted as "on time" or "late"
since it's after the Friday promise but within the business day window?
```

---

### 3. Walmart On-Time Delivery Rate (92.8%)

**Question**: How does Walmart calculate "on-time delivery"?

**What I need to know**:
- What is the **promised delivery window** Walmart shows to customers?
- Is it a **specific date** (e.g., "Arrives by Oct 10") or a **date range** (e.g., "Arrives Oct 10-12")?
- Does Walmart calculate from **order date** or **ship date**?
- What are the typical delivery commitments?
  - Standard Shipping: ___ days?
  - Two-Day Shipping: ___ days?
  - Next-Day Shipping: ___ days?
- Does Walmart use business days or calendar days?
- Does the promised delivery vary by **product category** or **seller tier**?

**Why this matters**:
- Your Walmart on-time rate (92.8%) is dangerously close to the 90% threshold
- I need to understand if Walmart's expectations are more aggressive than Amazon's
- This will determine if we need to use Expedited vs. Ground for Walmart orders

**Example scenario I need clarification on**:
```
Customer orders on Monday
Walmart shows: "Arrives by Thursday" (3 business days)
Package ships Tuesday, delivers Friday (1 day late)

Question: Is this counted as late? Or does Walmart have grace periods?
```

---

### 4. Shipping Speed Selection by Order

**Question**: Can you share data on which shipping speeds your customers select?

**What I need to know**:
- % of orders that are **Standard Shipping**
- % of orders that are **Expedited/Two-Day Shipping**
- % of orders that are **Next-Day/One-Day Shipping**
- % of orders that are **Prime** (if applicable on Amazon)

**Why this matters**:
- If 90% of your orders are Standard Shipping → I can optimize for Xparcel Ground
- If 50%+ are Expedited → I need to shift more volume to Xparcel Expedited or Priority
- This helps me understand which Xparcel service level to default to

**Can you provide this data from**:
- Amazon Seller Central → Reports → Shipping Performance
- Walmart Seller Center → Performance → Shipping Details
- ShipStation → Reports → Shipping Method breakdown

---

### 5. Geographic Distribution by Marketplace

**Question**: Do certain marketplaces ship to different regions?

**What I need to know**:
- Are your Amazon orders concentrated in specific states/regions?
- Are your Walmart orders different geographically than Amazon?
- Do you see different performance by destination zone (East Coast vs. West Coast)?

**Why this matters**:
- If Walmart ships more to Zone 7-8 (cross-country), that explains the 92.8% on-time rate
- If Amazon ships more regionally (Zones 1-4), that supports the 95.69% on-time rate
- I can optimize Xparcel service level selection by destination zone per marketplace

**Can you provide**:
- Top 10 destination states by marketplace (Amazon vs. Walmart)
- Or export from ShipStation filtered by marketplace

---

### 6. ShipStation Integration & Automation

**Question**: How do you currently select Xparcel service levels in ShipStation?

**What I need to know**:
- Are you using **ShipStation automation rules** to select Xparcel Ground vs. Expedited vs. Priority?
- Or are you **manually selecting** service level for each order?
- Are service levels mapped by:
  - Marketplace shipping speed selected by customer?
  - Destination zone?
  - Package weight?
  - Product SKU?
  - Default to one service level for everything?

**Why this matters**:
- If you're defaulting everything to Xparcel Ground → that explains the marketplace issues
- I can help you set up **ShipStation automation rules** to intelligently route:
  - Amazon 2-Day orders → Xparcel Expedited
  - Amazon Standard Shipping, Zones 1-4 → Xparcel Ground
  - Amazon Standard Shipping, Zones 5-8 → Xparcel Expedited
  - Walmart orders (closer to threshold) → Xparcel Expedited
  - High-value orders → Xparcel Priority

**Can you share**:
- Screenshot of your current ShipStation automation rules (if any)
- Or description of how you currently select service levels

---

### 7. Historical Performance Trends

**Question**: When did your marketplace metrics start declining?

**What I need to know**:
- What were your Amazon/Walmart on-time rates **before** you switched to FirstMile?
- What carrier were you using previously?
- When did you start using FirstMile? (What date did volume ramp up?)
- Have the metrics been declining steadily, or was there a sudden drop?

**Why this matters**:
- If metrics were 98% before FirstMile and dropped to 95% after → clearly a FirstMile issue
- If metrics were already 93% and dropped to 92% → might be seasonal or marketplace-wide
- This helps me understand if the issue is FirstMile-specific or broader operational changes

**Can you provide**:
- Amazon/Walmart performance history from Seller Central (last 90 days chart)
- Date you switched to FirstMile
- Previous carrier performance (if you tracked it)

---

### 8. Specific Tracking Numbers for Late Deliveries

**Question**: Can you provide 10-20 specific tracking numbers that Amazon/Walmart flagged as "late"?

**What I need to know**:
- Tracking numbers for shipments Amazon counted as "late shipment"
- Tracking numbers for shipments Amazon counted as "late delivery"
- Tracking numbers for shipments Walmart counted as "late delivery"

**Why this matters**:
- I can trace these exact shipments through FirstMile's system
- I can identify patterns:
  - Were they all to specific zones?
  - Were they all routed through a specific carrier (e.g., ACI services)?
  - Were they all a specific service level (Ground)?
  - Were they all a specific weight range?
  - Did they get stuck at a specific hub?
- This gives me **exact root cause** instead of assumptions

**Can you export from**:
- Amazon Seller Central → Orders → Filter by "Late Shipment" or "Late Delivery"
- Walmart Seller Center → Orders → Filter by "Late Delivery"
- Provide tracking numbers + order numbers + promised delivery dates

---

## 🎯 WHAT I'LL DO WITH THIS INFORMATION

Once you provide these answers, I can:

### 1. Map Marketplace Promises to Xparcel Service Levels
```
Amazon Standard Shipping (5-8 days) → Xparcel Ground (3-8 days) ✅
Amazon Expedited Shipping (2-4 days) → Xparcel Expedited (2-5 days) ✅
Amazon Two-Day Shipping (2 days) → Xparcel Priority (1-3 days) ✅

Walmart Standard (4-7 days) → Xparcel Ground or Expedited? (depends on your answer)
Walmart Two-Day (2 days) → Xparcel Priority (1-3 days) ✅
```

### 2. Configure ShipStation Automation Rules
```
IF marketplace = Amazon AND shipping_speed = "Two-Day"
   THEN use Xparcel Priority

IF marketplace = Amazon AND shipping_speed = "Standard" AND zone IN (1,2,3,4)
   THEN use Xparcel Ground

IF marketplace = Amazon AND shipping_speed = "Standard" AND zone IN (5,6,7,8)
   THEN use Xparcel Expedited

IF marketplace = Walmart
   THEN use Xparcel Expedited (to protect 92.8% on-time rate)
```

### 3. Optimize by Carrier Performance
```
Based on pivot table data:
- Route through ACL_Direct_Regional (2.87 days avg) for Ground-eligible
- Avoid ACI services (4.15-4.35 days avg) or force to Expedited
- Use DHL SmartMail strategically for Zones 1-4 only
```

### 4. Create Proactive Alerts
```
IF in_transit_days > (promised_delivery_date - ship_date - 2 days buffer)
   THEN alert JM Group: "Tracking ABC123 at risk of late delivery"
```

### 5. Generate Marketplace-Specific Reports
```
Daily report showing:
- Projected late shipment rate (Amazon definition)
- Projected on-time delivery rate (Amazon + Walmart definitions)
- At-risk tracking numbers
- Recommended service level adjustments
```

---

## 📧 SENDING THIS TO JM GROUP

**Subject**: Questions to Optimize Your FirstMile Xparcel Setup for Marketplace Performance

**Body**:

Yehoshua and Daniel,

Before we meet, I need to understand the exact marketplace performance calculations to properly optimize your Xparcel configuration. The screenshots you shared showed headline metrics, but I need the details behind them.

I've prepared 8 specific questions (attached) that will help me:
1. Map marketplace shipping promises to correct Xparcel service levels
2. Configure ShipStation automation rules for intelligent routing
3. Identify exact root causes of late deliveries
4. Create proactive alerts before packages risk being late

**Key questions**:
- How does Amazon define "Late Shipment" vs. "On-Time Delivery"?
- What are the promised delivery windows by shipping speed?
- Can you share 10-20 tracking numbers Amazon/Walmart flagged as late?
- What's your current ShipStation automation setup?

Once I have these answers, I can configure your Xparcel setup to protect your marketplace metrics.

Can you review the attached questions and provide answers before our meeting? This will make our discussion much more actionable.

Brett Walker
FirstMile
402-718-4727

---

**Attachment**: MARKETPLACE_METRICS_CLARIFICATION_QUESTIONS.md (this file)

---

## 📋 SUMMARY OF WHAT I NEED

**Critical (Need Before Meeting)**:
1. ✅ Amazon "Late Shipment" definition (ship date or delivery date based?)
2. ✅ Promised delivery windows by shipping speed (Amazon + Walmart)
3. ✅ 10-20 tracking numbers flagged as "late" by marketplaces
4. ✅ Current ShipStation automation rules (if any)

**Important (Can Discuss in Meeting)**:
5. 🔍 Shipping speed distribution (% Standard vs. Expedited vs. Next-Day)
6. 🔍 Geographic distribution by marketplace
7. 🔍 Historical performance trends (before/after FirstMile)

**Nice to Have (For Post-Meeting Optimization)**:
8. 📊 Additional marketplace performance data exports

---

**Status**: DRAFT - Ready to send to Yehoshua & Daniel
**Next Step**: Send via email before meeting invitation
**Expected Response Time**: 24-48 hours
