# SCIENTIFIC DOCUMENT RECONSTRUCTOR (v2.0.0)

[![GitHub Pages Deployment](https://img.shields.io/badge/GitHub%20Pages-Live%20v2.0.0-emerald)](https://lorenhey.github.io/scientific-document-reconstructor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standards: LaTeX / KaTeX / Provenance](https://img.shields.io/badge/Standards-LaTeX%20%7C%20KaTeX%20%7C%20Provenance-amber.svg)](https://lorenhey.github.io/scientific-document-reconstructor/)

> *A scanned scientific paper is not a document. It is a photograph of one.*  
> **Scientific Document Reconstructor (SDR)** es un sistema de ingeniería y arqueología documental para transformar páginas escaneadas en ediciones digitales estructuradas, semánticamente íntegras y forensemente auditables.

🔗 **Mesa de Reconstrucción Interactiva:** [https://lorenhey.github.io/scientific-document-reconstructor/](https://lorenhey.github.io/scientific-document-reconstructor/)

---

## 🔬 Capacidades Principales (v2.0.0)

1. **Recuperación Estructural & Orden Canónico de Lectura (Reading Order):**
   * Descompone la página en bloques topológicos (títulos, encabezados, párrafos a dos columnas, figuras y tablas).
   * Algoritmo de ordenación de flujo de lectura que reensambla columnas independientes sin mezclar líneas adyacentes.

2. **Integridad Matemática & Fórmulas en LaTeX:**
   * Reconoce y reconstruye ecuaciones en línea y en bloque numerado con renderizado tipográfico en KaTeX y exportación a LaTeX nativo (\begin{equation} ... \end{equation}).

3. **Incertidumbre Explícita vs Alucinación Silenciosa:**
   * Cuando un carácter, palabra o símbolo matemático no alcanza el umbral de certeza (< 85%), SDR lo marca formalmente como [UNCERTAIN] en lugar de alucinar un texto inventado.

4. **Trazabilidad Forense & Auditoría Inmutable (Provenance):**
   * Cada bloque mantiene un enlace bidireccional exacto con su *Bounding Box* en las coordenadas del escaneo original.
   * Cualquier corrección o edición humana no destruye la salida de la máquina: se registra cronológicamente en una cadena inmutable de operaciones (OBSERVED -> NORMALIZED -> HUMAN_CORRECTED).

5. **Exportación Multiformato:**
   * Exportación instantánea a documento compilable de **LaTeX** (.tex), modelo **JSON** estructurado y **Markdown** semántico.

---

## 🧪 Pruebas Unitarias

`ash
# Tests de la suite JavaScript / Web
node tests/test_sdr_engine.js

# Tests del motor Python
pytest
`

---

## 📄 Licencia

Código abierto bajo licencia [MIT](LICENSE). Desarrollado por **Lorenzo Perez** ([@lorenhey](https://github.com/lorenhey)).
