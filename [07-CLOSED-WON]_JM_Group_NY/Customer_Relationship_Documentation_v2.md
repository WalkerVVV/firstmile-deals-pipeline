# Customer Relationship Documentation - JM Group of NY

**Status**: 🚨 **CRITICAL - CANCELLED PICKUPS** (Oct 6, 2025)
**Stage**: [07-CLOSED-WON] → **AT RISK - IMMEDIATE ATTENTION REQUIRED**
**Deal Value**: TBD (Active Customer)
**Last Updated**: October 7, 2025 (11:45 AM)

---

## 🚨 CRITICAL SITUATION SUMMARY

**September 30, 2025**: Customer alerts FirstMile that marketplace performance metrics approaching dangerous thresholds. Daniel cancels pickups same day after reviewing FirstMile report showing 37.8% in-transit late rate.

**October 6, 2025**: Pickups formally cancelled. No response to meeting invitation.

**ROOT CAUSE**: FirstMile's in-transit visibility (37.8% late) creates marketplace risk perception, even though delivered performance (99.9%) is excellent. Amazon/Walmart account suspension risk > cost savings.

---

## Key Contacts

**Yehoshua** ("Shua") - Primary Contact, Owner
- Email: yehoshua.jmgroupny@gmail.com
- Phone: (347) 988-9391

**Daniel Ash** - Operations Manager
- Email: jmgroupny@gmail.com
- Phone: +1 (347) 260-7077
- Address: 2691 West 15th St, Brooklyn NY 11235
- Website: https://underessentials.com/

---

## Marketplace Performance Context (THE REAL DRIVER)

JM Group sells on Amazon (2 accounts) and Walmart. Marketplace performance thresholds:
- Amazon: <4% late shipment rate, >90% on-time delivery
- Walmart: >90% on-time delivery

**Current Status (Sep 30, 2025 from ShipStation)**:

| Marketplace | Metric | Current | Target | Risk Level |
|-------------|--------|---------|--------|------------|
| Amazon Acct 1 | Late Shipment Rate | 1.44% | <4% | Safe but monitoring |
| Amazon Acct 1 | On-Time Delivery | 95.69% | >90% | Meets standard |
| Amazon Acct 2 | On-Time Delivery | 94.84% | >90% | Close to threshold |
| Walmart | On-Time Delivery | 92.8% | >90% | Close to threshold |

**Quote from Yehoshua (Sep 30)**: "we wanna improve these before they get close to our max limit allowed"

**Quote from Daniel (Sep 30)**: "These performance metrics are extremely sensitive across all marketplaces—especially Amazon and Walmart... If we fail to uphold strong standards in these areas, any cost savings elsewhere become irrelevant, as we risk being restricted or removed from selling on these platforms entirely."

---

## Communication Timeline (Sep 30 - Oct 6)

**Sep 30, 9:01 AM** - Yehoshua requests ZIP-level performance export

**Sep 30, 12:19 PM** - Yehoshua flags marketplace metrics approaching thresholds

**Sep 30, 12:23 PM** - Yehoshua: Walmart at 92%, "thats cutting it close"

**Sep 30, 1:01 PM** - Daniel: "I'm considering a temporary pause on FM activity until we regain control of our metrics... please cancel the scheduled pickup"

**Sep 30, 4:32 PM** - Brett: "I'll cancel tomorrow's pickup. Let's jump on a call..."

**Sep 30, 5:50 PM** - Brett sends comprehensive performance report + FirstMile network data

**Oct 6, 10:00 AM** - Brett: Meeting invitation for Oct 6

**Oct 6, EOD** - **No response, pickups cancelled**

---

## Performance Analysis

### FirstMile Performance (Aug 7 - Sep 29, 2025)

**Delivered SLA Compliance**: 99.9%

| Service | SLA Window | Avg Transit | Network Avg | JM vs Network |
|---------|------------|-------------|-------------|---------------|
| Ground | 8 days | 3.3 days | 4.42 days | **25% faster** |
| Expedited | 5 days | 2.0 days | 4.14 days | **52% faster** |
| Priority | 3 days | Same day | 2.90 days | **Same day** |

**In-Transit Status (Sep 30)**:
- Total in-transit: 1,676 shipments
- Within SLA: 1,042 (62.2%)
- **Outside SLA: 634 (37.8%)** ⚠️

