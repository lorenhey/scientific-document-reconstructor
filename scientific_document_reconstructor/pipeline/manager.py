import os
import json
import hashlib
from typing import Optional
from ..core.models import Document, DocumentMetadata

class PipelineManager:
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.document = None
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "pages"), exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "figures"), exist_ok=True)

    def init_from_pdf(self, pdf_path: str) -> Document:
        """Initializes a new project from a PDF."""
        sha256 = self._compute_sha256(pdf_path)
        self.document = Document(
            source_path=pdf_path,
            source_sha256=sha256
        )
        self.save_project()
        return self.document

    def load_project(self) -> Document:
        """Loads an existing project."""
        project_file = os.path.join(self.project_dir, "project.json")
        if not os.path.exists(project_file):
            raise FileNotFoundError("Project file not found.")
        with open(project_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.document = Document.model_validate(data)
        return self.document

    def save_project(self):
        """Saves the current document state."""
        if self.document is None:
            return
        project_file = os.path.join(self.project_dir, "project.json")
        with open(project_file, 'w', encoding='utf-8') as f:
            f.write(self.document.model_dump_json(indent=2))

    def _compute_sha256(self, filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
