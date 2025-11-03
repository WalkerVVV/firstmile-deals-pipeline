# BoxiiShip October 2025 Service Crisis - Post-Mortem

**Meeting Date:** October 28, 2025
**Recording:** [Fathom Video](https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth) (34 mins)
**Attendees:** Brett Walker (FirstMile), Brock Hansen, Stephen Lineberry, Christopher Von Melville (ACI Logistix), Zach Green
**Account:** BoxiiShip (Texas + Utah locations) - Referral Partner
**Status:** 🔴 Critical - Customer Escalation Required

---

## Executive Summary

**Crisis:** 287+ DHL packages lost in transit October 6-7, followed by 300+ ACI Direct packages delayed October 7-20 due to partner last-mile provider failure. Network stabilized October 20th, but customer relationship at risk.

**Root Cause:** ACI's primary partner last-mile provider (DoorDash) wound down service zip codes over 2.5 weeks despite contractual agreement to deliver all in-flight packages. Packages were held in facilities for days without notification, causing **5.77-6.95 day delays to first scan** (should be <1-2 days). Packages retrieved and upgraded to USPS Ground Advantage at ACI expense.

**Customer Impact:**
- **35 documented complaints** (60% DHL, 14% ACI, 23% USPS)
  - **29 packages: No First Scan** (83% of complaints - critical issue)
  - 2 packages: Still in transit
  - 3 packages: Delivered
  - 1 package: System error (reverted status)
- **~320 packages** still showing "in transit" as of Oct 17th (many likely delivered but tracking not linked)
- **Operational disruption** from unannounced ACI switchover on Oct 6th
- **Lost confidence** in FirstMile/ACI reliability
- **$500K/month Make Wellness** win-back opportunity now at risk

**Performance Impact (30-Day Analysis):**
- ACI Direct first scan delays: **5.77 days (Expedited), 6.95 days (Ground)** vs. DHL/USPS at 1.5-1.8 days
- 13,694 total packages processed during crisis period
- Peak crisis days: Oct 6-8 (1,169-1,667 packages/day)

**Immediate Action Required:** Schedule call with Reed (BoxiiShip CEO) + Chris (ACI) for Oct 29 (12:30 PT+) or Oct 30 to provide transparent explanation and rebuild trust.

---

## Crisis Timeline

### Pre-Crisis (Sept 29 - Oct 5)
- **Sept 29:** ACI begins partner last-mile provider realignment due to poor performance
- **Oct 3-6:** FirstMile begins transitioning BoxiiShip to ACI routing (planned)
- **Oct 6 (weekend):** BoxiiShip was 95% DHL + USPS, planned ACI switchover pending confirmation

### Crisis Period (Oct 6 - Oct 20)

**October 6-7:**
- 287 DHL packages picked up, no scans recorded
- ACI labels activated without final confirmation to Brett/BoxiiShip
- Reed (BoxiiShip CEO) calls Brett on Oct 7: "ACI labels coming out, what's going on?"
- Operational chaos - customer (Wrinkles Schminkels) upset, BoxiiShip caught off-guard

**October 7-17:**
- ACI Direct packages flowing but experiencing severe delays
- DoorDash (partner last-mile provider) holding packages in facilities without delivery or notification
- Oct 8: 52 packages in transit (unresolved)
- Oct 13: 50 packages in transit (unresolved)
- Oct 17: 305 ACI Direct packages still showing in transit

**October 18-20:**
- ACI discovers DoorDash had put packages in Gaylords in facility corners, not delivering despite agreement
- ACI retrieves packages, upgrades to USPS Ground Advantage (at ACI expense)
- Network stabilization begins

**October 20+:**
- Network fully stabilized
- Backlog packages delivering (many with tracking not linking due to over-label issue)
- Oct 16: BoxiiShip reports "a lot" of packages returned (13 tracking numbers provided)
- Oct 28: Customer demanding immediate update, 35+ complaint tracking numbers submitted

---

