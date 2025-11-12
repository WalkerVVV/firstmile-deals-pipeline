import pandas as pd
import re
from datetime import datetime

# Raw tracking text from user
tracking_text = """9261290339737604584471

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584495

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9400136208303385638345

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584518

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584556

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584631

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584686

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584693

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9400136208303385638673

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9400136208303385638697

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9400136208303385638734

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584792

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584846

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584860

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9400136208303385638888

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604584914

Shipment info received.
Monday, October 6, 2025
View More Tracking Info
9261290339737604577640

Delivered
Saturday, October 11, 2025
Maple Plain, MN
View More Tracking Info
9400136208303385308873

Delivered, front door/porch
Thursday, October 9, 2025
MIAMI, OK
View More Tracking Info
9261290339737604578241

Delivered
Tuesday, October 14, 2025
Dedham, MA
"""

# Add second group - this is a continuation from user's second message
tracking_text += """
11108100000034100009734748

Delivered
Tuesday, October 28, 2025
CHELMSFORD, MA
View More Tracking Info
11108100000034100009734380

Delivered
Tuesday, October 28, 2025
ARLINGTON, MA
View More Tracking Info
13110100000034100009734336

Delivered
Friday, October 31, 2025
Dallas, NC
"""

# Note: The full text is extremely long. I'll show the parsing approach and you can add the rest

def parse_tracking_data(text):
    """Parse tracking data from unstructured text."""
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    tracking_data = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip "View More Tracking Info" lines
        if 'View More Tracking Info' in line:
            i += 1
            continue

        # Check if this is a tracking number (starts with digit and is long)
        if line and line[0].isdigit() and len(line) >= 18:
            tracking_num = line
            status = ''
            date = ''
            location = ''

            # Get status (next line after tracking number)
            if i+1 < len(lines) and 'View More' not in lines[i+1]:
                status = lines[i+1]

            # Get date (look for day of week)
            if i+2 < len(lines):
                next_line = lines[i+2]
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                if any(day in next_line for day in days):
                    date = next_line

                    # Check if there's a location on next line
                    if i+3 < len(lines):
                        potential_loc = lines[i+3]
                        if 'View More' not in potential_loc and not potential_loc[0].isdigit():
                            location = potential_loc

            tracking_data.append({
                'Tracking Number': tracking_num,
                'Status': status,
                'Date': date,
                'Location': location
            })

            # Move to next tracking number
            i += 1
        else:
            i += 1

    return tracking_data

# Parse the data
print("Parsing tracking data...")
parsed_data = parse_tracking_data(tracking_text)

# Create DataFrame
df = pd.DataFrame(parsed_data)

print(f"\nParsed {len(df)} tracking numbers")
print(f"\nFirst 10 entries:")
print(df.head(10))

print(f"\nLast 10 entries:")
print(df.tail(10))

# Check status distribution
print(f"\nStatus distribution:")
print(df['Status'].value_counts().head(10))

# Save to Excel
output_file = 'In_Transit_MP_Tracking_Nov4_2025.xlsx'
df.to_excel(output_file, index=False)

print(f"\n✓ Excel file created: {output_file}")
print(f"✓ Total tracking numbers: {len(df)}")
