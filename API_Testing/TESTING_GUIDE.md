# FirstMile Tracking API - Testing Guide

Quick guide to start testing the FirstMile Tracking API right now.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your JWT Token

**You need a JWT token to authenticate with the API. Contact FirstMile to obtain:**

1. **Test Environment Token** - For development/testing
2. **Production Token** - For live shipment tracking

**Where to get it:**
- Email: [FirstMile technical support/onboarding contact]
- Account Dashboard: [If FirstMile provides a web portal]
- API Key Request Form: [Contact your FirstMile account manager]

### Step 2: Install Requirements

```bash
# Navigate to testing directory
cd C:\Users\BrettWalker\FirstMile_Deals\API_Testing

# Install Python dependencies
pip install requests python-dotenv
```

### Step 3: Configure Environment

```bash
# Copy example .env file
copy .env.example .env

# Edit .env file and add your JWT token
notepad .env
```

**Add your token to .env:**
```
FIRSTMILE_JWT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
FIRSTMILE_ENVIRONMENT=test
```

### Step 4: Run Interactive Tester

```bash
python test_tracking_api.py
```

You'll see:
```
🚀 FirstMile Tracking API - Interactive Tester
Environment: 🟢 TEST
JWT Token: ✅ Set

🔍 Testing connection to 🟢 TEST environment...
   URL: https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net
✅ API is reachable

Enter tracking numbers to test (or 'q' to quit)
📦 Tracking Number: _
```

---

## 📋 Testing Without a JWT Token

If you don't have a token yet, you can still test using the **Mock Server**:

### Option 1: Use Mock Server (No Authentication)

```bash
# Run with mock environment
python -c "from test_tracking_api import FirstMileTrackingTester; t = FirstMileTrackingTester(jwt_token='mock', environment='mock'); t.get_tracking('123456789')"
```

### Option 2: Quick cURL Test (Mock)

```bash
curl -i https://acilogistix.redocly.app/_mock/xmethod/tracking/swagger/Tracking/v1/123456789
```

The mock server returns sample data to help you understand the response structure.

---

## 🧪 Testing Scenarios

### Test 1: Single Tracking Number

**Interactive Mode:**
```bash
python test_tracking_api.py

# At prompt, enter tracking number:
📦 Tracking Number: 123456789
```

**Command Line Mode:**
```bash
python test_tracking_api.py 123456789
```

### Test 2: Multiple Tracking Numbers (Batch)

```bash
python test_tracking_api.py 123456789 987654321 456789123
```

**Output:**
```
🔄 Batch Testing 3 Tracking Numbers
   Environment: 🟢 TEST

[1/3] Testing 123456789...
   ✅ Found - Status: Delivered
[2/3] Testing 987654321...
   ✅ Found - Status: In Transit
[3/3] Testing 456789123...
   ❌ Not found or error

📊 BATCH TEST SUMMARY
✅ Success: 2
❌ Not Found: 1
```

### Test 3: Environment Switching

In interactive mode:
```
📦 Tracking Number: e

Switch to which environment?
  1. Test (default)
  2. Production
  3. Mock
Choice (1-3): 2

✅ Switched to 🔴 PRODUCTION
```

### Test 4: Save Response to File

```
📦 Tracking Number: 123456789
[Response displays...]

📦 Tracking Number: s
💾 Response saved to: tracking_responses/123456789_20251009_143052.json
```

---

## 📦 Getting Real Tracking Numbers to Test

### Option 1: From FirstMile

**Ask FirstMile for test tracking numbers:**
- Request a few test shipments in the test environment
- They should provide tracking numbers that have events populated
- Good test numbers include: delivered, in-transit, and exception scenarios

### Option 2: Create Test Shipments

If you have access to FirstMile's shipping API:
1. Create a test label using the shipping API
2. Use the tracking number returned
3. Note: Newly created labels may not have events for 24-48 hours

### Option 3: Use Historical Data

If you have existing FirstMile shipments:
1. Pull tracking numbers from your order management system
2. Test with recently delivered shipments (90-day retention typical)
3. Look for shipments from the last 30 days for best results

---

## 🔍 What to Look For During Testing

### ✅ Successful Response Indicators

- **HTTP 200** status code
- **trackingNumber** field matches your input
- **events** array contains tracking scans
- **processedDate** is populated
- **serviceLevel** shows: "Ground", "Expedited", or "Priority"

