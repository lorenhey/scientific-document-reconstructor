/**
 * sdr-engine.js - Motor de Reconstrucción de Documentos Científicos (SDR)
 * Modela estructuras lógicas, análisis de columnas, trazabilidad/provenance,
 * incertidumbre explícita y exportación a LaTeX / JSON / Markdown.
 */

const BlockType = {
  HEADING: "HEADING",
  TEXT: "TEXT",
  EQUATION: "EQUATION",
  TABLE: "TABLE",
  FIGURE: "FIGURE",
  CAPTION: "CAPTION"
};

const Operation = {
  OBSERVED: "OBSERVED",
  NORMALIZED: "NORMALIZED",
  EQUATION_RECONSTRUCTED: "EQUATION_RECONSTRUCTED",
  HUMAN_CORRECTED: "HUMAN_CORRECTED",
  UNCERTAIN: "UNCERTAIN"
};

class Block {
  constructor({ id, type, content, latex = null, bbox = [0, 0, 100, 20], confidence = 0.95, column = 0 }) {
    this.id = id || `blk_${Math.random().toString(36).substring(2, 9)}`;
    this.type = type || BlockType.TEXT;
    this.content = content || "";
    this.latex = latex;
    this.bbox = bbox; // [x, y, width, height] en % o px
    this.confidence = Number(confidence);
    this.column = column;
    this.readingOrder = 0;
    this.isUncertain = this.confidence < 0.85 || this.content.includes("[UNCERTAIN]");
    this.provenance = [
      {
        operation: Operation.OBSERVED,
        timestamp: new Date().toISOString(),
        notes: `Extracción inicial OCR (Confianza: ${Math.round(this.confidence * 100)}%)`
      }
    ];
  }

  addCorrection(newContent, notes = "Corrección manual por revisor humano") {
    this.content = newContent;
    this.isUncertain = false;
    this.confidence = 1.0;
    this.provenance.push({
      operation: Operation.HUMAN_CORRECTED,
      timestamp: new Date().toISOString(),
      notes
    });
  }
}

class LayoutAnalyzer {
  /**
   * Ordena los bloques según el orden de lectura humano (Reading Order)
   * Detecta bloques a todo lo ancho (título, abstract) y columnas (izq/der).
   */
  static solveReadingOrder(blocks, pageWidth = 800) {
    const xMid = pageWidth / 2;

    // Clasificar bloques
    const fullWidth = [];
    const colLeft = [];
    const colRight = [];

    blocks.forEach(b => {
      const [x, y, w, h] = b.bbox;
      if (w > pageWidth * 0.65) {
        fullWidth.push(b);
      } else if (x + w / 2 < xMid) {
        b.column = 1;
        colLeft.push(b);
      } else {
        b.column = 2;
        colRight.push(b);
      }
    });

    // Ordenar verticalmente cada grupo
    fullWidth.sort((a, b) => a.bbox[1] - b.bbox[1]);
    colLeft.sort((a, b) => a.bbox[1] - b.bbox[1]);
    colRight.sort((a, b) => a.bbox[1] - b.bbox[1]);

    // Combinar en orden canónico
    const ordered = [];
    let orderIndex = 1;

    // Encabezados / títulos superiores
    const topHeaders = fullWidth.filter(b => b.bbox[1] < (colLeft[0]?.bbox[1] || 9999));
    topHeaders.forEach(b => {
      b.readingOrder = orderIndex++;
      ordered.push(b);
    });

    // Columna izquierda
    colLeft.forEach(b => {
      b.readingOrder = orderIndex++;
      ordered.push(b);
    });

    // Columna derecha
    colRight.forEach(b => {
      b.readingOrder = orderIndex++;
      ordered.push(b);
    });

    // Elementos a todo lo ancho inferiores (tablas, figuras finales, referencias)
    const bottomFull = fullWidth.filter(b => !topHeaders.includes(b));
    bottomFull.forEach(b => {
      b.readingOrder = orderIndex++;
      ordered.push(b);
    });

    return ordered;
  }
}

class Exporter {
  /**
   * Exporta a documento LaTeX limpio y estructurado
   */
  static toLaTeX(docTitle, authors, blocks) {
    let tex = `\\documentclass[11pt,a4paper]{article}\n`;
    tex += `\\usepackage[utf8]{inputenc}\n\\usepackage{amsmath,amssymb,graphicx,booktabs}\n\n`;
    tex += `\\title{${docTitle}}\n\\author{${authors}}\n\\date{\\today}\n\n`;
    tex += `\\begin{document}\n\\maketitle\n\n`;

    blocks.forEach(b => {
      if (b.type === BlockType.HEADING) {
        tex += `\\section{${b.content}}\n\n`;
      } else if (b.type === BlockType.EQUATION) {
        tex += `\\begin{equation}\n  ${b.latex || b.content}\n\\end{equation}\n\n`;
      } else if (b.type === BlockType.TABLE) {
        tex += `% [Table: ${b.content}]\n\\begin{table}[htbp]\n  \\centering\n  \\begin{tabular}{ll}\n    \\toprule\n    Param & Value \\\\\n    \\midrule\n    ... & ... \\\\\n    \\bottomrule\n  \\end{tabular}\n\\end{table}\n\n`;
      } else if (b.type === BlockType.FIGURE) {
        tex += `% [Figure: ${b.content}]\n\\begin{figure}[htbp]\n  \\centering\n  \\caption{${b.content}}\n\\end{figure}\n\n`;
      } else {
        tex += `${b.content}\n\n`;
      }
    });

    tex += `\\end{document}\n`;
    return tex;
  }

  /**
   * Exporta a Markdown semántico
   */
  static toMarkdown(docTitle, authors, blocks) {
    let md = `# ${docTitle}\n\n*${authors}*\n\n---\n\n`;
    blocks.forEach(b => {
      if (b.type === BlockType.HEADING) {
        md += `## ${b.content}\n\n`;
      } else if (b.type === BlockType.EQUATION) {
        md += `$$\n${b.latex || b.content}\n$$\n\n`;
      } else if (b.type === BlockType.FIGURE) {
        md += `> **Figura:** *${b.content}*\n\n`;
      } else {
        md += `${b.content}\n\n`;
      }
    });
    return md;
  }
}

// Exportación compatible Node y Browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { BlockType, Operation, Block, LayoutAnalyzer, Exporter };
}
