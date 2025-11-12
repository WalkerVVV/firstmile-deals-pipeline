# 📱 Create HubSpot Tasks from Mobile

**You can now create all 11 morning priority tasks with ONE TAP from your iPhone!**

---

## 🚀 Quick Start (First Time Setup - 2 mins)

### Step 1: Add GitHub Secret (One-Time Setup)

**On desktop or mobile browser**:

1. Go to: https://github.com/WalkerVVV/firstmile-deals-pipeline/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `HUBSPOT_API_KEY`
4. Value: `${HUBSPOT_API_KEY}` (your HubSpot API key)
5. Click **"Add secret"**

✅ **Done!** You only need to do this once.

---

## ⚡ Create Tasks from Mobile (Every Time)

### Method 1: GitHub Mobile App (Recommended)

1. Open **GitHub app** on iPhone
2. Go to **WalkerVVV/firstmile-deals-pipeline**
3. Tap **Actions** tab
4. Tap **"Create HubSpot Tasks"** workflow
5. Tap **"Run workflow"** button
6. Select **"morning_priorities"**
7. Tap **"Run workflow"**

**Takes 30 seconds** → Creates all 11 tasks automatically!

---

### Method 2: GitHub Mobile Web

1. Open Safari/Chrome on iPhone
2. Go to: https://github.com/WalkerVVV/firstmile-deals-pipeline/actions/workflows/create-hubspot-tasks.yml
3. Tap **"Run workflow"** dropdown
4. Keep **"Branch: main"** selected
5. Select **"morning_priorities"**
6. Tap **"Run workflow"**

**Status**: Check the Actions tab to see progress (takes ~30 seconds)

---

### Method 3: Direct Link (Fastest)

**Bookmark this URL** on your iPhone home screen:

```
https://github.com/WalkerVVV/firstmile-deals-pipeline/actions/workflows/create-hubspot-tasks.yml
```

Then just tap it → **"Run workflow"** → **Done!**

---

## 📋 What Gets Created

When you run the workflow, it automatically creates **11 HubSpot tasks**:

### 🚨 CRITICAL (Due TODAY)
1. **DYLN** - Verify RATE-1907 status ($3.6M deal - 17 days overdue)
2. **Josh's Frogs** - Follow up on Friday meeting outcome ($289K)
3. **Upstate Prep** - Push for go-live date ($950K at finish line)
4. **BoxiiShip** - Credit approval follow-up (overdue)

### 🔥 HIGH PRIORITY (Due TODAY)
5. **Stackd Logistics** - Send ZIP code request (draft ready)

### 📧 PROPOSAL FOLLOW-UPS (Due TOMORROW)
6. **COLDEST** - Weekly follow-up with Halloween urgency
7. **Caputron** - Weekly follow-up ($477K, 69+ days in stage)
8. **IronLink Skupreme** - Weekly follow-up ($233K)
9. **ODW Logistics** - Weekly follow-up
10. **OTW Shipping** - Weekly follow-up (156+ days - OVERDUE)
11. **Team Shipper** - Weekly follow-up ($500K)

---

## ✅ Verify Tasks Were Created

**After workflow completes**:

1. Open **HubSpot mobile app** or web
2. Go to **Tasks**
3. You should see 11 new tasks with today's/tomorrow's due dates
4. All tasks are associated with correct deals

---

## 🔧 Troubleshooting

### "Workflow not found"
- Make sure you've committed and pushed the workflow file
- Check: `.github/workflows/create-hubspot-tasks.yml` exists in repo

### "Secret not found"
- Go back to Step 1 and add the `HUBSPOT_API_KEY` secret
- Make sure the secret name is exactly: `HUBSPOT_API_KEY`

### "Access denied" errors
- Verify your HubSpot API key has these scopes:
  - ✅ crm.objects.deals.read
  - ✅ crm.objects.deals.write
  - ✅ crm.schemas.deals.read
  - ✅ crm.objects.contacts.read
  - ✅ crm.objects.contacts.write

### Tasks not appearing in HubSpot
- Check the workflow run logs in GitHub Actions
- Look for "Successfully created: X" in the output
- Make sure deals exist with matching names in your HubSpot

---

## 🎯 Future Enhancements

**Task sets you can add**:

- `critical_only` - Just the 4 critical tasks
- `proposal_followups` - Just the 7 proposal follow-ups
- `custom` - Define specific tasks on-demand

**To add**: Edit `.github/workflows/create-hubspot-tasks.yml`

---

## 💡 Pro Tips

### Bookmark for Quick Access
1. Open the workflow URL in Safari
2. Tap Share → **"Add to Home Screen"**
3. Name it: "Create Tasks"
4. Now you have ONE-TAP task creation!

### Use with Shortcuts App
Create iOS Shortcut:
1. Open **Shortcuts** app
2. Create new shortcut
3. Add: **"Open URL"** → workflow URL
4. Name: "Create HubSpot Tasks"
5. Add to widget or home screen

---

## 🔄 How It Works

```
iPhone (GitHub App)          GitHub Actions          HubSpot API
      |                            |                       |
      |── Trigger workflow ───────>|                       |
      |                            |                       |
      |                            |── Search for deals ───>|
      |                            |<── Return deal IDs ────|
      |                            |                       |
      |                            |── Create 11 tasks ────>|
      |                            |<── Confirm created ────|
      |                            |                       |
      |<── Workflow complete ──────|                       |
      |    (30 seconds)            |                       |
```

**No local machine needed!** Everything runs in the cloud.

---

## 📱 Made for Mobile

This entire workflow was designed and tested on **Claude Mobile** (iPhone app) to solve the problem of creating HubSpot tasks while on the go.

**Use case**: Monday morning, you're commuting, you read your morning action plan in Claude Mobile, and you want to create all your tasks RIGHT NOW without waiting to get to your desk.

**Solution**: One tap in GitHub mobile app → 11 tasks created automatically → Start executing immediately.

---

**Status**: ✅ READY TO USE
**Last Updated**: October 27, 2025
**Created via**: Claude Mobile (iPhone)
