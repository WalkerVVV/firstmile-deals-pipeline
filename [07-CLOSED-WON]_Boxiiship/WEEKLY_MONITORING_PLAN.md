# BoxiiShip Weekly Service Monitoring Plan
**Start Date:** Week of November 4, 2025
**Duration:** Through December 31, 2025 (9 weeks)
**Owner:** Stephen Lineberry
**Stakeholders:** Brett Walker, Brock Hansen, BoxiiShip (Reed)

---

## Monitoring Objectives

**Primary Goal:** Rebuild BoxiiShip confidence through transparent, data-driven performance reporting

**Success Criteria:**
- Zero critical delays (>3 days to first scan)
- Same-day scan rate >95%
- Zero customer complaints
- Stable transit performance (match or beat baseline)

---

## Weekly Metrics to Track

### 1. First Scan Performance (CRITICAL METRIC)
**Why This Matters:** Oct crisis showed 5.77-6.95 day delays (should be <1-2 days)

**Track:**
- Average days to first physical scan (by service type)
- Same-day scan rate %
- Packages >3 days to first scan (count + tracking numbers)

**Thresholds:**
- 🟢 Green: <1.5 days average, >95% same-day
- 🟡 Yellow: 1.5-2.5 days average, 90-95% same-day
- 🔴 Red: >2.5 days average, <90% same-day

### 2. Transit Performance
**Track:**
- Average transit days (Expedited vs. Ground)
- % meeting SLA (3-day Expedited, 8-day Ground)
- Comparison to baseline (1.76 days Expedited, 1.69 days Ground)

**Thresholds:**
- 🟢 Green: Within 10% of baseline, >95% SLA
- 🟡 Yellow: 10-25% variance, 90-95% SLA
- 🔴 Red: >25% variance, <90% SLA

### 3. Exception Tracking
**Track:**
- Customer complaint volume
- Packages marked lost/damaged
- Tracking system errors
- Delivery attempts failed

**Thresholds:**
- 🟢 Green: <5 exceptions/week
- 🟡 Yellow: 5-10 exceptions/week
- 🔴 Red: >10 exceptions/week

### 4. Volume Analysis
**Track:**
- Total packages/week
- Service mix (Expedited/Ground/Priority)
- Week-over-week growth trends
- Peak volume days

**Purpose:** Ensure network capacity handling growth

---

## Reporting Format

### Internal Report (Weekly - Mondays)
**Recipients:** Brett, Brock, Stephen
**Format:** Email summary + Excel dashboard

**Template:**

```
BoxiiShip Weekly Performance Report - Week of [Date]

EXECUTIVE SUMMARY:
- Overall Status: 🟢/🟡/🔴
- Critical Issues: [None OR description]
- Action Items: [Any escalations needed]

FIRST SCAN PERFORMANCE:
- Avg Days to First Scan: [X] days (Target: <1.5)
- Same-Day Scan Rate: [X]% (Target: >95%)
- Packages >3 Days: [X] (Target: 0)

TRANSIT PERFORMANCE:
- Avg Transit Days: [X] (Baseline: 1.7)
- SLA Compliance: [X]% (Target: >95%)
- Service Mix: [X]% Expedited, [X]% Ground

EXCEPTIONS:
- Customer Complaints: [X] (Target: <5)
- Lost/Damaged: [X]
- Tracking Errors: [X]

VOLUME:
- Total Packages: [X]
- WoW Growth: [+/-X]%
- Peak Day: [Date] ([X] packages)

ESCALATIONS:
[Any issues requiring Brett/Brock attention]
```

### Customer Report (Monthly - 1st of Month)
**Recipients:** Reed (BoxiiShip CEO)
**Format:** PDF executive summary

**Template:**