**THE PARADOX**: JM Group beats FirstMile network averages on delivered performance, BUT the 37.8% in-transit late rate creates marketplace risk perception.

---

## Recovery Strategy

### Meeting Agenda (45 minutes)

**1. Acknowledge the Issue (5 min)**
"You cancelled pickups Oct 6 after our Sep 30 conversation. I understand—your marketplace metrics are too close to thresholds, and our 37.8% in-transit late rate created unacceptable uncertainty."

**2. Root Cause (10 min)**
- In-transit visibility issue: Packages show "late" but deliver on time
- Marketplace reporting mismatch: FirstMile 8-day Ground ≠ Amazon/Walmart 2-5 day expectations
- Zone 7-8 cross-country lanes struggling
- Induction cadence delays inflate in-transit age

**3. Service Improvements (15 min)**

**Phase 1: Immediate Fixes**
- ZIP-limit high-risk destinations (Ground → Expedited)
- Marketplace-specific reporting (Amazon/Walmart format)
- Proactive alerts when packages approach thresholds
- Earlier pickup times to reduce induction lag

**Phase 2: Performance Guarantee**
- 95%+ on-time delivery (marketplace definition)
- <2% late shipment rate (well below Amazon 4% threshold)
- Daily performance dashboard
- Weekly check-ins until 4 consecutive weeks at target

**4. Customer Feedback (10 min)**
- What marketplace metrics concern you most?
- What performance thresholds would make you comfortable restarting?
- Are you currently using alternative carriers?

**5. Path Forward (5 min)**

**Phased Restart**:
- Week 1: Test batch (100 shipments), daily reports
- Week 2: Expand to 50% volume if Week 1 hits target
- Week 3: Full volume if Week 2 sustains
- Month 2: Performance review + volume growth

---

## Meeting Request Email (RECOMMENDED)

**Subject**: JM Group - Can We Meet This Week?

**To**: yehoshua.jmgroupny@gmail.com, jmgroupny@gmail.com

**Body**:
```
Yehoshua and Daniel,

Pickups were cancelled October 6. I understand why—marketplace metrics too close to thresholds.

Our September 30 report flagged 634 packages sitting late in-transit (37.8%). We've identified root causes and have marketplace-specific fixes ready (ZIP-limits, proactive alerts, Amazon/Walmart reporting format).

Can we meet this week?

Monday 2pm-5pm | Tuesday 10am-12pm or 2pm-5pm | Wednesday 9am-5pm

30-45 minutes. Your office or video call.

Brett Walker
FirstMile
402-718-4727
```

---

## Files & Data

**Performance Reports**:
- FirstMile_Xparcel_Performance_JM_Group_NY_20250930_1253.xlsx (Sep 30, 2025)
- In_Transit_Outside_SLA_Detail.csv (634 late packages)

**Marketplace Data** (ShipStation screenshots):
- Amazon Account 1: Late 1.44%, On-time 95.69%, Valid tracking 99.34%
- Amazon Account 2: On-time 94.84%
- Walmart: On-time 92.8%

**Scripts**:
- analyze_634_outside_sla.py
- sla_by_service_level.py
- firstmile_orchestrator.py

---

## Critical Success Factors

1. **Marketplace-focused reporting** - Speak Amazon/Walmart language
2. **Proactive alerts** - Warn before thresholds
3. **Fast response** - Meeting within 48 hours
4. **Performance guarantee** - Written commitments
5. **Test batch** - Low-risk restart

---

**🚨 SEND MEETING REQUEST TODAY**

---

## 📊 DETAILED VOLUME ANALYSIS (Aug 17 - Sep 30, 2025)

### Pivot Table Summary

**Total Volume**: 3,866 shipments

**Service Level Breakdown**:
- Ground: 3,520 (91.0%)
- Expedited: 315 (8.1%)
- Direct Call (Priority): 31 (0.8%)

### Ground Service Performance (3,520 shipments)

