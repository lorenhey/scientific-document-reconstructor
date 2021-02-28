from typing import Optional
from .pipeline.manager import PipelineManager
from .pipeline.ingestion import IngestionPipeline
from .pipeline.layout import LayoutAnalyzer
from .pipeline.ocr_text import TextRecognizer
from .pipeline.ocr_math import MathRecognizer
from .exporters.latex import LatexExporter

class Project:
    def __init__(self, project_dir: str):
        self.manager = PipelineManager(project_dir)
        try:
            self.manager.load_project()
        except FileNotFoundError:
            pass

    def export(self, format: str = "latex", output_dir: Optional[str] = None):
        if output_dir is None:
            output_dir = self.manager.project_dir + "_export"
            
        if format == "latex":
            exporter = LatexExporter(self.manager)
            exporter.export(output_dir)
        elif format == "json":
            from .exporters.json_exporter import JsonExporter
            exporter = JsonExporter(self.manager)
            exporter.export(output_dir)
        elif format == "html":
            from .exporters.html_exporter import HtmlExporter
            exporter = HtmlExporter(self.manager)
            exporter.export(output_dir)
        else:
            raise ValueError(f"Format {format} not supported.")

def reconstruct(pdf_path: str, project_dir: Optional[str] = None) -> Project:
    """High-level Python API for SDR."""
    if project_dir is None:
        project_dir = pdf_path + ".sdr"
        
    manager = PipelineManager(project_dir)
    manager.init_from_pdf(pdf_path)
    
    IngestionPipeline(manager).process()
    LayoutAnalyzer(manager).process()
    TextRecognizer(manager).process()
    MathRecognizer(manager).process()
    
    return Project(project_dir)
