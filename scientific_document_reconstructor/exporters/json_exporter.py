import os
import json
from ..core.models import Document

class JsonExporter:
    def __init__(self, manager):
        self.manager = manager

    def export(self, output_dir: str):
        doc = self.manager.document
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "reconstructed.json")
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(doc.model_dump_json(indent=2))
