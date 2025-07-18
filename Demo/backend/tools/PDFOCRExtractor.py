from PIL import Image
import pytesseract
import fitz  # PyMuPDF
from typing import Dict

class PDFOCRExtractor:
    def __init__(self):
        pass 

    def extract_ocr_text(self, path: str) -> str:
        """
        Extracts text from all pages of a PDF using OCR (Tesseract).
        This ignores any embedded text and uses OCR on images only.
        """
        doc = fitz.open(path)
        all_text = ""
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            all_text += text + "\n"
        return all_text

    def run(self, path: str) -> Dict[str, str]:
        """High-level method to run forced OCR and return result."""
        extracted_text = self.extract_ocr_text(path)
        return {
            "ocr_text": extracted_text
        }

# if __name__ == "__main__":
#     tool = PDFOCRExtractor()
#     result = tool.run("testing.pdf")  # Replace with your test path
#     print(result)
