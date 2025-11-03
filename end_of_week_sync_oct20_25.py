"""
End of Week Sync - October 20-25, 2025
Comprehensive weekly pipeline review and cleanup
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

# Configuration
DEALS_ROOT = r"C:\Users\BrettWalker\FirstMile_Deals"
DOWNLOADS = r"C:\Users\BrettWalker\Downloads"
PIPELINE_TRACKER = os.path.join(DOWNLOADS, "_PIPELINE_TRACKER.csv")
DAILY_LOG = os.path.join(DOWNLOADS, "_DAILY_LOG.md")
WEEK_START = "2025-10-20"
WEEK_END = "2025-10-25"

def load_pipeline_tracker():
    """Load current pipeline state"""
    if os.path.exists(PIPELINE_TRACKER):
        return pd.read_csv(PIPELINE_TRACKER)
    return pd.DataFrame()

def scan_deal_folders():
    """Scan all deal folders in repository"""
    deals = []

    for item in os.listdir(DEALS_ROOT):
        item_path = os.path.join(DEALS_ROOT, item)
        if os.path.isdir(item_path) and item.startswith("["):
            # Extract stage and company name
            if "]_" in item:
                stage_part = item.split("]")[0] + "]"
                company_part = item.split("]_", 1)[1] if "]_" in item else "Unknown"

                deals.append({
                    'folder_name': item,
                    'stage': stage_part,
                    'company': company_part,
                    'path': item_path
                })

    return pd.DataFrame(deals)

def generate_weekly_summary(df_tracker, df_folders):
    """Generate weekly activity summary"""
    summary = {
        'week_period': f"{WEEK_START} to {WEEK_END}",
        'total_active_deals': len(df_folders),
        'deals_by_stage': {},
        'new_deals_this_week': 0,
        'deals_moved_this_week': 0,
        'stale_deals_flagged': 0,
        'wins_this_week': 0,
        'losses_this_week': 0
    }

    # Count by stage
    if not df_folders.empty:
        stage_counts = df_folders['stage'].value_counts().to_dict()
        summary['deals_by_stage'] = stage_counts

    # Analyze tracker for weekly activity
    if not df_tracker.empty and 'last_modified' in df_tracker.columns:
        df_tracker['last_modified'] = pd.to_datetime(df_tracker['last_modified'], errors='coerce')
        week_start_dt = pd.to_datetime(WEEK_START)
        week_end_dt = pd.to_datetime(WEEK_END)

        weekly_activity = df_tracker[
            (df_tracker['last_modified'] >= week_start_dt) &
            (df_tracker['last_modified'] <= week_end_dt)
        ]

        summary['deals_moved_this_week'] = len(weekly_activity)
        summary['wins_this_week'] = len(weekly_activity[weekly_activity['stage'] == '[07-CLOSED-WON]'])
        summary['losses_this_week'] = len(weekly_activity[weekly_activity['stage'] == '[08-CLOSED-LOST]'])

    return summary

def identify_stale_deals(df_folders, df_tracker):
    """Identify deals that haven't moved in 30+ days"""
    stale_deals = []

    if df_tracker.empty or 'last_modified' not in df_tracker.columns:
        return stale_deals

    df_tracker['last_modified'] = pd.to_datetime(df_tracker['last_modified'], errors='coerce')
    today = pd.to_datetime(datetime.now())

    for _, deal in df_tracker.iterrows():
        if pd.notna(deal.get('last_modified')):
            days_stale = (today - deal['last_modified']).days

            # Flag deals over 30 days in non-terminal stages
            if days_stale > 30 and deal.get('stage') not in ['[07-CLOSED-WON]', '[08-CLOSED-LOST]']:
                stale_deals.append({
                    'company': deal.get('company', 'Unknown'),
                    'stage': deal.get('stage', 'Unknown'),
                    'days_stale': days_stale,
                    'last_modified': deal['last_modified'].strftime('%Y-%m-%d')
                })

    return sorted(stale_deals, key=lambda x: x['days_stale'], reverse=True)

