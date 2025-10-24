"""
Shared HubSpot API utilities for FirstMile Deals system.
Provides centralized API client with error handling, retries, and rate limiting.
"""
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from config import Config


class HubSpotError(Exception):
    """Base exception for HubSpot API errors."""
    pass


class HubSpotAPIError(HubSpotError):
    """Exception for HubSpot API HTTP errors."""
    def __init__(self, status_code: int, message: str, response_text: str = ""):
        self.status_code = status_code
        self.message = message
        self.response_text = response_text
        super().__init__(f"HubSpot API Error {status_code}: {message}")


class HubSpotRateLimitError(HubSpotError):
    """Exception for HubSpot rate limit exceeded."""
    pass


class HubSpotClient:
    """
    Centralized HubSpot API client with error handling and best practices.

    Features:
    - Automatic retries with exponential backoff
    - Rate limiting protection
    - Standardized error handling
    - Request/response logging
    - Timeout management
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize HubSpot client.

        Args:
            api_key: HubSpot API key (defaults to Config.HUBSPOT_API_KEY)
        """
        self.api_key = api_key or Config.HUBSPOT_API_KEY
        if not self.api_key:
            raise ValueError("HubSpot API key is required. Set HUBSPOT_API_KEY in .env file.")

        self.base_url = Config.HUBSPOT_API_BASE_URL
        self.timeout = Config.HUBSPOT_API_TIMEOUT
        self.owner_id = Config.HUBSPOT_OWNER_ID
        self.pipeline_id = Config.HUBSPOT_PIPELINE_ID

        # Rate limiting state
        self._request_times: List[float] = []
        self._rate_limit = Config.HUBSPOT_RATE_LIMIT
        self._rate_limit_window = 10  # seconds

    def _get_headers(self) -> Dict[str, str]:
        """Get standard API headers."""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _check_rate_limit(self):
        """Enforce rate limiting to avoid HubSpot API limits."""
        now = time.time()

        # Remove requests older than rate limit window
        self._request_times = [t for t in self._request_times if now - t < self._rate_limit_window]

        # Check if we're at the limit
        if len(self._request_times) >= self._rate_limit:
            # Calculate how long to wait
            oldest_request = self._request_times[0]
            wait_time = self._rate_limit_window - (now - oldest_request)
            if wait_time > 0:
                print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                # Clear old requests after waiting
                now = time.time()
                self._request_times = [t for t in self._request_times if now - t < self._rate_limit_window]

        # Record this request
        self._request_times.append(now)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        max_retries: int = 3
    ) -> requests.Response:
        """
        Make HTTP request to HubSpot API with retries and error handling.

        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            endpoint: API endpoint (e.g., '/crm/v3/objects/deals')
            data: JSON payload for POST/PATCH requests
            params: URL query parameters
            max_retries: Maximum number of retry attempts

        Returns:
            requests.Response object

        Raises:
            HubSpotAPIError: For HTTP errors
            HubSpotRateLimitError: For rate limit errors
            requests.exceptions.Timeout: For timeout errors
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        for attempt in range(max_retries):
            try:
                # Check rate limit before making request
                self._check_rate_limit()

                # Make request
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                    timeout=self.timeout
                )

                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', 10))
                    print(f"Rate limited by HubSpot. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                # Raise for other HTTP errors
                response.raise_for_status()

                return response

            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    raise
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request timeout. Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)

            except requests.exceptions.HTTPError as e:
                if attempt == max_retries - 1 or e.response.status_code < 500:
                    # Don't retry client errors (4xx) or on last attempt
                    raise HubSpotAPIError(
                        status_code=e.response.status_code,
                        message=str(e),
                        response_text=e.response.text
                    )
                wait_time = 2 ** attempt
                print(f"HTTP error {e.response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        raise HubSpotError(f"Max retries ({max_retries}) exceeded")

    def search_deals(
        self,
        filters: List[Dict],
        properties: List[str],
        limit: int = 100,
        sorts: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Search for deals using HubSpot Search API.

        Args:
            filters: List of filter dictionaries
            properties: List of properties to return
            limit: Maximum number of results
            sorts: Optional list of sort criteria

        Returns:
            API response with deals

        Example:
            filters = [
                {
                    'propertyName': 'dealstage',
                    'operator': 'EQ',
                    'value': '1090865183'
                }
            ]
            properties = ['dealname', 'amount', 'closedate']
            deals = client.search_deals(filters, properties)
        """
        payload = {
            'filterGroups': [{'filters': filters}],
            'properties': properties,
            'limit': limit
        }

        if sorts:
            payload['sorts'] = sorts

        response = self._make_request('POST', '/crm/v3/objects/deals/search', data=payload)
        return response.json()

    def get_deal(self, deal_id: str, properties: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get a single deal by ID.

        Args:
            deal_id: HubSpot deal ID
            properties: Optional list of properties to return

        Returns:
            Deal data
        """
        params = {}
        if properties:
            params['properties'] = ','.join(properties)

        response = self._make_request('GET', f'/crm/v3/objects/deals/{deal_id}', params=params)
        return response.json()

    def update_deal(self, deal_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a deal's properties.

        Args:
            deal_id: HubSpot deal ID
            properties: Dictionary of properties to update

        Returns:
            Updated deal data
        """
        payload = {'properties': properties}
        response = self._make_request('PATCH', f'/crm/v3/objects/deals/{deal_id}', data=payload)
        return response.json()

    def create_deal(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new deal.

        Args:
            properties: Dictionary of deal properties

        Returns:
            Created deal data
        """
        payload = {'properties': properties}
        response = self._make_request('POST', '/crm/v3/objects/deals', data=payload)
        return response.json()

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
            Created note data
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
                            'associationTypeId': 214
                        }
                    ]
                }
            ]
        }

        response = self._make_request('POST', '/crm/v3/objects/notes', data=payload)
        return response.json()

    def get_pipeline_stages(self, pipeline_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get pipeline configuration including stages.

        Args:
            pipeline_id: Pipeline ID (defaults to Config.HUBSPOT_PIPELINE_ID)

        Returns:
            Pipeline configuration
        """
        pipeline_id = pipeline_id or self.pipeline_id
        response = self._make_request('GET', f'/crm/v3/pipelines/deals/{pipeline_id}')
        return response.json()

    def get_deals_by_stage(
        self,
        stage_id: str,
        properties: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get all deals in a specific stage.

        Args:
            stage_id: HubSpot stage ID
            properties: Optional list of properties to return
            limit: Maximum number of results

        Returns:
            List of deals
        """
        if properties is None:
            properties = ['dealname', 'amount', 'closedate', 'createdate', 'notes_last_updated']

        filters = [
            {
                'propertyName': 'dealstage',
                'operator': 'EQ',
                'value': stage_id
            },
            {
                'propertyName': 'pipeline',
                'operator': 'EQ',
                'value': self.pipeline_id
            }
        ]

        result = self.search_deals(filters, properties, limit)
        return result.get('results', [])


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
        Formatted string (e.g., "$1,234.56")
    """
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    else:
        return f"${amount:,.2f}"


def get_status_emoji(days: int, threshold: int) -> str:
    """
    Get status emoji based on days and threshold.

    Args:
        days: Number of days
        threshold: Threshold for warning

    Returns:
        Status emoji
    """
    if days > threshold * 2:
        return '🔴'
    elif days > threshold:
        return '🟡'
    else:
        return '🟢'
