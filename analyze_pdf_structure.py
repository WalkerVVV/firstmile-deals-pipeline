"""
Analyze PDF structure to understand why text extraction failed
"""

import pdfplumber

pdf_path = r"c:\Users\BrettWalker\Downloads\FM 2025 Peak Season Surcharges_Final.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print("=" * 80)
    print("PDF ANALYSIS")
    print("=" * 80)
    print()

    print(f"Total pages: {len(pdf.pages)}")
    print()

    for page_num, page in enumerate(pdf.pages, 1):
        print(f"Page {page_num}:")
        print(f"  Width: {page.width}, Height: {page.height}")

        # Check for text
        text = page.extract_text()
        print(f"  Text content: {len(text) if text else 0} characters")

        # Check for images
        if hasattr(page, 'images'):
            print(f"  Images: {len(page.images)}")

        # Check for tables
        tables = page.extract_tables()
        print(f"  Tables: {len(tables)}")

        if tables:
            for i, table in enumerate(tables, 1):
                print(f"    Table {i}: {len(table)} rows")
                if table and len(table) > 0:
                    print(f"      First row: {table[0]}")

        # Try different extraction settings
        print("\n  Trying different extraction methods:")

        # Method 1: Extract with layout preservation
        text_layout = page.extract_text(layout=True)
        print(f"    Layout mode: {len(text_layout) if text_layout else 0} characters")

        # Method 2: Extract words
        words = page.extract_words()
        print(f"    Words extracted: {len(words)}")
        if words:
            print(f"      Sample words: {[w['text'] for w in words[:10]]}")

        print()

    print("=" * 80)
    print("METADATA")
    print("=" * 80)
    print(pdf.metadata)
