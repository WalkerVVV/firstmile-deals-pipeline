"""
Configuration module for FirstMile Deals system.
Handles environment variables and application settings securely.
"""
import os
from pathlib import Path
from typing import Optional

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    # Load .env file from project root
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables only.")
    print("Install with: pip install python-dotenv")


class Config:
    """Configuration manager for FirstMile Deals system."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent
    DOWNLOADS_FOLDER = Path.home() / 'Downloads'

    # HubSpot Configuration
    HUBSPOT_API_KEY: str = os.environ.get('HUBSPOT_API_KEY', '')
    HUBSPOT_OWNER_ID: str = os.environ.get('HUBSPOT_OWNER_ID', '699257003')
    HUBSPOT_PIPELINE_ID: str = os.environ.get('HUBSPOT_PIPELINE_ID', '8bd9336b-4767-4e67-9fe2-35dfcad7c8be')
    HUBSPOT_PORTAL_ID: str = os.environ.get('HUBSPOT_PORTAL_ID', '46526832')

    # HubSpot API Configuration
    HUBSPOT_API_BASE_URL: str = 'https://api.hubapi.com'
    HUBSPOT_API_TIMEOUT: int = 30  # seconds
    HUBSPOT_RATE_LIMIT: int = 100  # requests per 10 seconds

    # Environment Settings
    ENVIRONMENT: str = os.environ.get('ENVIRONMENT', 'development')
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')

    # File Paths
    FIRSTMILE_DEALS_PATH: Path = Path(os.environ.get('FIRSTMILE_DEALS_PATH', PROJECT_ROOT))
    PIPELINE_TRACKER_PATH: Path = DOWNLOADS_FOLDER / '_PIPELINE_TRACKER.csv'
    DAILY_LOG_PATH: Path = DOWNLOADS_FOLDER / '_DAILY_LOG.md'
    FOLLOW_UP_REMINDERS_PATH: Path = DOWNLOADS_FOLDER / 'FOLLOW_UP_REMINDERS.txt'

    # HubSpot Stage Mapping (VERIFIED 2025-10-10)
    STAGE_MAP = {
        '1090865183': '[01-DISCOVERY-SCHEDULED]',
        'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
        'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
        'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
        '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
        '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
        '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',
        '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
    }

    # Reverse mapping for convenience
    STAGE_NAME_TO_ID = {v: k for k, v in STAGE_MAP.items()}

    # Hub Mapping (for geographic analysis)
    HUB_MAP = {
        "CA": "LAX - West Coast",
        "TX": "DFW - South Central",
        "FL": "MIA - Southeast",
        "NY": "JFK/EWR - Northeast",
        "IL": "ORD - Midwest",
        "GA": "ATL - Southeast",
        "WA": "SEA - Pacific Northwest",
        "PA": "PHL - Northeast",
        "OH": "CVG - Midwest",
        "NV": "LAS - Southwest"
    }

    # SLA Windows (in days)
    SLA_WINDOWS = {
        'Xparcel Priority': 3,
        'Xparcel Expedited': 5,
        'Xparcel Ground': 8
    }

    # Performance Thresholds
    PERFORMANCE_THRESHOLDS = {
        'perfect': 100.0,
        'exceeds': 95.0,
        'meets': 90.0,
        'below': 0.0
    }

    # FirstMile Brand Colors
    FIRSTMILE_BLUE = '#366092'
    FIRSTMILE_LIGHT_GRAY = '#DDDDDD'

    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration is present.

        Returns:
            bool: True if configuration is valid

        Raises:
            ValueError: If required configuration is missing
        """
        errors = []

        if not cls.HUBSPOT_API_KEY:
            errors.append("HUBSPOT_API_KEY is not set")
        elif cls.HUBSPOT_API_KEY == 'your_api_key_here':
            errors.append("HUBSPOT_API_KEY is still set to placeholder value")

        if not cls.HUBSPOT_OWNER_ID:
            errors.append("HUBSPOT_OWNER_ID is not set")

        if not cls.HUBSPOT_PIPELINE_ID:
            errors.append("HUBSPOT_PIPELINE_ID is not set")

        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            error_msg += "\n\nPlease ensure .env file exists with correct values."
            error_msg += "\nSee .env.example for template."
            raise ValueError(error_msg)

        return True

    @classmethod
    def get_stage_id(cls, stage_name: str) -> Optional[str]:
        """Get HubSpot stage ID from stage name."""
        return cls.STAGE_NAME_TO_ID.get(stage_name)

    @classmethod
    def get_stage_name(cls, stage_id: str) -> Optional[str]:
        """Get stage name from HubSpot stage ID."""
        return cls.STAGE_MAP.get(stage_id)

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENVIRONMENT.lower() == 'production'

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENVIRONMENT.lower() == 'development'


# Validate configuration on import (but allow import to succeed for setup scripts)
try:
    Config.validate()
except ValueError as e:
    if Config.ENVIRONMENT != 'setup':
        print(f"Warning: {e}")
        print("Some functionality may not work until configuration is fixed.")