### ❌ Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| HTTP 401 Unauthorized | Invalid/missing JWT token | Check .env file, verify token with FirstMile |
| HTTP 404 Not Found | Tracking number doesn't exist | Verify number, check if label was created |
| Empty events array | No scans yet | Wait 24-48 hours after label creation |
| Connection timeout | API unreachable | Check internet, verify environment URL |
| HTTP 400 Bad Request | Invalid tracking number format | Check for typos, verify format with carrier |

---

## 📊 Sample Test Results

### Example 1: Delivered Shipment

```
✅ TRACKING FOUND: 123456789
📋 SHIPMENT DETAILS:
   Carrier: FirstMile
   Service Level: Ground
   Weight: 2.5 lbs
   Processed Date: 2023-08-01 10:00 AM

📅 DELIVERY ESTIMATES:
   Estimated: 2023-08-05
   Min Date: 2023-08-04
   Max Date (SLA): 2023-08-07

📍 DESTINATION:
   Company: FirstMile Inc.
   Name: John Doe
   Address: 123 Main St
            Suite 100
   City: Salt Lake City, UT US
   Type: Commercial

🚚 TRACKING EVENTS (4 total):
   1. ✅ Package Delivered
      Date: 2023-08-05 02:30 PM
      Location: New York, NY
      Status: Delivered
      Carrier: USPS

   2. 🚚 Out for Delivery
      Date: 2023-08-05 09:00 AM
      Location: New York, NY
      Status: Out for Delivery

   3. 🚚 In Transit
      Date: 2023-08-02 08:15 AM
      Location: Chicago, IL
      Status: In Transit

   4. 📦 Label Created
      Date: 2023-08-01 10:00 AM
      Location: Salt Lake City, UT
      Status: In Transit

📸 PROOF OF DELIVERY: 1 image(s) available
```

### Example 2: In-Transit Shipment

```
✅ TRACKING FOUND: 987654321
📋 SHIPMENT DETAILS:
   Carrier: FirstMile
   Service Level: Expedited
   Weight: 1.2 lbs
   Processed Date: 2023-10-09 08:00 AM

📅 DELIVERY ESTIMATES:
   Estimated: 2023-10-12
   Min Date: 2023-10-11
   Max Date (SLA): 2023-10-14

🚚 TRACKING EVENTS (2 total):
   1. 🚚 In Transit
      Date: 2023-10-10 03:45 PM
      Location: Denver, CO
      Status: In Transit

   2. 📦 Picked Up
      Date: 2023-10-09 02:15 PM
      Location: Los Angeles, CA
      Status: In Transit
```

---

## 🛠️ Advanced Testing

### Custom Python Script

Create `my_test.py`:

```python
from test_tracking_api import FirstMileTrackingTester

# Initialize with your token
api = FirstMileTrackingTester(
    jwt_token="your_token_here",
    environment='test'
)

# Test specific tracking number
tracking = "123456789"
response = api.get_tracking(tracking)

if response:
    # Extract specific data
    print(f"Service Level: {response.get('serviceLevel')}")
    print(f"Carrier: {response.get('carrier')}")

    # Check if delivered
    if response.get('events'):
        latest_status = response['events'][0]['status']
        if latest_status == 'Delivered':
            print("✅ Package was delivered!")

    # Save response
    api.save_response(response, tracking)
```

Run it:
```bash
python my_test.py
```

### Batch Testing from CSV

Create `batch_test.py`:

```python
import csv
from test_tracking_api import FirstMileTrackingTester

# Read tracking numbers from CSV
tracking_numbers = []
with open('tracking_numbers.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tracking_numbers.append(row['tracking_number'])

# Test all numbers
api = FirstMileTrackingTester(environment='test')
results = api.batch_test(tracking_numbers)

# Export results
with open('test_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['tracking', 'status', 'service_level', 'carrier'])
    writer.writeheader()
    writer.writerows(results['success'])

print(f"✅ Results exported to test_results.csv")
```

### Integration with Pandas

