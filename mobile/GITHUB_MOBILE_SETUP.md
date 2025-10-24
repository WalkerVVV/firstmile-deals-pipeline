# GitHub Mobile Setup Guide - Nebuchadnezzar v3.0

## Overview
Configure GitHub Mobile app for on-the-go pipeline management, branch approvals, and deal tracking from your phone.

## Installation

### iOS
1. Open App Store
2. Search "GitHub Mobile"
3. Download and install
4. Or direct link: https://apps.apple.com/app/github/id1477376905

### Android
1. Open Google Play Store
2. Search "GitHub Mobile"
3. Download and install
4. Or direct link: https://play.google.com/store/apps/details?id=com.github.android

## Initial Configuration

### 1. Sign In
```
1. Open GitHub Mobile app
2. Tap "Sign in"
3. Enter GitHub username/email
4. Enter password
5. Complete 2FA if enabled
6. Grant permissions for notifications
```

### 2. Repository Access
```
1. Tap "Repositories" tab
2. Search: "firstmile-deals-pipeline"
3. Tap to open repository
4. Tap star icon (⭐) to favorite
5. Repository now appears in "Starred" quick access
```

### 3. Notification Configuration
```
Settings → Notifications → Configure:

✅ New pull requests
✅ New commits to branches:
   - automation/*
   - mobile/*
   - desktop/*
✅ GitHub Actions workflow completed
✅ Mentions and comments
✅ Issue assignments

Notification Frequency: Real-time
Badge App Icon: Enabled
Sound: Enabled (or customize)
```

### 4. Branch Filters
```
Repository Settings → Branches:

Show branches:
- automation/*  (overnight scripts)
- mobile/*      (your quick notes)
- desktop/*     (your detailed work)
- sync/*        (scheduled syncs)

Hide branches:
- archive/*
- old/*
- test/*

Default view: main
```

## Quick Access Setup

### Home Screen Shortcut (iOS)
```
1. Open Safari on iPhone
2. Navigate to: https://github.com/WalkerVVV/firstmile-deals-pipeline
3. Tap Share icon
4. Tap "Add to Home Screen"
5. Name: "FirstMile Pipeline"
6. Tap "Add"
```

### Home Screen Widget (Android)
```
1. Long-press home screen
2. Tap "Widgets"
3. Find "GitHub"
4. Drag "Repository" widget to home screen
5. Select: firstmile-deals-pipeline
6. Resize as needed
```

## Daily Workflow

### Morning Review (7-8 AM)
```
1. Open GitHub Mobile
2. Tap "Notifications" tab
3. Review overnight automation commits
4. Check automation/* branches
5. Review any pending PRs
6. Approve auto-merge candidates
```

### On-the-Go Updates
```
Quick Actions:
- View recent commits
- Review branch diffs
- Read commit messages
- Check GitHub Actions status
- Approve simple merges
```

### Evening Sync Check
```
1. Open app before bed
2. Check EOD sync status
3. Review any failed actions
4. Flag items for tomorrow
```

## Mobile Features

### What You CAN Do on Mobile
- ✅ View all repositories and branches
- ✅ Read commit messages and diffs
- ✅ Review pull requests
- ✅ Approve/comment on PRs
- ✅ Merge branches (simple merges)
- ✅ Create issues
- ✅ View GitHub Actions logs
- ✅ Star/unstar repositories
- ✅ Manage notifications

### What's Better on Desktop
- ⚠️ Complex code reviews (large diffs)
- ⚠️ Resolving merge conflicts
- ⚠️ Editing files directly
- ⚠️ Creating pull requests
- ⚠️ Configuring Actions/workflows
- ⚠️ Repository settings changes

## Notification Management

### Priority Notifications (Real-time)
- Automation branch commits (overnight results)
- Failed GitHub Actions (need attention)
- Mentions in comments (collaboration)

### Standard Notifications (Batched)
- New commits to main (desktop work synced)
- Pull request comments (non-urgent)
- Issue updates (tracking)

### Muted Notifications
- Draft PR updates
- Closed issue comments
- Archived branch activity

## Security

### Best Practices
- ✅ Enable 2FA on GitHub account
- ✅ Use biometric lock (Face ID/Touch ID) on phone
- ✅ Never approve complex merges on mobile
- ✅ Review branch names before approving
- ✅ Check "Files changed" count before merge
- ✅ Flag for desktop review if uncertain

### PAT (Personal Access Token) Storage
```
If using mobile dashboard (mobile_review_dashboard.html):
1. Generate PAT at: github.com/settings/tokens
2. Scopes needed: repo (full control)
3. Store in browser localStorage (auto-prompt on first use)
4. Token never leaves your device
5. Expires: Set to 90 days, renew as needed
```

## Troubleshooting

### Issue: Notifications not appearing
**Solution**:
1. Check iOS/Android notification settings
2. Ensure GitHub app has permission
3. Verify notification preferences in app
4. Check "Do Not Disturb" mode

### Issue: Can't find repository
**Solution**:
1. Verify you're signed in
2. Check repository name spelling
3. Confirm you have access (private repo)
4. Try searching by full path: WalkerVVV/firstmile-deals-pipeline

### Issue: Branch merge fails on mobile
**Solution**:
1. Check for merge conflicts
2. Review "Files changed" tab
3. Flag for desktop review instead
4. Merge from desktop when home

### Issue: App crashes or slow
**Solution**:
1. Close and restart app
2. Check for app updates
3. Clear app cache (Settings → Apps → GitHub → Clear cache)
4. Reinstall if persists

## Advanced Tips

### Quick Branch Review
```
1. Swipe down to refresh branch list
2. Tap branch name to see commits
3. Tap commit to see diff
4. Swipe right to go back
5. Long-press branch to see options
```

### Keyboard Shortcuts (iOS with external keyboard)
```
⌘ + T: New tab
⌘ + R: Refresh
⌘ + F: Search
⌘ + [: Back
⌘ + ]: Forward
```

### Siri Shortcuts (iOS)
```
"Hey Siri, show FirstMile deals"
→ Opens GitHub app to repository

"Hey Siri, check pipeline status"
→ Opens notifications tab

(Configure in Shortcuts app)
```

## Performance

### Data Usage
- Light browsing: ~1-2 MB/hour
- Reviewing diffs: ~5-10 MB/hour
- Watching large files: ~20+ MB/hour

### Battery Impact
- Background refresh: Low (~2-3% per day)
- Active use: Moderate (~10-15% per hour)
- Recommendation: Enable low power mode for extended reviews

## Next Steps

1. ✅ Install GitHub Mobile app
2. ✅ Sign in and configure notifications
3. ✅ Star firstmile-deals-pipeline repository
4. ✅ Set up quick access (home screen)
5. ✅ Configure branch filters
6. 📱 Test workflow: Create branch → Review on mobile → Approve
7. 🌐 Set up mobile review dashboard (see MOBILE_DASHBOARD.md)
8. 🤖 Configure Claude.ai integration (see CLAUDE_MOBILE_INTEGRATION.md)

## Support

**GitHub Mobile Documentation**: https://docs.github.com/en/get-started/using-github/github-mobile

**Issues**: github.com/mobile/mobile/issues

**Questions**: Review mobile dashboard guide for web-based alternative

---

**Version**: 3.0.0
**Last Updated**: October 24, 2025
**Part of**: Nebuchadnezzar v3.0 Matrix Edition
