import os
import sys
from scientific_document_reconstructor.pipeline.manager import PipelineManager
from scientific_document_reconstructor.core.models import BlockType, EquationBlock

def run_benchmark():
    project_dir = "samples/synthetic_paper.pdf.sdr"
    if not os.path.exists(project_dir):
        print("Run 'sdr reconstruct samples/synthetic_paper.pdf' first.")
        sys.exit(1)
        
    manager = PipelineManager(project_dir)
    doc = manager.load_project()
    
    # Ground truth (from generate_synthetic.py)
    ground_truth = {
        "title": "The Thermodynamics of Synthetic Documents",
        "author": "L. Perez and M. Curie",
        "equation": "E = mc^2 (1)",
        "intro": "1. Introduction"
    }
    
    extracted_text = []
    equations = []
    
    for page in doc.pages:
        for block in page.blocks:
            if block.type == BlockType.EQUATION:
                if isinstance(block, EquationBlock) and block.latex:
                    equations.append(block.latex)
            else:
                if block.content:
                    extracted_text.append(block.content)
                    
    full_text = "\n".join(extracted_text)
    
    print("--- BENCHMARK RESULTS ---")
    score = 0
    total = len(ground_truth)
    
    for key, expected in ground_truth.items():
        if key == "equation":
            found = any(expected in eq for eq in equations)
            print(f"[{'PASS' if found else 'FAIL'}] Math: '{expected}'")
            if found: score += 1
        else:
            found = expected in full_text
            print(f"[{'PASS' if found else 'FAIL'}] Text: '{expected}'")
            if found: score += 1
            
    print(f"\nFinal Score: {score}/{total} ({(score/total)*100:.1f}%)")

if __name__ == "__main__":
    run_benchmark()
