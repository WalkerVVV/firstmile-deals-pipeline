# HubSpot Sync Core Module - Usage Guide

**Version**: 1.0.0
**Created**: 2025-11-06
**Author**: Claude Code SuperClaude

---

## Overview

The `hubspot_sync_core.py` module provides centralized HubSpot API integration with advanced rate limiting and error handling for the FirstMile Deals system.

### Key Features

1. **Advanced Rate Limiting**
   - Token bucket algorithm implementation
   - Burst limiting: 100 requests per 10 seconds
   - Daily limiting: 150,000 requests per 24 hours
   - Automatic token refill and request queuing

2. **Error Handling**
   - Automatic retry with exponential backoff
   - HubSpot 429 rate limit detection and handling
   - Request timeout management
   - Comprehensive error logging

3. **Request Management**
   - Connection pooling via requests.Session
   - Thread-safe rate limiting
   - Request history tracking
   - Performance metrics and statistics

4. **Common Operations**
   - Deal CRUD operations (Create, Read, Update, Delete)
   - Contact management
   - Company creation
   - Note creation with associations

---

## Installation

### Prerequisites

```bash
# Required packages
pip install requests python-dotenv
```

### Configuration

Ensure your `.env` file contains the required HubSpot credentials:

```env
HUBSPOT_API_KEY=pat-na1-your-actual-token-here
HUBSPOT_OWNER_ID=699257003
HUBSPOT_PIPELINE_ID=8bd9336b-4767-4e67-9fe2-35dfcad7c8be
HUBSPOT_PORTAL_ID=46526832
```

**Important**: Never commit your `.env` file. The API key should be kept secure.

---

## Basic Usage

### Initialize the Manager

```python
from hubspot_sync_core import HubSpotSyncManager

# Initialize with automatic config loading from .env
sync_manager = HubSpotSyncManager()

# Or initialize with explicit credentials
sync_manager = HubSpotSyncManager(
    api_key="your-api-key",
    owner_id="699257003",
    pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
)
```

### Context Manager Pattern (Recommended)

```python
from hubspot_sync_core import HubSpotSyncManager

with HubSpotSyncManager() as sync:
    deals = sync.fetch_deals(limit=10)
    # Process deals...

# Rate limit statistics automatically logged on exit
```

---

## Deal Operations

### Fetch Deals

```python
# Fetch all deals in configured pipeline
deals = sync_manager.fetch_deals(limit=100)

# Fetch deals in specific stage
deals = sync_manager.fetch_deals(
    stage_id="1090865183",  # [01-DISCOVERY-SCHEDULED]
    limit=50
)

# Fetch with custom properties
deals = sync_manager.fetch_deals(
    properties=['dealname', 'amount', 'closedate', 'custom_property'],
    limit=100
)

# Process results
for deal in deals:
    deal_id = deal['id']
    props = deal['properties']
    print(f"Deal: {props.get('dealname')} - ${props.get('amount', 0)}")
```

### Get Single Deal

```python
# Get deal by ID
deal = sync_manager.get_deal(
    deal_id="12345678",
    properties=['dealname', 'amount', 'dealstage']
)

print(f"Deal Name: {deal['properties']['dealname']}")
print(f"Amount: ${deal['properties']['amount']}")
```

### Update Deal

```python
# Update deal properties
updated_deal = sync_manager.update_deal(
    deal_id="12345678",
    properties={
        'dealstage': 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',  # [04-PROPOSAL-SENT]
        'amount': 150000,
        'closedate': '2025-12-31'
    }
)

print(f"Updated: {updated_deal['properties']['dealname']}")
```

### Create Deal

```python
# Create new deal
new_deal = sync_manager.create_deal(
    properties={
        'dealname': 'Acme Corp - Xparcel Ground',
        'amount': 150000,
        'dealstage': '1090865183',  # [01-DISCOVERY-SCHEDULED]
        'pipeline': '8bd9336b-4767-4e67-9fe2-35dfcad7c8be',
        'closedate': '2025-12-31',
        'hubspot_owner_id': '699257003'
    }
)

print(f"Created deal ID: {new_deal['id']}")
```

---

## Contact Operations

### Create Contact

