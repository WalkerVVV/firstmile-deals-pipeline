# N8N Integration Guide - Nebuchadnezzar v3.0

## Overview
This guide explains how to integrate N8N workflows with the Git automation system for automatic commit creation when deals move through the pipeline.

## Architecture

```
Folder Rename → N8N File Watcher → Extract Deal Info → Check Lock →
Acquire Lock → Execute Git Commit → Update HubSpot → Release Lock → Log Action
```

## N8N Workflow Configuration

### Workflow: "Git Commit on Folder Move"

#### Node 1: File System Watcher
**Type**: File Trigger
**Configuration**:
```json
{
  "path": "C:\\Users\\BrettWalker\\FirstMile_Deals\\",
  "events": ["rename", "move"],
  "recursive": false,
  "debounce": 1000
}
```

#### Node 2: Extract Deal Info (Code Node)
**Type**: Function
**Code**:
```javascript
const path = $input.item.json.path;
const filename = path.split('\\').pop();

// Parse folder name: [##-STAGE]_Company_Name
const match = filename.match(/\[(\d{2})-([A-Z0-9\-]+)\]_(.+)/);

if (!match) {
  return { json: { error: 'Invalid folder format' } };
}

const stage = match[2];
const companyName = match[3];

// Determine old stage from previous path (if available)
const oldPath = $input.item.json.oldPath || '';
const oldMatch = oldPath.match(/\[(\d{2})-([A-Z0-9\-]+)\]/);
const oldStage = oldMatch ? oldMatch[2] : 'UNKNOWN';

return {
  json: {
    company_name: companyName,
    old_stage: oldStage,
    new_stage: stage,
    timestamp: new Date().toISOString(),
    folder_path: path
  }
};
```

#### Node 3: Check Lock (HTTP Request)
**Type**: HTTP Request (or Execute Command)
**Configuration**:
```json
{
  "method": "POST",
  "url": "http://localhost:5678/webhook/check-lock",
  "body": {
    "deal_name": "={{ $json.company_name }}",
    "agent_type": "automation"
  }
}
```

**Alternative (Direct Python Execution)**:
```json
{
  "command": "python",
  "arguments": [
    "git_automation/branch_manager.py",
    "acquire",
    "={{ $json.company_name }}",
    "automation",
    "30"
  ],
  "cwd": "C:\\Users\\BrettWalker\\FirstMile_Deals"
}
```

#### Node 4: Git Commit (Execute Command)
**Type**: Execute Command
**Configuration**:
```json
{
  "command": "python",
  "arguments": [
    "git_automation/commit_wrapper.py",
    "={{ $json.company_name }}",
    "automation",
    "stage_change",
    "Moved from {{ $json.old_stage }} to {{ $json.new_stage }}"
  ],
  "cwd": "C:\\Users\\BrettWalker\\FirstMile_Deals"
}
```

#### Node 5: Update HubSpot (HTTP Request)
**Type**: HTTP Request
**Configuration**:
```json
{
  "method": "PATCH",
  "url": "https://api.hubapi.com/crm/v3/objects/deals/={{ $json.deal_id }}",
  "headers": {
    "Authorization": "Bearer {{ $credentials.hubspot.apiKey }}",
    "Content-Type": "application/json"
  },
  "body": {
    "properties": {
      "dealstage": "={{ $json.new_stage_id }}",
      "notes": "Stage changed via automation at {{ $json.timestamp }}"
    }
  }
}
```

#### Node 6: Release Lock (Execute Command)
**Type**: Execute Command
**Configuration**:
```json
{
  "command": "python",
  "arguments": [
    "git_automation/branch_manager.py",
    "release",
    "={{ $json.company_name }}"
  ],
  "cwd": "C:\\Users\\BrettWalker\\FirstMile_Deals"
}
```

#### Node 7: Log Action (Append File)
**Type**: Write File
**Configuration**:
```json
{
  "file_path": "C:\\Users\\BrettWalker\\Downloads\\_DAILY_LOG.md",
  "action": "append",
  "content": "\n[{{ $json.timestamp }}] AUTOMATION: {{ $json.company_name }} moved from {{ $json.old_stage }} to {{ $json.new_stage }}\n"
}
```

## Testing the Integration

### Manual Test
1. Create a test deal folder: `[01-QUALIFIED]_Test_Company_A`
2. Move it to a new stage: `[02-DISCOVERY-COMPLETE]_Test_Company_A`
3. Verify N8N workflow triggers
4. Check that Git commit was created
5. Verify HubSpot was updated
6. Check `_DAILY_LOG.md` for entry

### Command Line Test
```bash
# Test lock acquisition
python git_automation/branch_manager.py acquire "Test_Company_A" automation 30

# Test quick commit
python git_automation/commit_wrapper.py "Test_Company_A" automation stage_change "Test automation integration"

# Test lock release
python git_automation/branch_manager.py release "Test_Company_A"

# Check branch created
git branch | grep automation

# Check commit
git log --oneline -1
```

## Webhook Alternative (Optional)

If you prefer webhooks over file watching:

### Webhook Endpoint Configuration
**URL**: `http://localhost:5678/webhook/git-commit`
**Method**: POST
**Body**:
```json
{
  "deal_name": "Company_Name",
  "agent_type": "automation",
  "action": "stage_change",
  "description": "Moved to new stage",
  "old_stage": "QUALIFIED",
  "new_stage": "DISCOVERY-COMPLETE"
}
```

### Webhook Handler (N8N)
**Node**: Webhook
**Response**:
```json
{
  "success": true,
  "branch": "automation/company_name_stage_change",
  "commit_hash": "abc123",
  "auto_mergeable": true
}
```

## Troubleshooting

### Issue: Lock file not releasing
**Solution**: Check for stale locks
```bash
python git_automation/branch_manager.py locks
# Manually release if needed
python git_automation/branch_manager.py release "CompanyName"
```

### Issue: Git commits not being created
**Solution**: Check Python execution in N8N
- Verify Python path in N8N settings
- Check working directory is correct
- Review N8N execution logs

### Issue: HubSpot sync breaking
**Solution**: Verify HubSpot API credentials
- Check `.env` file for correct API key
- Verify deal ID mapping
- Test HubSpot API separately

## Security Considerations

1. **.env Protection**: Never commit `.env` file (pre-commit hook prevents this)
2. **Lock Timeouts**: Default 30 minutes, adjust if needed
3. **Error Handling**: N8N should catch errors and alert via email
4. **Logging**: All actions logged to `_DAILY_LOG.md`

## Next Steps

1. Set up N8N workflow using above configuration
2. Test with 2-3 sample deals
3. Monitor for 1-2 days before full rollout
4. Adjust timeout and retry settings as needed
5. Add error notifications (email/Slack)

## Support

For issues with:
- **Git automation**: Check `git_automation/` scripts
- **N8N workflows**: Review N8N execution logs
- **HubSpot integration**: Test API separately
- **Lock conflicts**: Use `branch_manager.py locks` command
