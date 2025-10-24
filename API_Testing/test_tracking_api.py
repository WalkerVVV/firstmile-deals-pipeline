"""
FirstMile Tracking API - Interactive Testing Script
===================================================

This script allows you to test the FirstMile Tracking API with real tracking numbers.

Usage:
    python test_tracking_api.py

Requirements:
    pip install requests python-dotenv
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. Set JWT_TOKEN environment variable manually.")


class FirstMileTrackingTester:
    """Interactive tester for FirstMile Tracking API"""

    def __init__(self, jwt_token=None, environment='test'):
        self.jwt_token = jwt_token or os.getenv('FIRSTMILE_JWT_TOKEN')

        if not self.jwt_token:
            print("\n⚠️  WARNING: No JWT token found!")
            print("   Set FIRSTMILE_JWT_TOKEN environment variable or create .env file")
            print("   Example: FIRSTMILE_JWT_TOKEN=your_token_here\n")

        # Set base URL based on environment
        if environment == 'production':
            self.base_url = "https://trackingapi.firstmile.com"
            self.env_name = "🔴 PRODUCTION"
        elif environment == 'test':
            self.base_url = "https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net"
            self.env_name = "🟢 TEST"
        elif environment == 'mock':
            self.base_url = "https://acilogistix.redocly.app/_mock/xmethod/tracking/swagger"
            self.env_name = "🔵 MOCK"
        else:
            raise ValueError("Environment must be 'production', 'test', or 'mock'")

        self.environment = environment

    def test_connection(self):
        """Test if API is reachable"""
        print(f"\n🔍 Testing connection to {self.env_name} environment...")
        print(f"   URL: {self.base_url}")

        try:
            # Try a simple request (will fail auth, but tests connection)
            response = requests.get(f"{self.base_url}/Tracking/v1/TEST", timeout=10)
            print(f"✅ API is reachable (Status: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot reach API: {str(e)}")
            return False

    def get_tracking(self, tracking_number, tech_partner_id=None, verbose=True):
        """
        Get tracking information for a shipment

        Args:
            tracking_number (str): The tracking number to look up
            tech_partner_id (str, optional): TechPartnerId if provided
            verbose (bool): Print detailed output

        Returns:
            dict: Tracking response data or None if failed
        """
        url = f"{self.base_url}/Tracking/v1/{tracking_number}"

        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Accept": "application/json"
        }

        params = {}
        if tech_partner_id:
            params['TechPartnerId'] = tech_partner_id

        if verbose:
            print(f"\n📦 Looking up tracking number: {tracking_number}")
            print(f"   Environment: {self.env_name}")

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if verbose:
                    self._print_tracking_summary(data)
                return data

            elif response.status_code == 401:
                print(f"❌ Authentication failed (401)")
                print(f"   Check your JWT token")
                return None

            elif response.status_code == 404:
                print(f"❌ Tracking number not found (404)")
                print(f"   Tracking number may not exist or not yet in system")
                return None

            elif response.status_code == 400:
                print(f"❌ Invalid request (400)")
                print(f"   Check tracking number format")
                return None

            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            print(f"❌ Request timeout - API took too long to respond")
            return None

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            return None

    def _print_tracking_summary(self, data):
        """Print formatted tracking summary"""
        print(f"\n{'='*70}")
        print(f"✅ TRACKING FOUND: {data['trackingNumber']}")
        print(f"{'='*70}")

        # Basic info
        print(f"\n📋 SHIPMENT DETAILS:")
        print(f"   Carrier: {data.get('carrier', 'N/A')}")
        print(f"   Service Level: {data.get('serviceLevel', 'N/A')}")
        print(f"   Weight: {data.get('weightLbs', 'N/A')} lbs")
        print(f"   Processed Date: {self._format_date(data.get('processedDate'))}")

        # Airway bill (international)
        if data.get('airwayBill'):
            print(f"   Airway Bill: {data['airwayBill']} (International)")

        # Delivery estimates
        if data.get('deliveryDateEstimated'):
            print(f"\n📅 DELIVERY ESTIMATES:")
            print(f"   Estimated: {data.get('deliveryDateEstimated')}")
            print(f"   Min Date: {data.get('deliveryDateMin', 'N/A')}")
            print(f"   Max Date (SLA): {data.get('deliveryDateMax', 'N/A')}")

        # Address
        if data.get('shipmentAddress'):
            addr = data['shipmentAddress']
            print(f"\n📍 DESTINATION:")
            if addr.get('companyName'):
                print(f"   Company: {addr['companyName']}")
            print(f"   Name: {addr.get('name', 'N/A')}")
            print(f"   Address: {addr.get('address1', 'N/A')}")
            if addr.get('address2'):
                print(f"            {addr['address2']}")
            print(f"   City: {addr.get('city', 'N/A')}, {addr.get('regionCode', 'N/A')} {addr.get('countryCode', 'N/A')}")
            print(f"   Type: {'Residential' if addr.get('residential') else 'Commercial'}")

        # Events
        if data.get('events'):
            print(f"\n🚚 TRACKING EVENTS ({len(data['events'])} total):")
            for i, event in enumerate(data['events'][:10], 1):  # Show first 10
                status_icon = self._get_status_icon(event.get('status'))
                print(f"\n   {i}. {status_icon} {event.get('eventType', 'Unknown Event')}")
                print(f"      Date: {self._format_date(event.get('eventDate'))}")
                print(f"      Location: {event.get('location', 'N/A')}")
                print(f"      Status: {event.get('status', 'N/A')}")
                if event.get('description'):
                    print(f"      Description: {event['description']}")
                if event.get('carrierCode'):
                    print(f"      Carrier: {event['carrierCode']}")

            if len(data['events']) > 10:
                print(f"\n   ... and {len(data['events']) - 10} more events")
        else:
            print(f"\n🚚 TRACKING EVENTS: No events recorded yet")

        # POD
        if data.get('podImageURLSBase64') and len(data['podImageURLSBase64']) > 0:
            print(f"\n📸 PROOF OF DELIVERY: {len(data['podImageURLSBase64'])} image(s) available")

        # Errors
        if data.get('errors') and len(data['errors']) > 0:
            print(f"\n⚠️  ERRORS:")
            for error in data['errors']:
                print(f"   • {error.get('errorCode', 'N/A')}: {error.get('errorMessage', 'N/A')}")

        # Tracking URL
        if data.get('trackingURL'):
            print(f"\n🔗 TRACKING URL: {data['trackingURL']}")

        print(f"\n{'='*70}\n")

    def _get_status_icon(self, status):
        """Get emoji icon for status"""
        status_lower = (status or '').lower()
        if 'delivered' in status_lower:
            return '✅'
        elif 'transit' in status_lower:
            return '🚚'
        elif 'exception' in status_lower:
            return '⚠️'
        elif 'returned' in status_lower:
            return '↩️'
        else:
            return '📦'

    def _format_date(self, date_str):
        """Format ISO date string to readable format"""
        if not date_str:
            return 'N/A'
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %I:%M %p %Z')
        except:
            return date_str

    def save_response(self, data, tracking_number):
        """Save API response to JSON file"""
        output_dir = Path('tracking_responses')
        output_dir.mkdir(exist_ok=True)

        filename = output_dir / f"{tracking_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Response saved to: {filename}")
        return filename

    def interactive_mode(self):
        """Run interactive testing session"""
        print("\n" + "="*70)
        print("🚀 FirstMile Tracking API - Interactive Tester")
        print("="*70)
        print(f"\nEnvironment: {self.env_name}")
        print(f"Base URL: {self.base_url}")
        print(f"JWT Token: {'✅ Set' if self.jwt_token else '❌ Not Set'}")

        # Test connection
        if not self.test_connection():
            print("\n⚠️  Cannot proceed - API not reachable")
            return

        print("\n" + "-"*70)
        print("Enter tracking numbers to test (or 'q' to quit)")
        print("Commands:")
        print("  • Enter tracking number to look up")
        print("  • 's' to save last response to file")
        print("  • 'e' to switch environment")
        print("  • 'q' to quit")
        print("-"*70)

        last_response = None
        last_tracking = None

        while True:
            try:
                user_input = input("\n📦 Tracking Number: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'q':
                    print("\n👋 Goodbye!")
                    break

                if user_input.lower() == 's':
                    if last_response and last_tracking:
                        self.save_response(last_response, last_tracking)
                    else:
                        print("❌ No response to save - look up a tracking number first")
                    continue

                if user_input.lower() == 'e':
                    print("\nSwitch to which environment?")
                    print("  1. Test (default)")
                    print("  2. Production")
                    print("  3. Mock")
                    choice = input("Choice (1-3): ").strip()

                    env_map = {'1': 'test', '2': 'production', '3': 'mock'}
                    new_env = env_map.get(choice, 'test')

                    self.__init__(self.jwt_token, new_env)
                    print(f"\n✅ Switched to {self.env_name}")
                    continue

                # Look up tracking number
                response = self.get_tracking(user_input)

                if response:
                    last_response = response
                    last_tracking = user_input

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted - Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    def batch_test(self, tracking_numbers):
        """Test multiple tracking numbers"""
        print(f"\n🔄 Batch Testing {len(tracking_numbers)} Tracking Numbers")
        print(f"   Environment: {self.env_name}\n")

        results = {
            'success': [],
            'not_found': [],
            'errors': []
        }

        for i, tracking in enumerate(tracking_numbers, 1):
            print(f"[{i}/{len(tracking_numbers)}] Testing {tracking}...")

            response = self.get_tracking(tracking, verbose=False)

            if response:
                status = 'Unknown'
                if response.get('events'):
                    status = response['events'][0].get('status', 'Unknown')

                results['success'].append({
                    'tracking': tracking,
                    'status': status,
                    'service_level': response.get('serviceLevel'),
                    'carrier': response.get('carrier')
                })
                print(f"   ✅ Found - Status: {status}")
            else:
                results['not_found'].append(tracking)
                print(f"   ❌ Not found or error")

        # Print summary
        print(f"\n{'='*70}")
        print(f"📊 BATCH TEST SUMMARY")
        print(f"{'='*70}")
        print(f"✅ Success: {len(results['success'])}")
        print(f"❌ Not Found: {len(results['not_found'])}")
        print(f"⚠️  Errors: {len(results['errors'])}")

        if results['success']:
            print(f"\n✅ SUCCESSFUL LOOKUPS:")
            for r in results['success']:
                print(f"   • {r['tracking']}: {r['status']} ({r['service_level']})")

        return results


def main():
    """Main entry point"""
    import sys

    # Check for command line arguments
    if len(sys.argv) > 1:
        # Batch mode with tracking numbers from command line
        tracking_numbers = sys.argv[1:]
        tester = FirstMileTrackingTester(environment='test')
        tester.batch_test(tracking_numbers)
    else:
        # Interactive mode
        tester = FirstMileTrackingTester(environment='test')
        tester.interactive_mode()


if __name__ == "__main__":
    main()
