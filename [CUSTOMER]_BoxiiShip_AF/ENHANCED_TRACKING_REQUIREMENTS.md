# Enhanced Tracking Visibility - Make Wellness Shipments

**Date**: November 12, 2025
**Customer**: BoxiiShip AF / Make Wellness
**Priority**: HIGH (Required before Week 1 shipments)

---

## Business Requirement

**From Meeting**: Enable enhanced tracking visibility for Nate's shipments to rebuild trust after April 2025 performance issues.

**Purpose**:
- Real-time shipment visibility for all Make Wellness packages
- Proactive SLA monitoring and alerts
- Transparency to prevent issues before they become problems
- Build confidence during phased ramp-up (10k → 30k packages/month)

---

## Technical Requirements

### 1. Real-Time Shipment Visibility

**Scope**: All Make Wellness shipments via BoxiiShip AF

**Features Required**:
- Live tracking status for every package
- Estimated delivery dates vs. SLA window
- Current location and last scan event
- Exception alerts (delays, routing issues, delivery failures)

**Access**: Dashboard or API for Nate to view all Make Wellness shipments

---

### 2. SLA Monitoring Dashboard

**Metrics to Display**:
- Total shipments (daily, weekly, monthly)
- On-time delivery percentage (target: ≥95%)
- Average transit time by service level
- SLA compliance by day
- Exception count and types

**Alerting**:
- Real-time alerts for packages approaching SLA breach
- Daily summary report emailed to Nate and Brett
- Weekly performance summary for Tuesday check-ins

**Access**: Web dashboard with login credentials for Nate

---

### 3. Automated Alerts

**Alert Triggers**:
- Package delayed beyond expected transit time
- SLA window approaching (e.g., Day 2 of 3-day service)
- Delivery exception (bad address, refused, damaged)
- Routing issue detected (ACI-WS or other problematic facility)

**Notification Methods**:
- Email to Nate (primary)
- SMS for critical alerts (optional)
- Dashboard notifications

**Alert Recipients**:
- Nate (BoxiiShip AF)
- Brett Walker (FirstMile)
- Jeff (FirstMile - optional)

---

### 4. Performance Reports

**Daily Report** (Email - 8 AM CT):
- Yesterday's shipment count
- SLA compliance percentage
- Any exceptions or delays
- Forecast for today

**Weekly Report** (Email - Monday 8 AM CT):
- Last 7 days summary
- SLA compliance trend
- Top 5 destination states performance
- Exceptions and resolutions

**Monthly Report** (First of month):
- Full month performance review
- Volume growth (10k → 20k → 30k)
- SLA compliance trends
- Cost savings vs. UPS

---

## Implementation Plan

### Phase 1: Immediate Setup (Before Week 1 Shipments)

**Due: November 13, 2025**

1. **Identify Make Wellness Shipments**
   - Tracking number prefix or range
   - Origin facility: BoxiiShip American Fork
   - Consignee name patterns
   - Create filter in system to auto-tag Make Wellness packages

2. **Create SLA Monitoring View**
   - Query: All shipments tagged "Make Wellness"
   - Display: Tracking #, Ship Date, Service Level, Transit Days, SLA Status
   - Sort: By SLA urgency (approaching breach first)

3. **Setup Basic Alerts**
   - Email alert when package exceeds expected transit time
   - Daily summary report at 8 AM CT
   - Nate and Brett as recipients

### Phase 2: Enhanced Dashboard (Week 2)

**Due: November 19, 2025**

1. **Build Web Dashboard**
   - Login credentials for Nate
   - Real-time shipment tracking table
   - SLA compliance charts
   - Performance metrics widgets

2. **Advanced Alerting**
   - Proactive alerts (Day 2 of 3-day service not yet in transit)
   - Exception categorization (delivery failure, routing issue, etc.)
   - SMS alerts for critical issues (optional)

3. **Weekly Reporting**
   - Automated Monday morning reports
   - Performance trends and insights
   - Volume growth tracking

### Phase 3: API Integration (Week 3-4)

**Due: December 3, 2025 (optional)**

1. **API Access for Nate**
   - RESTful API endpoint for shipment queries
   - JSON response with tracking data
   - Authentication via API key

2. **BoxiiShip System Integration** (if desired)
   - Direct feed of Make Wellness tracking into BoxiiShip's system
   - Reduce manual checking
   - Automated reporting

---

## Ownership & Contacts

### FirstMile Operations Team

**Primary Contact**: [Ops Manager Name/Email]
**Responsibility**:
- Implement enhanced tracking system
- Configure alerts and reports
- Create dashboard access for Nate
- Ongoing monitoring and maintenance

### FirstMile IT/Dev Team (if needed)

**Contact**: [Dev Team Email]
**Responsibility**:
- API integration (Phase 3)
- Dashboard development (Phase 2)
- Custom alert logic

### Brett Walker (Account Manager)

**Responsibility**:
- Coordinate implementation
- User acceptance testing with Nate
- Training and onboarding
- Ongoing support

---

## Success Criteria

**Week 1** (November 12-18):
- ✅ Basic shipment visibility operational
- ✅ Daily email alerts working
- ✅ Nate can track all Make Wellness packages

**Week 2** (November 19-25):
- ✅ Dashboard live with Nate's login
- ✅ SLA compliance charts visible
- ✅ Weekly reports automated

**Week 3-4** (November 26 - December 10):
- ✅ Proactive alerting functional
- ✅ API access (if requested)
- ✅ Zero tracking gaps or blind spots

**Ongoing**:
- ≥95% SLA compliance maintained
- <1 hour alert response time
- 100% shipment visibility (no missing tracking data)

---

## Risks & Mitigation

**Risk 1**: Tracking data gaps (packages not updating)
- **Mitigation**: Daily data quality checks, automated gap detection

**Risk 2**: Alert fatigue (too many notifications)
- **Mitigation**: Intelligent filtering, configurable thresholds

**Risk 3**: Dashboard downtime
- **Mitigation**: Email fallback alerts, uptime monitoring

**Risk 4**: Integration delays
- **Mitigation**: Phased rollout (manual → automated), prioritize Phase 1

---

## Next Actions

**Immediate** (November 12-13):
1. [ ] Contact FirstMile ops team with this requirements doc
2. [ ] Identify Make Wellness shipment filter criteria
3. [ ] Setup basic email alerts (8 AM CT daily summary)
4. [ ] Test with first Make Wellness shipments

**This Week** (November 13-15):
1. [ ] Create Nate's dashboard login
2. [ ] Demo tracking visibility to Nate
3. [ ] Adjust alert thresholds based on feedback

**Week 2** (November 19-25):
1. [ ] Review Week 1 data in Tuesday check-in
2. [ ] Launch weekly performance reports
3. [ ] Enhance dashboard with SLA charts

---

## Reference

**Action Item Source**: BoxiiShip AF Meeting - November 12, 2025
**Meeting Notes**: `MEETING_NOTES_NOV12_2025_MAKE_WELLNESS_RELAUNCH.md`
**Recording**: https://fathom.video/share/yuh743yJwHULoZgWGzBbnzgeixXu6Lyq

**Business Context**:
- Make Wellness left FirstMile in July 2025 after April performance collapse
- Tracking visibility is critical to rebuilding trust
- Weekly check-ins will review SLA compliance data
- $7.1M annual revenue recovery opportunity depends on excellent execution

**Success Depends On**: Proactive visibility and communication to prevent any performance issues from escalating.

