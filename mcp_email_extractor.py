#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Email Extractor - Superhuman Integration via Chrome MCP

Reads email data from superhuman_emails.json (extracted by Claude Code using Chrome MCP)
Returns structured JSON for sync reports.

Usage:
    python mcp_email_extractor.py

Output (JSON):
    {
        "success": true/false,
        "critical": ["email 1", "email 2"],
        "yesterday": ["email 1", "email 2"],
        "last_week": ["email 1", "email 2"],
        "error": null or "error message"
    }
"""

import sys
import json
import os
import io
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emoji support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Path to email data file (created by Claude Code using Chrome MCP)
EMAIL_DATA_FILE = Path(__file__).parent / "superhuman_emails.json"


def load_superhuman_emails():
    """
    Load email data from superhuman_emails.json

    This file is created/updated by Claude Code using Chrome MCP tools
    to extract real email data from Superhuman inbox.
    """

    result = {
        "success": False,
        "critical": [],
        "yesterday": [],
        "last_week": [],
        "error": None,
        "mode": "unknown"
    }

    try:
        # Check if email data file exists
        if not EMAIL_DATA_FILE.exists():
            result["error"] = f"Email data file not found: {EMAIL_DATA_FILE}"
            result["mode"] = "file_missing"
            return result

        # Load email data
        with open(EMAIL_DATA_FILE, 'r', encoding='utf-8') as f:
            email_data = json.load(f)

        # Check if data is stale (smart business hours logic)
        if "timestamp" in email_data:
            data_time = datetime.fromisoformat(email_data["timestamp"])
            now = datetime.now()
            age_hours = (now - data_time).total_seconds() / 3600

            # Smart staleness: Allow weekend-old data on Monday morning
            # Monday before noon: Accept Friday data (up to 72 hours)
            # Otherwise: Accept data from same business day (up to 24 hours)
            max_age_hours = 24
            if now.weekday() == 0 and now.hour < 12:  # Monday before noon
                max_age_hours = 72

            if age_hours > max_age_hours:
                result["error"] = f"Email data is stale ({age_hours:.1f} hours old). Run Chrome MCP extraction to update."
                result["mode"] = "stale"
                return result

        # Extract email lists
        result["critical"] = email_data.get("critical", [])
        result["yesterday"] = email_data.get("yesterday", [])
        result["last_week"] = email_data.get("last_week", [])
        result["mode"] = email_data.get("mode", "live")
        result["success"] = True

        return result

    except json.JSONDecodeError as e:
        result["error"] = f"Invalid JSON in email data file: {str(e)}"
        result["mode"] = "json_error"
        return result

    except Exception as e:
        result["error"] = f"Error loading email data: {str(e)}"
        result["mode"] = "error"
        return result


def main():
    """Main entry point - returns JSON only to stdout"""

    try:
        result = load_superhuman_emails()

        # Print ONLY JSON to stdout (this is what unified_sync.py will read)
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # Exit with appropriate code
        sys.exit(0 if result["success"] else 1)

    except Exception as e:
        # On catastrophic failure, return error JSON
        error_result = {
            "success": False,
            "critical": [],
            "yesterday": [],
            "last_week": [],
            "error": f"Fatal error in mcp_email_extractor: {str(e)}",
            "mode": "fatal_error"
        }

        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
