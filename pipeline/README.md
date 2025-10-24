# FirstMile Data Pipeline

Automated workflow for processing customer CSV files into FirstMile-branded Excel reports with SLA compliance metrics.

## Features

- **Automated CSV Processing**: Handles various CSV formats with robust parsing
- **FirstMile Business Logic**: Applies billable weight rules, SLA compliance, zone analysis
- **Branded Excel Reports**: Generates professional reports with FirstMile styling (#366092)
- **SLA Compliance Tracking**: Calculates compliance based on service windows
- **Hub Mapping**: Assigns regional hubs based on destination state
- **Zone Categorization**: Groups into Regional (1-4) vs Cross-Country (5-8)

## Installation

```bash
# Install required dependencies
pip install pandas numpy openpyxl
```

## Quick Start

### Basic Usage

```bash
python run_pipeline.py customer_shipments.csv
```

### With Customer Details

```bash
python run_pipeline.py data.csv --customer "BoxiiShip" --period "October 2025"
```

### Specify Service Level

```bash
python run_pipeline.py data.csv --customer "OTW Shipping" --service "Xparcel Ground"
```

### Custom Output Directory

```bash
python run_pipeline.py data.csv --output "./reports"
```

## Command-Line Options

```
positional arguments:
  csv_file              Path to customer CSV file

optional arguments:
  -h, --help            Show help message
  --customer, -c        Customer name for report (default: Customer)
  --period, -p          Report period description (default: Recent Period)
  --service, -s         Service level filter (default: All Services)
  --output, -o          Output directory for report (default: same as input)
  --required-cols       Required columns in CSV (default: Delivered Status, Days In Transit)
```

## CSV Requirements

### Required Columns
- `Delivered Status` - Package delivery status
- `Days In Transit` - Transit time in days

### Optional Columns (Enhance Reports)
- `Service` or `Service Level` - Service type
- `Weight` - Package weight (for billable weight calculation)
- `Destination State` - For hub assignment
- `Calculated Zone` or `Zone` - Shipping zone
- `Request Date` or `ShipDate` - Ship date
- `tracking` or `Tracking Number` - Tracking number

## Business Logic

### SLA Windows
- **Xparcel Priority**: 3 days (1-3 day service)
- **Xparcel Expedited**: 5 days (2-5 day service)
- **Xparcel Ground**: 8 days (3-8 day service)

### Performance Thresholds
- **Perfect Compliance**: 100%
- **Exceeds Standard**: ≥95%
- **Meets Standard**: ≥90%
- **Below Standard**: <90%

### Billable Weight Rules
- **Under 1 lb**: Round UP to next whole oz (max 15.99 oz)
- **16 oz exactly**: Bills as 1 lb
- **Over 1 lb**: Round UP to next whole pound

### Hub Mapping
- CA → LAX - West Coast
- TX → DFW - South Central
- FL → MIA - Southeast
- NY/NJ → JFK/EWR - Northeast
- IL → ORD - Midwest
- GA → ATL - Southeast
- Others → National Network

## Output Report Structure

The generated Excel report includes:

1. **Executive Summary** - High-level KPIs and metrics
2. **Raw Data** - Complete processed dataset
3. *(Additional tabs can be added in future versions)*

### Report Features
- FirstMile blue (#366092) header styling
- Auto-sized columns for readability
- Auto-filters on all data tables
- Professional alignment and borders
- Timestamp in filename

## Pipeline Architecture

```
Customer CSV → Ingestion → Validation → Transformation → Enrichment → Report Generation → Output
```

### Stage Details

1. **Ingestion**: Read CSV, handle encoding, parse dates, clean data
2. **Validation**: Check required columns, data quality
3. **Transformation**: Apply billable weight, service mapping, SLA calculations
4. **Enrichment**: Zone grouping, hub mapping, geographic analysis
5. **Report Generation**: Create 9-tab Excel with FirstMile branding
6. **Output**: Save to customer deal folder with timestamp

## Examples

### Process BoxiiShip Data

```bash
python run_pipeline.py "[07-CLOSED-WON]_BoxiiShip_AF/customer_shipments.csv" \
  --customer "BoxiiShip" \
  --period "September 1-30, 2025" \
  --service "Xparcel Ground"
```

### Process OTW Shipping Analysis

```bash
python run_pipeline.py "[04-PROPOSAL-SENT]_OTW_Shipping/pld_data.csv" \
  --customer "OTW Shipping" \
  --period "Q3 2025"
```

### Batch Processing Multiple Customers

```bash
# Create a simple batch script
for file in **/customer_*.csv; do
  python run_pipeline.py "$file" --customer "$(basename $(dirname $file))"
done
```

## Troubleshooting

### Missing Required Columns
```
Error: Missing required columns: ['Delivered Status']
Available columns: ['Status', 'Transit Days', ...]
```

**Solution**: Use `--required-cols` to specify different column names:
```bash
python run_pipeline.py data.csv --required-cols "Status" "Transit Days"
```

### Date Parsing Issues
The pipeline automatically handles multiple date formats. If dates aren't parsing:
- Ensure dates are in `YYYY-MM-DD` or `MM/DD/YYYY` format
- Check for empty date values

### Tracking Number Scientific Notation
The pipeline automatically converts tracking numbers from scientific notation to standard format.

## Advanced Usage

### Programmatic Usage

```python
from firstmile_data_pipeline import FirstMileDataPipeline

# Configure pipeline
config = {
    'customer_name': 'Acme Corp',
    'report_period': 'October 2025',
    'service_level': 'Xparcel Ground',
    'required_columns': ['Delivered Status', 'Days In Transit']
}

# Run pipeline
pipeline = FirstMileDataPipeline(config)
output_path = pipeline.run('customer_data.csv', output_dir='./reports')

print(f"Report saved: {output_path}")
```

### Custom Transformations

Extend the `FirstMileTransformations` class to add custom business logic:

```python
from firstmile_data_pipeline import FirstMileTransformations

class CustomTransformations(FirstMileTransformations):
    @staticmethod
    def custom_metric(df, col):
        # Your custom logic
        return df
```

## File Structure

```
pipeline/
├── firstmile_data_pipeline.py    # Main pipeline logic
├── run_pipeline.py                # CLI wrapper
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Version History

- **v1.0.0** (2025-10-13): Initial release
  - CSV ingestion with robust parsing
  - FirstMile business logic transformations
  - Branded Excel report generation
  - CLI interface

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the examples for common use cases
- Contact Brett Walker for FirstMile-specific questions

---

**Generated by:** FirstMile Data Pipeline v1.0.0
**Last Updated:** 2025-10-13
