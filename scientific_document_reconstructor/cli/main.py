import typer
import os
from typing import Optional
from ..pipeline.manager import PipelineManager
from ..pipeline.ingestion import IngestionPipeline
from ..pipeline.layout import LayoutAnalyzer
from ..pipeline.ocr_text import TextRecognizer
from ..exporters.latex import LatexExporter
from rich.console import Console

app = typer.Typer(help="Scientific Document Reconstructor CLI")
console = Console()

@app.command()
def inspect(pdf_path: str):
    """Inspects a PDF and prints basic metadata."""
    console.print(f"[bold green]Inspecting {pdf_path}[/bold green]")
    import pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            console.print(f"Pages: {len(pdf.pages)}")
            console.print(f"Metadata: {pdf.metadata}")
    except Exception as e:
        console.print(f"[red]Error reading PDF: {e}[/red]")

@app.command()
def reconstruct(pdf_path: str, profile: str = "default", project_dir: Optional[str] = None):
    """Reconstructs a document from a PDF scan."""
    if project_dir_ := project_dir:
        out_dir = project_dir_
    else:
        out_dir = pdf_path + ".sdr"
    
    console.print(f"[bold blue]Initializing project at {out_dir}[/bold blue]")
    manager = PipelineManager(out_dir)
    manager.init_from_pdf(pdf_path)
    
    console.print("Extracting pages...")
    ingestion = IngestionPipeline(manager)
    ingestion.process()
    
    console.print("Analyzing layout...")
    layout = LayoutAnalyzer(manager)
    layout.process()
    
    console.print("Recognizing text...")
    ocr = TextRecognizer(manager)
    ocr.process()
    
    console.print(f"[bold green]Reconstruction complete. Saved to {out_dir}[/bold green]")

@app.command()
def export(project_dir: str, format: str = "latex"):
    """Exports a reconstructed project to a specific format."""
    manager = PipelineManager(project_dir)
    manager.load_project()
    
    if format == "latex":
        exporter = LatexExporter(manager)
        out_dir = os.path.join(project_dir, "export")
        exporter.export(out_dir)
        console.print(f"[bold green]Exported LaTeX to {out_dir}[/bold green]")
    else:
        console.print(f"[red]Format {format} not supported yet.[/red]")

@app.command()
def review(project_dir: str, port: int = 8000):
    """Launch the local human review interface."""
    import uvicorn
    import os
    console.print(f"[bold green]Starting review server on port {port}...[/bold green]")
    os.environ["SDR_PROJECT_DIR"] = project_dir
    uvicorn.run("scientific_document_reconstructor.ui.app:app", host="127.0.0.1", port=port, reload=False)

if __name__ == "__main__":
    app()
