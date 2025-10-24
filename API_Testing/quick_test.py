"""
Quick Test Script - No setup required for Mock Server
====================================================

This script tests the FirstMile Tracking API using the mock server.
No JWT token or authentication required - perfect for learning the API!

Usage:
    python quick_test.py
"""

import requests
import json

def test_mock_api():
    """Test using the mock server (no authentication needed)"""

    print("\n" + "="*70)
    print("🚀 FirstMile Tracking API - Quick Mock Test")
    print("="*70)
    print("\nUsing Mock Server (No Authentication Required)")
    print("URL: https://acilogistix.redocly.app/_mock/xmethod/tracking/swagger/\n")

    # Mock server endpoint
    url = "https://acilogistix.redocly.app/_mock/xmethod/tracking/swagger/Tracking/v1/123456789"

    print("📦 Testing with tracking number: 123456789\n")
    print("🔄 Sending request...")

    try:
        response = requests.get(url, timeout=10)

        print(f"✅ Response received! (Status: {response.status_code})\n")

        if response.status_code == 200:
            data = response.json()

            # Print formatted response
            print("="*70)
            print("📋 SAMPLE TRACKING RESPONSE")
            print("="*70)
            print(json.dumps(data, indent=2))
            print("="*70)

            # Extract key information
            print("\n🔍 KEY INFORMATION EXTRACTED:\n")
            print(f"   Tracking Number: {data.get('trackingNumber')}")
            print(f"   Carrier: {data.get('carrier')}")
            print(f"   Service Level: {data.get('serviceLevel')}")
            print(f"   Weight: {data.get('weightLbs')} lbs")
            print(f"   Processed Date: {data.get('processedDate')}")

            if data.get('deliveryDateEstimated'):
                print(f"\n   📅 Delivery Estimate: {data.get('deliveryDateEstimated')}")
                print(f"   📅 Delivery Window: {data.get('deliveryDateMin')} to {data.get('deliveryDateMax')}")

            if data.get('shipmentAddress'):
                addr = data['shipmentAddress']
                print(f"\n   📍 Destination:")
                print(f"      {addr.get('name')}")
                print(f"      {addr.get('address1')}")
                if addr.get('address2'):
                    print(f"      {addr.get('address2')}")
                print(f"      {addr.get('city')}, {addr.get('regionCode')} {addr.get('countryCode')}")

            if data.get('events'):
                print(f"\n   🚚 Tracking Events: {len(data['events'])} events")
                print(f"\n   Latest Event:")
                latest = data['events'][0]
                print(f"      Type: {latest.get('eventType')}")
                print(f"      Status: {latest.get('status')}")
                print(f"      Location: {latest.get('location')}")
                print(f"      Date: {latest.get('eventDate')}")

            print("\n✅ SUCCESS! Mock server is working perfectly.")
            print("\n💡 This is sample data. Real API requires JWT authentication.")
            print("   See TESTING_GUIDE.md for how to test with real data.\n")

        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {str(e)}\n")

if __name__ == "__main__":
    test_mock_api()