```python
# Create new contact (email required)
contact = sync_manager.create_contact({
    'email': 'john.smith@company.com',
    'firstname': 'John',
    'lastname': 'Smith',
    'company': 'Acme Corp',
    'phone': '555-1234',
    'jobtitle': 'Shipping Manager'
})

print(f"Created contact ID: {contact['id']}")
```

### Get Contact

```python
# Get contact by ID
contact = sync_manager.get_contact(
    contact_id="12345",
    properties=['firstname', 'lastname', 'email']
)

print(f"Contact: {contact['properties']['firstname']} {contact['properties']['lastname']}")
```

### Update Contact

```python
# Update contact properties
updated_contact = sync_manager.update_contact(
    contact_id="12345",
    properties={
        'phone': '555-5678',
        'jobtitle': 'Director of Shipping'
    }
)
```

---

## Company Operations

### Create Company

```python
# Create new company
company = sync_manager.create_company({
    'name': 'Acme Corporation',
    'domain': 'acme.com',
    'industry': 'eCommerce',
    'city': 'New York',
    'state': 'NY'
})

print(f"Created company ID: {company['id']}")
```

---

## Note Operations

### Create Note on Deal

```python
# Create note associated with deal
note = sync_manager.create_note(
    deal_id="12345678",
    note_body="<p>Discovery call completed. Customer interested in Xparcel Ground service.</p>"
)

print(f"Created note ID: {note['id']}")

# Create note with custom timestamp
import time
note = sync_manager.create_note(
    deal_id="12345678",
    note_body="<p>Follow-up scheduled for next week.</p>",
    timestamp=int(time.time() * 1000)  # Current time in milliseconds
)
```

---

## Rate Limiting

### Understanding Rate Limits

The module implements dual-tier rate limiting:

1. **Burst Limit**: 100 requests per 10 seconds
   - Prevents overwhelming the API with rapid requests
   - Automatically throttles when approaching limit

2. **Daily Limit**: 150,000 requests per 24 hours
   - Tracks total daily usage
   - Raises `RateLimitError` if exhausted

### Monitoring Rate Limits

```python
# Get current rate limit statistics
stats = sync_manager.get_rate_limit_stats()

print(f"Burst tokens available: {stats['burst_tokens_available']}/{stats['burst_capacity']}")
print(f"Burst utilization: {stats['burst_utilization']}")
print(f"Daily tokens available: {stats['daily_tokens_available']}/{stats['daily_capacity']}")
print(f"Daily utilization: {stats['daily_utilization']}")
print(f"Total requests made: {stats['total_requests']}")
print(f"Total wait time: {stats['total_wait_time']}")
print(f"Requests per minute: {stats['requests_per_minute']}")

# Log statistics
sync_manager.log_rate_limit_stats()
```

### Handling Rate Limit Errors

```python
from hubspot_sync_core import HubSpotSyncManager, RateLimitError

try:
    sync_manager = HubSpotSyncManager()
    deals = sync_manager.fetch_deals(limit=100)

except RateLimitError as e:
    print(f"Rate limit exhausted: {e}")
    # Wait or schedule for later

except HubSpotAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
    # Handle specific error
```

---

## Error Handling

### Exception Types

```python
from hubspot_sync_core import HubSpotAPIError, RateLimitError

try:
    sync_manager = HubSpotSyncManager()
    deal = sync_manager.get_deal("invalid_id")

except RateLimitError as e:
    # Daily rate limit exhausted
    print(f"Rate limit error: {e}")
    # Schedule retry for later

except HubSpotAPIError as e:
    # API errors (401, 404, 500, etc.)
    print(f"API error {e.status_code}: {e.message}")
    if e.status_code == 404:
        print("Deal not found")
    elif e.status_code == 401:
        print("Invalid API key")

except ValueError as e:
    # Configuration errors
    print(f"Configuration error: {e}")
```

### Automatic Retries

The module automatically retries failed requests with exponential backoff:

- **Max retries**: 3 attempts (configurable)
- **Backoff strategy**: 2^attempt seconds (1s, 2s, 4s)
- **Retry conditions**: Timeouts and 5xx server errors
- **No retry**: 4xx client errors (except 429 rate limit)