```
BoxiiShip Performance Summary - [Month]

Network Stability Metrics:
- First Scan Performance: [X] days avg (98% same-day)
- Transit Performance: [X] days avg (37% faster than DHL)
- SLA Compliance: [X]%
- Zero critical delays (>3 days)

Volume Handled:
- Total Packages: [X]
- Service Distribution: [breakdown]
- Peak Season Readiness: [status]

Your Business Impact:
- Cost Savings vs. DHL: $[X]/month (XX% reduction)
- Faster Delivery: [X]% of packages delivered [X] days faster
- Customer Complaints: [X] (vs. [X] prior month)

Network Confidence:
- Daily leadership monitoring: Active
- Partner diversification: [X] providers
- Tracking system reliability: >99%
```

---

## Escalation Protocols

### Immediate Escalation (Same Day)
**Triggers:**
- Any day with >10 packages showing >3 days to first scan
- Customer complaint about specific package delay
- Tracking system failure affecting >5% of volume
- Same-day scan rate drops below 85%

**Action:**
- Stephen alerts Brett + Brock immediately
- Investigate root cause with ACI (Lindsay/Chris)
- Provide status update to BoxiiShip within 4 hours
- Document incident and resolution

### Weekly Escalation (Monday Report)
**Triggers:**
- 🔴 Red status on any metric for 2+ consecutive weeks
- Trend showing degradation (week-over-week decline)
- Customer feedback indicating service concerns

**Action:**
- Schedule call with ACI leadership
- Review network stability measures
- Adjust monitoring thresholds if needed
- Prepare customer communication if required

### Monthly Review (1st of Month)
**Participants:** Brett, Brock, Stephen, Reed (BoxiiShip)
**Agenda:**
- Review monthly performance summary
- Discuss any concerns or trends
- Preview upcoming month (peak season prep)
- Adjust service levels if needed

---

## Data Sources

**Primary:**
- BoxiiShip shipment data (Stephen's access)
- ACI performance reports (Lindsay)
- Customer complaint tracking (Brock/BoxiiShip)

**Tools:**
- Excel dashboards (Stephen's existing tools)
- HubSpot deal activity (customer complaints)
- ACI portal (if access available)

---

## Success Milestones

**Week 1-2 (Nov 4-15):**
- Establish baseline metrics post-crisis
- Validate data sources and reporting format
- Share first internal reports with Brett/Brock

**Week 3-4 (Nov 18-29):**
- Send first monthly customer report to Reid
- Confirm metrics show stable performance
- Adjust monitoring if needed based on feedback

**Week 5-8 (Dec 2-27 - Peak Season):**
- Daily monitoring during peak volume days
- Proactive alerts if any degradation
- Weekly check-ins with BoxiiShip

**Week 9 (Dec 30-31):**
- End-of-year performance summary
- Transition to standard quarterly reporting
- Document lessons learned

---

## Budget & Resources

**Stephen's Time:**
- Weekly reporting: ~2 hours/week
- Monthly customer report: ~3 hours/month
- Escalation investigation: As needed
- Total: ~12 hours/month

**Tools Needed:**
- Excel/Python for data analysis (existing)
- Access to BoxiiShip shipment data (existing)
- ACI performance data (coordinate with Lindsay)

**No Additional Budget Required:** Using existing tools and data sources

---

## Communication Plan

**Internal (Weekly):**
- Monday AM: Stephen sends report to Brett/Brock
- Any day: Immediate escalation if triggers hit
- Friday: Week-ahead preview if peak volume expected

**Customer (Monthly):**
- 1st of month: Performance summary to Reid
- As needed: Proactive alerts if issues detected
- Quarterly: Business review meeting

---

## Exit Criteria

**When to End Weekly Monitoring:**
- 8+ consecutive weeks of 🟢 Green status across all metrics
- Zero customer complaints for 60 days
- Make Wellness win-back successfully completed
- BoxiiShip relationship fully restored

**Transition to:** Quarterly business review cadence (standard customer reporting)

---

**Document Owner:** Brett Walker
**Last Updated:** October 30, 2025
**Next Review:** After first weekly report (Nov 4)
**Status:** Ready to Activate
