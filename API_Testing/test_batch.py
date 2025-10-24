"""
Batch Tracking Test - Production Server
"""

import requests
import json
import os
from datetime import datetime

# Tracking numbers to test
TRACKING_NUMBERS = [
    "9261290339737604364714",
    "9261290339737604467729",
    "9261290339737604467446",
    "9400136208303372628595",
    "9261290339737604478176"
]

# Configuration
BASE_URL = "https://trackingapi.firstmile.com"
JWT_TOKEN = os.getenv('FIRSTMILE_JWT_TOKEN', '')

def test_tracking(tracking_number):
    """Test a single tracking number"""
    url = f"{BASE_URL}/Tracking/v1/{tracking_number}"

    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/json"
    }

    print(f"\n{'='*70}")
    print(f"Testing: {tracking_number}")
    print(f"{'='*70}")

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Print summary
            print(f"SUCCESS - Tracking Found")
            print(f"\nCarrier: {data.get('carrier', 'N/A')}")
            print(f"Service Level: {data.get('serviceLevel', 'N/A')}")
            print(f"Weight: {data.get('weightLbs', 'N/A')} lbs")
            print(f"Processed: {data.get('processedDate', 'N/A')}")

            # Delivery info
            if data.get('deliveryDateEstimated'):
                print(f"\nDelivery Estimate: {data.get('deliveryDateEstimated')}")
                print(f"SLA Window: {data.get('deliveryDateMin')} to {data.get('deliveryDateMax')}")

            # Address
            if data.get('shipmentAddress'):
                addr = data['shipmentAddress']
                print(f"\nDestination:")
                print(f"  {addr.get('name', 'N/A')}")
                print(f"  {addr.get('city', 'N/A')}, {addr.get('regionCode', 'N/A')}")

            # Events
            if data.get('events'):
                print(f"\nTracking Events: {len(data['events'])} total")

                # Show latest 3 events
                for i, event in enumerate(data['events'][:3], 1):
                    print(f"\n  {i}. {event.get('eventType', 'Unknown')}")
                    print(f"     Date: {event.get('eventDate', 'N/A')}")
                    print(f"     Location: {event.get('location', 'N/A')}")
                    print(f"     Status: {event.get('status', 'N/A')}")

                if len(data['events']) > 3:
                    print(f"\n  ... and {len(data['events']) - 3} more events")
            else:
                print(f"\nNo tracking events yet (label may be newly created)")

            # Save full response
            save_response(data, tracking_number)

            return data

        elif response.status_code == 401:
            print(f"ERROR 401 - Authentication Failed")
            print(f"Check your JWT token in environment variable FIRSTMILE_JWT_TOKEN")
            return None

        elif response.status_code == 404:
            print(f"ERROR 404 - Tracking Number Not Found")
            print(f"This tracking number may not exist or is not in the system yet")
            return None

        elif response.status_code == 400:
            print(f"ERROR 400 - Bad Request")
            print(f"Invalid tracking number format")
            return None

        else:
            print(f"ERROR {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return None

    except requests.exceptions.Timeout:
        print(f"ERROR - Request Timeout")
        print(f"API took too long to respond")
        return None

    except requests.exceptions.RequestException as e:
        print(f"ERROR - Request Failed: {str(e)}")
        return None

def save_response(data, tracking_number):
    """Save response to JSON file"""
    output_dir = 'tracking_responses'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{output_dir}/{tracking_number}_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nFull response saved to: {filename}")

def main():
    """Run batch test"""
    print("="*70)
    print("FirstMile Tracking API - Batch Test")
    print("="*70)
    print(f"\nEnvironment: PRODUCTION")
    print(f"URL: {BASE_URL}")
    print(f"JWT Token: {'SET' if JWT_TOKEN else 'NOT SET - Will test anyway'}")
    print(f"\nTesting {len(TRACKING_NUMBERS)} tracking numbers...\n")

    results = {
        'success': [],
        'failed': []
    }

    for i, tracking in enumerate(TRACKING_NUMBERS, 1):
        print(f"\n[{i}/{len(TRACKING_NUMBERS)}]")
        response = test_tracking(tracking)

        if response:
            results['success'].append(tracking)
        else:
            results['failed'].append(tracking)

    # Summary
    print("\n" + "="*70)
    print("BATCH TEST SUMMARY")
    print("="*70)
    print(f"\nSuccess: {len(results['success'])}/{len(TRACKING_NUMBERS)}")
    print(f"Failed: {len(results['failed'])}/{len(TRACKING_NUMBERS)}")

    if results['success']:
        print(f"\nSuccessful Lookups:")
        for tn in results['success']:
            print(f"  - {tn}")

    if results['failed']:
        print(f"\nFailed Lookups:")
        for tn in results['failed']:
            print(f"  - {tn}")

    print("\n" + "="*70)

if __name__ == "__main__":
    main()
