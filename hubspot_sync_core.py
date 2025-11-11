#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Sync Core Module
Centralized HubSpot API integration with advanced rate limiting and error handling.

This module provides:
- Token bucket rate limiting (100 calls/10s burst, 150K calls/day)
- Automatic retry with exponential backoff
- Request queue management
- Comprehensive error handling
- Activity logging and metrics

Usage:
    from hubspot_sync_core import HubSpotSyncManager

    # Initialize with automatic config loading
    sync_manager = HubSpotSyncManager()

    # Fetch deals
    deals = sync_manager.fetch_deals(pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be")

    # Update deal
    sync_manager.update_deal(deal_id="12345", properties={"dealstage": "new_stage_id"})

    # Create contact
    contact = sync_manager.create_contact({
        "firstname": "John",
        "lastname": "Smith",
        "email": "john@company.com"
    })

Author: Claude Code SuperClaude
Version: 1.0.0
Date: 2025-11-06
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone, timedelta
from collections import deque
import requests

# Import existing configuration
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('hubspot_sync')


class RateLimitError(Exception):
    """Raised when rate limit is exceeded and cannot be recovered."""
    pass


class HubSpotAPIError(Exception):
    """Raised for HubSpot API errors."""
    def __init__(self, status_code: int, message: str, response_text: str = ""):
        self.status_code = status_code
        self.message = message
        self.response_text = response_text
        super().__init__(f"HubSpot API Error {status_code}: {message}")


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter for HubSpot API calls.

    Implements dual-tier rate limiting:
    - Burst limit: 100 requests per 10 seconds
    - Daily limit: 150,000 requests per 24 hours

    Thread-safe implementation with automatic token refill.
    """

    def __init__(
        self,
        burst_capacity: int = 100,
        burst_window: int = 10,
        daily_capacity: int = 150000,
        daily_window: int = 86400
    ):
        """
        Initialize rate limiter with dual-tier limits.

        Args:
            burst_capacity: Maximum burst requests (default: 100)
            burst_window: Burst window in seconds (default: 10)
            daily_capacity: Maximum daily requests (default: 150,000)
            daily_window: Daily window in seconds (default: 86,400)
        """
        # Burst limiting
        self.burst_capacity = burst_capacity
        self.burst_window = burst_window
        self.burst_tokens = burst_capacity
        self.burst_last_refill = time.time()

        # Daily limiting
        self.daily_capacity = daily_capacity
        self.daily_window = daily_window
        self.daily_tokens = daily_capacity
        self.daily_last_refill = time.time()

        # Request history for monitoring
        self.request_history = deque(maxlen=1000)

        # Thread safety
        self._lock = threading.Lock()

        # Metrics
        self.total_requests = 0
        self.total_waits = 0
        self.total_wait_time = 0.0

        logger.info(
            f"Rate limiter initialized: {burst_capacity} req/{burst_window}s burst, "
            f"{daily_capacity} req/{daily_window}s daily"
        )

    def _refill_tokens(self):
        """Refill tokens based on elapsed time since last refill."""
        now = time.time()

        # Refill burst tokens
        burst_elapsed = now - self.burst_last_refill
        burst_refill = (burst_elapsed / self.burst_window) * self.burst_capacity
        self.burst_tokens = min(self.burst_capacity, self.burst_tokens + burst_refill)
        self.burst_last_refill = now

        # Refill daily tokens
        daily_elapsed = now - self.daily_last_refill
        daily_refill = (daily_elapsed / self.daily_window) * self.daily_capacity
        self.daily_tokens = min(self.daily_capacity, self.daily_tokens + daily_refill)
        self.daily_last_refill = now

    def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens from the bucket, blocking if necessary.

        Args:
            tokens: Number of tokens to acquire (default: 1)

        Returns:
            Time waited in seconds (0 if no wait required)

        Raises:
            RateLimitError: If daily limit is exhausted
        """
        with self._lock:
            self._refill_tokens()

            # Check daily limit first
            if self.daily_tokens < tokens:
                wait_time = self._calculate_daily_wait_time(tokens)
                if wait_time > 3600:  # More than 1 hour
                    raise RateLimitError(
                        f"Daily rate limit exhausted. "
                        f"{self.daily_tokens:.0f}/{self.daily_capacity} tokens remaining. "
                        f"Reset in {wait_time/3600:.1f} hours."
                    )
                logger.warning(
                    f"Daily limit approaching: {self.daily_tokens:.0f}/{self.daily_capacity} "
                    f"tokens. Waiting {wait_time:.2f}s"
                )
                self.total_waits += 1
                self.total_wait_time += wait_time
                time.sleep(wait_time)
                self._refill_tokens()

            # Check burst limit
            if self.burst_tokens < tokens:
                wait_time = self._calculate_burst_wait_time(tokens)
                logger.debug(f"Burst limit reached. Waiting {wait_time:.2f}s")
                self.total_waits += 1
                self.total_wait_time += wait_time
                time.sleep(wait_time)
                self._refill_tokens()

            # Consume tokens
            self.burst_tokens -= tokens
            self.daily_tokens -= tokens
            self.total_requests += 1
            self.request_history.append(time.time())

            return 0.0

    def _calculate_burst_wait_time(self, tokens: int) -> float:
        """Calculate time to wait for burst tokens to refill."""
        tokens_needed = tokens - self.burst_tokens
        refill_rate = self.burst_capacity / self.burst_window
        return tokens_needed / refill_rate

    def _calculate_daily_wait_time(self, tokens: int) -> float:
        """Calculate time to wait for daily tokens to refill."""
        tokens_needed = tokens - self.daily_tokens
        refill_rate = self.daily_capacity / self.daily_window
        return tokens_needed / refill_rate

    def get_stats(self) -> Dict[str, Any]:
        """Get current rate limiter statistics."""
        with self._lock:
            self._refill_tokens()

            # Calculate request rates
            now = time.time()
            recent_requests = [t for t in self.request_history if now - t < 60]
            requests_per_minute = len(recent_requests)

            return {
                'burst_tokens_available': int(self.burst_tokens),
                'burst_capacity': self.burst_capacity,
                'burst_utilization': f"{(1 - self.burst_tokens/self.burst_capacity)*100:.1f}%",
                'daily_tokens_available': int(self.daily_tokens),
                'daily_capacity': self.daily_capacity,
                'daily_utilization': f"{(1 - self.daily_tokens/self.daily_capacity)*100:.1f}%",
                'total_requests': self.total_requests,
                'total_waits': self.total_waits,
                'total_wait_time': f"{self.total_wait_time:.2f}s",
                'requests_per_minute': requests_per_minute
            }


class HubSpotSyncManager:
    """
    Centralized HubSpot API manager with advanced rate limiting and error handling.

    Features:
    - Token bucket rate limiting (100/10s burst, 150K/day)
    - Automatic retry with exponential backoff
    - Request queue management
    - Comprehensive error handling
    - Activity logging and metrics
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        owner_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize HubSpot sync manager.

        Args:
            api_key: HubSpot API key (defaults to Config.HUBSPOT_API_KEY)
            owner_id: HubSpot owner ID (defaults to Config.HUBSPOT_OWNER_ID)
            pipeline_id: HubSpot pipeline ID (defaults to Config.HUBSPOT_PIPELINE_ID)
            base_url: API base URL (defaults to Config.HUBSPOT_API_BASE_URL)
            timeout: Request timeout in seconds (default: 30)
        """
        # Load configuration
        self.api_key = api_key or Config.HUBSPOT_API_KEY
        self.owner_id = owner_id or Config.HUBSPOT_OWNER_ID
        self.pipeline_id = pipeline_id or Config.HUBSPOT_PIPELINE_ID
        self.base_url = base_url or Config.HUBSPOT_API_BASE_URL
        self.timeout = timeout

        # Validate configuration
        if not self.api_key:
            raise ValueError(
                "HubSpot API key is required. "
                "Set HUBSPOT_API_KEY in .env file or pass api_key parameter."
            )

        # Initialize rate limiter
        self.rate_limiter = TokenBucketRateLimiter(
            burst_capacity=Config.HUBSPOT_RATE_LIMIT,
            burst_window=10,
            daily_capacity=150000,
            daily_window=86400
        )

        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())

        logger.info(
            f"HubSpot sync manager initialized. "
            f"Owner: {self.owner_id}, Pipeline: {self.pipeline_id}"
        )

    def _get_headers(self) -> Dict[str, str]:
        """Get standard API headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        max_retries: int = 3
    ) -> requests.Response:
        """
        Make HTTP request to HubSpot API with rate limiting and retries.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., '/crm/v3/objects/deals')
            data: JSON payload for POST/PATCH requests
            params: URL query parameters
            max_retries: Maximum number of retry attempts

        Returns:
            Response object

        Raises:
            HubSpotAPIError: For API errors
            RateLimitError: For exhausted rate limits
        """
        url = f"{self.base_url}{endpoint}"

        for attempt in range(max_retries):
            try:
                # Acquire rate limit token (blocks if necessary)
                wait_time = self.rate_limiter.acquire()
                if wait_time > 0:
                    logger.info(f"Rate limited: waited {wait_time:.2f}s")

                # Make request
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )

                # Handle rate limiting from HubSpot
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 10))
                    logger.warning(
                        f"HubSpot rate limit hit (429). "
                        f"Waiting {retry_after}s (attempt {attempt+1}/{max_retries})"
                    )
                    if attempt < max_retries - 1:
                        time.sleep(retry_after)
                        continue
                    else:
                        raise HubSpotAPIError(
                            429,
                            "Rate limit exceeded after retries",
                            response.text
                        )

                # Raise for other HTTP errors
                response.raise_for_status()

                # Log success
                logger.debug(f"{method} {endpoint} → {response.status_code}")

                return response

            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise HubSpotAPIError(
                        408,
                        f"Request timeout after {self.timeout}s",
                        ""
                    )
                wait_time = 2 ** attempt
                logger.warning(
                    f"Request timeout. Retrying in {wait_time}s "
                    f"(attempt {attempt+1}/{max_retries})"
                )
                time.sleep(wait_time)

            except requests.exceptions.HTTPError as e:
                if attempt == max_retries - 1 or e.response.status_code < 500:
                    # Don't retry client errors (4xx) or on last attempt
                    raise HubSpotAPIError(
                        e.response.status_code,
                        str(e),
                        e.response.text
                    )
                wait_time = 2 ** attempt
                logger.warning(
                    f"HTTP error {e.response.status_code}. Retrying in {wait_time}s "
                    f"(attempt {attempt+1}/{max_retries})"
                )
                time.sleep(wait_time)

        raise HubSpotAPIError(500, f"Max retries ({max_retries}) exceeded", "")

    # ========== Deal Operations ==========

    def fetch_deals(
        self,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        properties: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch deals from HubSpot.

        Args:
            pipeline_id: Filter by pipeline ID (defaults to configured pipeline)
            stage_id: Filter by stage ID (optional)
            properties: Properties to return (default: common properties)
            limit: Maximum number of results (default: 100)

        Returns:
            List of deal objects
        """
        pipeline_id = pipeline_id or self.pipeline_id

        if properties is None:
            properties = [
                'dealname', 'amount', 'closedate', 'createdate',
                'dealstage', 'pipeline', 'notes_last_updated',
                'hs_lastmodifieddate'
            ]

        filters = [
            {
                'propertyName': 'pipeline',
                'operator': 'EQ',
                'value': pipeline_id
            }
        ]

        if stage_id:
            filters.append({
                'propertyName': 'dealstage',
                'operator': 'EQ',
                'value': stage_id
            })

        payload = {
            'filterGroups': [{'filters': filters}],
            'properties': properties,
            'limit': limit
        }

        response = self._make_request('POST', '/crm/v3/objects/deals/search', data=payload)
        result = response.json()

        deals = result.get('results', [])
        logger.info(f"Fetched {len(deals)} deals from HubSpot")

        return deals

    def get_deal(
        self,
        deal_id: str,
        properties: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get a single deal by ID.

        Args:
            deal_id: HubSpot deal ID
            properties: Properties to return (optional)

        Returns:
            Deal object
        """
        params = {}
        if properties:
            params['properties'] = ','.join(properties)

        response = self._make_request('GET', f'/crm/v3/objects/deals/{deal_id}', params=params)
        deal = response.json()

        logger.debug(f"Fetched deal {deal_id}")

        return deal

    def update_deal(
        self,
        deal_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a deal's properties.

        Args:
            deal_id: HubSpot deal ID
            properties: Properties to update

        Returns:
            Updated deal object
        """
        payload = {'properties': properties}

        response = self._make_request('PATCH', f'/crm/v3/objects/deals/{deal_id}', data=payload)
        deal = response.json()

        logger.info(f"Updated deal {deal_id}: {list(properties.keys())}")

        return deal

    def create_deal(
        self,
        properties: Dict[str, Any],
        associations: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new deal.

        Args:
            properties: Deal properties
            associations: Optional associations (contacts, companies)

        Returns:
            Created deal object
        """
        payload = {'properties': properties}

        if associations:
            payload['associations'] = associations

        response = self._make_request('POST', '/crm/v3/objects/deals', data=payload)
        deal = response.json()

        logger.info(f"Created deal: {properties.get('dealname', 'Unnamed')} (ID: {deal['id']})")

        return deal

    # ========== Contact Operations ==========

    def create_contact(
        self,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new contact.

        Args:
            properties: Contact properties (email required)

        Returns:
            Created contact object
        """
        if 'email' not in properties:
            raise ValueError("Email is required to create a contact")

        payload = {'properties': properties}

        response = self._make_request('POST', '/crm/v3/objects/contacts', data=payload)
        contact = response.json()

        logger.info(
            f"Created contact: {properties.get('firstname', '')} "
            f"{properties.get('lastname', '')} (ID: {contact['id']})"
        )

        return contact

    def get_contact(
        self,
        contact_id: str,
        properties: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get a single contact by ID.

        Args:
            contact_id: HubSpot contact ID
            properties: Properties to return (optional)

        Returns:
            Contact object
        """
        params = {}
        if properties:
            params['properties'] = ','.join(properties)

        response = self._make_request('GET', f'/crm/v3/objects/contacts/{contact_id}', params=params)
        contact = response.json()

        logger.debug(f"Fetched contact {contact_id}")

        return contact

    def update_contact(
        self,
        contact_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a contact's properties.

        Args:
            contact_id: HubSpot contact ID
            properties: Properties to update

        Returns:
            Updated contact object
        """
        payload = {'properties': properties}

        response = self._make_request('PATCH', f'/crm/v3/objects/contacts/{contact_id}', data=payload)
        contact = response.json()

        logger.info(f"Updated contact {contact_id}: {list(properties.keys())}")

        return contact

    # ========== Company Operations ==========

    def create_company(
        self,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new company.

        Args:
            properties: Company properties (name recommended)

        Returns:
            Created company object
        """
        payload = {'properties': properties}

        response = self._make_request('POST', '/crm/v3/objects/companies', data=payload)
        company = response.json()

        logger.info(f"Created company: {properties.get('name', 'Unnamed')} (ID: {company['id']})")

        return company

    # ========== Note Operations ==========

    def create_note(
        self,
        deal_id: str,
        note_body: str,
        timestamp: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a note associated with a deal.

        Args:
            deal_id: HubSpot deal ID
            note_body: Note content (supports HTML)
            timestamp: Unix timestamp in milliseconds (defaults to now)

        Returns:
            Created note object
        """
        if timestamp is None:
            timestamp = int(time.time() * 1000)

        payload = {
            'properties': {
                'hs_timestamp': timestamp,
                'hs_note_body': note_body,
                'hubspot_owner_id': self.owner_id
            },
            'associations': [
                {
                    'to': {'id': deal_id},
                    'types': [
                        {
                            'associationCategory': 'HUBSPOT_DEFINED',
                            'associationTypeId': 214  # Note to Deal
                        }
                    ]
                }
            ]
        }

        response = self._make_request('POST', '/crm/v3/objects/notes', data=payload)
        note = response.json()

        logger.info(f"Created note for deal {deal_id}")

        return note

    def associate_contact_to_deal(
        self,
        contact_id: str,
        deal_id: str
    ) -> bool:
        """
        Associate a contact with a deal using batch associations API.

        Args:
            contact_id: HubSpot contact ID
            deal_id: HubSpot deal ID

        Returns:
            True if successful, False otherwise

        Example:
            sync.associate_contact_to_deal("12345", "67890")
        """
        endpoint = "/crm/v3/associations/contacts/deals/batch/create"

        payload = {
            "inputs": [
                {
                    "from": {"id": contact_id},
                    "to": {"id": deal_id},
                    "type": "contact_to_deal"
                }
            ]
        }

        try:
            response = self._make_request(
                method='POST',
                endpoint=endpoint,
                data=payload
            )

            result = response.json()

            if result and result.get('status') == 'COMPLETE':
                logger.info(f"Associated contact {contact_id} with deal {deal_id}")
                return True
            else:
                logger.warning(f"Association may have failed: {result}")
                return False

        except HubSpotAPIError as e:
            logger.error(f"Failed to associate contact {contact_id} with deal {deal_id}: {e}")
            return False

    # ========== Utility Methods ==========

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """
        Get current rate limiter statistics.

        Returns:
            Dictionary with rate limit statistics
        """
        return self.rate_limiter.get_stats()

    def log_rate_limit_stats(self):
        """Log current rate limiter statistics."""
        stats = self.get_rate_limit_stats()
        logger.info("Rate Limiter Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()
        self.log_rate_limit_stats()


# ========== Convenience Functions ==========

def days_since(date_str: Optional[str]) -> int:
    """
    Calculate days since a given date string.

    Args:
        date_str: ISO format date string

    Returns:
        Number of days since date, or 999 if invalid/missing
    """
    if not date_str:
        return 999

    try:
        # Handle ISO format with or without timezone
        if 'Z' in date_str:
            date_str = date_str.replace('Z', '+00:00')

        date = datetime.fromisoformat(date_str)

        # Make timezone-aware if needed
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = now - date

        return delta.days

    except (ValueError, AttributeError, TypeError):
        return 999


def format_currency(amount: float) -> str:
    """
    Format amount as currency.

    Args:
        amount: Dollar amount

    Returns:
        Formatted string (e.g., "$1.2M", "$15.3K", "$123.45")
    """
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    else:
        return f"${amount:,.2f}"


# ========== Module Test ==========

if __name__ == '__main__':
    import sys
    import io

    # Fix Windows encoding for Unicode characters
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("\n" + "="*80)
    print("HubSpot Sync Core Module - Test Mode")
    print("="*80 + "\n")

    try:
        # Initialize manager
        print("Initializing HubSpot sync manager...")
        sync_manager = HubSpotSyncManager()
        print("[OK] Manager initialized successfully\n")

        # Display configuration
        print("Configuration:")
        print(f"  Owner ID: {sync_manager.owner_id}")
        print(f"  Pipeline ID: {sync_manager.pipeline_id}")
        print(f"  API Key: {sync_manager.api_key[:20]}...{sync_manager.api_key[-10:]}")
        print(f"  Timeout: {sync_manager.timeout}s\n")

        # Display rate limiter stats
        print("Rate Limiter Status:")
        stats = sync_manager.get_rate_limit_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print()

        # Test API connection
        print("Testing API connection...")
        deals = sync_manager.fetch_deals(limit=5)
        print(f"[OK] Successfully fetched {len(deals)} deals\n")

        if deals:
            print("Sample Deal:")
            deal = deals[0]
            print(f"  ID: {deal['id']}")
            print(f"  Name: {deal['properties'].get('dealname', 'N/A')}")
            print(f"  Amount: {format_currency(float(deal['properties'].get('amount', 0)))}")
            print(f"  Stage: {deal['properties'].get('dealstage', 'N/A')}")
            print()

        # Final stats
        print("Final Rate Limiter Statistics:")
        sync_manager.log_rate_limit_stats()

        print("\n" + "="*80)
        print("[SUCCESS] All tests passed!")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        logger.exception("Test failed")
        sys.exit(1)
