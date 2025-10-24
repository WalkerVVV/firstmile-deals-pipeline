# Service Level Mismatch Email - JM Group

**Date**: October 7, 2025
**From**: Brett Walker, FirstMile
**To**: yehoshua.jmgroupny@gmail.com, jmgroupny@gmail.com
**Subject**: JM Group - I Found the Service Level Mismatch

---

## EMAIL BODY

Yehoshua and Daniel,

I found it. After seeing your MeUndies Amazon store shows "FREE delivery Saturday, October 11" (5 days from today), I understand exactly what happened.

**The Service Level Mismatch:**

Your Amazon Standard Shipping promises **5-day delivery**. We configured you on **Xparcel Ground (3-8 day capability)**.

FirstMile delivered 99.9% of your packages within our 8-day Ground SLA—only 41 packages out of 3,866 took longer than 8 days. Our average transit was 3.53 days, which looked excellent by shipping industry standards.

**But here's the problem:** When Xparcel Ground packages took 6, 7, or 8 days (perfectly normal for a 3-8 day service), they blew past your 5-day Amazon promise. Even though FirstMile performed well by our standards, those packages showed up as late deliveries in your Amazon metrics.

**This explains everything:**
- Amazon Account 1: 95.69% on-time (4.31% late)
- Amazon Account 2: 94.84% on-time (5.16% late)
- Walmart: 92.8% on-time (7.2% late)

**This is a preventable configuration issue, and I'm frustrated because we could have avoided this.**

Every time we reviewed FirstMile's performance together, I explained Xparcel Ground as a 3-8 day service. If you had mentioned even once that Amazon gives you 5 days for Standard Shipping, I would have immediately said: "Then you need Xparcel Expedited (2-5 day capability), not Ground."

**The Solution:**

For your Amazon Standard Shipping orders (5-day promise), you should use:
- ✅ **Xparcel Expedited (2-5 day capability)** - matches your marketplace promise
- ❌ **NOT Xparcel Ground (3-8 day capability)** - tail end causes late deliveries

**What Amazon Changed (August 2024):**

Amazon recently dropped their Standard Shipping maximum transit time from 8 days to 5 days. A setup that might have worked before August no longer aligns with Amazon's current requirements.

I've created a comprehensive Amazon OTDR specification document that explains how Amazon calculates on-time delivery. I need to understand your specific transit time settings and shipping speed breakdown so I can map them to the correct Xparcel service levels.

**Here's what I need from you to fix this:**

1. **Shipping Speed Breakdown**: What % of your orders are Standard Shipping vs Expedited vs Two-Day?
2. **Transit Time Settings**: What transit times have you set in your Amazon shipping templates?
3. **Handling Time**: What is your handling time setting? (Amazon uses Order Date + Handling Time + Transit Time)
4. **Late Delivery Samples**: Can you share 10-20 tracking numbers Amazon flagged as late deliveries?
5. **ShipStation Automation**: How is ShipStation currently selecting Xparcel service levels?

**Attached**: Full questionnaire with 8 detailed questions to help us align correctly.

**Can we meet this week to fix this configuration together?**

**My availability:**
- Monday: 2pm-5pm MDT
- Tuesday: 10am-12pm or 2pm-5pm MDT
- Wednesday: 9am-5pm MDT

30-45 minutes. Your office (2691 West 15th St, Brooklyn) or video call—whatever works best.

If you can review the attached questions before our meeting, great. If not, we can discuss them live and get you configured correctly so we can restart pickups.

Best,

Brett Walker
FirstMile
C: 402-718-4727
E: Brett.Walker@firstmile.com

---

**Attachment**: MARKETPLACE_METRICS_CLARIFICATION_QUESTIONS.md

---

## KEY MESSAGING ELEMENTS

### ✅ What This Email Does Well

1. **Specific Diagnosis**: Identifies exact mismatch (5-day promise vs 3-8 day capability)
2. **Data-Backed**: Uses FirstMile's 99.9% SLA and Amazon's visible 5-day promise
3. **Honest Frustration**: "I'm frustrated because we could have avoided this"
4. **Shared Responsibility**: "If you had mentioned" (not blame, but communication gap)
5. **Clear Solution**: Expedited for Standard Shipping orders
6. **Context for Why**: Amazon changed policy in August 2024
7. **Specific Next Steps**: 5 questions that will lead to solution
8. **Path to Restart**: "Get you configured correctly so we can restart pickups"

### ✅ Tone Elements

- **Discovery-focused**: "I found it" (not "you screwed up" or "I screwed up")
- **Confident**: Presents FirstMile's 99.9% performance as evidence of capability
- **Honest**: Expresses frustration constructively
- **Collaborative**: "Fix this configuration together"
- **Solution-oriented**: Clear path from problem to resolution

### ❌ What This Email Avoids

- Defensive apologizing or blame-taking
- Overpromising without data
- Premature detailed solutions (shifting specific volume buckets)
- Naming specific carriers (ACI, etc.)
- Making assumptions about their full setup

---

## WHY THIS APPROACH WORKS

### 1. You Have the Smoking Gun
✅ MeUndies Amazon store shows 5-day Standard Shipping
✅ Xparcel Ground capability is 3-8 days
✅ Tail end (6-8 days) = late by Amazon's 5-day standard

### 2. Explains the Communication Gap
✅ "Every time we reviewed performance, I explained 3-8 day service"
✅ "If you had mentioned 5-day requirement, I would have said Expedited"
✅ Positions as preventable through better communication (both sides)

### 3. Amazon Policy Context
✅ Amazon changed rules August 2024 (8 days → 5 days)
✅ Setup that worked before may not work now
✅ Gives them "out" (policy changed, not their mistake)

### 4. Clear Resolution Path
✅ Specific service level recommendation (Expedited for Standard Shipping)
✅ Questions to optimize full configuration
✅ Meeting to implement and restart

### 5. Balances Accountability
✅ FirstMile: "We performed well by shipping standards"
✅ JM Group: "If you'd mentioned 5-day requirement"
✅ Amazon: "They changed the policy in August"
✅ Solution: "We need to align service levels to marketplace promises"

---

## EXPECTED RESPONSE

### Best Case
"That makes total sense—yes, our Standard Shipping is 5 days. Let's meet Tuesday to reconfigure. Here are answers to your questions..."

### Good Case
"I didn't realize Ground went up to 8 days. Let's discuss the Expedited option and cost difference."

### Acceptable Case
"We'll review the questions and get back to you with our settings."

### Worst Case
"We're evaluating other carriers."
→ Response: "Understood. If you decide to give FirstMile another chance, Expedited alignment will solve this. We're here when you're ready."

---

## COST/BENEFIT CONSIDERATION

**They will likely ask**: "What's the cost difference between Ground and Expedited?"

**Your response should be ready**:
- "Let's look at your shipping speed breakdown first"
- "If 80% of your orders are Standard Shipping (5-day), we configure those on Expedited"
- "If 20% are Free Economy (8-day), those can stay on Ground"
- "I'll calculate the exact cost impact based on your actual speed mix"
- "The alternative cost is marketplace suspension—there's no recovering from that"

**Key point**: Don't lead with cost, lead with solution. Cost conversation happens AFTER they agree service alignment is necessary.

---

**Status**: READY TO SEND
**Next Step**: User approval
**Tone**: Honest discovery, confident solution, collaborative path forward
**Goal**: Meeting this week to reconfigure and restart pickups
