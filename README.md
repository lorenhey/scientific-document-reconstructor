# SCIENTIFIC DOCUMENT RECONSTRUCTOR

> A scanned scientific paper is not a document. It is a photograph of one.

**Scientific Document Reconstructor (SDR)** is an open-source system for transforming scanned pages into structured, semantically meaningful, and auditable digital editions.

Recovering the words is only the first half of reconstructing a scientific paper. Most OCR engines output a flat stream of text, oblivious to the fact that scientific literature is built on structure: sections, equations, tables, figures, captions, and references. SDR is built to recover the *document* behind the image.

## Features

- **Document Structure Recovery:** Infers reading order, columns, headings, and paragraph boundaries.
- **Mathematical Integrity:** Reconstructs inline and display equations, recognizing numbered formulas.
- **Tables and Figures:** Extracts figures, structural tables, and associates them with their proper captions.
- **Provenance and Auditability:** Every recognized block maintains a trace to its bounding box on the original scan. Manual corrections are stored without deleting the machine's initial output.
- **Explicit Uncertainty:** If an equation or word cannot be confidently read, it is explicitly flagged (e.g. `[UNCERTAIN]`) rather than silently hallucinated.
- **Rich Export:** Outputs semantic LaTeX, structured JSON, Markdown, and HTML.

## Pipeline Overview

The reconstruction pipeline is highly modular and avoids destroying the original representation:

1. **Ingestion & Profiling:** Inspects the PDF/images, determines dimensions, and extracts embedded text if available.
2. **Image Preprocessing:** Safely corrects rotation, skew, and normalizes contrast without modifying the immutable source files.
3. **Layout Analysis:** Detects regions, columns, equations, figures, and establishes reading order.
4. **Text & Math Recognition:** Applies specialized OCR backends to text regions and mathematical regions independently.
5. **Semantic Structuring:** Assembles regions into a logical Document Model.
6. **Validation & Review:** Flags low-confidence regions for human-in-the-loop review.
7. **Export:** Generates target formats like LaTeX or JSON.

## Installation

This project requires Python 3.9+ and depends on system libraries for image manipulation and PDF rendering (like Poppler).

```bash
# Clone the repository
git clone https://github.com/lorenhey/scientific-document-reconstructor.git
cd scientific-document-reconstructor

# Install dependencies (consider using a virtual environment)
pip install -e .
```

You also need Tesseract OCR installed on your system if you use the default text recognition backend.

## CLI Usage

SDR provides a powerful command-line interface for batch processing and inspection.

```bash
# Reconstruct a document
sdr reconstruct paper.pdf

# Reconstruct using a specific profile (e.g. for historical documents)
sdr reconstruct 19th_century_paper.pdf --profile historical

# Export an already processed project to LaTeX
sdr export project.sdr --format latex

# Generate a final validation report
sdr validate project.sdr
```

## Review Interface

Automatic extraction of scientific data is inherently risky. SDR includes a local visual review interface to inspect the layout, compare the OCR with the original scan, and correct mistakes.

```bash
sdr review project.sdr
```

## Formats and Outputs

By default, the pipeline generates a standalone project directory (`.sdr` format internally handled as JSON) that keeps the immutable source, page checkpoints, and block metadata.
You can export this to:
- **LaTeX:** Semantic LaTeX (using `\section`, `\begin{equation}`, etc.).
- **JSON:** Fully structured representation for programmatic use.
- **Markdown/HTML:** For web reading.

## Limitations

- **Handwritten Notes:** Marginalia or handwritten text is often unresolvable.
- **Poor Scans:** Extreme bleed-through or warped pages degrade both layout and recognition.
- **Historical Typography:** Fraktur or 17th-century ligatures require specific models not loaded by default.
- **Mathematical Accuracy:** OCR on dense, poorly printed mathematics is imperfect. Do not trust scientific values (exponents, signs, constants) extracted automatically without human review.

## Contributing

We welcome contributions to backends (new OCR engines, better layout detection), exporters (e.g. TEI), and synthetic benchmarks. See `CONTRIBUTING.md` for guidelines.

## License

MIT License. See `LICENSE` for details.