```python
import pandas as pd
from test_tracking_api import FirstMileTrackingTester

# Load shipments from Excel
df = pd.read_excel('shipments.xlsx')

# Initialize API
api = FirstMileTrackingTester(environment='production')

# Test each tracking number
results = []
for tracking in df['tracking_number']:
    response = api.get_tracking(tracking, verbose=False)
    if response:
        results.append({
            'tracking': tracking,
            'status': response['events'][0]['status'] if response.get('events') else 'Unknown',
            'delivered_date': response['events'][0]['eventDate'] if response.get('events') and response['events'][0]['status'] == 'Delivered' else None,
            'service_level': response.get('serviceLevel'),
            'weight': response.get('weightLbs')
        })

# Create results DataFrame
results_df = pd.DataFrame(results)
results_df.to_excel('tracking_results.xlsx', index=False)
```

---

## 🔑 How to Get JWT Token

### Method 1: Contact FirstMile Directly

**Email your FirstMile account manager or technical contact:**

```
Subject: API Access Request - Tracking API JWT Token

Hi [FirstMile Contact],

I need access to the FirstMile Tracking API for [purpose: testing/integration/production].

Please provide:
1. JWT authentication token for Test environment
2. JWT authentication token for Production environment (when ready)
3. Token expiration and refresh information
4. TechPartnerId (if applicable)

Account Details:
- Company: [Your Company]
- Account Number: [If applicable]
- Contact: [Your Name/Email]

Thank you!
```

### Method 2: FirstMile Developer Portal (If Available)

Some platforms provide a self-service portal:
1. Log in to FirstMile customer portal
2. Navigate to Developer/API section
3. Generate API keys/tokens
4. Copy JWT token to .env file

### Method 3: Through FirstMile Sales/Onboarding

During account setup:
1. Request API access during onboarding
2. Specify need for Tracking API
3. Receive credentials via secure channel

---

## 📝 Testing Checklist

Before building your integration, verify:

- [ ] JWT token works in test environment
- [ ] Can retrieve tracking for valid tracking numbers
- [ ] Error handling works (404, 401, 400 tested)
- [ ] Events array populates correctly
- [ ] Delivery estimates are accurate
- [ ] Service levels map correctly (Ground/Expedited/Priority)
- [ ] Address data is complete
- [ ] POD images can be decoded (for delivered shipments)
- [ ] Batch lookups work efficiently
- [ ] Response time is acceptable (<2 seconds typical)
- [ ] Production token works when ready

---

## 🐛 Troubleshooting

### Issue: "No JWT token found"

**Solution:**
```bash
# Verify .env file exists
dir .env

# Check contents
type .env

# Make sure it contains:
FIRSTMILE_JWT_TOKEN=your_actual_token_here
```

### Issue: HTTP 401 Unauthorized

**Solutions:**
1. Verify token is correct (no extra spaces/line breaks)
2. Check token hasn't expired
3. Verify you're using correct environment (test token for test env)
4. Contact FirstMile to regenerate token

### Issue: HTTP 404 Not Found

**Solutions:**
1. Verify tracking number is correct
2. Check if tracking number exists in that environment
3. Wait 24-48 hours if label just created
4. Try a different tracking number

### Issue: Empty events array

**Explanation:**
- Label created but not yet scanned by carrier
- Normal for labels <24 hours old

**Solutions:**
1. Wait for carrier to scan package
2. Use a delivered shipment for testing
3. Request test numbers from FirstMile with populated events

---

## 📞 Support

**FirstMile Technical Support:**
- Documentation: https://acilogistix.redocly.app/xmethod/tracking/swagger/tracking
- Email: [Contact your account manager for support email]
- Phone: [Contact your account manager for support phone]

**Common Questions:**
1. **How do I get a JWT token?** → Contact FirstMile technical support
2. **How long are tokens valid?** → Check with FirstMile (typically 30-90 days)
3. **Can I use test tokens in production?** → No, separate tokens required
4. **What tracking numbers should I test with?** → Request test data from FirstMile

---

## ✅ Next Steps

After successful testing:

1. **Review [FIRSTMILE_TRACKING_API_MEGA_GUIDE.md](../FIRSTMILE_TRACKING_API_MEGA_GUIDE.md)** - Complete API reference
2. **Build Integration** - Use code examples from mega guide
3. **Implement Error Handling** - Follow best practices
4. **Set Up Monitoring** - Track API performance
5. **Request Production Access** - When ready to go live
6. **Load Testing** - Test with production volumes

---

**Happy Testing! 🚀**
