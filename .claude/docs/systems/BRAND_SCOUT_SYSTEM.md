# Brand Scout v3.7 - FirstMile Integration Guide

## 🎯 Mission

Autonomous lead research system that generates comprehensive Brand Scout reports for eCommerce brands, integrated with the Nebuchadnezzar v2.0 pipeline and HubSpot CRM.

---

## 🚀 Quick Start

### Single Brand Research
```
"Generate Brand Scout report for [BRAND NAME]"
"Scout this brand: https://example.com"
"Research OLIPOP and create lead record"
```

### Batch Processing
```
"Scout these 3 brands: Dr. Squatch, OLIPOP, Carbon38"
"Generate reports for all leads in my pipeline CSV"
```

### Custom Focus
```
"Focus on shipping intelligence for Brand X"
"Emphasize contact discovery for Brand Y"
"Quick scout (15 min max) for Brand Z"
```

---

## 📁 System Architecture

### Directory Structure
```
.claude/brand_scout/
├── templates/
│   └── brand_scout_v3.7_template.md
├── output/
│   └── [BRAND_NAME]_brand_scout_[DATE].md
└── config/
    ├── research_guidelines.md
    └── chrome_devtools_playbook.md
```

### Integration Points

#### 1. Nebuchadnezzar Pipeline
- Research outputs feed [00-LEAD] stage
- Auto-creates deal folders with naming convention
- Populates initial deal data structure
- Triggers N8N watch folder automation

#### 2. HubSpot CRM
- Section 6 generates copy/paste HubSpot fields
- Owner ID: 699257003 (Brett Walker)
- Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Ready for `qm hubspot create-lead` command

#### 3. Daily Operations
- Morning: Batch research queued leads
- Noon: Process new web form submissions
- EOD: Quality check and HubSpot sync

---

## 🆕 Brand Scout v4.0 - November 2025 Update

### What's New

**Structured Report Format (5 Sections)**:
1. **HubSpot Lead Record** - Direct field mappings for lead creation (table format)
2. **Shipping Operations** - Comprehensive carrier and fulfillment data (table format)
3. **Detailed Findings & Evidence** - Narrative summaries with confidence indicators
4. **Confidence Levels & Sources** - All data points marked ✅ ⚠️ or ❌ with source URLs
5. **Research Sources** - Complete source documentation

**6-Step HubSpot Automation**:
1. Extract and Normalize Data
2. Create/Upsert Contacts (Primary + Secondary decision makers)
3. Create/Upsert Company (match by domain)
4. Associate Contacts to Company
5. Create Lead/Deal (Sales Pipeline, Qualification stage)
6. Log Results and Gaps

**Key Improvements**:
- ✅ HubSpot-ready tables (copy/paste directly into fields)
- ✅ Confidence level indicators throughout (✅ ⚠️ ❌)
- ✅ Specific 3PL provider requirements (company name, not just "they use a 3PL")
- ✅ Customer review pattern analysis for actual performance data
- ✅ Python automation script included in documentation

### Migration from v3.7 to v4.0

**When to Use v4.0 Template**:
- All NEW Brand Scout leads (starting Nov 13, 2025)
- Manual research converted to structured format
- Competitive intelligence reports

**When to Use v3.7 Template** (Legacy):
- Existing leads already in pipeline (no need to migrate)
- Quick reference reports (< 15 minutes)
- Internal research notes (not for HubSpot entry)

**Backward Compatibility**:
- v3.7 reports remain valid and usable
- No need to regenerate existing reports
- Both templates supported through 2025

---

## 🧠 Research Protocol

### Phase 1: Initial Discovery (5-10 min)
1. Navigate to target website using Chrome DevTools MCP
2. Take snapshot to capture page structure
3. Scrape homepage, about, shipping pages
4. Search for company revenue, funding, leadership

### Phase 2: Deep Intelligence (10-15 min)
1. Shipping page analysis (carriers, pricing, SLAs)
2. About/Team pages (contacts, org structure)
3. Review sites (Trustpilot, BBB for complaints)
4. LinkedIn (stakeholders, company page)
5. Press releases (funding, growth, announcements)

### Phase 3: Verification (5 min)
1. Cross-check data across sources
2. Validate contact info
3. Verify metrics through multiple sources
4. Flag uncertain data with ⚠️

### Phase 4: Report Generation (5 min)
1. Read template
2. Fill all 9 sections
3. Calculate derived metrics
4. Write to output directory
5. Generate HubSpot record

**Total Time Budget**: 25-35 minutes per brand

---

## 📊 Output Structure (9 Sections)

### Section 1: Snapshot
Brand overview, revenue, AOV, volume, growth rate

### Section 2: Shipping Intelligence
Carriers, service levels, pricing, pain points, 3PL partners

### Section 3: Company Overview
Legal name, HQ, founding, DTC/wholesale split, mission

### Section 4: Stakeholders & Contacts
Decision makers with verified contact info and LinkedIn

### Section 5: Observations & Competitors
Strengths, complaints, competitor benchmarks, risk factors