def check_brand_scout_output():
    """Check for new Brand Scout research reports"""
    brand_scout_output = os.path.join(DEALS_ROOT, ".claude", "brand_scout", "output")

    if not os.path.exists(brand_scout_output):
        return []

    reports = []
    week_start_dt = datetime.strptime(WEEK_START, "%Y-%m-%d")
    week_end_dt = datetime.strptime(WEEK_END, "%Y-%m-%d")

    for file in os.listdir(brand_scout_output):
        if file.endswith("_brand_scout_2025-10-25.md") or file.endswith(".md"):
            file_path = os.path.join(brand_scout_output, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            if week_start_dt <= file_time <= week_end_dt:
                reports.append({
                    'filename': file,
                    'created': file_time.strftime('%Y-%m-%d'),
                    'path': file_path
                })

    return reports

def generate_weekly_report(summary, stale_deals, brand_scout_reports):
    """Generate formatted weekly report"""

    # Calculate metrics
    velocity = summary['deals_moved_this_week']
    wins = summary['wins_this_week']
    win_rate = (wins / max(velocity, 1) * 100)
    status = 'HEALTHY' if len(stale_deals) < 5 else 'NEEDS ATTENTION' if len(stale_deals) < 10 else 'CRITICAL'

    report = f"""
# END OF WEEK SYNC REPORT
## Week of {WEEK_START} to {WEEK_END}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## PIPELINE OVERVIEW

**Total Active Deals**: {summary['total_active_deals']}
**Deals Moved This Week**: {summary['deals_moved_this_week']}
**New Wins**: {summary['wins_this_week']}
**Losses**: {summary['losses_this_week']}

### Deals by Stage

"""

    # Add stage breakdown
    for stage, count in sorted(summary['deals_by_stage'].items()):
        report += f"- **{stage}**: {count} deals\n"

    # Stale deals section
    report += f"\n---\n\n## STALE DEALS ALERT ({len(stale_deals)} flagged)\n\n"

    if stale_deals:
        report += "| Company | Stage | Days Stale | Last Modified |\n"
        report += "|---------|-------|------------|---------------|\n"

        for deal in stale_deals[:10]:  # Top 10 stale deals
            report += f"| {deal['company']} | {deal['stage']} | {deal['days_stale']} days | {deal['last_modified']} |\n"

        if len(stale_deals) > 10:
            report += f"\n*+ {len(stale_deals) - 10} more stale deals (see full tracker)*\n"
    else:
        report += "*No stale deals detected - excellent pipeline velocity!*\n"

    # Brand Scout section
    report += f"\n---\n\n## BRAND SCOUT ACTIVITY ({len(brand_scout_reports)} new reports)\n\n"

    if brand_scout_reports:
        for report_info in brand_scout_reports:
            report += f"- **{report_info['filename']}** (Created: {report_info['created']})\n"
    else:
        report += "*No new Brand Scout reports this week*\n"

    # Action items
    report += """
---

## RECOMMENDED ACTIONS

### High Priority
1. **Follow up on stale deals** - Review deals 30+ days without movement
2. **Review Brand Scout reports** - Process new leads into HubSpot
3. **Update follow-up reminders** - Ensure all active deals have next actions scheduled

### Weekly Maintenance
- [ ] Archive completed deals (CLOSED-WON/LOST)
- [ ] Update pipeline tracker with manual stage changes
- [ ] Review and update deal priorities
- [ ] Schedule discovery calls for new leads

### Next Week Focus
- Target stale [03-RATE-CREATION] deals (bottleneck stage)
- Convert [04-PROPOSAL-SENT] to [05-SETUP-DOCS-SENT]
- Process Brand Scout leads through discovery

---

## PIPELINE HEALTH METRICS

**Velocity**: {velocity} deals moved this week
**Conversion**: {wins} wins / {velocity} moved = {win_rate:.1f}% win rate
**Bottleneck**: Check [03-RATE-CREATION] stage for accumulation

**Status**: {status}

---

*Report generated by Nebuchadnezzar v2.0 - End of Week Sync*
"""

    return report

def main():
    """Execute end-of-week sync"""
    print("=" * 60)
    print(f"END OF WEEK SYNC: {WEEK_START} to {WEEK_END}")
    print("=" * 60)
    print()

    # Load data
    print(">> Loading pipeline data...")
    df_tracker = load_pipeline_tracker()
    df_folders = scan_deal_folders()

    print(f"   - Found {len(df_folders)} deal folders")
    print(f"   - Loaded tracker with {len(df_tracker)} records")
    print()

    # Generate summary
    print(">> Generating weekly summary...")
    summary = generate_weekly_summary(df_tracker, df_folders)
    print(f"   - Active deals: {summary['total_active_deals']}")
    print(f"   - Wins this week: {summary['wins_this_week']}")
    print()

    # Identify stale deals
    print(">> Identifying stale deals...")
    stale_deals = identify_stale_deals(df_folders, df_tracker)
    print(f"   - Flagged {len(stale_deals)} stale deals (30+ days)")
    print()

    # Check Brand Scout
    print(">> Checking Brand Scout activity...")
    brand_scout_reports = check_brand_scout_output()
    print(f"   - Found {len(brand_scout_reports)} new reports")
    print()

    # Generate report
    print(">> Generating weekly report...")
    report = generate_weekly_report(summary, stale_deals, brand_scout_reports)

    # Save report
    output_file = os.path.join(DOWNLOADS, f"WEEKLY_SYNC_{WEEK_START}_to_{WEEK_END}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"   => Report saved to: {output_file}")
    print()

    # Display summary
    print("=" * 60)
    print("WEEKLY SUMMARY")
    print("=" * 60)
    print(report)

    # Save JSON summary for programmatic access
    json_output = os.path.join(DOWNLOADS, f"WEEKLY_SYNC_{WEEK_START}_to_{WEEK_END}.json")
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': summary,
            'stale_deals': stale_deals,
            'brand_scout_reports': brand_scout_reports,
            'generated_at': datetime.now().isoformat()
        }, f, indent=2)

    print(f"\n>> JSON data saved to: {json_output}")

    return summary, stale_deals, brand_scout_reports

if __name__ == "__main__":
    main()
