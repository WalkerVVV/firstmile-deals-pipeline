"""
Extract text from FM 2025 Peak Season Surcharges_Final.pdf
"""

try:
    import PyPDF2
    pdf_available = True
except ImportError:
    pdf_available = False
    print("PyPDF2 not installed. Installing...")

if not pdf_available:
    import subprocess
    subprocess.check_call(['pip', 'install', 'PyPDF2'])
    import PyPDF2

# Load the PDF
pdf_path = r"c:\Users\BrettWalker\Downloads\FM 2025 Peak Season Surcharges_Final.pdf"

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)

    # Open output file with UTF-8 encoding
    output_path = "FM_2025_Peak_Season_Surcharges.md"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# FirstMile 2025 Peak Season Surcharges\n\n")
        f.write("**Source:** FM 2025 Peak Season Surcharges_Final.pdf\n\n")
        f.write("---\n\n")

        # Extract text from all pages
        num_pages = len(pdf_reader.pages)
        print(f"Total pages: {num_pages}")

        for page_num in range(num_pages):
            print(f"Extracting page {page_num + 1}...")
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            f.write(f"## Page {page_num + 1}\n\n")
            f.write(text)
            f.write("\n\n---\n\n")

print(f"\nContent extracted successfully to: {output_path}")
print("File saved with UTF-8 encoding to preserve all characters.")