### Section 6: HubSpot Lead Record
Ready-to-paste fields for CRM entry

### Section 7: CRM Contact Summary
One-line summary for pipeline tracker

### Section 8: Technical Integration
Platform, APIs, monitoring requirements

### Section 9: Methodology & Versioning
Data sources, tools used, confidence score

---

## 🔧 Chrome DevTools MCP - Core Capabilities

### Navigation & Scraping
```python
chrome-devtools:navigate_page(url="https://brand.com")
chrome-devtools:take_snapshot()
chrome-devtools:scrape_tool(url="https://brand.com/shipping")
chrome-devtools:take_screenshot(fullPage=true)
```

### Data Extraction
```python
chrome-devtools:evaluate_script(
  function="() => { return document.title }"
)
chrome-devtools:list_network_requests()
```

### Interaction
```python
chrome-devtools:click(uid="element-123")
chrome-devtools:fill(uid="input-456", value="query")
chrome-devtools:scroll(direction="down", wheel_times=3)
```

---

## 📋 Quality Standards

### Data Confidence Levels
- ✅ **HIGH** (80%+): Ready for immediate use
- ⚠️ **MEDIUM** (60-79%): Minor review needed
- ❌ **LOW** (<60%): Do not submit

### Mandatory Fields
- Company Name
- Website URL
- Elevator Pitch
- At least 1 verified contact
- Current Carrier(s)
- HQ Address

### Verification Requirements
- Revenue: 2+ sources
- Contacts: Email matches domain
- Shipping: Policy page AND checkout flow
- Address: Google Maps verified

---

## 🔄 Workflow Integration

### For New Leads (00-LEAD Stage)

1. **Research**:
   ```
   "Scout brand: [URL]"
   ```

2. **Review Output**:
   - Check `.claude/brand_scout/output/[BRAND]_brand_scout_[DATE].md`
   - Verify data confidence score

3. **Create Deal Folder**:
   ```bash
   mkdir "[00-LEAD]_[BRAND_NAME]"
   cp .claude/brand_scout/output/[BRAND]_*.md "[00-LEAD]_[BRAND_NAME]/"
   ```

4. **HubSpot Entry**:
   - Copy Section 6 from report
   - Run: `qm hubspot create-lead --interactive`
   - Paste HubSpot fields

5. **Pipeline Tracker**:
   - N8N automation detects new folder
   - Updates `_PIPELINE_TRACKER.csv`
   - Adds to `_DAILY_LOG.md`

### For Discovery Calls (01-02 Stages)

Use Brand Scout report to:
- Prepare discovery questions
- Validate shipping intelligence
- Confirm contact accuracy
- Reference competitor insights

### For Rate Creation (03 Stage)

Extract from report:
- Annual volume estimates
- Current carrier costs (if available)
- Service level requirements
- Zone distribution (from HQ address)

---

## 🎯 Research Strategies by Section

### Shipping Intelligence Deep Dive

**Sources**:
1. Shipping/Delivery policy page
2. Checkout flow (add to cart → shipping options)
3. Order tracking page (reveals carriers)
4. FAQ/Help center (delivery issues)
5. Trustpilot reviews (filter "shipping")

**Carrier Detection**:
- Track17.net → USPS
- tools.usps.com → USPS
- wwwapps.ups.com → UPS
- fedex.com/tracking → FedEx
- ShipStation → Multi-carrier (likely USPS)

### Contact Discovery Tactics

**Primary Sources**:
1. Website "Team" or "About" page
2. LinkedIn: `site:linkedin.com [BRAND] founder`
3. LinkedIn: `site:linkedin.com [BRAND] operations`
4. Press releases (CEO quotes)
5. Crunchbase leadership tab

**Validation**:
- Email format matches domain
- LinkedIn profile exists
- Title makes sense for decision-making
- Contact is current (not outdated)

### Revenue Estimation Methods

**Direct Sources**:
1. Press releases (funding announcements)
2. Crunchbase (revenue range)
3. News articles (growth metrics)

**Calculation Methods**:
- Funding rounds: ARR ≈ Funding ÷ 10
- Employee count: Revenue ≈ Employees × $200K
- Product catalog: Products × Avg Price × Est. Monthly Sales
- Mark estimates with "Est."

---

## 🚨 Common Pitfalls & Solutions

### ❌ Problem: No Shipping Info Found
**✅ Solution**:
- Test checkout flow (add item to cart)
- Check customer service FAQ
- Search: `"[BRAND] shipping policy"`
- Estimate based on typical DTC practices

### ❌ Problem: No Contact Info Found
**✅ Solution**:
- Try generic emails: info@, hello@, support@
- LinkedIn "See all employees"
- Press release quotes for names
- Mark as ⚠️ Unverified

### ❌ Problem: Revenue Data Unavailable
**✅ Solution**:
- Estimate from funding (10x ARR)
- Glassdoor employees × $200K
- Product count × price × monthly sales
- Always mark as "Est."

