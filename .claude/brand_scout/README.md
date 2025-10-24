# Brand Scout v3.7 - Autonomous Lead Research System

**Integrated with Nebuchadnezzar v2.0 Pipeline | HubSpot CRM Ready | Chrome DevTools MCP Powered**

---

## 🎯 What This Does

Generates comprehensive 9-section Brand Scout reports for eCommerce brands in 25-35 minutes using:
- **Chrome DevTools MCP**: Full browser automation for web research
- **Web Search**: Real-time company intelligence gathering
- **Web Fetch**: Deep content extraction
- **Automated Analysis**: Shipping carriers, contacts, revenue, competitors

**Output**: HubSpot-ready lead records with verified data for FirstMile sales pipeline.

---

## 📁 System Structure

```
brand_scout/
├── BRAND_SCOUT_INSTRUCTIONS.md  # Claude Code operating manual
├── templates/
│   └── brand_scout_v3.7_template.md
├── output/
│   └── [Generated reports saved here]
├── config/
│   └── research_guidelines.md
└── README.md (this file)
```

---

## 🚀 Quick Start

### Single Brand Research

In Claude Code chat:
```
"Generate Brand Scout report for Dr. Squatch"
"Scout this brand: https://drinkolipop.com"
"Research OLIPOP and create HubSpot lead record"
```

### Batch Processing

```
"Scout these 3 brands: Dr. Squatch, OLIPOP, Carbon38"
"Process Brand Scout queue from research_queue.txt"
```

### Custom Focus

```
"Focus on shipping intelligence for Brand X"
"Quick scout (15 min max) for Brand Y"
"Emphasize contact discovery for Brand Z"
```

---

## 📊 Report Structure (9 Sections)

### 1. Snapshot
Brand overview, revenue, AOV, ship volume, growth rate

### 2. Shipping Intelligence
Carriers, service levels, pricing, pain points, 3PL partners

### 3. Company Overview
Legal name, HQ, founding, DTC/wholesale split, mission

### 4. Stakeholders & Contacts
Decision makers with verified emails and LinkedIn profiles

### 5. Observations & Competitors
Strengths, complaints, competitor benchmarks, risk factors

### 6. HubSpot Lead Record
Copy/paste fields for CRM entry (Owner: Brett Walker)

### 7. CRM Contact Summary
One-line format for pipeline tracker

### 8. Technical Integration
Platform (Shopify, WooCommerce), APIs, monitoring

### 9. Methodology & Versioning
Data sources, tools used, confidence score

---

## ✅ Quality Standards

### Data Confidence Levels
- **HIGH (80%+)**: Ready for immediate use
- **MEDIUM (60-79%)**: Minor review needed
- **LOW (<60%)**: Do not submit

### Mandatory Fields
- Company Name
- Website URL
- Elevator Pitch
- At least 1 verified contact
- Current Carrier(s) or "Unknown"
- HQ Address (minimum: city, state)

### Verification Requirements
- Revenue: 2+ sources preferred
- Contacts: Email domain matches company
- Shipping: Policy page + checkout flow ideal
- Address: Google Maps verified

---

## 🔄 Workflow Integration

### For New Leads ([00-LEAD] Stage)

1. **Generate Report**:
   ```
   "Scout brand: [URL]"
   ```

2. **Review Output**:
   ```
   .claude/brand_scout/output/[BRAND]_brand_scout_[DATE].md
   ```

3. **Create Deal Folder**:
   ```bash
   mkdir "[00-LEAD]_[BRAND_NAME]"
   cp .claude/brand_scout/output/[BRAND]_*.md "[00-LEAD]_[BRAND_NAME]/"
   ```

4. **HubSpot Entry**:
   - Copy Section 6 from report
   - Run: `qm hubspot create-lead --interactive`
   - Paste fields

5. **Pipeline Automation**:
   - N8N detects new folder
   - Updates `_PIPELINE_TRACKER.csv`
   - Logs to `_DAILY_LOG.md`

### For Discovery Calls ([01-02] Stages)

Use Brand Scout to:
- Prepare discovery questions
- Validate shipping intelligence
- Confirm contact accuracy
- Reference competitor insights

### For Rate Creation ([03] Stage)

Extract from report:
- Annual volume estimates
- Current carrier costs
- Service level requirements
- Geographic distribution (from HQ)

---

## 🧠 Chrome DevTools MCP Capabilities

### Navigation & Scraping
```python
mcp__chrome-devtools__navigate_page(url="https://brand.com")
mcp__chrome-devtools__take_snapshot()
mcp__chrome-devtools__scrape_tool()
mcp__chrome-devtools__take_screenshot(fullPage=True)
```

### Data Extraction
```python
mcp__chrome-devtools__evaluate_script(function="() => { return document.title }")
mcp__chrome-devtools__list_network_requests()
```

### Interaction
```python
mcp__chrome-devtools__click(uid="element-123")
mcp__chrome-devtools__fill(uid="input-456", value="search")
```

---

## 📈 Performance Metrics

