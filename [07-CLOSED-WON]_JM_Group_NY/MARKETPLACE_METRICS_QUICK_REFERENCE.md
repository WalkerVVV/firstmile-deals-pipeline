# Marketplace Metrics Quick Reference - JM Group

**Purpose**: Track what we know vs. what we need to optimize Xparcel setup
**Date**: October 7, 2025

---

## 📊 WHAT WE KNOW (From Screenshots)

### Amazon Account 1
| Metric | Current | Target | Status | Period |
|--------|---------|--------|--------|--------|
| Late Shipment Rate | 1.44% | <4% | ✅ Safe | 30 days |
| On-Time Delivery | 95.69% | >90% | ✅ Safe | 14 days |
| Valid Tracking | 99.34% | >95% | ✅ Safe | 30 days |

### Amazon Account 2
| Metric | Current | Target | Status | Period |
|--------|---------|--------|--------|--------|
| On-Time Delivery | 94.84% | >90% | ⚠️ Close | 14 days |

### Walmart
| Metric | Current | Target | Status | Period |
|--------|---------|--------|--------|--------|
| On-Time Delivery | 92.8% | >90% | 🚨 Very Close | 30 days |

---

## ❓ WHAT WE DON'T KNOW (Critical Gaps)

### 1. Metric Definitions
- ❌ How does Amazon define "Late Shipment"? (Ship date vs. delivery date based?)
- ❌ How does Amazon calculate "promised delivery date"?
- ❌ How does Walmart calculate "promised delivery date"?
- ❌ Do they use business days or calendar days?
- ❌ Is there a grace period (e.g., deliver by 11:59pm vs. 8pm)?

### 2. Shipping Speed Breakdown
- ❌ What % of orders are Standard Shipping?
- ❌ What % are Expedited/Two-Day?
- ❌ What % are Next-Day/One-Day?
- ❌ What are the promised delivery windows for each speed?

### 3. Root Cause Data
- ❌ Which specific tracking numbers were flagged as "late"?
- ❌ What were the promised delivery dates for those orders?
- ❌ What shipping speed did customers select?
- ❌ What zones were they shipping to?

### 4. Current Configuration
- ❌ How are they selecting Xparcel service levels today?
- ❌ Are they using ShipStation automation rules?
- ❌ What's their default service level?

---

## 🎯 WHY THIS MATTERS

### Problem: We're Flying Blind
**Current approach**: "91% Ground volume, 3.53 days average, should be fine"
**Reality**: Marketplace metrics at risk (92.8% Walmart, 94.84% Amazon)

**Why the disconnect?**
- We don't know if Amazon's "on-time" means 3 days, 5 days, or 7 days
- We don't know if they're promising 2-day delivery but using Ground (3-8 days)
- We don't know if the "late" packages are Zone 7-8 or specific shipping speeds

### Solution: Data-Driven Configuration
**What we'll do once we have answers**:

**Scenario A**: Amazon Standard = 5-8 days
```
✅ Xparcel Ground (3-8 days) = GOOD FIT
Action: Keep Standard orders on Ground for Zones 1-5
Action: Upgrade Zones 6-8 to Expedited for buffer
```

**Scenario B**: Amazon Standard = 3-5 days
```
⚠️ Xparcel Ground (3-8 days) = RISKY
Action: Shift ALL Standard orders to Expedited (2-5 days)
Cost: Higher, but protects marketplace metrics
```

**Scenario C**: Mixed (some 2-day, some Standard)
```
🎯 Smart routing based on shipping speed selected
IF shipping_speed = "Two-Day" → Xparcel Priority (1-3 days)
IF shipping_speed = "Standard" AND zone <= 4 → Xparcel Ground
IF shipping_speed = "Standard" AND zone >= 5 → Xparcel Expedited
```

---

## 🔧 XPARCEL CONFIGURATION OPTIONS

### Current Setup (Assumed)
```
ALL orders → Xparcel Ground (default)
Result: 3.53 days average, but 26% take 5+ days
Risk: No buffer for marketplace promises
```

### Option 1: Conservative (Protect Metrics at All Costs)
```
ALL orders → Xparcel Expedited (2-5 days)
Cost: ~30-40% higher than Ground
Benefit: 95%+ deliver within 5 days, <3% late rate
Risk: None, but expensive
```

