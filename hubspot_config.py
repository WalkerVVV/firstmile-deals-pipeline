#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Configuration Module
Centralized configuration for all HubSpot API scripts

Usage:
    from hubspot_config import get_hubspot_config

    config = get_hubspot_config()
    api_key = config['API_KEY']
    owner_id = config['OWNER_ID']
"""

import os

def get_hubspot_config():
    """
    Get HubSpot configuration from environment variables or defaults.

    Environment variables (recommended for security):
        HUBSPOT_API_KEY - Your HubSpot Private App access token
        HUBSPOT_OWNER_ID - Your HubSpot user ID (Brett Walker)
        HUBSPOT_PIPELINE_ID - The FM pipeline ID
        HUBSPOT_PORTAL_ID - Your HubSpot portal ID

    Returns:
        dict: Configuration dictionary with all HubSpot settings
    """
    return {
        'API_KEY': os.environ.get('HUBSPOT_API_KEY', 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'),
        'OWNER_ID': os.environ.get('HUBSPOT_OWNER_ID', '699257003'),
        'PIPELINE_ID': os.environ.get('HUBSPOT_PIPELINE_ID', '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'),
        'PORTAL_ID': os.environ.get('HUBSPOT_PORTAL_ID', '46526832'),
        'BASE_URL': 'https://api.hubapi.com',
    }

def get_api_headers(api_key=None):
    """
    Get standard API headers for HubSpot requests.

    Args:
        api_key (str, optional): API key to use. If None, loads from config.

    Returns:
        dict: Headers dictionary for requests
    """
    if api_key is None:
        config = get_hubspot_config()
        api_key = config['API_KEY']

    return {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

# Stage ID to Folder Name mapping (verified October 7, 2025)
STAGE_MAPPING = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-CLOSED-WON]",
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[08-CLOSED-LOST]"
}

# Reverse mapping (Folder name to Stage ID)
FOLDER_TO_STAGE_ID = {v: k for k, v in STAGE_MAPPING.items()}

# Association Type IDs (verified)
ASSOCIATION_IDS = {
    'CONTACT_TO_COMPANY': 279,
    'LEAD_TO_CONTACT': 608,  # REQUIRED
    'LEAD_TO_COMPANY': 610,
    'DEAL_TO_COMPANY': 341,
    'DEAL_TO_CONTACT': 3,
    'TASK_TO_DEAL': 216
}

if __name__ == '__main__':
    # Test configuration
    config = get_hubspot_config()
    print("HubSpot Configuration:")
    print(f"  Owner ID: {config['OWNER_ID']}")
    print(f"  Pipeline ID: {config['PIPELINE_ID']}")
    print(f"  Portal ID: {config['PORTAL_ID']}")
    print(f"  API Key: {config['API_KEY'][:20]}...{config['API_KEY'][-10:]}")
    print(f"\nStage Mapping: {len(STAGE_MAPPING)} stages")
    print(f"Association IDs: {len(ASSOCIATION_IDS)} types")
