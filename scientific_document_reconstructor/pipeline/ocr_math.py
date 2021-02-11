import pdfplumber
import cv2
from ..core.models import Page, BlockType, Operation

class MathRecognizer:
    def __init__(self, manager):
        self.manager = manager

    def process(self):
        doc = self.manager.document
        
        try:
            with pdfplumber.open(doc.source_path) as pdf:
                for i, page in enumerate(doc.pages):
                    pdf_page = pdf.pages[i]
                    self._recognize_page(page, pdf_page)
        except Exception:
            for page in doc.pages:
                self._recognize_page(page, None)
                
        self.manager.save_project()

    def _recognize_page(self, page: Page, pdf_page):
        if not page.image_path:
            return
            
        for block in page.blocks:
            if block.type == BlockType.EQUATION and block.bbox:
                if pdf_page is not None:
                    try:
                        scale_x = float(pdf_page.width) / page.width
                        scale_y = float(pdf_page.height) / page.height
                        
                        x0 = block.bbox.x0 * scale_x
                        y0 = block.bbox.y0 * scale_y
                        x1 = block.bbox.x1 * scale_x
                        y1 = block.bbox.y1 * scale_y
                        
                        crop = pdf_page.within_bbox((x0, y0, x1, y1))
                        text = crop.extract_text()
                        
                        if text:
                            block.latex = text.strip()
                            block.add_provenance(Operation.RECOGNIZED, recognizer="pdfplumber_math")
                            continue
                    except Exception as e:
                        pass
                
                # Fallback to external math recognizer (e.g. nougat / pix2tex)
                # For MVP, just mark unresolved if we couldn't extract embedded text.
                block.add_provenance(Operation.UNRESOLVED, notes="Math OCR not fully implemented for image scans yet.")