### ❌ Problem: Website Blocks Automation
**✅ Solution**:
- Use Wayback Machine: `web.archive.org/web/*/DOMAIN`
- Search cached: `cache:DOMAIN`
- LinkedIn company page as backup

---

## 📈 Performance Metrics

Track for each report:
- Time to completion (target: 25-35 min)
- Data confidence score (target: 80%+)
- Number of sources used (target: 5+)
- Fields completed (target: 90%+)
- Manual corrections needed (target: <5)

---

## 🔗 HubSpot Integration

### Lead Creation Workflow

1. **Generate Report**:
   - Section 6 contains all HubSpot fields

2. **Quick Method** (Copy/Paste):
   ```bash
   qm hubspot create-lead --interactive
   ```
   - Paste Section 6 fields when prompted

3. **Bulk Method** (Multiple Leads):
   ```bash
   qm hubspot bulk-leads --from-reports .claude/brand_scout/output/
   ```

4. **Verification**:
   - Check HubSpot for new lead record
   - Verify owner assignment (Brett Walker)
   - Confirm pipeline placement (Default > New)

### Deal Conversion

When moving lead to discovery:
```bash
qm hubspot convert-to-deal [LEAD_ID] --stage "01-DISCOVERY-SCHEDULED"
```

---

## 🛠️ Automation Commands

### Batch Research Queue
```bash
# Create queue file
echo "Dr. Squatch|https://drsquatch.com" > research_queue.txt
echo "OLIPOP|https://drinkolipop.com" >> research_queue.txt
echo "Carbon38|https://carbon38.com" >> research_queue.txt

# Process queue
"Process Brand Scout queue from research_queue.txt"
```

### Morning Batch (9AM Sync)
```
"Scout all new leads from yesterday's web forms"
```

### Quality Check
```
"Review Brand Scout output for [BRAND] and verify shipping intelligence"
```

---

## 📚 Reference Files

### Core Templates (v4.0 - Nov 2025)
- **Brand Scout Report Template**: `.claude/brand_scout/BRAND_SCOUT_TEMPLATE.md` ⭐ **NEW**
  - 5-section structured format with HubSpot field mappings
  - Confidence level indicators (✅ ⚠️ ❌)
  - Specific 3PL provider requirements
  - Customer review pattern analysis

- **HubSpot Lead Creation Process**: `.claude/brand_scout/HUBSPOT_LEAD_CREATION_PROCESS.md` ⭐ **NEW**
  - 6-step automation process for Brett Walker's account
  - API endpoint documentation with examples
  - Field validation and error handling
  - Python implementation reference

### Legacy Templates (v3.7)
- **Main Instructions**: `.claude/brand_scout/BRAND_SCOUT_INSTRUCTIONS.md`
- **Template**: `.claude/brand_scout/templates/brand_scout_v3.7_template.md`
- **Research Guide**: `.claude/brand_scout/config/research_guidelines.md`
- **Chrome Playbook**: `.claude/brand_scout/config/chrome_devtools_playbook.md`

### Integration Guides
- **HubSpot Integration**: `.claude/HUBSPOT_WORKFLOW_GUIDE.md`
- **Pipeline Reference**: `.claude/NEBUCHADNEZZAR_REFERENCE.md`

---

## 🎓 Training Examples

### Example 1: Dr. Squatch
```
"Generate Brand Scout report for Dr. Squatch (https://drsquatch.com) with emphasis on shipping intelligence"
```

**Expected Output**:
- Company: Dr. Squatch
- Revenue: $100M+ (Est.)
- Carriers: USPS, UPS
- Contacts: 2-3 verified
- Confidence: HIGH

### Example 2: Quick Scout
```
"Quick Brand Scout (15 min) for OLIPOP - focus on contacts and current carriers"
```

**Expected Output**:
- Reduced depth
- Core fields only
- Contact + shipping focus
- Confidence: MEDIUM

---

## 🔐 Security & Privacy

- Never store API keys in reports
- Redact sensitive customer data
- Mark proprietary info as confidential
- Follow GDPR/CCPA for contact data
- Encrypt reports if containing PII

---

## 📊 Success Metrics

### Per Report
- Completion time: 25-35 min
- Data confidence: 80%+
- Verified contacts: 2+
- HubSpot ready: Yes
- Manual edits needed: <5

### Weekly Goals
- Reports generated: 15-20
- Conversion to discovery: 30%
- Time savings vs manual: 60%
- Data accuracy: 90%+

---

## 🚀 Next Steps

1. **Test Run**: Scout a known brand to verify system
2. **Batch Process**: Queue up 5 leads from pipeline
3. **HubSpot Sync**: Import first batch of reports
4. **Monitor**: Track quality and time metrics
5. **Optimize**: Refine research strategies based on results

---

**Version**: Brand Scout v4.0 (November 2025 Update)
**Last Updated**: 2025-11-13
**Owner**: Brett Walker, FirstMile Revenue Architect
**Integration**: Nebuchadnezzar v3.0 Pipeline + HubSpot CRM Automation