```python
# Customize retry behavior
response = sync_manager._make_request(
    method='GET',
    endpoint='/crm/v3/objects/deals/12345',
    max_retries=5  # Override default
)
```

---

## Utility Functions

### Days Since Date

```python
from hubspot_sync_core import days_since

# Calculate days since a date
days = days_since('2025-10-15T10:30:00Z')
print(f"Days since: {days}")

# Returns 999 for invalid/missing dates
days = days_since(None)  # Returns 999
days = days_since('invalid-date')  # Returns 999
```

### Format Currency

```python
from hubspot_sync_core import format_currency

# Format amounts as currency
print(format_currency(1500000))    # "$1.5M"
print(format_currency(15000))      # "$15.0K"
print(format_currency(150))        # "$150.00"
```

---

## Migration from Existing Code

### Before (hubspot_utils.py)

```python
from hubspot_utils import HubSpotClient

client = HubSpotClient()
deals = client.search_deals(
    filters=[{'propertyName': 'dealstage', 'operator': 'EQ', 'value': 'stage_id'}],
    properties=['dealname', 'amount'],
    limit=100
)
```

### After (hubspot_sync_core.py)

```python
from hubspot_sync_core import HubSpotSyncManager

sync = HubSpotSyncManager()
deals = sync.fetch_deals(stage_id='stage_id', limit=100)
# Simpler API with built-in rate limiting
```

---

## Best Practices

### 1. Use Context Manager

```python
# Recommended: Automatically logs statistics and closes session
with HubSpotSyncManager() as sync:
    deals = sync.fetch_deals()
    # Process deals...
```

### 2. Batch Operations

```python
# Group multiple operations together
with HubSpotSyncManager() as sync:
    # Fetch all data first
    deals = sync.fetch_deals(limit=100)
    contacts = [sync.get_contact(deal['properties']['contact_id']) for deal in deals]

    # Process locally (no API calls)
    # ...

    # Update in batch
    for deal, contact in zip(deals, contacts):
        sync.update_deal(deal['id'], {'custom_property': 'value'})
```

### 3. Monitor Rate Limits

```python
# Check rate limit status before large operations
stats = sync.get_rate_limit_stats()
if stats['daily_tokens_available'] < 1000:
    print("Warning: Low daily token count")
    # Consider deferring non-critical operations
```

### 4. Handle Errors Gracefully

```python
from hubspot_sync_core import HubSpotAPIError

def safe_update_deal(sync, deal_id, properties):
    """Safely update deal with error handling."""
    try:
        return sync.update_deal(deal_id, properties)
    except HubSpotAPIError as e:
        if e.status_code == 404:
            logger.warning(f"Deal {deal_id} not found")
        else:
            logger.error(f"Failed to update deal {deal_id}: {e}")
        return None
```

### 5. Log Important Operations

```python
import logging

# Enable debug logging for development
logging.getLogger('hubspot_sync').setLevel(logging.DEBUG)

# Use info logging for production
logging.getLogger('hubspot_sync').setLevel(logging.INFO)
```

---

## Performance Metrics

### Request Throughput

The rate limiter allows:
- **Burst**: 10 requests/second sustained
- **Daily**: ~1.7 requests/second average over 24 hours
- **Typical**: 5-8 requests/second with automatic throttling

### Request Latency

- **Local rate limit check**: <1ms
- **API call**: 100-500ms typical
- **Retry backoff**: 1s, 2s, 4s (exponential)
- **Rate limit wait**: Variable based on token availability

---

## Troubleshooting

### Issue: 401 Unauthorized

**Cause**: Invalid or expired API key

**Solution**:
1. Verify API key in `.env` file
2. Check key format: `pat-na1-...`
3. Regenerate key in HubSpot if expired

### Issue: 429 Rate Limit

**Cause**: Too many requests in short period

**Solution**:
- Module automatically handles 429 responses
- Waits for `Retry-After` header duration
- Check rate limit stats with `get_rate_limit_stats()`

### Issue: Connection Timeout

**Cause**: Network issues or slow HubSpot response

