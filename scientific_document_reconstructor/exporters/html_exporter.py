import os
from ..core.models import BlockType, EquationBlock

class HtmlExporter:
    def __init__(self, manager):
        self.manager = manager

    def export(self, output_dir: str):
        doc = self.manager.document
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "reconstructed.html")
        
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html><head><meta charset='utf-8'><title>SDR Reconstruction</title>")
        html.append("<style>body { max-width: 800px; margin: 40px auto; font-family: 'Times New Roman', serif; line-height: 1.6; }</style>")
        html.append("</head><body>")
        
        if doc.metadata.title:
            html.append(f"<h1>{self._escape(doc.metadata.title)}</h1>")
            
        for page in doc.pages:
            html.append(f"<hr/><p style='color: #999;'>Page {page.page_number}</p>")
            for block in page.blocks:
                if block.type == BlockType.TEXT:
                    if block.content:
                        html.append(f"<p>{self._escape(block.content)}</p>")
                elif block.type == BlockType.EQUATION:
                    # In a real exporter we'd use MathJax, but for now just pre
                    if isinstance(block, EquationBlock) and block.latex:
                        html.append(f"<pre style='background: #f4f4f4; padding: 10px;'>{self._escape(block.latex)}</pre>")
                    else:
                        html.append("<pre style='color: red;'>[UNCERTAIN EQUATION]</pre>")
                elif block.type == BlockType.HEADING:
                    if block.content:
                        html.append(f"<h2>{self._escape(block.content)}</h2>")
                        
        html.append("</body></html>")
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(html))
            
    def _escape(self, text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
