"""
FirstMile Data Pipeline - CLI Wrapper
Simple command-line interface for running the data pipeline

Usage:
    python run_pipeline.py <csv_file> [options]

Examples:
    python run_pipeline.py customer_data.csv
    python run_pipeline.py customer_data.csv --customer "Acme Corp" --period "Q3 2025"
"""

import argparse
import sys
from pathlib import Path
from firstmile_data_pipeline import FirstMileDataPipeline


def main():
    parser = argparse.ArgumentParser(
        description='FirstMile Data Pipeline - Process customer CSV into branded Excel report',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py customer_shipments.csv
  python run_pipeline.py data.csv --customer "BoxiiShip" --period "October 2025"
  python run_pipeline.py data.csv --service "Xparcel Ground" --output "./reports"
        """
    )

    parser.add_argument(
        'csv_file',
        help='Path to customer CSV file'
    )

    parser.add_argument(
        '--customer', '-c',
        default='Customer',
        help='Customer name for report (default: Customer)'
    )

    parser.add_argument(
        '--period', '-p',
        default='Recent Period',
        help='Report period description (default: Recent Period)'
    )

    parser.add_argument(
        '--service', '-s',
        default='All Services',
        choices=['All Services', 'Xparcel Ground', 'Xparcel Expedited', 'Xparcel Priority'],
        help='Service level filter (default: All Services)'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Output directory for report (default: same as input CSV)'
    )

    parser.add_argument(
        '--required-cols',
        nargs='+',
        default=['Delivered Status', 'Days In Transit'],
        help='Required columns in CSV (default: Delivered Status, Days In Transit)'
    )

    args = parser.parse_args()

    # Validate CSV file exists
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file not found: {args.csv_file}")
        sys.exit(1)

    # Build configuration
    config = {
        'customer_name': args.customer,
        'report_period': args.period,
        'service_level': args.service,
        'required_columns': args.required_cols
    }

    try:
        # Initialize and run pipeline
        pipeline = FirstMileDataPipeline(config)
        output_path = pipeline.run(str(csv_path), args.output)

        print(f"\n✓ Success! Report saved to:")
        print(f"  {output_path}")

    except Exception as e:
        print(f"\n✗ Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
