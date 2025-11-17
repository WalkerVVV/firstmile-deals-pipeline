#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action prioritization engine for FirstMile sync system.

This module provides intelligent scoring and ranking of actions
from HubSpot deals and Superhuman emails to determine top 3
priorities for each sync cycle.

Author: Claude Code
Created: 2025-11-17
"""

import sys
import io
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# NOTE: UTF-8 encoding wrapper is handled by calling script (unified_sync.py)
# Do not apply wrapper here to avoid conflicts

# Absolute paths
PROJECT_ROOT = Path("C:/Users/BrettWalker/FirstMile_Deals")
CONFIG_PATH = PROJECT_ROOT / ".claude/templates/ACTION_PRIORITY_CONFIG.yaml"


@dataclass
class Action:
    """
    Represents a prioritized action for the user.

    Attributes:
        title: Brief action title
        type: 'email' or 'deal' or 'system'
        priority: 'HIGH', 'MEDIUM', or 'LOW'
        score: Calculated priority score (0-100+)
        context: Description providing background
        next_step: Specific action to take
        due_by: Timeframe for completion
        deal_id: HubSpot deal ID (if type='deal')
        deal_url: Direct link to HubSpot deal
        deal_folder: Path to deal folder
        email_reference: Email subject/sender (if type='email')
    """
    title: str
    type: str  # 'email', 'deal', 'system'
    priority: str  # 'HIGH', 'MEDIUM', 'LOW'
    score: float
    context: str
    next_step: str
    due_by: str
    deal_id: Optional[str] = None
    deal_url: Optional[str] = None
    deal_folder: Optional[str] = None
    email_reference: Optional[str] = None


class ActionPrioritizer:
    """
    Intelligent action prioritization engine.

    Loads scoring configuration from YAML and applies scoring rules
    to HubSpot deals and Superhuman emails to generate top priority actions.
    """

    def __init__(self, config_path: Path = CONFIG_PATH):
        """
        Initialize prioritizer with configuration.

        Args:
            config_path: Path to ACTION_PRIORITY_CONFIG.yaml
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is malformed
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config file: {e}")

    def prioritize_actions(self,
                          hubspot_deals: List[Dict[str, Any]],
                          emails: Dict[str, List[str]],
                          sync_type: str) -> List[Action]:
        """
        Generate prioritized action list from deals and emails.

        Args:
            hubspot_deals: List of active deals from HubSpot API
            emails: Dict with 'critical', 'yesterday', 'last_week' keys
            sync_type: '9am', 'noon', '3pm', or 'eod'

        Returns:
            Top N actions sorted by priority score (N from config)
        """
        actions = []

        # Score and create actions from emails
        actions.extend(self._score_emails(emails))

        # Score and create actions from deals
        actions.extend(self._score_deals(hubspot_deals))

        # Sort by score (descending)
        actions.sort(key=lambda a: a.score, reverse=True)

        # Return top N actions
        top_n = self.config.get('top_action_count', 3)
        return actions[:top_n]

    def _score_emails(self, emails: Dict[str, List[str]]) -> List[Action]:
        """
        Score emails and create Action objects.

        Args:
            emails: Dict with 'critical', 'yesterday', 'last_week' keys

        Returns:
            List of Action objects from emails
        """
        actions = []
        email_scores = self.config.get('email_scores', {})

        # Critical emails (last hour)
        for email_str in emails.get('critical', []):
            score = email_scores.get('critical_last_hour', 50)
            action = self._create_email_action(
                email_str=email_str,
                category='critical',
                score=score,
                due_by='Today (urgent)'
            )
            if action:
                actions.append(action)

        # Yesterday's emails
        for email_str in emails.get('yesterday', []):
            score = email_scores.get('yesterday', 20)
            action = self._create_email_action(
                email_str=email_str,
                category='yesterday',
                score=score,
                due_by='Today'
            )
            if action:
                actions.append(action)

        # Last week emails (lower priority, only include top few)
        last_week_emails = emails.get('last_week', [])[:3]  # Limit to top 3
        for email_str in last_week_emails:
            score = email_scores.get('last_week', 10)
            action = self._create_email_action(
                email_str=email_str,
                category='last_week',
                score=score,
                due_by='This week'
            )
            if action:
                actions.append(action)

        return actions

    def _create_email_action(self,
                            email_str: str,
                            category: str,
                            score: float,
                            due_by: str) -> Optional[Action]:
        """
        Create Action from email string.

        Args:
            email_str: Email string like "📧 **Sender** - Subject (time ago)"
            category: 'critical', 'yesterday', or 'last_week'
            score: Base score for this email
            due_by: Timeframe string

        Returns:
            Action object or None if parsing fails
        """
        try:
            # Parse email string format: "📧 **Sender** - Subject (time ago)"
            # Remove emoji and extract parts
            email_str = email_str.replace('📧', '').replace('🔧', '').replace('📋', '')
            email_str = email_str.replace('💼', '').replace('💰', '').replace('📅', '')
            email_str = email_str.replace('📊', '').replace('🚀', '').replace('✅', '')
            email_str = email_str.replace('📦', '').replace('📝', '').replace('📈', '')
            email_str = email_str.strip()

            # Extract sender and subject
            if ' - ' in email_str:
                sender_part, subject_part = email_str.split(' - ', 1)
                sender = sender_part.replace('**', '').strip()
                subject = subject_part.split('(')[0].strip()
            else:
                sender = "Unknown"
                subject = email_str

            # Determine priority based on category
            if category == 'critical':
                priority = 'HIGH'
            elif category == 'yesterday':
                priority = 'MEDIUM'
            else:
                priority = 'LOW'

            return Action(
                title=f"Respond to {sender}",
                type='email',
                priority=priority,
                score=score,
                context=f"Email from {sender}: \"{subject}\"",
                next_step=f"Review email and respond to {sender}",
                due_by=due_by,
                email_reference=email_str
            )

        except Exception as e:
            print(f"⚠️ Failed to parse email: {email_str}. Error: {e}")
            return None

    def _score_deals(self, deals: List[Dict[str, Any]]) -> List[Action]:
        """
        Score deals and create Action objects.

        Args:
            deals: List of HubSpot deals with properties

        Returns:
            List of Action objects from deals
        """
        actions = []
        deal_scores = self.config.get('deal_scores', {})
        stage_weights = self.config.get('stage_weights', {})
        time_thresholds = self.config.get('time_thresholds', {})

        for deal in deals:
            try:
                score = self._calculate_deal_score(
                    deal, deal_scores, stage_weights, time_thresholds
                )

                action = self._create_deal_action(deal, score)
                if action:
                    actions.append(action)

            except Exception as e:
                deal_name = deal.get('properties', {}).get('dealname', 'Unknown')
                print(f"⚠️ Failed to score deal '{deal_name}': {e}")
                continue

        return actions

    def _calculate_deal_score(self,
                              deal: Dict[str, Any],
                              deal_scores: Dict[str, float],
                              stage_weights: Dict[str, float],
                              time_thresholds: Dict[str, int]) -> float:
        """
        Calculate priority score for a deal.

        Args:
            deal: HubSpot deal dict
            deal_scores: Scoring rules from config
            stage_weights: Stage importance weights
            time_thresholds: Time-based thresholds

        Returns:
            Total priority score
        """
        score = 0.0
        props = deal.get('properties', {})

        # Base score from stage
        stage_id = props.get('dealstage', '')
        score += stage_weights.get(stage_id, 0)

        # High priority flag (HubSpot returns lowercase "high" or null)
        priority = props.get('hs_priority')
        if priority and priority.lower() == 'high':
            score += deal_scores.get('high_priority', 40)

        # Stuck deal (based on last modified date)
        # CRITICAL FIX: Deals stuck 21+ days get NEGATIVE points (dead deals)
        last_modified = props.get('hs_lastmodifieddate')
        if last_modified:
            try:
                last_mod_date = datetime.fromisoformat(
                    last_modified.replace('Z', '+00:00')
                )
                days_since_update = (datetime.now(last_mod_date.tzinfo) - last_mod_date).days

                if days_since_update >= time_thresholds.get('stuck_critical_days', 21):
                    # DEAD DEAL - negative points to push it down
                    score += deal_scores.get('stuck_21_days', -50)
                elif days_since_update >= time_thresholds.get('stuck_warning_days', 14):
                    # STALE DEAL - negative points
                    score += deal_scores.get('stuck_14_days', -25)
                elif days_since_update >= 7:
                    # Needs follow-up - small bonus
                    score += deal_scores.get('stuck_7_days', 15)
            except (ValueError, TypeError):
                pass  # Skip if date parsing fails

        # Stage-specific bonuses
        stage_name = self._get_stage_name(stage_id)
        if 'IMPLEMENTATION' in stage_name:
            score += deal_scores.get('implementation_stage', 15)
        elif 'RATE-CREATION' in stage_name:
            score += deal_scores.get('rate_creation_stage', 15)
        elif 'PROPOSAL-SENT' in stage_name:
            score += deal_scores.get('proposal_sent_stage', 10)

        # Deal value tiebreaker (small bonus to prioritize larger deals when scores are tied)
        # Scaled logarithmically: $1M = 3pts, $10M = 6pts, $100M = 9pts
        amount = float(props.get('amount', 0) or 0)
        if amount > 0:
            import math
            value_bonus = math.log10(amount) - 3  # Subtract 3 so $1K = 0pts, $1M = 3pts
            score += max(0, value_bonus)  # No negative bonus for small deals

        return score

    def _get_stage_name(self, stage_id: str) -> str:
        """
        Get stage name from ID.

        Args:
            stage_id: HubSpot stage ID

        Returns:
            Stage name string
        """
        stage_map = {
            "1090865183": "[01-DISCOVERY-SCHEDULED]",
            "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
            "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
            "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
            "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
            "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
            "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-STARTED-SHIPPING]",
        }
        return stage_map.get(stage_id, "Unknown Stage")

    def _create_deal_action(self, deal: Dict[str, Any], score: float) -> Optional[Action]:
        """
        Create Action from deal.

        Args:
            deal: HubSpot deal dict
            score: Calculated priority score

        Returns:
            Action object or None if creation fails
        """
        try:
            props = deal.get('properties', {})
            deal_id = deal.get('id', '')
            deal_name = props.get('dealname', 'Unnamed Deal')
            stage_id = props.get('dealstage', '')
            stage_name = self._get_stage_name(stage_id)

            # Determine priority level
            if score >= 50:
                priority = 'HIGH'
                due_by = 'Today'
            elif score >= 30:
                priority = 'MEDIUM'
                due_by = 'This week'
            else:
                priority = 'LOW'
                due_by = 'Soon'

            # Get next step recommendation
            next_step = self._get_next_step(stage_id, deal_name)

            # Build deal URL
            deal_url = f"https://app.hubspot.com/contacts/8210927/deal/{deal_id}"

            # Build folder path (simplified - may need adjustment)
            deal_folder = f"{stage_name}_{deal_name.replace(' ', '_')}"

            return Action(
                title=f"{deal_name} - {stage_name}",
                type='deal',
                priority=priority,
                score=score,
                context=f"Deal in {stage_name} stage",
                next_step=next_step,
                due_by=due_by,
                deal_id=deal_id,
                deal_url=deal_url,
                deal_folder=deal_folder
            )

        except Exception as e:
            print(f"⚠️ Failed to create action from deal: {e}")
            return None

    def _get_next_step(self, stage_id: str, deal_name: str) -> str:
        """
        Get next-step recommendation based on stage.

        Args:
            stage_id: HubSpot stage ID
            deal_name: Name of the deal

        Returns:
            Next-step recommendation string
        """
        next_step_templates = self.config.get('next_step_templates', {})
        template = next_step_templates.get(
            stage_id,
            "Review deal status and determine next action"
        )

        # Personalize template with deal name
        return template


