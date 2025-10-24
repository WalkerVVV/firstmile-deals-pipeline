# Brand Scout v3.7 - System Verification

Run this checklist to verify your Brand Scout system is ready for production.

---

## ✅ File Structure Check

### Required Files
- [ ] `.claude/brand_scout/INDEX.md`
- [ ] `.claude/brand_scout/QUICKSTART.md`
- [ ] `.claude/brand_scout/README.md`
- [ ] `.claude/brand_scout/BRAND_SCOUT_INSTRUCTIONS.md`
- [ ] `.claude/brand_scout/templates/brand_scout_v3.7_template.md`
- [ ] `.claude/brand_scout/config/research_guidelines.md`
- [ ] `.claude/BRAND_SCOUT_SYSTEM.md`
- [ ] `BRAND_SCOUT_SETUP_COMPLETE.md`

### Required Directories
- [ ] `.claude/brand_scout/output/` (for generated reports)
- [ ] `.claude/brand_scout/templates/`
- [ ] `.claude/brand_scout/config/`

---

## ✅ Integration Check

### Claude Code
- [ ] Project opened in Claude Code
- [ ] Can read `.claude/brand_scout/BRAND_SCOUT_INSTRUCTIONS.md`
- [ ] Can read `.claude/brand_scout/templates/brand_scout_v3.7_template.md`

### Chrome DevTools MCP
- [ ] Chrome DevTools MCP server running
- [ ] Can execute: `mcp__chrome-devtools__list_pages()`
- [ ] Can navigate to test URL
- [ ] Can take snapshot of page

### HubSpot Integration
- [ ] HubSpot MCP configured
- [ ] Can execute: `qm hubspot --help`
- [ ] Owner ID verified: 699257003 (Brett Walker)
- [ ] Pipeline ID verified: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

### Nebuchadnezzar Pipeline
- [ ] `[00-LEAD]_Template` folder exists
- [ ] N8N automation watch folder active
- [ ] `_PIPELINE_TRACKER.csv` present
- [ ] `_DAILY_LOG.md` present

---

## ✅ Functionality Test

### Test 1: Generate Report
```
"Generate Brand Scout report for Dr. Squatch"
```

**Expected Result**:
- Report generated in 25-35 minutes
- Saved to `.claude/brand_scout/output/DrSquatch_brand_scout_[DATE].md`
- All 9 sections present
- Data confidence score provided

### Test 2: Review Output
**Check report contains**:
- [ ] Company name in header
- [ ] Website URL verified
- [ ] At least 1 contact with ✅
- [ ] Current carrier identified
- [ ] HubSpot section (Section 6) fully populated
- [ ] Data confidence ≥ 75%

### Test 3: HubSpot Import
```
qm hubspot create-lead --interactive
```

**Copy Section 6 fields, verify**:
- [ ] Lead created successfully
- [ ] Owner = Brett Walker
- [ ] Pipeline = Default
- [ ] Stage = New

### Test 4: Deal Folder Creation
```bash
mkdir "[00-LEAD]_DrSquatch"
cp .claude/brand_scout/output/DrSquatch_*.md "[00-LEAD]_DrSquatch/"
```

**Verify**:
- [ ] Folder created with correct naming
- [ ] Report copied successfully
- [ ] N8N detects new folder (check logs)

---

## ✅ Documentation Access

### Can you access these files?
- [ ] [QUICKSTART.md](.claude/brand_scout/QUICKSTART.md)
- [ ] [README.md](.claude/brand_scout/README.md)
- [ ] [BRAND_SCOUT_SYSTEM.md](.claude/BRAND_SCOUT_SYSTEM.md)
- [ ] [BRAND_SCOUT_SETUP_COMPLETE.md](BRAND_SCOUT_SETUP_COMPLETE.md)

### Documentation indexed?
- [ ] Brand Scout listed in [DOCUMENTATION_INDEX.md](.claude/DOCUMENTATION_INDEX.md)
- [ ] Daily workflow integration noted
- [ ] Lead creation workflow updated

---

## ✅ Performance Baseline

Generate 3 test reports and track:

| Metric | Report 1 | Report 2 | Report 3 | Target |
|--------|----------|----------|----------|--------|
| Time (min) | ___ | ___ | ___ | 25-35 |
| Confidence (%) | ___ | ___ | ___ | 80%+ |
| Verified Contacts | ___ | ___ | ___ | 2+ |
| HubSpot Ready | Y/N | Y/N | Y/N | Yes |

---

## ✅ Common Commands Work

Test these commands in Claude Code:

### Single Brand
```
"Generate Brand Scout report for OLIPOP"
```
- [ ] Works

### Batch Processing
```
"Scout these brands: Dr. Squatch, OLIPOP"
```
- [ ] Works

### Custom Focus
```
"Quick scout (15 min) for Carbon38 - focus on shipping"
```
- [ ] Works

### Quality Check
```
"Review Brand Scout output for [BRAND] and verify data confidence"
```
- [ ] Works

---

## ✅ Error Handling

Test fallback scenarios:

### Website Down
```
"Scout a brand with blocked website: [TEST SITE]"
```
- [ ] Falls back to Wayback Machine or LinkedIn
- [ ] Marks confidence appropriately
- [ ] Documents limitation in Section 9

### No Shipping Info
```
"Scout a brand with no shipping page: [TEST SITE]"
```
- [ ] Checks FAQ/Help
- [ ] Searches for policy
- [ ] Estimates based on typical DTC
- [ ] Marks as ⚠️

### No Contacts
```
"Scout a brand with no team page: [TEST SITE]"
```
- [ ] Tries LinkedIn search
- [ ] Uses generic emails
- [ ] Marks as ⚠️ Unverified
- [ ] Documents in Section 9

---

## 🎯 Production Readiness Checklist

### System
- [ ] All files present
- [ ] All integrations working
- [ ] Documentation accessible
- [ ] Test reports successful

### Workflow
- [ ] Can generate reports
- [ ] Can review outputs
- [ ] Can import to HubSpot
- [ ] Can create deal folders

### Quality
- [ ] Data confidence ≥ 75%
- [ ] Verified contacts present
- [ ] HubSpot fields complete
- [ ] Time within 25-35 min

### Knowledge
- [ ] Read QUICKSTART.md
- [ ] Understand report structure
- [ ] Know quality standards
- [ ] Familiar with commands

---

## 🚀 Go/No-Go Decision

**Go to Production if**:
✅ All file structure checks pass
✅ All integration checks pass
✅ All functionality tests pass
✅ Performance within targets
✅ Error handling works

**Do NOT go to Production if**:
❌ Chrome DevTools MCP not working
❌ Cannot generate reports
❌ HubSpot import failing
❌ Data confidence consistently <60%
❌ Documentation inaccessible

---

## 📊 Weekly Health Check

Run this weekly to maintain system health:

### Monday Morning
- [ ] Generate 1 test report
- [ ] Verify time within target
- [ ] Check data confidence
- [ ] Test HubSpot import

### Friday EOD
- [ ] Review week's reports (quantity)
- [ ] Calculate average confidence
- [ ] Track discovery conversion
- [ ] Document improvements

---

**System Status**: ✅ Ready for Production
**Last Verified**: October 8, 2025
**Next Check**: October 15, 2025
