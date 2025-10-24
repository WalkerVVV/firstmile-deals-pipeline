# GitHub Pages Setup Guide

**Phase 3, Task 3.2 - Mobile Dashboard Deployment**

The mobile review dashboard has been deployed to the `docs/` folder and pushed to GitHub. Now you need to configure GitHub Pages to serve it.

## Step 1: Enable GitHub Pages

1. Go to your GitHub repository: https://github.com/WalkerVVV/firstmile-deals-pipeline

2. Click **Settings** (top menu bar)

3. Click **Pages** (left sidebar under "Code and automation")

4. Under **"Source"**, select:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs`

5. Click **Save**

6. GitHub will display: "Your site is live at https://walkervvv.github.io/firstmile-deals-pipeline/"

## Step 2: Wait for Deployment

GitHub Pages typically takes 1-2 minutes to build and deploy. You'll see a deployment status at the top of the Pages settings page.

When ready, you'll see: ✅ **Your site is published at https://walkervvv.github.io/firstmile-deals-pipeline/**

## Step 3: Access the Dashboard

### On Mobile:
1. Open Safari (iOS) or Chrome (Android)
2. Navigate to: **https://walkervvv.github.io/firstmile-deals-pipeline/**
3. Tap "Share" → "Add to Home Screen" for quick access
4. Enter your GitHub Personal Access Token when prompted

### On Desktop:
1. Visit: **https://walkervvv.github.io/firstmile-deals-pipeline/**
2. Bookmark for quick access
3. Enter your GitHub PAT when prompted

## GitHub Personal Access Token (PAT) Setup

The dashboard needs a GitHub PAT to approve merges and manage branches.

### Create a PAT:
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a descriptive name: `FirstMile Mobile Dashboard`
4. Set expiration: **90 days** (or longer)
5. Select scopes:
   - ✅ **repo** (Full control of private repositories)
     - repo:status
     - repo_deployment
     - public_repo
     - repo:invite
     - security_events
6. Click **"Generate token"**
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again)
8. Store securely in password manager

### Enter PAT in Dashboard:
1. Open the dashboard URL
2. Click **"Setup Token"** button
3. Paste your GitHub PAT
4. Token is stored in browser localStorage (device-specific, secure)

## Dashboard Features

### Status Bar (Top)
- **Pending**: Total branches awaiting review
- **Auto-Merge**: Branches safe for automatic merge
- **Review**: Branches requiring manual review

### Branch Cards
Each card shows:
- **Branch name**: Deal and action description
- **Agent badge**: automation / mobile / desktop / sync
- **Safety indicator**: Auto-Merge Safe / Manual Review
- **Action buttons**:
  - **Approve & Merge**: Merge to main immediately
  - **Desktop Review**: Flag for detailed desktop review
  - **Reject**: Delete branch (cannot be undone)

### Auto-Refresh
Dashboard automatically refreshes every 60 seconds to show new branches.

## Troubleshooting

### Dashboard shows "GitHub Token Required"
**Solution**: You need to set up your GitHub PAT (see above)

### Dashboard shows "Error Loading Branches"
**Possible causes**:
1. GitHub PAT expired or invalid
2. Network connection issue
3. Repository permissions changed

**Solution**:
- Click "Setup Token" to re-enter PAT
- Check network connection
- Verify PAT has `repo` permissions

### GitHub Pages shows 404 error
**Possible causes**:
1. GitHub Pages not configured correctly
2. Deployment still in progress

**Solution**:
- Verify Settings → Pages shows `/docs` folder selected
- Wait 2-3 minutes for deployment
- Check repository Actions tab for deployment status

### Changes to dashboard not appearing
**Cause**: GitHub Pages caching

**Solution**:
- Wait 2-3 minutes for cache to clear
- Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache if issue persists

## Security Notes

### PAT Storage
- Token stored in browser localStorage (not transmitted anywhere)
- Each device/browser needs its own token entry
- Token never leaves your device except for GitHub API calls

### Revoking Access
To revoke mobile access:
1. Go to: https://github.com/settings/tokens
2. Find your "FirstMile Mobile Dashboard" token
3. Click **"Delete"**
4. Mobile dashboard will no longer be able to approve merges

### Token Best Practices
- Use shortest practical expiration (90 days recommended)
- Create separate tokens for mobile vs desktop
- Revoke immediately if device is lost
- Never share token via email, Slack, or text

## Testing the Deployment

### Basic Functionality Test:
1. Open dashboard on mobile
2. Verify status bar loads with numbers
3. Check that branch cards display correctly
4. Test "Setup Token" flow (don't actually enter token yet)

### Full Integration Test:
1. Create a test branch from desktop:
   ```bash
   python git_automation/commit_wrapper.py "Test_Deal" mobile test "Testing mobile dashboard"
   ```
2. Wait 60 seconds for dashboard auto-refresh
3. Verify test branch appears in dashboard
4. Test "Desktop Review" button (flags for review)
5. Delete test branch manually:
   ```bash
   git branch -D mobile/Test_Deal_test
   git push origin --delete mobile/Test_Deal_test
   ```

## Mobile Workflow Recommendations

### Morning Review (9 AM):
1. Open dashboard on mobile
2. Review overnight automation branches
3. Approve safe auto-merge candidates
4. Flag complex changes for desktop review

### On-the-Go (Throughout Day):
1. Receive GitHub notification of new branch
2. Quick review in dashboard
3. Approve if straightforward
4. Flag for desktop if complex

### Evening Sync (End of Day):
1. Final review of pending branches
2. Approve accumulated changes
3. Verify no branches stuck in limbo

## Next Steps

After configuring GitHub Pages:
1. ✅ Test dashboard on mobile device
2. ✅ Set up GitHub PAT
3. ✅ Bookmark dashboard URL
4. ✅ Add to mobile home screen
5. ➡️ Continue to Task 3.3: Claude.ai Mobile Integration Guide

## Phase 3 Progress

- ✅ Task 3.1: GitHub Mobile Setup Guide
- ✅ Task 3.2: Mobile Review Dashboard (deployment complete, awaiting Pages config)
- ⏳ Task 3.3: Claude.ai Mobile Integration Guide
- ⏳ Task 3.4: Test Mobile Approval Workflow

---

**Deployment URL**: https://walkervvv.github.io/firstmile-deals-pipeline/

**Last Updated**: Phase 3, October 24, 2025
**Status**: Dashboard deployed, awaiting GitHub Pages configuration
