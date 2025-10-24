# FirstMile Deal Memory - Auto-Store Workflow

**Purpose:** Automatically store every customer analysis in domain memory for cumulative intelligence

**Version:** 1.0
**Last Updated:** October 13, 2025

---

## Quick Store Command

After completing any FirstMile analysis, use this prompt:

```
Store this FirstMile analysis in domain memory using this template:

**Company:** [Company Name]
**Industry:** [Industry/Vertical]
**Analysis Date:** [YYYY-MM-DD]
**Pipeline Stage:** [00-09 with name]

**Volume:** [Monthly/Annual packages]
**Current Spend:** [$ annual], [$ per package]
**Current Carrier(s):** [Carrier mix with %]

**FirstMile Opportunity:**
- Revenue: $[Annual revenue potential]
- Savings: $[Annual savings], [%]
- New Cost: $[Per package]

**Profile:** [Key shipping characteristics - weight, zones, geography]

**Optimizations:** [Top 3 opportunities]

**Services:** [Xparcel Ground/Expedited/Priority recommendations]

**Critical:** [Must-know factors, blockers, special requirements]

**Next Steps:** [3-5 immediate actions]

**Tags:** [8-12 relevant tags for semantic search]
```

---

## Template with All Fields

### Required Fields

```markdown
**Company:** Full legal name
**Industry:** Primary vertical (eCommerce, 3PL, Manufacturing, etc.)
**Analysis Date:** YYYY-MM-DD
**Pipeline Stage:** [00-09] Stage Name
```

### Volume & Current State

```markdown
**Volume Profile:**
- Monthly: X,XXX packages
- Annual: XXX,XXX packages (if known)
- Daily Average: XXX packages

**Current State:**
- Annual Spend: $X,XXX,XXX
- Cost per Package: $X.XX
- Current Carrier(s): [Carrier 1 (XX%), Carrier 2 (XX%)]
```

### FirstMile Opportunity

```markdown
**FirstMile Opportunity:**
- Annual Revenue Potential: $X,XXX,XXX
- Customer Savings: $XXX,XXX - $XXX,XXX (XX-XX%)
- New Average Cost: $X.XX - $X.XX per package
- Confidence: [High/Medium/Low] + reason if not high
```

### Shipping Profile

```markdown
**Shipping Profile:**
- Weight: XX% under 1 lb, average X.XX lbs
- Geography: [Origin state/city], XX% regional (Zones 1-4)
- Top States: [Top 5 states]
- Dimensions: XX% under 1 cubic foot
- Special: [Any unique characteristics]
```

### Key Opportunities

```markdown
**Key Optimization Opportunities:**
1. [Specific opportunity with data]
2. [Specific opportunity with data]
3. [Specific opportunity with data]
```

### Service Recommendations

```markdown
**Service Level Recommendations:**
- Xparcel Ground (3-8d): [% of volume, use case]
- Xparcel Expedited (2-5d): [% of volume, use case]
- Xparcel Priority (1-3d): [% of volume, use case]
```

### Critical Factors

```markdown
**Critical Success Factors:**
- [Must-have requirement or blocker]
- [Special consideration]
- [Risk or challenge]
```

### Next Steps

```markdown
**Next Actions:**
- [ ] [Action 1 with owner/timeline]
- [ ] [Action 2 with owner/timeline]
- [ ] [Action 3 with owner/timeline]
```

### Tags (8-12 minimum)

```markdown
**Tags:**
Industry: ecommerce, 3pl, retail, etc.
Stage: discovery, proposal-sent, closed-won, etc.
Profile: lightweight, regional, heavyweight, etc.
Priority: high-value, urgent, critical, at-risk, etc.
Optimization: weight-optimization, zone-skipping, etc.
Special: live-animals, hazmat, compliance-required, etc.
Competitive: USPS-competitive, UPS-competitive, etc.
Status: pilot-candidate, data-verification-needed, etc.
```

---

## Tag Categories & Examples

### Industry Tags
`ecommerce` `3pl` `fulfillment` `retail` `manufacturing` `pharmaceutical` `medical` `food-beverage` `electronics` `apparel`

### Pipeline Stage Tags
`lead` `discovery` `qualified` `rate-creation` `proposal-sent` `setup-docs` `implementation` `closed-won` `closed-lost` `win-back`

### Profile Tags
`lightweight` `heavyweight` `regional` `national` `zone-skipping-opportunity` `dimensional-weight` `multi-carrier` `single-carrier`

### Value Tags
`high-value` `enterprise` `mid-market` `smb` `pilot-candidate` `growth-trajectory` `seasonal`

### Priority Tags
`urgent` `critical` `at-risk` `hot-lead` `slow-burn` `long-sales-cycle`

### Optimization Tags
`weight-optimization` `billable-weight-issue` `threshold-packages` `zone-optimization` `carrier-consolidation` `service-level-mix`

### Special Requirement Tags
`live-animals` `hazmat` `cold-chain` `oversized` `international` `compliance-required` `api-integration` `custom-workflow`

### Competitive Tags
`USPS-competitive` `UPS-competitive` `FedEx-competitive` `DHL-competitive` `regional-carrier` `switching-from-[carrier]`

### Status Tags
`data-verification-needed` `rate-pending` `technical-integration` `compliance-review` `pilot-running` `performance-issues` `service-recovery`

### Savings Tags
`high-savings` `moderate-savings` `conservative-estimate` `aggressive-estimate` `savings-10-20` `savings-20-30` `savings-30-plus`

