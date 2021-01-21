import cv2
import numpy as np
from typing import List
from ..core.models import Page, Block, BlockType, BoundingBox

class LayoutAnalyzer:
    def __init__(self, manager):
        self.manager = manager

    def process(self):
        doc = self.manager.document
        for page in doc.pages:
            self._analyze_page(page)
        self.manager.save_project()

    def _analyze_page(self, page: Page):
        if not page.image_path:
            return
        
        img = cv2.imread(page.image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return

        # Simple heuristic layout analysis:
        # 1. Binarize
        # 2. Dilate horizontally to connect words into lines
        # 3. Dilate vertically to connect lines into paragraphs
        
        # Binarize (invert so text is white)
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        
        # Kernel for paragraph detection
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 20))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours top-to-bottom (simple reading order)
        # For a 2-column layout, we would sort x first then y, or do more complex clustering.
        # This is an MVP top-to-bottom.
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        bounding_boxes = sorted(bounding_boxes, key=lambda b: (b[1], b[0]))
        
        for x, y, w, h in bounding_boxes:
            # Filter out noise
            if w < 20 or h < 10:
                continue
                
            bbox = BoundingBox(x0=float(x), y0=float(y), x1=float(x+w), y1=float(y+h))
            
            # Simple heuristic for type: if it's very wide but short, maybe text.
            # If it's isolated, maybe equation.
            # Real layout analysis would use a deep learning model.
            block = Block(
                type=BlockType.TEXT,
                bbox=bbox
            )
            block.add_provenance("OBSERVED", notes="Detected by contour heuristics")
            page.blocks.append(block)
