import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

def is_image_based(file_path, text_threshold=10):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        return True
    elif ext == '.pdf':
        doc = fitz.open(file_path)
        image_based = True
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text()
            if len(text.strip()) > text_threshold:
                image_based = False
                break
        doc.close()
        return image_based
    else:
        raise ValueError(f"Unsupported file type for: {file_path}")

def extract_text_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_content = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        all_content.append({"page": page_num+1, "text": text, "extraction_method": "text"})
    doc.close()
    return all_content

def extract_text_ocr_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_content = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img)
        all_content.append({"page": page_num+1, "text": text, "extraction_method": "ocr"})
    doc.close()
    return all_content

def extract_text_ocr_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return [{"page": 1, "text": text, "extraction_method": "ocr"}]

def agentic_ocr_framework(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
        print(f"[INFO] {os.path.basename(file_path)} is an image. Using OCR...")
        return extract_text_ocr_image(file_path)
    elif ext == '.pdf':
        if is_image_based(file_path):
            print(f"[INFO] {os.path.basename(file_path)} seems image-based. Using OCR...")
            return extract_text_ocr_pdf(file_path)
        else:
            print(f"[INFO] {os.path.basename(file_path)} is machine-readable. Using standard extraction...")
            return extract_text_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type for: {file_path}")

if __name__ == "__main__":
    doc_paths = ["./sampleData/testing.pdf", "./sampleData/sample_ocr_test.png"]
    for doc in doc_paths:
        result = agentic_ocr_framework(doc)
        for item in result:
            print(f"Page {item['page']} ({item['extraction_method']}):")
            print("-------")
            print(item['text'][:500])
            print("=======")
