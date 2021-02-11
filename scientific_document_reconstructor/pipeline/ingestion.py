import os
import pdfplumber
from ..core.models import Page, Document

class IngestionPipeline:
    def __init__(self, manager):
        self.manager = manager

    def process(self, resolution=300) -> Document:
        """Converts PDF to images and creates Page objects."""
        doc = self.manager.document
        if not doc.source_path or not os.path.exists(doc.source_path):
            raise FileNotFoundError("Source PDF not found.")

        pages_dir = os.path.join(self.manager.project_dir, "pages")
        
        with pdfplumber.open(doc.source_path) as pdf:
            for i, pdf_page in enumerate(pdf.pages):
                page_num = i + 1
                image_path = os.path.join(pages_dir, f"page_{page_num:04d}.png")
                
                # Convert page to image
                img = pdf_page.to_image(resolution=resolution).original
                img.save(image_path, format="PNG")
                
                page = Page(
                    page_number=page_num,
                    width=float(pdf_page.width),
                    height=float(pdf_page.height),
                    image_path=image_path
                )
                doc.pages.append(page)
        
        self.manager.save_project()
        return doc