---

## Real Examples

### Example 1: Josh's Frogs

```
**Company:** Josh's Frogs
**Industry:** Live Insect/Reptile Supplier (eCommerce)
**Analysis Date:** 2025-10-08
**Pipeline Stage:** [01] Discovery Scheduled

**Volume:** 27K-31K/month, 324K annual
**Current Spend:** $1.44M/year, $8.21/pkg
**Current Carrier:** USPS 59%, FedEx 26%, UPS 11%

**FirstMile Opportunity:**
- Revenue: $2.34M
- Savings: $312K-$384K (12-15%)
- New Cost: $7.00-$7.22/pkg

**Profile:** 43.7% <1lb, PA origin, 65.1% regional, 93.1% <1 cuft

**Optimizations:**
1. 7,996 packages at 15-15.99oz threshold
2. UPS → Xparcel Ground (142% cost difference)
3. Zone-skip 65% regional via Select Network

**Services:** Ground (59% USPS volume), Expedited (time-sensitive), Priority (premium)

**Critical:** Live animal compliance verification required

**Next Steps:**
- Present 12-15% savings rate card
- Verify Xparcel live insect compatibility
- Plan API integration
- Setup Q1 2025 pilot (1K packages)

**Tags:** ecommerce, high-value, live-animals, discovery, lightweight, regional, weight-optimization, pilot-candidate, Q1-2025-target, USPS-dominant, Pennsylvania-origin, savings-10-20
```

### Example 2: Service Recovery (JM Group)

```
**Company:** JM Group of NY
**Industry:** eCommerce/3PL
**Analysis Date:** 2025-09-30
**Pipeline Stage:** [07] Closed Won - CRITICAL AT RISK

**Status:** 🚨 CANCELLED PICKUPS (Oct 6, 2025)

**Volume:** 2,817 shipments (Aug-Sep sample)

**Performance:**
- Delivered SLA: 99.9% ✅
- In-Transit On-Time: 62.2%
- In-Transit Late: 37.8% (634 packages) 🚨

**Root Cause:** Zone 7-8 performance, linehaul delays, induction timing

**Recovery Plan:**
- Urgent meeting (48hr window)
- ZIP-limit → Expedited for problem destinations
- Enhanced in-transit monitoring
- Target: 95%+ in-transit on-time

**Critical:** Fast response, transparent root cause, concrete commitments

**Next Steps:**
- Schedule urgent meeting with Yehoshua & Daniel
- Present root cause analysis
- Propose ZIP-limits and monitoring
- Request phased pickup resumption

**Tags:** closed-won, at-risk, service-recovery, urgent, in-transit-issues, zone-7-8-challenges, customer-retention, cancelled-service, critical-priority, action-required-48hr
```

---

## Automation Ideas (Future)

### Auto-Store After Analysis Script

Add to end of analysis scripts:

```python
def auto_store_in_memory(analysis_data):
    """
    Automatically format and store analysis in domain memory
    """
    memory_entry = {
        "company": analysis_data["company_name"],
        "industry": analysis_data.get("industry", "eCommerce"),
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "pipeline_stage": analysis_data.get("stage", "Unknown"),
        # ... rest of template
    }

    # TODO: Call domain-memory-agent MCP store_document
    # when MCP is available after restart

    return memory_entry
```

### Slash Command Idea

Create `/store-analysis` command that:
1. Reads last completed analysis summary
2. Extracts key fields automatically
3. Prompts for missing fields
4. Stores in domain memory with tags

### Weekly Batch Store

```
"Review all analyses completed this week and store any that aren't in domain memory yet"
```

---

## Search Patterns (When MCP Available)

### Find Similar Deals

```
"Search memory for all deals with 40%+ savings in ecommerce vertical"
```

### Find By Profile

```
"Search memory for lightweight customers (<50% under 1 lb) in discovery stage"
```

### Find By Challenge

```
"Search memory for how we handled live animal compliance objections"
```

### Competitive Intelligence

```
"Search memory for all prospects switching from UPS, show average savings%"
```

### Pipeline Intelligence

```
"Search memory for deals that closed within 14 days, what were the common factors?"
```

---

## Migration Checklist (For MCP)

When domain-memory-agent MCP is available:

- [ ] Restart Claude Code
- [ ] Verify `mcp__domain-memory-agent__store_document` available
- [ ] Test store_document with sample data
- [ ] Migrate Josh's Frogs from JSON → MCP
- [ ] Migrate Stackd Logistics from JSON → MCP
- [ ] Migrate JM Group NY from JSON → MCP
- [ ] Test semantic_search functionality
- [ ] Test summarize functionality
- [ ] Document search patterns that work best
- [ ] Create shortcut commands for common searches
- [ ] Update this workflow with MCP-specific instructions

---

## Best Practices

### Always Include
1. **Quantitative data** - Numbers, not adjectives
2. **Specific tags** - 8-12 minimum for good searchability
3. **Next actions** - So future you knows what to do
4. **Critical factors** - Blockers, risks, must-knows

### Never Skip
1. Pipeline stage (critical for filtering)
2. Volume (monthly at minimum)
3. Savings % and $ amount
4. Tags (makes search useful)

### Pro Tips
1. **Tag liberally** - More tags = better search results
2. **Update regularly** - When deal progresses, update the memory
3. **Link related deals** - Tag competitors or similar profiles
4. **Note what worked** - When deal closes, document why

---

**Next:** Restart Claude Code and migrate to MCP domain-memory-agent for semantic search! 🚀
