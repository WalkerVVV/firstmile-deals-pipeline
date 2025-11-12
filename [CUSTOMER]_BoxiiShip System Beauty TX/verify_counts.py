import pandas as pd

df = pd.read_excel('BLANK_MP_Tracking_Nov4_2025.xlsx')
print(f'BLANK -MP Total rows: {len(df)}')
print(f'With Status: {len(df[df["Status"] != ""])}')
print(f'Blank Status: {len(df[df["Status"] == ""])}')
print(f'\nFirst 5 rows:')
print(df.head())
