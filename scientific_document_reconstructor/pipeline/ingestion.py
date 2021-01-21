import os
from typing import List
from pdf2image import convert_from_path
from ..core.models import Page, Document

class IngestionPipeline:
    def __init__(self, manager):
        self.manager = manager

    def process(self, dpi=300) -> Document:
        """Converts PDF to images and creates Page objects."""
        doc = self.manager.document
        if not doc.source_path or not os.path.exists(doc.source_path):
            raise FileNotFoundError("Source PDF not found.")

        pages_dir = os.path.join(self.manager.project_dir, "pages")
        
        # In a real scenario, check if already extracted
        images = convert_from_path(doc.source_path, dpi=dpi)
        
        for i, img in enumerate(images):
            page_num = i + 1
            image_path = os.path.join(pages_dir, f"page_{page_num:04d}.png")
            img.save(image_path, "PNG")
            
            page = Page(
                page_number=page_num,
                width=img.width,
                height=img.height,
                image_path=image_path
            )
            doc.pages.append(page)
        
        self.manager.save_project()
        return doc
