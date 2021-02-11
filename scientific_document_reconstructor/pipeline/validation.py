import json
import os
from ..core.models import Document, BlockType, EquationBlock, Operation

class Validator:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        doc = self.manager.document
        
        total_blocks = 0
        equations = 0
        low_confidence_regions = 0
        unresolved = 0
        
        for page in doc.pages:
            for block in page.blocks:
                total_blocks += 1
                if block.type == BlockType.EQUATION:
                    equations += 1
                    
                has_unresolved = any(p.operation == Operation.UNRESOLVED for p in block.provenance)
                if has_unresolved:
                    unresolved += 1
                    low_confidence_regions += 1
                    
        print(f"Document: {doc.metadata.title or 'Unknown'}")
        print(f"Pages: {len(doc.pages)}\n")
        print(f"Text blocks/Equations/Tables/Figures: {total_blocks}")
        print(f"Equations: {equations}\n")
        print(f"Low-confidence regions: {low_confidence_regions}")
        print(f"Unresolved equations: {unresolved}\n")
        
        if unresolved > 0:
            print("[WARNING] Document requires human review.")
        else:
            print("[SUCCESS] Document reconstructed successfully.")
