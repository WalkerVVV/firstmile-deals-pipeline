"""
Extract text from FM 2025 Peak Season Surcharges_Final.pdf using pdfplumber
"""

try:
    import pdfplumber
    pdf_available = True
except ImportError:
    pdf_available = False
    print("pdfplumber not installed. Installing...")

if not pdf_available:
    import subprocess
    subprocess.check_call(['pip', 'install', 'pdfplumber'])
    import pdfplumber

# Load the PDF
pdf_path = r"c:\Users\BrettWalker\Downloads\FM 2025 Peak Season Surcharges_Final.pdf"

with pdfplumber.open(pdf_path) as pdf:
    # Open output file with UTF-8 encoding
    output_path = "FM_2025_Peak_Season_Surcharges.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# FirstMile 2025 Peak Season Surcharges\n\n")
        f.write("**Source:** FM 2025 Peak Season Surcharges_Final.pdf\n\n")
        f.write("---\n\n")

        # Extract text from all pages
        num_pages = len(pdf.pages)
        print(f"Total pages: {num_pages}")

        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Extracting page {page_num}...")
            text = page.extract_text()

            if text:
                f.write(f"## Page {page_num}\n\n")
                f.write(text)
                f.write("\n\n---\n\n")
            else:
                print(f"  Warning: No text found on page {page_num}")

            # Also try to extract tables
            tables = page.extract_tables()
            if tables:
                f.write(f"### Tables from Page {page_num}\n\n")
                for i, table in enumerate(tables, 1):
                    f.write(f"**Table {i}:**\n\n")
                    for row in table:
                        if row:
                            row_text = " | ".join([str(cell) if cell else "" for cell in row])
                            f.write(row_text + "\n")
                    f.write("\n")

print(f"\nContent extracted successfully to: {output_path}")
print("File saved with UTF-8 encoding to preserve all characters.")