def main():
    """Test function for action prioritizer."""
    print("🧪 Testing ActionPrioritizer...")

    # Initialize
    prioritizer = ActionPrioritizer()
    print(f"✅ Loaded config from {prioritizer.config_path}")

    # Test with sample data
    sample_emails = {
        "critical": [
            "📧 **Christopher, Lindsey** - [External] Trace Request (3 mins ago)"
        ],
        "yesterday": [
            "📊 **Reid, Merrick** - Wednesday CVM Check-in (Thu 4:17 PM)"
        ],
        "last_week": [
            "💰 **Josh** - FirstMile Quote (Wed 6:46 AM)"
        ]
    }

    sample_deals = [
        {
            "id": "123",
            "properties": {
                "dealname": "Test Deal",
                "dealstage": "e1c4321e-afb6-4b29-97d4-2b2425488535",  # Rate creation
                "hs_priority": "HIGH",
                "hs_lastmodifieddate": "2025-10-15T12:00:00Z"
            }
        }
    ]

    # Generate actions
    actions = prioritizer.prioritize_actions(sample_deals, sample_emails, '9am')

    print(f"\n✅ Generated {len(actions)} priority actions:")
    for i, action in enumerate(actions, 1):
        print(f"\n{i}. {action.title} [{action.score:.1f}pts]")
        print(f"   Type: {action.type} | Priority: {action.priority}")
        print(f"   Next: {action.next_step}")
        print(f"   Due: {action.due_by}")


if __name__ == "__main__":
    main()
