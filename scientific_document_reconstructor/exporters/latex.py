import os
from ..core.models import Document, BlockType, EquationBlock

class LatexExporter:
    def __init__(self, manager):
        self.manager = manager

    def export(self, output_dir: str):
        doc = self.manager.document
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "reconstructed.tex")
        
        lines = []
        lines.append("\\documentclass{article}")
        lines.append("\\usepackage{amsmath}")
        lines.append("\\usepackage{graphicx}")
        lines.append("\\begin{document}")
        
        if doc.metadata.title:
            lines.append(f"\\title{{{self._escape_latex(doc.metadata.title)}}}")
            if doc.metadata.authors:
                lines.append(f"\\author{{{self._escape_latex(' and '.join(doc.metadata.authors))}}}")
            lines.append("\\maketitle")
            
        for page in doc.pages:
            lines.append(f"%% Page {page.page_number}")
            for block in page.blocks:
                if block.type == BlockType.TEXT:
                    if block.content:
                        lines.append(self._escape_latex(block.content) + "\n")
                elif block.type == BlockType.EQUATION:
                    lines.append("\\begin{equation}")
                    if isinstance(block, EquationBlock) and block.latex:
                        lines.append(block.latex)
                    else:
                        lines.append("% [UNCERTAIN EQUATION]")
                    lines.append("\\end{equation}\n")
                elif block.type == BlockType.HEADING:
                    if block.content:
                        lines.append(f"\\section*{{{self._escape_latex(block.content)}}}\n")
            
            lines.append("\\newpage")
            
        lines.append("\\end{document}")
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
            
    def _escape_latex(self, text: str) -> str:
        # Minimal LaTeX escaping for MVP
        chars = {
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '^': '\\textasciicircum{}',
            '\\': '\\textbackslash{}',
        }
        res = "".join(chars.get(c, c) for c in text)
        return res