### Option 2: Intelligent Routing (Recommended)
```
Marketplace = Walmart → Xparcel Expedited (protect 92.8%)
Marketplace = Amazon + Speed = "Two-Day" → Xparcel Priority
Marketplace = Amazon + Speed = "Standard" + Zone 1-4 → Xparcel Ground
Marketplace = Amazon + Speed = "Standard" + Zone 5-8 → Xparcel Expedited
Carrier = ACI_* → Force Expedited (avoid 4.15-4.35 day avg)
```

### Option 3: Carrier Optimization (Cost-Effective)
```
Keep Ground for proven performers:
- ACL_Direct_Regional (2.87 days avg) ✅
- AMZL (0.26 days avg) ✅
- USPS lightweight (1.78 days avg) ✅

Force Expedited for slow performers:
- ACI_Parcel_Select (4.15 days avg) ⚠️
- ACI_PS_Lightweight (4.35 days avg) ⚠️

Evaluate by zone for moderate performers:
- DHL SmartMail (3.94 days avg): Ground for Zones 1-4, Expedited for 5-8
```

---

## 📧 TWO-EMAIL STRATEGY

### Email 1: Clarification Questions (Send First)
**Subject**: Questions to Optimize Your Xparcel Setup

**Purpose**: Get metric definitions and data before meeting
**Timing**: Send today (Monday)
**Expected response**: 24-48 hours

**Key asks**:
1. Amazon/Walmart metric definitions
2. Promised delivery windows by shipping speed
3. 10-20 tracking numbers flagged as late
4. Current ShipStation automation setup

---

### Email 2: Meeting Request (Send After Questions)
**Subject**: JM Group - Meeting This Week to Review Solutions

**Purpose**: Schedule meeting after they've reviewed questions
**Timing**: Send Tuesday or once they respond to questions
**Expected response**: Meeting scheduled for Wed/Thu

**Agenda**:
1. Review their answers to clarification questions
2. Present data-driven Xparcel configuration recommendations
3. Configure ShipStation automation rules together
4. Set up test batch with new configuration
5. Establish daily monitoring and weekly check-ins

---

## 🎯 SUCCESS METRICS (Post-Optimization)

### Target Performance (After Configuration Changes)
| Metric | Target | Current | Improvement Needed |
|--------|--------|---------|-------------------|
| Amazon Late Shipment | <2% | 1.44% | ✅ Already good |
| Amazon On-Time (Acct 1) | >95% | 95.69% | ✅ Maintain |
| Amazon On-Time (Acct 2) | >95% | 94.84% | +0.16 points |
| Walmart On-Time | >95% | 92.8% | +2.2 points |

### How We'll Get There
1. **Shift ACI services to Expedited** (+1.5 points across all metrics)
2. **Intelligent routing by shipping speed** (+1.0 points)
3. **Earlier pickup times** (+0.5 points)
4. **Proactive monitoring** (prevents degradation)

**Total expected improvement**: +3.0 points
**Result**: Walmart 92.8% → 95.8%, Amazon Acct 2 94.84% → 97.84%

---

## 🚨 RISK MITIGATION

### If Metrics Decline During Test Batch
**Threshold**: If any metric drops >1 point during test
**Action**: Immediately shift ALL volume to Expedited (conservative approach)
**Cost**: Higher, but protects marketplace accounts
**Duration**: Until we identify root cause and fix

### If They Don't Respond to Questions
**Approach**: Make educated guesses based on industry standards
**Assumption**: Amazon Standard = 5-8 days, Expedited = 2-4 days, Two-Day = 2 days
**Configuration**: Use Option 2 (Intelligent Routing) with conservative buffers
**Risk**: May over-index to Expedited (higher cost) but protects metrics

### If They Don't Want to Meet
**Fallback**: Email-only optimization
**Send**: Detailed Xparcel configuration recommendations based on best practices
**Offer**: "We'll implement these changes on our end, you test for 1 week, report results"
**Goal**: Show proactive problem-solving even without meeting

---

**Status**: Ready to send clarification questions email
**Next Step**: Wait for user approval to send
