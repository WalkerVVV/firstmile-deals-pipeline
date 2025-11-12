# _LEADS Folder - Workflow Guide

## Purpose
Centralized repository for all cold leads and Brand Scout research. Keeps the main FirstMile_Deals folder clean and focused on active opportunities.

## Folder Structure
```
_LEADS/
  ├── README.md (Overview)
  ├── WORKFLOW_GUIDE.md (This file)
  ├── Company_Name_1/ (Brand Scout research)
  ├── Company_Name_2/ (Manual lead research)
  └── ...
```

## Workflow

### 1. Brand Scout Drops Reports Here
- Automated overnight Brand Scout runs drop research reports into `_LEADS/`
- Each company gets its own folder: `_LEADS/CompanyName/`
- Contains Brand Scout markdown report with company info, contacts, shipping data

### 2. Review Leads
- Check `_LEADS/` folder during 9AM sync
- Review Brand Scout reports for quality leads
- Prioritize based on:
  - Deal size potential
  - Industry fit (wellness, D2C, eCommerce)
  - Contact quality

### 3. Push to HubSpot When Ready
When ready to pursue a lead:
```bash
# Option 1: Use HubSpot MCP command
qm hubspot create-lead --company "CompanyName" --first-name "John" --last-name "Smith" --email "john@company.com"

# Option 2: Create deal directly
qm hubspot create-deal --deal-name "CompanyName - Xparcel Ground" --amount 500000
```

### 4. Move to Active Pipeline
Once deal is created in HubSpot and discovery is scheduled:
```bash
# Move folder from _LEADS to active pipeline
mv "_LEADS/CompanyName" "[01-DISCOVERY-SCHEDULED]_CompanyName"
```

### 5. Archive Rejected Leads
For leads that don't qualify:
- Leave in `_LEADS/` folder
- Add note to README explaining why rejected
- Keep for future reference

## System Integration

### Prioritization Agent
- **Excludes** `_LEADS/` folder from priority scoring
- Focuses only on active deals (stages 1-6)
- Cold leads don't clutter daily priorities

### Brand Scout Agent
- Automatically creates folders in `_LEADS/`
- No manual folder creation needed
- Runs overnight Monday 6AM (10 leads)

## Best Practices

1. **Review Daily**: Check `_LEADS/` during 9AM sync
2. **Act Fast on Hot Leads**: Don't let good opportunities sit
3. **Keep Clean**: Archive or delete clearly unqualified leads
4. **Track in HubSpot**: All active outreach goes through HubSpot
5. **Document Why**: Add notes for rejected leads

## Quick Commands

```bash
# List all leads
ls _LEADS/

# Count leads
ls _LEADS/ | wc -l

# Search for specific company
ls _LEADS/ | grep -i "company"

# Move lead to active pipeline
mv "_LEADS/CompanyName" "[01-DISCOVERY-SCHEDULED]_CompanyName"
```