## Root Cause Analysis

### Primary Cause: Partner Last-Mile Provider Contract Breach
**What Happened:**
- ACI's primary partner (DoorDash) agreed to deliver all in-flight packages through agreed dates during zip code wind-down
- Instead, DoorDash held packages in facilities (Gaylords in corners) for multiple days without notifying ACI
- This occurred over 2.5 weeks across multiple zip code tranches (not all at once)

**Why It Happened:**
- DoorDash winding down contract with ACI while launching competing parcel delivery network
- Suspected sabotage: Create service disruptions to poach clients ("We're already moving your volume anyway...")
- Operational disconnect between agreement and execution

**ACI Response:**
- Facility sweeps to retrieve held packages
- Upgraded all retrieved packages to USPS Ground Advantage (faster service, ACI expense)
- Reallocated volume to multiple new partner last-mile providers
- Network fully stabilized by October 20th

### Contributing Factors

**1. Communication Breakdown (FirstMile ↔ BoxiiShip)**
- ACI routing turned on October 6th before final confirmation to Brett
- BoxiiShip not prepared for operational change (sorting, labeling)
- Reed learned about switch when ACI labels started printing
- "Threw a huge wrench in their plans"

**2. Operational Transition (DHL → ACI DFW)**
- Previous: DHL packages delivered directly to DHL induction terminal
- New: All packages to ACI DFW for receipt, sort, scan
- Customer perception: "We switched to new product + new facility = terrible results"
- Multiple simultaneous changes amplified impact

**3. Tracking Link Issues**
- Over-labeled packages (original ACI → USPS GA) not linking tracking properly
- Patch deployed Wed/Thu week of Oct 23rd to fix
- Many packages delivered but showing as "in transit" in systems

---

## Customer Impact & Metrics

### BoxiiShip Account Profile
- **Locations:** 3 total (Texas largest, 2 in Utah)
- **Historical Volume:** $500K/month (lost Make Wellness July 13th due to prior service issues)
- **Current Status:** Top 20 revenue account, significant growth potential
- **Relationship:** Referral partner agreement (financially motivated to work with FirstMile)

### Service Disruption Metrics

**Known Consignee Complaints (Stephen Lineberry - Oct 28):**
- **35 total complaints** submitted with tracking numbers
  - 29 packages: No First Scan (🔴 critical - 83%)
  - 2 packages: Still In Transit (🟡 monitoring)
  - 3 packages: Delivered (✅ resolved)
  - 1 package: Reverted to "Label Created" from "In Transit" (🟠 system error)

**Complaint Breakdown by Routing Method:**
- **DHL SmartMail Ground:** 21 complaints (60%)
- **USPS GA Under 1lb:** 8 complaints (23%)
- **ACI Direct Regional:** 5 complaints (14%)
- **DHL SmartMail Expedited Max:** 1 complaint (3%)

**Historical Volume Impact:**
- **287 packages:** DHL, no scans, Oct 6th pickup (some returned to sender)
- **305+ packages:** ACI Direct, showing in transit Oct 17th
- **Total volume (30 days):** 13,694 packages across all routing methods
- **Unknown:** Total end-customer complaints received by BoxiiShip from their clients

### Performance Metrics Analysis (Stephen Lineberry - 30 Day Window)

**Label Request to First Scan Times (🚨 CRITICAL METRIC):**

*Expedited Service:*
- **ACI Direct:** 5.77 days (**🔴 RED FLAG** - should be <1 day)
- **DHL SmartMail:** 1.58 days (acceptable)
- **USPS GA Under 1lb:** 1.81 days (acceptable)
- **Overall Average:** 2.81 days

*Ground Service:*
- **ACI Direct:** 6.95 days (**🔴 RED FLAG** - should be <2 days)
- **DHL SmartMail:** 1.68 days (acceptable)
- **USPS GA Under 1lb:** 1.78 days (acceptable)
- **Overall Average:** 3.48 days

