"""
Extract image from PDF and attempt OCR
"""

import pdfplumber
from PIL import Image
import io

try:
    import pytesseract
    ocr_available = True
except ImportError:
    print("pytesseract not available - will extract image only")
    ocr_available = False

pdf_path = r"c:\Users\BrettWalker\Downloads\FM 2025 Peak Season Surcharges_Final.pdf"

with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[0]

    print("Extracting image from PDF...")

    # Convert page to image
    img = page.to_image(resolution=200)

    # Save the image
    img_path = "peak_surcharges_page.png"
    img.save(img_path)
    print(f"Image saved to: {img_path}")

    if ocr_available:
        try:
            print("\nAttempting OCR...")
            # Load the image for OCR
            pil_img = Image.open(img_path)
            text = pytesseract.image_to_string(pil_img)

            # Save extracted text
            with open("FM_2025_Peak_Season_Surcharges_OCR.txt", 'w', encoding='utf-8') as f:
                f.write(text)

            print("OCR extraction successful!")
            print("\nExtracted text preview:")
            print("=" * 80)
            print(text[:500])
            print("=" * 80)
        except Exception as e:
            print(f"OCR failed: {e}")
            print("Please install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki")
    else:
        print("\nOCR not available. Install pytesseract and Tesseract to extract text.")
        print("Image has been saved - please provide the content manually.")