**Solution**:
- Module automatically retries (3 attempts default)
- Increase timeout: `HubSpotSyncManager(timeout=60)`
- Check network connectivity

### Issue: Daily Limit Exhausted

**Cause**: Made 150,000+ requests in 24 hours

**Solution**:
- Wait for daily reset (24 hours from first request)
- Optimize script to reduce API calls
- Implement caching for frequently accessed data

---

## Examples

### Daily Sync Script

```python
#!/usr/bin/env python3
"""Daily deal sync script using HubSpot Sync Core."""

from hubspot_sync_core import HubSpotSyncManager, format_currency
from datetime import datetime

def main():
    print(f"\n{'='*80}")
    print(f"Daily Deal Sync - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print(f"{'='*80}\n")

    with HubSpotSyncManager() as sync:
        # Fetch all active deals
        deals = sync.fetch_deals(limit=100)
        print(f"Fetched {len(deals)} active deals\n")

        # Group by stage
        by_stage = {}
        for deal in deals:
            stage = deal['properties'].get('dealstage', 'Unknown')
            by_stage.setdefault(stage, []).append(deal)

        # Report by stage
        for stage_id, stage_deals in by_stage.items():
            stage_name = Config.get_stage_name(stage_id) or stage_id
            total_value = sum(
                float(d['properties'].get('amount', 0))
                for d in stage_deals
            )
            print(f"{stage_name}: {len(stage_deals)} deals, {format_currency(total_value)}")

        print(f"\n{'='*80}")
        sync.log_rate_limit_stats()
        print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
```

### Update Deal Stages

```python
#!/usr/bin/env python3
"""Update deal stages based on age."""

from hubspot_sync_core import HubSpotSyncManager, days_since
from config import Config

def auto_advance_deals():
    """Automatically advance stagnant deals."""

    with HubSpotSyncManager() as sync:
        # Get deals in Discovery stage
        discovery_stage_id = Config.get_stage_id('[01-DISCOVERY-SCHEDULED]')
        deals = sync.fetch_deals(stage_id=discovery_stage_id)

        print(f"Checking {len(deals)} deals in Discovery stage...")

        for deal in deals:
            props = deal['properties']
            days_in_stage = days_since(props.get('createdate'))

            # If > 14 days, move to Discovery Complete
            if days_in_stage > 14:
                new_stage_id = Config.get_stage_id('[02-DISCOVERY-COMPLETE]')
                sync.update_deal(
                    deal_id=deal['id'],
                    properties={'dealstage': new_stage_id}
                )

                # Add note
                sync.create_note(
                    deal_id=deal['id'],
                    note_body=f"<p>Auto-advanced after {days_in_stage} days in Discovery.</p>"
                )

                print(f"  ✓ Advanced: {props.get('dealname')}")

if __name__ == '__main__':
    auto_advance_deals()
```

---

## API Reference

### HubSpotSyncManager

#### Constructor

```python
HubSpotSyncManager(
    api_key: Optional[str] = None,
    owner_id: Optional[str] = None,
    pipeline_id: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: int = 30
)
```

#### Methods

**Deal Operations**:
- `fetch_deals(pipeline_id, stage_id, properties, limit)` → List[Dict]
- `get_deal(deal_id, properties)` → Dict
- `update_deal(deal_id, properties)` → Dict
- `create_deal(properties, associations)` → Dict

**Contact Operations**:
- `create_contact(properties)` → Dict
- `get_contact(contact_id, properties)` → Dict
- `update_contact(contact_id, properties)` → Dict

**Company Operations**:
- `create_company(properties)` → Dict

**Note Operations**:
- `create_note(deal_id, note_body, timestamp)` → Dict

**Utility Methods**:
- `get_rate_limit_stats()` → Dict
- `log_rate_limit_stats()` → None

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review error logs in console output
3. Verify `.env` configuration
4. Consult HubSpot API documentation: https://developers.hubspot.com/docs/api/overview

---

## Changelog

### Version 1.0.0 (2025-11-06)
- Initial release
- Token bucket rate limiting (100/10s, 150K/day)
- Automatic retry with exponential backoff
- Deal, contact, company, and note operations
- Comprehensive error handling
- Performance metrics and logging
- Thread-safe implementation