**Analysis:** ACI Direct's "Days to First Physical Scan" metric is 3-4x worse than DHL/USPS during crisis period. This confirms Christopher Von Melville's explanation - packages were held in DoorDash facilities without scanning.

**Transit Performance (When Working Properly):**

*Expedited Service:*
- **ACI Direct:** 1.76 days avg, $6.76 cost (14% of volume, 50% of expedited)
- **DHL SmartMail:** 2.81 days avg, $8.91 cost (25% of volume, slower + 32% more expensive)

*Ground Service:*
- **ACI Direct:** 1.69 days avg, $5.77 cost (19% of volume, 40% of ground)
- **DHL SmartMail:** 3.66 days avg, $8.87 cost (22% of volume, 2.2x slower + 54% more expensive)

**Key Insight:** ACI Direct SHOULD be the superior service (faster + cheaper), but October crisis reversed this. Network stabilization critical to restore value proposition.

**Volume Distribution (30 Days):**
- **Total Packages:** 13,694
- **Daily Average:** 456 packages
- **Peak Day:** Oct 8 (1,667 packages)
- **Service Mix:** 50% Expedited, 47% Ground, 3% Priority

**Peak Volume Days During Crisis:**
- Sept 29: 1,204 packages (crisis begins at ACI)
- Oct 6-8: 1,169-1,667 packages/day (BoxiiShip transition period)
- Oct 13: 1,096 packages (ongoing issues)
- Oct 17: 1,246 packages (worst day for in-transit packages)

### Financial Risk
- **Current Revenue:** Top 20 account (Texas location primary)
- **Lost Revenue:** Make Wellness ($500K/month) July 2025 due to prior Compton facility delays
- **Win-Back Opportunity:** Make Wellness considering return but paused due to current crisis
- **Referral Revenue:** At risk if BoxiiShip loses confidence

### Relationship Status
- **Trust Level:** 🔴 Severely damaged
- **Escalation:** CEO (Reed) demanding immediate updates
- **Decision Risk:** "Will you just remove ACI?" conversation possible
- **Opportunity:** Referral agreement = vested interest in resolution

---

## Action Items

### Immediate (Next 24-48 Hours)

**1. Schedule Customer Call** 🚨 URGENT
**Owner:** Brett Walker
**Deadline:** Oct 29 12:30 PT or Oct 30
**Attendees Required:**
- Brett Walker (FirstMile - lead)
- Brock Hansen (FirstMile)
- Christopher Von Melville (ACI - technical explanation)
- Lindsay (ACI - tracking/logistics detail) - CRITICAL
- Optional: Stephen Lineberry (FirstMile)