| Carrier/Service | Shipments | % of Ground | Avg Transit Days | Risk Level |
|-----------------|-----------|-------------|------------------|------------|
| ACL_Direct_Regional\ParcelDelivery | 1,233 | 35.0% | 2.87 days | ✅ Low |
| DHL SmartMail Parcel Ground | 762 | 21.7% | 3.95 days | 🔍 Moderate |
| DHL SmartMail Parcel Plus Ground | 830 | 23.6% | 3.94 days | 🔍 Moderate |
| ACI_Parcel_Select | 271 | 7.7% | 4.15 days | ⚠️ High |
| ACI_PS_Lightweight | 331 | 9.4% | 4.35 days | ⚠️ High |
| AMZL_Ground_ParcelDelivery | 84 | 2.4% | 0.26 days | ✅ Low |
| USPS_GA_Under1Lb | 9 | 0.3% | 1.78 days | ✅ Low |
| **Grand Total** | **3,520** | **100%** | **3.53 days** | - |

### Transit Day Distribution

| Days | Shipments | % | Cumulative % | Marketplace Impact |
|------|-----------|---|--------------|-------------------|
| 0 | 293 | 5.77% | 5.77% | ✅ Excellent |
| 1 | 582 | 10.28% | 16.05% | ✅ Excellent |
| 2 | 422 | 11.99% | 28.04% | ✅ Excellent |
| 3 | 612 | 17.39% | 45.43% | ✅ Good |
| 4 | **1,004** | **28.52%** | **73.95%** | 🔍 Acceptable (no buffer) |
| 5 | 506 | 14.38% | 88.33% | ⚠️ Risk zone |
| 6 | 206 | 5.85% | 94.18% | ⚠️ Risk zone |
| 7 | 119 | 3.38% | 97.56% | ⚠️ High risk |
| 8+ | 86 | 2.44% | 100.00% | 🚨 Late |

**Critical Insights**:
- **73.95% deliver within 4 days** (good for Amazon expectations)
- **26.05% take 5+ days** (912 shipments creating marketplace anxiety)
- **Day 4 "bulge"**: 1,004 shipments (28.52%) = zero buffer for delays

---

## 🎯 DATA-DRIVEN RECOVERY STRATEGY

### Phase 1: Immediate Carrier Optimization

**Problem Segment**: ACI Services (602 shipments, 15.6% of volume)
- ACI_Parcel_Select: 271 ships, 4.15 days avg
- ACI_PS_Lightweight: 331 ships, 4.35 days avg
- **These are your highest-risk packages**

**Solution**: Shift all ACI services from Ground → Expedited
- Expected improvement: 4.15-4.35 days → 2.0 days
- Cost impact: Moderate (15.6% of volume)
- Marketplace impact: Eliminates highest-risk segment

**Keep on Ground** (proven performers):
- ACL_Direct_Regional: 2.87 days avg (35% of volume) ✅
- AMZL: 0.26 days avg (Amazon's network) ✅
- USPS_GA_Under1Lb: 1.78 days avg (lightweight) ✅

**Evaluate for Zones 5-8 Upgrade**:
- DHL SmartMail (45% of volume, 3.94 days avg)
- If budget allows, upgrade cross-country lanes to Expedited

### Phase 2: Performance Targets (Data-Driven)

**Achievable Targets Based on Pivot Analysis**:
- **85%+ deliver within 4 days** (currently 73.95%, need +11 points)
- **95%+ deliver within 5 days** (currently 88.33%, need +7 points)
- **<3% late shipment rate** (marketplace definition)

**How We'll Get There**:
1. Shift 602 ACI shipments to Expedited (+10 points to 4-day delivery)
2. Upgrade Zone 7-8 DHL shipments to Expedited (+5 points to 5-day delivery)
3. Earlier pickup times to reduce induction lag (+2-3 points across all metrics)

---

## 📧 MEETING PRESENTATION (WITH PIVOT DATA)

**Opening**: "I've analyzed your 3,866 shipments from August 17 to September 30..."

**The Data Story**:
1. **91% Ground volume** - Heavy concentration creates marketplace risk
2. **28.52% deliver on Day 4** - Zero buffer for marketplace metrics
3. **26% take 5+ days** - These 912 shipments are triggering your concerns
4. **ACI services average 4.15-4.35 days** - Highest-risk segment (602 ships)

**The Solution**:
"We're going to shift your ACI services (15.6% of volume) to Expedited immediately. This will move your 4-day delivery rate from 74% to 85%+, and your 5-day rate from 88% to 95%+."

**Expected Marketplace Impact**:
- Late shipment rate: <2% (well below Amazon 4% threshold)
- On-time delivery: 95%+ (safely above 90% threshold)
- Buffer zone: Comfortable margin for marketplace compliance

---

**Files Updated**: Customer_Relationship_Documentation_v2.md
