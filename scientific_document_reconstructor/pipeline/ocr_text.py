import cv2
import pytesseract
from PIL import Image
from ..core.models import Page, Block, BlockType, Operation

class TextRecognizer:
    def __init__(self, manager, lang="eng"):
        self.manager = manager
        self.lang = lang

    def process(self):
        doc = self.manager.document
        for page in doc.pages:
            self._recognize_page(page)
        self.manager.save_project()

    def _recognize_page(self, page: Page):
        if not page.image_path:
            return
            
        img = cv2.imread(page.image_path)
        if img is None:
            return

        for block in page.blocks:
            if block.type == BlockType.TEXT and block.bbox:
                # Crop image
                x0, y0, x1, y1 = int(block.bbox.x0), int(block.bbox.y0), int(block.bbox.x1), int(block.bbox.y1)
                
                # Expand slightly to avoid cutting edges
                pad = 2
                y0_p = max(0, y0 - pad)
                y1_p = min(img.shape[0], y1 + pad)
                x0_p = max(0, x0 - pad)
                x1_p = min(img.shape[1], x1 + pad)
                
                roi = img[y0_p:y1_p, x0_p:x1_p]
                if roi.size == 0:
                    continue
                
                # Tesseract OCR
                text = pytesseract.image_to_string(roi, lang=self.lang).strip()
                
                if text:
                    block.content = text
                    # We can use image_to_data to get confidence, for MVP we just mark RECOGNIZED.
                    block.add_provenance(Operation.RECOGNIZED, recognizer="pytesseract")
                else:
                    block.add_provenance(Operation.UNRESOLVED, recognizer="pytesseract", notes="Empty output")