**Pre-Call Actions:**
- Brett: Call Reed to understand full scope of customer complaints
- Brett: Get specific count (not just 35 tracking numbers - what's total impact?)
- Team: Prepare transparent communication talking points (see below)
- DO NOT send detailed tracking report - risk opening Pandora's box

**2. Gather Complete Tracking Intelligence**
**Owner:** Lindsay (ACI) + Brock Hansen
**Deadline:** Before customer call
**Priority Focus:** 29 packages with "No First Scan" status (83% of complaints)
**Scope:**
- **287 DHL packages (Oct 6)** - current status (delivered/returned/lost?)
- **29 No First Scan packages** - where are they? (21 DHL Ground, 8 USPS GA)
- **305+ ACI packages (Oct 17)** - how many actually delivered vs. tracking not linked?
- **Over-label tracking link patch** - did it resolve all issues or still broken?
- **2 packages still in transit** - ETA and carrier location
- **1 package reverted to "Label Created"** - system error or actual issue?
- Any packages still genuinely undelivered vs. system artifacts?

**Key Question for Lindsay:** Why are 29 packages showing zero scans? Are they:
- Still in ACI/partner facilities unscanned?
- Delivered but never entered tracking system?
- Lost in DoorDash handoff chaos?
- System integration failures?

### Communication Strategy

**Chris Von Melville's Recommended Approach:** ✅ APPROVED
> "Transparent while maintaining positive spin"

**Key Talking Points:**

**1. Acknowledge Reality**
- "We experienced a service disruption October 6-20 that impacted your packages"
- "This was unacceptable and we take full responsibility"
- Specific numbers: 287 DHL packages, 305+ ACI packages delayed

**2. Explain Root Cause (Transparent)**
- "We made a strategic rebalancing of our partner last-mile provider network"
- "Why: Previous provider showed poor performance, misdeliveries, needed to ensure stable peak season"
- "Unfortunately: Provider agreed to deliver in-flight packages but failed to do so"
- "They held packages in facilities for days without notification - breach of agreement"

**3. Show Resolution Actions**
- "We immediately retrieved all held packages"
- "Upgraded all affected packages to USPS Ground Advantage (faster service, our expense)"
- "Completed facility sweeps to ensure no packages left behind"
- "Network fully stabilized October 20th"

**4. Address Operational Confusion**
- "The October 6th switch happened before we completed final communication with you"
- "We recognize this created operational challenges for your team"
- "Multiple changes happened simultaneously which amplified the impact"

**5. Future State Commitment**
- "Network is now stable with stronger partner providers"
- "Tracking systems have been patched to prevent linking issues"
- "We have high confidence in stable, consistent peak season performance"
- "Daily leadership monitoring in place through peak"
- "Scott Riddle (ACI leadership) directly engaged"

**6. Reinforce Value Proposition** ✅ NEW
- "When operating properly, ACI Direct delivers **faster** transit times than DHL:"
  - ACI Expedited: 1.76 days vs. DHL: 2.81 days (37% faster)
  - ACI Ground: 1.69 days vs. DHL: 3.66 days (54% faster)
- "ACI Direct is also more **cost-effective**:"
  - Expedited: $6.76 vs. DHL: $8.91 (32% savings)
  - Ground: $5.77 vs. DHL: $8.87 (54% savings)
- "The October crisis was an anomaly - 30-day data shows our network delivers when partners perform"
- "This is why we moved to ACI: superior speed and economics for your business"

**What NOT to Say:**
- ❌ Don't blame DoorDash by name (keep "partner provider" generic)
- ❌ Don't promise it was sabotage (speculation, even if suspected)
- ❌ Don't overshare technical details unless asked
- ❌ Don't minimize BoxiiShip's experience ("it wasn't that bad")

**Positioning:**
- Frame as: "Short-term pain for long-term network stability"
- Emphasize: "Peak season is our priority - this is why we acted now"
- Leverage: "You have a referral agreement - we're invested in your success"

### Follow-Up Actions

**3. Win-Back Make Wellness**
**Owner:** Brett Walker
**Timing:** After BoxiiShip relationship stabilized (30 days)
**Value:** $500K/month revenue
**Approach:** "Network issues resolved, here's our new stability metrics"

**4. Establish Service Level Monitoring**
**Owner:** Stephen Lineberry
**Frequency:** Weekly through Dec 31
**Metrics:**
- Days to First Physical Scan
- Critical delay rates
- Same-day scan rates
- Customer complaint volume

**5. Document Lessons Learned**
**Owner:** Brock Hansen + Brett Walker
**Deadline:** Nov 15
**Content:**
- Communication protocols for major routing changes
- Customer notification requirements before service switches
- ACI network stability verification checklist
- Escalation playbook for partner provider failures

---

## Technical Details

### Service Configuration Changes

**Before October 6:**
- **DHL:** 95% of volume
- **USPS:** Gap-fill only
- **Delivery:** Direct to DHL induction terminal
- **Status:** Stable, predictable, BoxiiShip comfortable

**After October 6:**
- **ACI Direct:** Primary (Xparcel routing)
- **ACI DFW Facility:** All receipt, sort, scan operations
- **Partner Last-Mile:** DoorDash (then multiple providers post-crisis)
- **USPS Ground Advantage:** Upgrade path for retrieved packages

### Affected Volume Breakdown
- **Zach's Analysis (pre-Oct 6):** 2,600-2,700 shipments eligible for ACI routing
- **Actual Impact:** 287 (DHL) + 305+ (ACI) = 590+ packages confirmed affected
- **Unknown Factor:** Total packages shipped Oct 6-20 vs. complaint rate

### Tracking Over-Label Process
**Problem:** ACI Direct label → USPS GA over-label → tracking not linking
**Patch:** Deployed Wed/Thu (Oct 23/24)
**Impact:** Many "in transit" packages actually delivered, systems not updated
**Resolution:** Patch should recapture historical data + fix future labels

---

## Network Stability Assessment

### Current State (Oct 20+)
✅ **Partner Providers:** Multiple new providers onboarded, volume diversified
✅ **Daily Monitoring:** ACI leadership standups active
✅ **Operations Team:** Marshall, Kyle actively managing stability
✅ **Funding/Support:** Adequate resources committed
✅ **Peak Readiness:** High confidence in network capacity

**Chris Von Melville Quote (Oct 28):**
> "I am an optimist, but I'm also very real. I'm a realist. I will tell you that I do feel like we are headed in the right direction now. We have the right support, the right funding, the right everything in place."

### Risk Mitigation
- **DoorDash Removed:** No longer partner last-mile provider
- **Volume Diversification:** Not dependent on single provider
- **Sweep Protocols:** Active facility monitoring for held packages
- **Escalation Paths:** Direct leadership engagement (Scott Riddle)

### Peak Season Outlook
**Confidence Level:** HIGH (per Chris Von Melville)
**Timeline:** Next 8-10 weeks (through Jan 2026)
**Commitment:** "Extremely stable and consistent peak"

---

## Competitive & Strategic Context

### DoorDash Competitive Threat
**Intel (Suspected):**
- DoorDash launching own parcel delivery network (multi-year effort)
- Recent progress: "Getting wind in their sails"
- Motive for sabotage: Create FirstMile/ACI service issues → poach clients
- Tactic: "We're already moving your volume, switch to us"

**Status:** Unconfirmed but plausible based on timing and behavior

### BoxiiShip Referral Partnership
**Structure:** Financial agreement for client referrals
**Implication:** BoxiiShip has vested interest in FirstMile success
**Risk:** Severe service issues could override financial motivation
**Opportunity:** Can position resolution as "protecting mutual revenue"

---

## Stephen Lineberry's Data Analysis (October 28)

### Complaint Tracking Detail

**Current Status of 35 Known Complaints:**
- ✅ **3 delivered** (8.6%)
- 🟡 **2 in transit** (5.7%)
- 🔴 **29 no first scan** (82.9%) - CRITICAL ISSUE
- 🟠 **1 reverted status** (2.9%) - system error

**Complaint Distribution by Service:**
| Routing Method | Count | % of Total |
|---|---|---|
| DHL SmartMail Ground | 21 | 60% |
| USPS GA Under 1lb | 8 | 23% |
| ACI Direct Regional | 5 | 14% |
| DHL SmartMail Expedited Max | 1 | 3% |

**Key Insight:** Most complaints are DHL (62%), not ACI (14%), likely because majority of volume was still DHL before Oct 6 transition. However, ACI's first scan delays are the root cause of visibility issues.

### First Scan Performance Crisis

**"Days to First Physical Scan" Comparison:**

| Service Level | ACI Direct | DHL SmartMail | USPS | ACI vs. Others |
|---|---|---|---|---|
| Expedited | 🔴 5.77 days | ✅ 1.58 days | ✅ 1.81 days | 3.6x worse |
| Ground | 🔴 6.95 days | ✅ 1.68 days | ✅ 1.78 days | 4.0x worse |

**Impact:** Packages taking nearly a **week** to receive first scan during crisis period. This confirms Christopher Von Melville's explanation - packages sitting in DoorDash facilities unscanned.

### Transit Performance Baseline

**Pre-Crisis/Post-Crisis Performance (When Network Healthy):**

| Service | Method | Avg Transit | Avg Cost | Volume % |
|---|---|---|---|---|
| Expedited | ACI Direct | 1.76 days | $6.76 | 14% |
| Expedited | DHL SmartMail | 2.81 days | $8.91 | 25% |
| Ground | ACI Direct | 1.69 days | $5.77 | 19% |
| Ground | DHL SmartMail | 3.66 days | $8.87 | 22% |

**Value Proposition:** ACI Direct is 37-54% faster and 32-54% cheaper than DHL SmartMail when operating normally.

### Volume Analysis

**30-Day Window (Sept 22 - Oct 24, 2025):**
- **Total Packages:** 13,694
- **Daily Average:** 456 packages
- **Peak Day:** Oct 8 (1,667 packages)
- **Service Mix:** 50% Expedited, 47% Ground, 3% Priority

**Crisis Period Volume (Oct 6-20):**
- Estimated 6,000-7,000 packages during disruption window
- 287 confirmed DHL issues (Oct 6)
- 305+ confirmed ACI issues (Oct 17)
- ~600 packages with documented problems = **8-10% failure rate**

### Tracking Status Update (Oct 28)

Stephen Lineberry provided real-time updates showing:
- 2 ACI shipments moved from "In Transit" to "Delivered" (improvement)
- 29 packages still showing "No First Scan" (unchanged - critical)
- 1 package reverted from "In Transit" to "Label Created" (system degradation)

**Interpretation:** Some packages are slowly resolving, but the "No First Scan" cohort (82.9% of complaints) remains unresolved and is the highest priority for Lindsay/ACI investigation.

---

## Related Documentation

### HubSpot Deal Records
- **BoxiiShip System Beauty (Magna, Utah)**
- **BoxiiShip American Fork (Utah)** - Make Wellness (lost July 13)
- **BoxiiShip Texas** - Primary revenue location

### Previous Incidents
- **July 13, 2025:** Make Wellness departure ($500K/month)
- **Cause:** Compton, CA facility delays (5-10 days)
- **Switch To:** UPS 2-Day (+$45K/month cost)
- **CEO Impact:** Direct escalation to Make Wellness CEO

### Follow-Up Materials Needed
- Tracking report (287 DHL packages) - DO NOT send yet
- Tracking report (305 ACI Oct 17) - DO NOT send yet
- Service level metrics (Oct 20+) - Prepare for customer call
- Peak season capacity plan - Share on call

---

## Meeting Recording Highlights

🎥 **Full Recording:** [Fathom Video - 34 mins](https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth)

**Key Timestamps:**
- **6:24 - 10:52:** [Christopher explains delivery partner realignment](https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth?timestamp=408.452) - Root cause, timeline, resolution details
- **19:08 - 21:19:** [Christopher's transparent communication strategy](https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth?timestamp=1115.2) - Recommended talking points for customer
- **29:38 - 30:20:** [Action item confirmation](https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth?timestamp=1785.9999) - Call scheduling, attendees needed

---

## Tags
`#customer-crisis` `#boxiiship` `#aci-logistix` `#service-disruption` `#post-mortem` `#october-2025` `#referral-partner` `#action-required` `#data-analysis` `#first-scan-delays` `#doordash-failure`

---

**Document Owner:** Brett Walker
**Contributors:** Stephen Lineberry (Data Analysis), Brock Hansen (Account Management), Christopher Von Melville (ACI Technical)
**Last Updated:** October 30, 2025
**Next Review:** After customer call (Oct 29/30)
**Status:** 🔴 Active Crisis - Daily Updates Required

**Data Sources:**
- Fathom meeting recording (Oct 28, 2025)
- Stephen Lineberry 30-day performance analysis
- BoxiiShip complaint submissions (35 tracking numbers)
- HubSpot deal records