### Per Report
- **Time**: 25-35 minutes
- **Confidence**: 80%+ target
- **Verified Contacts**: 2+ preferred
- **HubSpot Ready**: Yes
- **Manual Edits**: <5 target

### Weekly Goals
- **Reports Generated**: 15-20
- **Conversion to Discovery**: 30%
- **Time Savings vs Manual**: 60%
- **Data Accuracy**: 90%+

---

## 🎓 Example Commands

### Standard Research
```
"Generate Brand Scout report for Dr. Squatch (https://drsquatch.com)"
```

**Output**: Complete 9-section report with HIGH confidence

### Quick Scout (Time-Limited)
```
"Quick Brand Scout (15 min) for OLIPOP - focus on contacts and carriers"
```

**Output**: Core fields only, MEDIUM confidence

### Emphasis Research
```
"Scout Carbon38 with emphasis on shipping intelligence and competitor analysis"
```

**Output**: Enhanced shipping section, detailed competitor benchmarks

---

## 🔗 Integration Points

### Nebuchadnezzar v2.0 Pipeline
- Feeds [00-LEAD] stage
- Auto-creates deal folders
- Triggers N8N automation
- Populates pipeline tracker

### HubSpot CRM
- Section 6 = Ready to paste
- Owner ID: 699257003 (Brett Walker)
- Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Compatible with `qm hubspot` commands

### Daily Operations
- **9AM Sync**: Batch research queued leads
- **NOON Sync**: Process web form submissions
- **EOD Sync**: Quality check and HubSpot sync

---

## 📚 Documentation Reference

| File | Purpose |
|------|---------|
| `BRAND_SCOUT_INSTRUCTIONS.md` | Full operating manual for Claude Code |
| `templates/brand_scout_v3.7_template.md` | Report template structure |
| `config/research_guidelines.md` | Tactical research playbook |
| `../.claude/BRAND_SCOUT_SYSTEM.md` | System overview and integration guide |
| `../.claude/HUBSPOT_WORKFLOW_GUIDE.md` | HubSpot API integration |
| `../.claude/NEBUCHADNEZZAR_REFERENCE.md` | Pipeline reference |

---

## 🚨 Common Issues & Solutions

### Issue: Website Blocks Automation
**Solution**: Use Wayback Machine or LinkedIn company page as backup

### Issue: No Shipping Info Found
**Solution**: Test checkout flow, check FAQ, estimate based on typical DTC

### Issue: No Contact Info Found
**Solution**: Try generic emails (info@, hello@), LinkedIn employees, mark as ⚠️

### Issue: Revenue Data Unavailable
**Solution**: Estimate from funding (÷10), employees (×$200K), mark as "Est."

---

## 🔐 Security & Privacy

- Never store API keys in reports
- Redact sensitive customer data
- Mark proprietary info as confidential
- Follow GDPR/CCPA for contact data
- Reports stored locally only

---

## 📊 Output Examples

### File Naming
```
output/DrSquatch_brand_scout_2025-10-08.md
output/OLIPOP_brand_scout_2025-10-08.md
output/Carbon38_brand_scout_2025-10-08.md
```

### Report Header
```markdown
10/08/2025 14:30 MST

# Brand Scout v3.7 – Dr. Squatch

**Generated by**: Claude Code
**Research Duration**: 28 minutes
**Data Confidence**: HIGH (90%)
**Primary Sources**: Website, LinkedIn, Crunchbase, Trustpilot
```

---

## 🎯 Success Criteria

**Report is successful when**:
- [ ] All 9 sections completed
- [ ] 80%+ data confidence
- [ ] 2+ verified contacts
- [ ] HubSpot section ready to paste
- [ ] Current carrier identified
- [ ] HQ address verified
- [ ] <5 manual corrections needed

---

## 🛠️ Troubleshooting

### Report Quality Issues
- Check data confidence score in header
- Verify mandatory fields present
- Cross-reference revenue sources
- Validate contact email domains

### HubSpot Import Issues
- Ensure all Section 6 fields populated
- Check date format (YYYY-MM-DD)
- Verify owner = "Brett Walker"
- Confirm pipeline = "Default"

### Time Overruns
- Set 35-minute hard stop
- Use quick search strategies
- Estimate when appropriate
- Don't over-research optional fields

---

## 🚀 Next Steps

1. **Test Run**: Scout a known brand (e.g., Dr. Squatch)
2. **Batch Process**: Queue 5 leads from pipeline
3. **HubSpot Sync**: Import first batch
4. **Monitor**: Track quality and time metrics
5. **Optimize**: Refine based on results

---

## 📞 Support

For issues or questions:
- Review `BRAND_SCOUT_INSTRUCTIONS.md` for detailed guidance
- Check `research_guidelines.md` for tactical patterns
- Reference `../.claude/BRAND_SCOUT_SYSTEM.md` for system overview
- Consult Nebuchadnezzar documentation for pipeline integration

---

**Version**: Brand Scout v3.7
**Last Updated**: 2025-10-08
**Owner**: Brett Walker, FirstMile Revenue Architect
**Integration**: Nebuchadnezzar v2.0 Pipeline + HubSpot CRM
**Technology**: Claude Code + Chrome DevTools MCP
