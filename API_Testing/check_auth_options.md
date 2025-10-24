# FirstMile Tracking API - Authentication Investigation

## Current Status

The API endpoint `https://trackingapi.firstmile.com/Tracking/v1/{trackingNumber}` **requires authentication** (returns 401 Unauthorized without Bearer token).

## What Your IT Might Mean

Your IT said "you don't need one for the trackingapi" - here are possible interpretations:

### Option 1: Different Tracking Endpoint (Public Portal)

FirstMile might have a **public tracking portal** (web-based) that doesn't require API authentication:

**Possible URLs to try:**
```
https://trackingapi.firstmile.com/track/{trackingNumber}
https://tracking.firstmile.com/track/{trackingNumber}
https://www.firstmile.com/track/{trackingNumber}
https://trackingapi.firstmile.com/public/track/{trackingNumber}
```

### Option 2: API Key Instead of JWT

Some APIs use simpler API key authentication instead of Bearer JWT:

**Try:**
```bash
# API Key in header
curl -H "X-API-Key: your_api_key" https://trackingapi.firstmile.com/Tracking/v1/9261290339737604364714

# API Key in query parameter
curl "https://trackingapi.firstmile.com/Tracking/v1/9261290339737604364714?apiKey=your_key"
```

### Option 3: Pre-Authenticated Access (IP Whitelisting)

Your organization's IP addresses might be whitelisted, requiring no additional auth when accessed from your network.

**To test:**
- Must be run from your company network
- Might not work from home/VPN

### Option 4: Different Service (Not REST API)

Your IT might be referring to:
- **SOAP/XML tracking service** (legacy)
- **Email-based tracking queries**
- **FTP file drops**
- **EDI tracking updates**

### Option 5: Embedded Widget/iFrame

FirstMile might provide a tracking widget that you embed:
```html
<iframe src="https://trackingapi.firstmile.com/widget?tracking=9261290339737604364714"></iframe>
```

## What to Ask Your IT

**Clarifying Questions:**

1. **"What is the exact URL or endpoint you use for tracking?"**
   - Get the full URL they're using

2. **"How do you currently track shipments - what system/tool?"**
   - Web browser? API call? Integrated system?

3. **"Do you have any credentials, API keys, or configuration for tracking?"**
   - They might have credentials they're not calling a "JWT token"

4. **"Can you show me an example of how you query tracking information?"**
   - See their actual method

5. **"Are we whitelisted by IP address for tracking API access?"**
   - This might explain "no authentication needed"

## Next Steps

### Step 1: Check if Public Portal Exists

Let me search for a public tracking page...

### Step 2: Ask IT for Specifics

**Email Template:**

```
Subject: Tracking API - Need Clarification on Authentication

Hi [IT Contact],

I'm working on integrating FirstMile tracking. You mentioned we don't need
authentication for the tracking API. Can you clarify:

1. What is the exact URL/endpoint you use for tracking?
2. How do you currently query tracking information?
3. Do you have any credentials, API keys, or configuration docs?
4. Are we IP-whitelisted for FirstMile tracking access?

I'm trying to track these shipments:
- 9261290339737604364714
- 9261290339737604467729
- 9261290339737604467446
- 9400136208303372628595
- 9261290339737604478176

The REST API endpoint (https://trackingapi.firstmile.com/Tracking/v1/)
requires a Bearer token, so I want to make sure I'm using the right method.

Thanks!
```

## Test Results

**REST API Endpoint:** `https://trackingapi.firstmile.com/Tracking/v1/{trackingNumber}`
- ❌ Without auth: 401 Unauthorized
- ❌ With TechPartnerId only: 401 Unauthorized
- ✅ Requires: Bearer JWT token

**Tested:**
- Direct access: FAILED (401)
- TechPartnerId param: FAILED (401)
- Public access: FAILED (401)

**Conclusion:**
The REST API definitely requires authentication. Your IT must be referring to a different tracking method or endpoint.
