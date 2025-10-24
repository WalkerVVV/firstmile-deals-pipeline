# FirstMile REST Tracking API - Complete Reference Guide

**Version:** 1.0
**Documentation Generated:** 2025-10-09
**API Provider:** FirstMile/FASTGroup/ACI Logistics

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Base URLs & Environments](#base-urls--environments)
4. [Core Endpoint](#core-endpoint)
5. [Request Structure](#request-structure)
6. [Response Structure](#response-structure)
7. [Data Models & Schemas](#data-models--schemas)
8. [Error Handling](#error-handling)
9. [Service Levels](#service-levels)
10. [Delivery Estimates](#delivery-estimates)
11. [Event Types & Tracking](#event-types--tracking)
12. [Address Structure](#address-structure)
13. [Proof of Delivery (POD)](#proof-of-delivery-pod)
14. [Code Examples](#code-examples)
15. [Best Practices](#best-practices)
16. [Integration Checklist](#integration-checklist)

---

## API Overview

The FirstMile REST Tracking API provides real-time shipment tracking information through a simple RESTful interface. This API allows you to:

- Retrieve detailed tracking events for shipments
- Access delivery estimates and SLA windows
- View shipment addresses and package details
- Download proof of delivery images
- Monitor carrier routing and status
- Track both domestic and international shipments

**Key Features:**
- Bearer token authentication (JWT)
- RESTful architecture
- JSON response format
- Support for Xparcel service levels (Ground, Expedited, Priority)
- International tracking via DHL Airway Bills
- Proof of delivery image retrieval

---

## Authentication

### Security Scheme

**Type:** Bearer Token (JWT)

**Header Format:**
```
Authorization: Bearer <YOUR_JWT_TOKEN>
```

**Example:**
```bash
curl -i -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

**Authentication Notes:**
- JWT tokens must be obtained from FirstMile's authentication service (separate endpoint)
- Tokens typically expire after a set period (check with FirstMile for specifics)
- Include the full "Bearer " prefix in the Authorization header
- Unauthorized requests return HTTP 401

---

## Base URLs & Environments

### Production Environment
```
https://trackingapi.firstmile.com/
```
**Use for:** Live production tracking queries

### Test Environment
```
https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net/
```
**Use for:** Development and testing integration

### Mock Server
```
https://acilogistix.redocly.app/_mock/xmethod/tracking/swagger/
```
**Use for:** API exploration and schema validation (no authentication required)

---

## Core Endpoint

### GET /Tracking/v1/{trackingNumber}

**Description:** Retrieves detailed tracking events and shipment information for the provided tracking number.

**Method:** GET

**Path Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `trackingNumber` | string | Yes | The tracking number to retrieve information for | `123456789` |

**Query Parameters:**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `TechPartnerId` | string | No | Optional TechPartnerId supplied by FirstMile | `partner-123` |

**Full URL Examples:**

```
Production:
https://trackingapi.firstmile.com/Tracking/v1/123456789

Test:
https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net/Tracking/v1/123456789

With TechPartnerId:
https://trackingapi.firstmile.com/Tracking/v1/123456789?TechPartnerId=partner-123
```

---

## Request Structure

### Complete Request Example

```bash
curl -i -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789?TechPartnerId=string' \
  -H 'Authorization: Bearer <YOUR_JWT_HERE>'
```

### Request Headers

| Header | Required | Value | Description |
|--------|----------|-------|-------------|
| `Authorization` | Yes | `Bearer <token>` | JWT authentication token |
| `Accept` | No | `application/json` | Preferred response format (default: JSON) |
| `Content-Type` | No | `application/json` | Not required for GET requests |

---

## Response Structure

### HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| **200** | Success | Tracking information successfully retrieved |
| **400** | Bad Request | Invalid tracking number format or missing required parameters |
| **401** | Unauthorized | Missing or invalid authentication token |
| **404** | Not Found | Tracking number not found in system |
| **500** | Server Error | Internal server error occurred |

### Response Content Types

The API supports multiple response formats:
- `application/json` (default)
- `text/json`
- `text/plain`

### Success Response (HTTP 200)

**Complete Response Structure:**

```json
{
  "trackingNumber": "123456789",
  "airwayBill": "AWB987654321",
  "shipmentAddress": {
    "companyName": "FirstMile Inc.",
    "name": "John Doe",
    "address1": "123 Main St",
    "address2": "Suite 100",
    "address3": null,
    "city": "Salt Lake City",
    "region": "Utah",
    "regionCode": "UT",
    "country": "United States",
    "countryCode": "US",
    "email": "john.doe@example.com",
    "phoneNumber": "+1-555-1234",
    "residential": false,
    "residentialSpecified": true,
    "deliveryPoint": "Front Door"
  },
  "weightLbs": 2.5,
  "processedDate": "2023-08-01T10:00:00Z",
  "events": [
    {
      "eventType": "Label Created",
      "eventDate": "2023-08-01T10:00:00Z",
      "location": "Salt Lake City, UT",
      "description": "Shipping label created",
      "carrierCode": "USPS",
      "scanType": "ORIGIN",
      "latitude": 40.7608,
      "longitude": -111.8910,
      "status": "In Transit"
    },
    {
      "eventType": "Package Delivered",
      "eventDate": "2023-08-05T14:30:00Z",
      "location": "New York, NY",
      "description": "Package delivered to recipient",
      "carrierCode": "USPS",
      "scanType": "DELIVERY",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "status": "Delivered"
    }
  ],
  "errors": [],
  "carrier": "FirstMile",
  "trackingURL": "https://trackingapi.firstmile.com/track/123456789",
  "deliveryDateEstimated": "2023-08-05",
  "deliveryDateMax": "2023-08-07",
  "deliveryDateMin": "2023-08-04",
  "podImageURLSBase64": [],
  "serviceLevel": "Ground"
}
```

---

## Data Models & Schemas

### Root Response Object

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| `trackingNumber` | string | Yes | No | The tracking number the information is for |
| `airwayBill` | string | No | Yes | The Airway Bill for international shipments (DHL) |
| `shipmentAddress` | [Address](#address-object) | Yes | No | Destination address information |
| `weightLbs` | number(double) | Yes | No | The weight of the shipment in pounds |
| `processedDate` | string(date-time) | Yes | No | The processed date of the shipment (ISO 8601) |
| `events` | [TrackingEvent](#trackingevent-object)[] | No | Yes | Array of detailed tracking events |
| `errors` | [TrackingError](#trackingerror-object)[] | No | Yes | Array of error information if any |
| `carrier` | string | No | Yes | Carrier responsible for the shipment |
| `trackingURL` | string | No | Yes | URL to view tracking information |
| `deliveryDateEstimated` | string | No | Yes | Estimated delivery date (YYYY-MM-DD) |
| `deliveryDateMax` | string | No | Yes | Maximum expected delivery date |
| `deliveryDateMin` | string | No | Yes | Minimum expected delivery date |
| `podImageURLSBase64` | string[] | No | Yes | List of base64-encoded URLs for POD images |
| `serviceLevel` | string | No | Yes | Service level (enum: "Ground", "Expedited", "Priority") |

---

## Address Structure

### Address Object

The `shipmentAddress` object contains complete destination information.

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| `companyName` | string | No | Yes | Company or business name |
| `name` | string | Yes | No | Recipient name |
| `address1` | string | Yes | No | Primary address line (street number and name) |
| `address2` | string | No | Yes | Secondary address line (suite, apt, unit) |
| `address3` | string | No | Yes | Third address line (rarely used) |
| `city` | string | Yes | No | City name |
| `region` | string | Yes | No | State or region full name |
| `regionCode` | string | Yes | No | State or region code (e.g., "UT", "CA") |
| `country` | string | Yes | No | Country full name |
| `countryCode` | string | Yes | No | ISO country code (e.g., "US", "CA") |
| `email` | string | No | Yes | Recipient email address |
| `phoneNumber` | string | No | Yes | Recipient phone number with country code |
| `residential` | boolean | Yes | No | Whether address is residential (true) or commercial (false) |
| `residentialSpecified` | boolean | Yes | No | Whether residential flag was explicitly set |
| `deliveryPoint` | string | No | Yes | Specific delivery location (e.g., "Front Door", "Lobby") |

**Example:**
```json
{
  "companyName": "FirstMile Inc.",
  "name": "John Doe",
  "address1": "123 Main St",
  "address2": "Suite 100",
  "address3": null,
  "city": "Salt Lake City",
  "region": "Utah",
  "regionCode": "UT",
  "country": "United States",
  "countryCode": "US",
  "email": "john.doe@example.com",
  "phoneNumber": "+1-555-1234",
  "residential": false,
  "residentialSpecified": true,
  "deliveryPoint": "Front Door"
}
```

---

## Event Types & Tracking

### TrackingEvent Object

Each event in the `events` array represents a scan or status update in the shipment journey.

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| `eventType` | string | Yes | No | Type of tracking event (e.g., "Label Created", "In Transit", "Delivered") |
| `eventDate` | string(date-time) | Yes | No | ISO 8601 timestamp of the event |
| `location` | string | No | Yes | City, State where event occurred |
| `description` | string | No | Yes | Human-readable description of the event |
| `carrierCode` | string | No | Yes | Carrier code responsible for this leg (e.g., "USPS", "UPS", "FEDEX") |
| `scanType` | string | No | Yes | Type of scan (e.g., "ORIGIN", "TRANSIT", "DELIVERY") |
| `latitude` | number(double) | No | Yes | Geographic latitude of event location |
| `longitude` | number(double) | No | Yes | Geographic longitude of event location |
| `status` | string | Yes | No | Current status (e.g., "In Transit", "Delivered", "Exception") |

**Common Event Types:**

| Event Type | Description | Scan Type |
|------------|-------------|-----------|
| Label Created | Shipping label generated | ORIGIN |
| Picked Up | Package picked up from shipper | ORIGIN |
| Accepted at FirstMile | Package received at FirstMile facility | ORIGIN |
| In Transit | Package moving through network | TRANSIT |
| Out for Delivery | Package on delivery vehicle | DELIVERY |
| Delivered | Package delivered to recipient | DELIVERY |
| Delivery Attempted | Delivery attempt unsuccessful | DELIVERY |
| Exception | Issue requiring attention | EXCEPTION |
| Returned to Sender | Package being returned | RETURN |

**Example Events Array:**
```json
"events": [
  {
    "eventType": "Label Created",
    "eventDate": "2023-08-01T10:00:00Z",
    "location": "Salt Lake City, UT",
    "description": "Shipping label created",
    "carrierCode": "USPS",
    "scanType": "ORIGIN",
    "latitude": 40.7608,
    "longitude": -111.8910,
    "status": "In Transit"
  },
  {
    "eventType": "In Transit",
    "eventDate": "2023-08-02T08:15:00Z",
    "location": "Chicago, IL",
    "description": "Package in transit to destination",
    "carrierCode": "USPS",
    "scanType": "TRANSIT",
    "latitude": 41.8781,
    "longitude": -87.6298,
    "status": "In Transit"
  },
  {
    "eventType": "Out for Delivery",
    "eventDate": "2023-08-05T09:00:00Z",
    "location": "New York, NY",
    "description": "Package out for delivery",
    "carrierCode": "USPS",
    "scanType": "DELIVERY",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "status": "Out for Delivery"
  },
  {
    "eventType": "Delivered",
    "eventDate": "2023-08-05T14:30:00Z",
    "location": "New York, NY",
    "description": "Package delivered to recipient",
    "carrierCode": "USPS",
    "scanType": "DELIVERY",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "status": "Delivered"
  }
]
```

---

## Error Handling

### TrackingError Object

Errors encountered during tracking lookups are returned in the `errors` array.

| Field | Type | Required | Nullable | Description |
|-------|------|----------|----------|-------------|
| `errorCode` | string | Yes | No | Machine-readable error code |
| `errorMessage` | string | Yes | No | Human-readable error description |

**Common Error Scenarios:**

| HTTP Status | Error Code | Error Message | Cause |
|-------------|------------|---------------|-------|
| 400 | INVALID_TRACKING_NUMBER | Invalid tracking number format | Malformed tracking number |
| 401 | UNAUTHORIZED | Authentication required | Missing or invalid JWT token |
| 404 | TRACKING_NOT_FOUND | Tracking number not found | Number doesn't exist in system |
| 404 | NO_TRACKING_DATA | No tracking data available yet | Label created but not scanned |
| 500 | INTERNAL_ERROR | Internal server error | System error |
| 500 | CARRIER_TIMEOUT | Carrier system timeout | Downstream carrier API unavailable |

**Error Response Example:**
```json
{
  "trackingNumber": "123456789",
  "errors": [
    {
      "errorCode": "NO_TRACKING_DATA",
      "errorMessage": "Tracking label created but no carrier scans available yet"
    }
  ],
  "events": [],
  "carrier": "FirstMile",
  "processedDate": "2023-08-01T10:00:00Z"
}
```

**HTTP Error Response Example (404):**
```json
{
  "status": 404,
  "title": "Not Found",
  "detail": "Tracking number not found in system",
  "instance": "/Tracking/v1/999999999"
}
```

---

## Service Levels

### ServiceLevel Enum

FirstMile offers three Xparcel service levels with different delivery windows.

| Service Level | SLA Window | Description | Use Case |
|--------------|------------|-------------|----------|
| **Ground** | 3-8 days | Economy ground service | Standard eCommerce shipments |
| **Expedited** | 2-5 days | Faster ground service (1-20 lb) | Time-sensitive packages |
| **Priority** | 1-3 days | Premium with money-back guarantee | Critical shipments |

**Response Field:**
```json
"serviceLevel": "Ground"
```

**Possible Values:**
- `"Ground"`
- `"Expedited"`
- `"Priority"` (may appear as "Direct Call" in some data sources)
- `null` (if service level not specified)

**Service Level Mapping:**

When processing tracking data, you may encounter variations:

| API Value | Display As | SLA Window |
|-----------|-----------|------------|
| `"Ground"` | Xparcel Ground | 3-8 days |
| `"Expedited"` | Xparcel Expedited | 2-5 days |
| `"Priority"` or `"Direct Call"` | Xparcel Priority | 1-3 days |

---

## Delivery Estimates

### Delivery Date Fields

The API provides three delivery date estimates to help set customer expectations.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `deliveryDateEstimated` | string | Most likely delivery date | `"2023-08-05"` |
| `deliveryDateMin` | string | Earliest possible delivery | `"2023-08-04"` |
| `deliveryDateMax` | string | Latest expected delivery (SLA) | `"2023-08-07"` |

**Date Format:** YYYY-MM-DD (ISO 8601 date string)

**Example:**
```json
{
  "deliveryDateEstimated": "2023-08-05",
  "deliveryDateMax": "2023-08-07",
  "deliveryDateMin": "2023-08-04",
  "serviceLevel": "Ground"
}
```

**Calculation Logic:**

- **Ground (3-8 day):**
  - Min: processedDate + 3 business days
  - Estimated: processedDate + 5 business days
  - Max: processedDate + 8 business days

- **Expedited (2-5 day):**
  - Min: processedDate + 2 business days
  - Estimated: processedDate + 3 business days
  - Max: processedDate + 5 business days

- **Priority (1-3 day):**
  - Min: processedDate + 1 business day
  - Estimated: processedDate + 2 business days
  - Max: processedDate + 3 business days

**SLA Compliance:**

A shipment is considered **within SLA** if delivered on or before `deliveryDateMax`.

---

## Proof of Delivery (POD)

### POD Image URLs

Proof of delivery images are provided as base64-encoded URLs for security.

**Field:**
```json
"podImageURLSBase64": [
  "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAABaA..."
]
```

**Characteristics:**

- **Type:** Array of strings
- **Format:** Base64-encoded image data URLs
- **Image Formats:** JPEG, PNG
- **Nullable:** Yes (may be empty array if no POD available)
- **Availability:** Typically populated 1-24 hours after delivery

**POD Availability:**

| Delivery Status | POD Available | Notes |
|----------------|---------------|-------|
| Delivered | Usually yes | May take 1-24 hours to appear |
| In Transit | No | Not yet delivered |
| Out for Delivery | No | Delivery in progress |
| Delivery Attempted | Sometimes | If signature/photo was attempted |
| Exception | No | Delivery not completed |

**Decoding POD Images:**

```python
import base64
from io import BytesIO
from PIL import Image

# Assuming pod_url is from podImageURLSBase64 array
pod_url = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD..."

# Extract base64 data (remove prefix)
header, encoded = pod_url.split(",", 1)
image_data = base64.b64decode(encoded)

# Save to file
with open("pod_image.jpg", "wb") as f:
    f.write(image_data)

# Or open in memory
image = Image.open(BytesIO(image_data))
image.show()
```

---

## Code Examples

### Python Example

```python
import requests
import json
from datetime import datetime

class FirstMileTrackingAPI:
    def __init__(self, jwt_token, environment='production'):
        self.jwt_token = jwt_token

        if environment == 'production':
            self.base_url = "https://trackingapi.firstmile.com"
        elif environment == 'test':
            self.base_url = "https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net"
        else:
            raise ValueError("Environment must be 'production' or 'test'")

    def get_tracking(self, tracking_number, tech_partner_id=None):
        """
        Get tracking information for a shipment

        Args:
            tracking_number (str): The tracking number to look up
            tech_partner_id (str, optional): TechPartnerId if provided by FirstMile

        Returns:
            dict: Tracking response data
        """
        url = f"{self.base_url}/Tracking/v1/{tracking_number}"

        headers = {
            "Authorization": f"Bearer {self.jwt_token}",
            "Accept": "application/json"
        }

        params = {}
        if tech_partner_id:
            params['TechPartnerId'] = tech_partner_id

        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Check your JWT token.")
            elif response.status_code == 404:
                raise Exception(f"Tracking number {tracking_number} not found.")
            elif response.status_code == 400:
                raise Exception(f"Invalid tracking number format: {tracking_number}")
            else:
                raise Exception(f"HTTP Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

    def get_delivery_status(self, tracking_number):
        """
        Get simple delivery status for a tracking number

        Returns:
            dict: Simplified status information
        """
        data = self.get_tracking(tracking_number)

        # Get most recent event
        latest_event = data['events'][0] if data.get('events') else None

        return {
            'tracking_number': data['trackingNumber'],
            'status': latest_event['status'] if latest_event else 'Unknown',
            'service_level': data.get('serviceLevel'),
            'estimated_delivery': data.get('deliveryDateEstimated'),
            'last_event': latest_event['eventType'] if latest_event else None,
            'last_location': latest_event['location'] if latest_event else None,
            'last_update': latest_event['eventDate'] if latest_event else None,
            'carrier': data.get('carrier'),
            'has_pod': len(data.get('podImageURLSBase64', [])) > 0
        }

    def is_delivered(self, tracking_number):
        """
        Check if shipment has been delivered

        Returns:
            bool: True if delivered, False otherwise
        """
        status = self.get_delivery_status(tracking_number)
        return status['status'] == 'Delivered'

    def get_transit_days(self, tracking_number):
        """
        Calculate days in transit

        Returns:
            int: Number of days between processed date and delivery (or today)
        """
        data = self.get_tracking(tracking_number)

        processed_date = datetime.fromisoformat(data['processedDate'].replace('Z', '+00:00'))

        # Check if delivered
        delivered_event = None
        for event in data.get('events', []):
            if event['status'] == 'Delivered':
                delivered_event = event
                break

        if delivered_event:
            end_date = datetime.fromisoformat(delivered_event['eventDate'].replace('Z', '+00:00'))
        else:
            end_date = datetime.now(processed_date.tzinfo)

        return (end_date - processed_date).days


# Usage Example
if __name__ == "__main__":
    # Initialize API client
    api = FirstMileTrackingAPI(
        jwt_token="your_jwt_token_here",
        environment='production'
    )

    # Get full tracking data
    tracking_data = api.get_tracking("123456789")
    print(json.dumps(tracking_data, indent=2))

    # Get simplified status
    status = api.get_delivery_status("123456789")
    print(f"Status: {status['status']}")
    print(f"Estimated Delivery: {status['estimated_delivery']}")

    # Check if delivered
    if api.is_delivered("123456789"):
        print("Package has been delivered!")

    # Get transit time
    days = api.get_transit_days("123456789")
    print(f"Days in transit: {days}")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

class FirstMileTrackingAPI {
  constructor(jwtToken, environment = 'production') {
    this.jwtToken = jwtToken;

    if (environment === 'production') {
      this.baseUrl = 'https://trackingapi.firstmile.com';
    } else if (environment === 'test') {
      this.baseUrl = 'https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net';
    } else {
      throw new Error("Environment must be 'production' or 'test'");
    }
  }

  async getTracking(trackingNumber, techPartnerId = null) {
    const url = `${this.baseUrl}/Tracking/v1/${trackingNumber}`;

    const config = {
      headers: {
        'Authorization': `Bearer ${this.jwtToken}`,
        'Accept': 'application/json'
      },
      params: techPartnerId ? { TechPartnerId: techPartnerId } : {},
      timeout: 30000
    };

    try {
      const response = await axios.get(url, config);
      return response.data;

    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          throw new Error('Authentication failed. Check your JWT token.');
        } else if (error.response.status === 404) {
          throw new Error(`Tracking number ${trackingNumber} not found.`);
        } else if (error.response.status === 400) {
          throw new Error(`Invalid tracking number format: ${trackingNumber}`);
        } else {
          throw new Error(`HTTP Error: ${error.response.status} - ${error.response.data}`);
        }
      } else {
        throw new Error(`Request failed: ${error.message}`);
      }
    }
  }

  async getDeliveryStatus(trackingNumber) {
    const data = await this.getTracking(trackingNumber);

    const latestEvent = data.events && data.events.length > 0 ? data.events[0] : null;

    return {
      trackingNumber: data.trackingNumber,
      status: latestEvent ? latestEvent.status : 'Unknown',
      serviceLevel: data.serviceLevel,
      estimatedDelivery: data.deliveryDateEstimated,
      lastEvent: latestEvent ? latestEvent.eventType : null,
      lastLocation: latestEvent ? latestEvent.location : null,
      lastUpdate: latestEvent ? latestEvent.eventDate : null,
      carrier: data.carrier,
      hasPod: data.podImageURLSBase64 && data.podImageURLSBase64.length > 0
    };
  }

  async isDelivered(trackingNumber) {
    const status = await this.getDeliveryStatus(trackingNumber);
    return status.status === 'Delivered';
  }
}

// Usage Example
(async () => {
  const api = new FirstMileTrackingAPI('your_jwt_token_here', 'production');

  try {
    // Get full tracking data
    const trackingData = await api.getTracking('123456789');
    console.log(JSON.stringify(trackingData, null, 2));

    // Get simplified status
    const status = await api.getDeliveryStatus('123456789');
    console.log(`Status: ${status.status}`);
    console.log(`Estimated Delivery: ${status.estimatedDelivery}`);

    // Check if delivered
    if (await api.isDelivered('123456789')) {
      console.log('Package has been delivered!');
    }

  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

### cURL Examples

```bash
# Basic tracking query (production)
curl -i -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'

# With TechPartnerId parameter
curl -i -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789?TechPartnerId=partner-123' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'

# Test environment
curl -i -X GET \
  'https://tracking-rest-api-test-dzfbetgsepgkfrh5.westus-01.azurewebsites.net/Tracking/v1/123456789' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN'

# Pretty print JSON response
curl -s -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' | jq '.'

# Extract just the status from latest event
curl -s -X GET \
  'https://trackingapi.firstmile.com/Tracking/v1/123456789' \
  -H 'Authorization: Bearer YOUR_JWT_TOKEN' | jq -r '.events[0].status'
```

---

## Best Practices

### 1. Authentication Management

**Do:**
- Cache JWT tokens and reuse them until expiration
- Implement token refresh logic before expiration
- Store tokens securely (environment variables, secrets manager)

**Don't:**
- Include tokens in version control
- Log full tokens in application logs
- Request new tokens for every API call

### 2. Error Handling

**Implement Retry Logic:**
```python
import time

def get_tracking_with_retry(api, tracking_number, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api.get_tracking(tracking_number)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            if "500" in str(e) or "timeout" in str(e).lower():
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                raise
```

**Handle All Status Codes:**
- 200: Success - process normally
- 400: Validation error - check tracking number format
- 401: Auth error - refresh token and retry
- 404: Not found - inform user, don't retry
- 500: Server error - retry with backoff

### 3. Rate Limiting

**Recommended Practices:**
- Implement exponential backoff for retries
- Batch tracking lookups when possible
- Cache results for repeated lookups (5-15 min TTL)
- Respect any rate limit headers returned by API

### 4. Data Validation

**Always Validate:**
```python
def validate_tracking_response(data):
    """Validate required fields are present"""
    required_fields = ['trackingNumber', 'processedDate', 'weightLbs']

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate date format
    try:
        datetime.fromisoformat(data['processedDate'].replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f"Invalid processedDate format: {data['processedDate']}")

    return True
```

### 5. Event Processing

**Sort Events Chronologically:**
```python
def sort_events(data):
    """Sort events from oldest to newest"""
    if data.get('events'):
        data['events'].sort(
            key=lambda e: datetime.fromisoformat(e['eventDate'].replace('Z', '+00:00'))
        )
    return data
```

**Identify Delivery Event:**
```python
def get_delivery_event(events):
    """Find the delivery event in event list"""
    for event in reversed(events):  # Start from most recent
        if event['eventType'] in ['Delivered', 'Package Delivered']:
            return event
    return None
```

### 6. Performance Optimization

**Batch Processing:**
```python
import asyncio
import aiohttp

async def fetch_tracking(session, tracking_number, jwt_token):
    url = f"https://trackingapi.firstmile.com/Tracking/v1/{tracking_number}"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    async with session.get(url, headers=headers) as response:
        return await response.json()

async def batch_tracking_lookup(tracking_numbers, jwt_token):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_tracking(session, tn, jwt_token) for tn in tracking_numbers]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
results = asyncio.run(batch_tracking_lookup(['123', '456', '789'], 'token'))
```

### 7. Logging

**Structured Logging:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def track_with_logging(api, tracking_number):
    logger.info(f"Fetching tracking for: {tracking_number}")

    try:
        data = api.get_tracking(tracking_number)
        logger.info(f"Successfully retrieved tracking for {tracking_number}, status: {data['events'][0]['status']}")
        return data

    except Exception as e:
        logger.error(f"Failed to fetch tracking for {tracking_number}: {str(e)}")
        raise
```

---

## Integration Checklist

### Pre-Integration

- [ ] Obtain JWT authentication token from FirstMile
- [ ] Verify access to test environment
- [ ] Review API documentation and data models
- [ ] Understand service level SLA windows
- [ ] Identify required tracking data fields for your use case

### Development

- [ ] Implement authentication with Bearer token
- [ ] Build tracking lookup function with error handling
- [ ] Implement retry logic with exponential backoff
- [ ] Add input validation for tracking numbers
- [ ] Parse and store tracking events
- [ ] Extract delivery status and estimates
- [ ] Handle POD images if needed
- [ ] Implement response caching
- [ ] Add comprehensive logging

### Testing

- [ ] Test with valid tracking numbers in test environment
- [ ] Test with invalid tracking numbers (verify 404 handling)
- [ ] Test with malformed requests (verify 400 handling)
- [ ] Test authentication failures (verify 401 handling)
- [ ] Test timeout scenarios
- [ ] Verify event sorting and processing
- [ ] Test delivery date calculations
- [ ] Load test with multiple concurrent requests
- [ ] Verify POD image decoding

### Production

- [ ] Switch to production base URL
- [ ] Verify production authentication credentials
- [ ] Implement monitoring and alerting
- [ ] Set up error tracking (Sentry, Rollbar, etc.)
- [ ] Configure rate limiting and throttling
- [ ] Enable response caching
- [ ] Document API usage for team
- [ ] Create runbook for common issues

### Monitoring

- [ ] Track API response times
- [ ] Monitor error rates by status code
- [ ] Alert on authentication failures
- [ ] Track tracking number not found rate
- [ ] Monitor POD image availability
- [ ] Measure delivery estimate accuracy
- [ ] Track SLA compliance based on delivery dates

---

## Appendix A: Tracking Number Formats

FirstMile and carrier partners use various tracking number formats:

| Carrier | Format | Example | Length |
|---------|--------|---------|--------|
| USPS | 22 digits | 9400111899563512345678 | 20-22 |
| UPS | 1Z format | 1Z999AA10123456784 | 18 |
| FedEx | 12-15 digits | 986578902637 | 12-15 |
| DHL | 10-11 digits | 1234567890 | 10-11 |
| FirstMile | Various | FM123456789 | Varies |

**Validation Regex Examples:**

```python
import re

TRACKING_PATTERNS = {
    'USPS': re.compile(r'^\d{20,22}$'),
    'UPS': re.compile(r'^1Z[A-Z0-9]{16}$'),
    'FEDEX': re.compile(r'^\d{12,15}$'),
    'DHL': re.compile(r'^\d{10,11}$'),
}

def identify_carrier(tracking_number):
    """Identify carrier from tracking number format"""
    for carrier, pattern in TRACKING_PATTERNS.items():
        if pattern.match(tracking_number):
            return carrier
    return 'UNKNOWN'
```

---

## Appendix B: Time Zones & Date Handling

**ISO 8601 Format:**
All timestamps use ISO 8601 format with UTC timezone:
```
2023-08-01T10:00:00Z
```

**Python Parsing:**
```python
from datetime import datetime

# Parse ISO 8601 string
date_str = "2023-08-01T10:00:00Z"
dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

# Convert to local timezone
import pytz
local_tz = pytz.timezone('America/New_York')
local_dt = dt.astimezone(local_tz)
```

**JavaScript Parsing:**
```javascript
const dateStr = "2023-08-01T10:00:00Z";
const date = new Date(dateStr);

// Format for display
console.log(date.toLocaleString()); // Local timezone
console.log(date.toISOString());    // UTC
```

---

## Appendix C: Contact & Support

**FirstMile Support:**
- API Documentation: https://acilogistix.redocly.app/xmethod/tracking/swagger/tracking
- Technical Support: [Contact FirstMile for support details]
- API Access Requests: [Contact FirstMile sales/onboarding]

**Common Support Requests:**
1. JWT token generation and refresh
2. Rate limit increases
3. TechPartnerId provisioning
4. Production access credentials
5. Webhook notifications (if available)
6. Custom integration requirements

---

## Appendix D: Frequently Asked Questions

### Q: How often is tracking data updated?
**A:** Tracking data is updated in real-time as carriers scan packages. There may be delays of 15 minutes to several hours depending on carrier integration.

### Q: What should I do if a tracking number returns 404?
**A:** Verify the tracking number format. If correct, the label may have been created but not yet scanned by the carrier. Wait 24-48 hours and retry.

### Q: How long are tracking records retained?
**A:** Contact FirstMile for specific retention policies. Typically 90-365 days after delivery.

### Q: Can I get webhook notifications instead of polling?
**A:** Contact FirstMile to inquire about webhook/push notification options for real-time updates.

### Q: What's the difference between `carrier` and `carrierCode` fields?
**A:** `carrier` (root level) is the overall responsible carrier (usually "FirstMile"). `carrierCode` (in events) indicates which carrier performed each specific scan.

### Q: How accurate are delivery estimates?
**A:** Delivery estimates are based on service level SLAs and historical performance. Actual delivery depends on weather, carrier capacity, and destination accessibility.

### Q: Can I track international shipments?
**A:** Yes. International shipments will include an `airwayBill` field (typically DHL) for downstream tracking.

### Q: What if events array is empty?
**A:** An empty events array means the label was created but no carrier scans have occurred yet. Check the `processedDate` - if recent (< 24 hours), this is normal.

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-09 | Initial comprehensive API guide created |

---

**END OF DOCUMENT**
