import cv2
import pdfplumber
from ..core.models import Page, Block, BlockType, BoundingBox

class LayoutAnalyzer:
    def __init__(self, manager):
        self.manager = manager

    def process(self):
        doc = self.manager.document
        
        try:
            with pdfplumber.open(doc.source_path) as pdf:
                for i, page in enumerate(doc.pages):
                    pdf_page = pdf.pages[i]
                    self._analyze_page_with_pdf(page, pdf_page)
        except Exception:
            for page in doc.pages:
                self._analyze_page_image_only(page)
                
        self.manager.save_project()

    def _analyze_page_with_pdf(self, page: Page, pdf_page):
        # Extract words and cluster them into lines/paragraphs
        words = pdf_page.extract_words()
        if not words:
            self._analyze_page_image_only(page)
            return
            
        scale_x = page.width / float(pdf_page.width)
        scale_y = page.height / float(pdf_page.height)
        
        # Simple clustering by y-coordinate to form lines
        # This is a basic MVP layout analysis
        words.sort(key=lambda w: (w['top'], w['x0']))
        
        blocks = []
        current_block_words = []
        
        for word in words:
            if not current_block_words:
                current_block_words.append(word)
                continue
                
            last_word = current_block_words[-1]
            
            # If vertical distance is small, it's the same block
            if abs(word['top'] - last_word['top']) < 15 or (word['top'] - last_word['bottom'] < 10):
                current_block_words.append(word)
            else:
                blocks.append(current_block_words)
                current_block_words = [word]
                
        if current_block_words:
            blocks.append(current_block_words)
            
        for b_words in blocks:
            x0 = min(w['x0'] for w in b_words) * scale_x
            top = min(w['top'] for w in b_words) * scale_y
            x1 = max(w['x1'] for w in b_words) * scale_x
            bottom = max(w['bottom'] for w in b_words) * scale_y
            
            bbox = BoundingBox(x0=x0, y0=top, x1=x1, y1=bottom)
            
            # Simple heuristic: if text has '=', treat as equation
            text_content = " ".join(w['text'] for w in b_words)
            if "=" in text_content and len(text_content) < 50:
                from ..core.models import EquationBlock
                block = EquationBlock(bbox=bbox)
            else:
                block = Block(type=BlockType.TEXT, bbox=bbox)
                
            block.add_provenance("OBSERVED", notes="Extracted via PDF text layout")
            page.blocks.append(block)

    def _analyze_page_image_only(self, page: Page):
        if not page.image_path:
            return
        
        img = cv2.imread(page.image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return
            
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 20))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))
        
        for x, y, w, h in bounding_boxes:
            if w < 20 or h < 10:
                continue
            bbox = BoundingBox(x0=float(x), y0=float(y), x1=float(x+w), y1=float(y+h))
            block = Block(type=BlockType.TEXT, bbox=bbox)
            block.add_provenance("OBSERVED", notes="Detected by contour heuristics")
            page.blocks.append(block)
