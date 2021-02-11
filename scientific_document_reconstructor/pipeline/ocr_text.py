import cv2
import pdfplumber
import pytesseract
from PIL import Image
from ..core.models import Page, Block, BlockType, Operation

class TextRecognizer:
    def __init__(self, manager, lang="eng"):
        self.manager = manager
        self.lang = lang

    def process(self):
        doc = self.manager.document
        
        # Try to open the original PDF to get embedded text
        try:
            with pdfplumber.open(doc.source_path) as pdf:
                for i, page in enumerate(doc.pages):
                    pdf_page = pdf.pages[i]
                    self._recognize_page(page, pdf_page)
        except Exception as e:
            # Fallback if no PDF or error
            for page in doc.pages:
                self._recognize_page(page, None)
                
        self.manager.save_project()

    def _recognize_page(self, page: Page, pdf_page):
        if not page.image_path:
            return
            
        img = cv2.imread(page.image_path)
        if img is None:
            return

        # Simple check if PDF has text
        has_text = False
        if pdf_page is not None:
            text = pdf_page.extract_text()
            if text and len(text.strip()) > 50:
                has_text = True

        for block in page.blocks:
            if block.type == BlockType.TEXT and block.bbox:
                # If we have embedded text, use pdfplumber bounding box crop
                if has_text and pdf_page is not None:
                    # pdfplumber uses standard PDF coordinates (y from bottom or top depending on setup, but typically top for crop)
                    # We might need to adjust coordinates if resolutions differ, but assuming they match:
                    try:
                        # Convert bbox to pdfplumber crop box
                        # pdf_page width/height usually matches if resolution was default (72dpi), 
                        # but we used 300dpi, so we need to scale.
                        scale_x = float(pdf_page.width) / page.width
                        scale_y = float(pdf_page.height) / page.height
                        
                        x0 = block.bbox.x0 * scale_x
                        y0 = block.bbox.y0 * scale_y
                        x1 = block.bbox.x1 * scale_x
                        y1 = block.bbox.y1 * scale_y
                        
                        crop = pdf_page.within_bbox((x0, y0, x1, y1))
                        text = crop.extract_text()
                        
                        if text:
                            block.content = text.strip()
                            block.add_provenance(Operation.RECOGNIZED, recognizer="pdfplumber")
                            continue
                    except Exception as e:
                        pass
                        
                # Fallback to Tesseract
                try:
                    x0, y0, x1, y1 = int(block.bbox.x0), int(block.bbox.y0), int(block.bbox.x1), int(block.bbox.y1)
                    pad = 2
                    y0_p = max(0, y0 - pad)
                    y1_p = min(img.shape[0], y1 + pad)
                    x0_p = max(0, x0 - pad)
                    x1_p = min(img.shape[1], x1 + pad)
                    
                    roi = img[y0_p:y1_p, x0_p:x1_p]
                    if roi.size > 0:
                        text = pytesseract.image_to_string(roi, lang=self.lang).strip()
                        if text:
                            block.content = text
                            block.add_provenance(Operation.RECOGNIZED, recognizer="pytesseract")
                        else:
                            block.add_provenance(Operation.UNRESOLVED, recognizer="pytesseract", notes="Empty output")
                except Exception as e:
                    block.add_provenance(Operation.UNRESOLVED, notes=f"OCR failed: {e}")
