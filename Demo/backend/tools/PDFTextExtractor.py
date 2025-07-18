import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict

class PDFTextExtractor:
    def __init__(self):
        pass  

    def extract_text_from_pdf(self, path: str) -> str:
        """Extracts text from a PDF, falling back to OCR if necessary."""
        doc = fitz.open(path)
        all_text = ""
        for page in doc:
            text = page.get_text()
            if not text.strip():
                # Fallback to OCR
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)
            all_text += text
        return all_text

    def chunk_text(self, text: str) -> List[str]:
        """Chunks extracted text using a recursive splitter."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        return splitter.split_text(text)

    def run(self, path: str) -> Dict[str, List[str]]:
        """High-level method to extract and chunk text from PDF."""
        extracted_text = self.extract_text_from_pdf(path)
        chunks = self.chunk_text(extracted_text)
        return {
            "chunks": chunks
        }

# if __name__ == "__main__":
#     tool = PDFTextExtractor()
#     result = tool.run("testing.pdf")  # Replace with actual PDF path
#     print(result)
