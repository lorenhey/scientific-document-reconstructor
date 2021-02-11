import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "The Thermodynamics of Synthetic Documents")
    
    # Author
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 92, "L. Perez and M. Curie")
    
    # Abstract
    c.setFont("Helvetica-Oblique", 10)
    text = "Abstract: This paper presents a synthetic approach to testing document reconstruction pipelines."
    c.drawString(72, height - 120, text)
    
    # Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 160, "1. Introduction")
    
    # Paragraph
    c.setFont("Helvetica", 11)
    text = "We propose that a document is not merely a collection of pixels, but a structured sequence of information."
    c.drawString(72, height - 180, text)
    
    # Equation
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 220, "E = mc^2")
    c.drawString(500, height - 220, "(1)")
    
    # Paragraph
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 260, "Where E is energy, m is mass, and c is the speed of light.")
    
    c.save()

if __name__ == "__main__":
    generate_pdf("samples/synthetic_paper.pdf")
