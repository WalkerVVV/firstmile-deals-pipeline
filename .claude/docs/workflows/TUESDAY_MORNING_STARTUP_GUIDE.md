# TUESDAY MORNING STARTUP GUIDE
**Nebuchadnezzar v3.0 - For Dummies Edition**

---

## ☕ STEP 1: BOOT UP (You're Here!)

**What you just did:**
1. ✅ Turned on computer
2. ✅ Opened VSCode
3. ✅ File > Open Folder → `C:\Users\BrettWalker\FirstMile_Deals`

**What's happening now:**
- VSCode is loading the FirstMile_Deals workspace
- Claude Code extension is warming up
- You're ready to talk to me!

---

## 💬 STEP 2: START THE CHAT (Do This Now!)

**In VSCode, open Claude Code chat:**

**Option A - Keyboard shortcut:**
- Press `Ctrl+Shift+P` (opens command palette)
- Type: "Claude Code: Open Chat"
- Press Enter

**Option B - Click method:**
- Look for the Claude icon in the left sidebar (looks like a robot face)
- Click it
- Chat panel opens on the right side

**You should see:**
- A chat window with a text box at the bottom
- Previous conversation history (optional, can clear if you want fresh start)

---

## 🔄 STEP 3: LOAD TODAY'S CONTEXT (Copy/Paste This)

**Type or paste this into the Claude Code chat:**

```
run 9am sync
```

**What this does:**
- Loads yesterday's EOD log from Downloads folder
- Loads today's priority action list
- Checks HubSpot for overnight changes
- Gives you the morning briefing

**You'll see:**
- Today's top priorities (Stackd email, Team Shipper, BoxiiShip)
- Pipeline health snapshot
- Action items in order of urgency

---

## 🔐 STEP 4: API TOKEN CHECK (One-Time Setup)

**Good news:** Your API token is already configured! Here's how it works:

### How It's Set Up (No Action Needed)
- Your HubSpot Private App Token is: `${HUBSPOT_API_KEY}`
- It's stored in Python scripts with a fallback default
- Works automatically on your local machine
- No environment variables needed for local work

### If You Ever Need to Check It
**Location:** `C:\Users\BrettWalker\FirstMile_Deals\hubspot_config.py`

**To verify it's working:**
```
Hey Claude, can you verify the HubSpot API connection?
```

I'll run a quick test and tell you if everything's good.

### If It Ever Breaks (Unlikely)
**Symptoms:**
- "401 Unauthorized" errors when syncing
- "Invalid token" messages

**Fix:**
1. Go to HubSpot > Settings > Integrations > Private Apps
2. Find your "Nebuchadnezzar" app (or whatever you named it)
3. Copy the access token
4. Tell me: "Hey Claude, update the HubSpot token to: [paste token here]"

---

## 📋 STEP 5: GET YOUR MORNING PRIORITIES (Automatic)

**After running `run 9am sync`, you'll see this:**

### Priority 1 - IMMEDIATE
1. **Stackd Logistics** - SEND EMAIL (everything ready)
2. **Team Shipper** - SEND PROPOSAL (34d overdue)
3. **BoxiiShip** - Melissa follow-up (verify encoding fix)

### What You Should Do Next
**Ask me to help with Priority 1:**
```
Hey Claude, help me send the Stackd Logistics email. Where is it?
```

**I'll respond with:**
- Exact file path to the email draft
- Attachments to include
- Quick review of what we're sending

---

## 🚀 STEP 6: EXECUTE FIRST ACTION (Let's Do It!)

**For Stackd Logistics email:**

**You say:**
```
Open the Stackd email draft for me
```

**I'll do:**
- Find the email file
- Read it to you
- Show you what attachments to include
- Ask if you want to make changes

**You do:**
- Review the email
- Copy it to your email client (Outlook/Gmail)
- Attach the files I list
- Hit send!

**You tell me:**
```
Stackd email sent!
```

**I'll do:**
- Mark it complete in your daily log
- Move to Priority 2 (Team Shipper)
- Update your progress

---

## 🔁 STEP 7: REPEAT FOR EACH PRIORITY

**The Pattern:**
1. **You ask:** "Help me with [next priority]"
2. **I find:** Email draft / proposal / files
3. **You do:** Send email / make call / update HubSpot
4. **You tell me:** "[Action] done!"
5. **I update:** Daily log and move to next priority

**Keep going until you say:**
```
I'm done for now, let's do EOD sync
```

---

## 📊 STEP 8: CHECK PROGRESS ANYTIME

**Want to see what's left?**
```
What's my progress today?
```

**I'll show you:**
- ✅ What's complete
- 🔄 What you're working on
- ⏳ What's still pending

---

## 🛑 STEP 9: WHEN THINGS GO WRONG

### "I can't find a file"
**You say:**
```
Hey Claude, I can't find the Team Shipper email draft. Can you search for it?
```

**I'll search:**
- Use Glob tool to find all Team Shipper files
- Show you exact paths
- Open the right file

### "The API isn't working"
**You say:**
```
Claude, HubSpot sync is failing. Can you check the connection?
```

**I'll run:**
- Test query to HubSpot API
- Show you the error message
- Tell you how to fix it

### "I need to update a deal in HubSpot"
**You say:**
```
Move Tactical Logistic to Closed Won in HubSpot
```

**I'll do:**
- Run Python script to update deal stage
- Verify the change
- Update your local tracking

---

## 🌙 STEP 10: END OF DAY

**When you're done (around 5pm):**
```
run eod sync
```

**I'll do:**
- Summarize what you completed today
- List what's pending for tomorrow
- Save context for tomorrow's 9am sync
- Generate tomorrow's priority list

---

## 🎯 QUICK REFERENCE CARD

| What You Want | What You Type |
|---------------|---------------|
| Start your day | `run 9am sync` |
| Get help with next action | `Help me with [task name]` |
| Find a file | `Find [filename or deal name]` |
| Check progress | `What's my progress today?` |
| Update HubSpot | `Move [deal] to [stage]` |
| End your day | `run eod sync` |
| Just chat | Type anything! I'm here to help |

---

## 💡 PRO TIPS

### Tip 1: I Remember Everything
You can reference things from earlier:
```
"Remember that BoxiiShip issue? What was the status?"
```

### Tip 2: I Can Multitask
Ask me to do multiple things:
```
"Find the Team Shipper proposal AND check if Tactical Logistic is ready to close"
```

### Tip 3: I Learn Your Patterns
The more we work together, the better I understand your workflow:
- How you like emails formatted
- When you prefer detailed explanations vs. quick answers
- Your naming conventions

### Tip 4: Use Me as Your Memory
Forgot something from last week?
```
"What was the savings percentage we calculated for Stackd?"
```

### Tip 5: I Can Search Email (If You Share It)
If you paste email content:
```
"Here's the email I got from Reid. What should I respond?"
```

---

## 🆘 EMERGENCY CONTACTS

**If Claude Code isn't working:**
1. Close and reopen VSCode
2. Check your internet connection
3. Restart Claude Code extension (Ctrl+Shift+P > "Reload Window")

**If HubSpot API breaks:**
1. Check Settings > Integrations > Private Apps in HubSpot
2. Verify token hasn't expired
3. Tell me and I'll walk you through fixing it

**If you're just stuck:**
```
"Claude, I'm stuck. Can you help me figure out what to do next?"
```

---

## ✅ YOU'RE READY!

**Right now, type this to get started:**
```
run 9am sync
```

**I'll take it from there!** 🚀

---

**Last Updated:** October 7, 2025
**Version:** Nebuchadnezzar v3.0
**Your AI Copilot:** Claude (that's me! 👋)
