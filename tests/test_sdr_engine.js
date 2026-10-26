const assert = require('assert');
const { BlockType, Operation, Block, LayoutAnalyzer, Exporter } = require('../js/sdr-engine.js');

console.log("=== INICIANDO SUITE DE PRUEBAS PARA SDR-ENGINE ===");

// TEST 1: Creación de Bloque y Provenance Inicial
console.log("Test 1: Creación de Bloque y Trazabilidad (Provenance)");
const blk = new Block({
  type: BlockType.EQUATION,
  content: "E = mc^2",
  latex: "E = m c^2",
  bbox: [100, 250, 400, 40],
  confidence: 0.98
});
assert.strictEqual(blk.type, BlockType.EQUATION, "Tipo debe ser EQUATION");
assert.strictEqual(blk.confidence, 0.98, "Confianza debe ser 0.98");
assert.strictEqual(blk.isUncertain, false, "Confianza 0.98 no debe ser incierta");
assert.strictEqual(blk.provenance.length, 1, "Debe tener 1 registro inicial de provenance");
assert.strictEqual(blk.provenance[0].operation, Operation.OBSERVED, "Operación inicial debe ser OBSERVED");
console.log("  -> OK: Bloque y provenance inicial validados.");

// TEST 2: Corrección Humana e Inmutabilidad de Historial
console.log("Test 2: Auditoría de Corrección Humana");
const uncertainBlk = new Block({
  type: BlockType.TEXT,
  content: "The velo[UNCERTAIN] of light is constant",
  confidence: 0.72
});
assert.strictEqual(uncertainBlk.isUncertain, true, "Debe marcarse como incierto");

uncertainBlk.addCorrection("The velocity of light is constant", "Corrección de OCR por revisor");
assert.strictEqual(uncertainBlk.content, "The velocity of light is constant");
assert.strictEqual(uncertainBlk.isUncertain, false, "Tras corrección no debe ser incierto");
assert.strictEqual(uncertainBlk.confidence, 1.0, "Confianza debe subir a 1.0");
assert.strictEqual(uncertainBlk.provenance.length, 2, "Debe preservar historial (2 entradas)");
assert.strictEqual(uncertainBlk.provenance[1].operation, Operation.HUMAN_CORRECTED);
console.log("  -> OK: Auditoría forense de correcciones validada.");

// TEST 3: Algoritmo de Orden de Lectura en Columnas
console.log("Test 3: Análisis de Layout y Reading Order");
const rawBlocks = [
  new Block({ id: "right_col", bbox: [450, 200, 300, 100], content: "Columna Derecha Párrafo 1" }),
  new Block({ id: "title", bbox: [50, 50, 700, 60], content: "Título a todo lo ancho" }),
  new Block({ id: "left_col", bbox: [50, 200, 300, 100], content: "Columna Izquierda Párrafo 1" })
];

const ordered = LayoutAnalyzer.solveReadingOrder(rawBlocks, 800);
assert.strictEqual(ordered[0].id, "title", "El título superior debe leerse primero (Reading Order 1)");
assert.strictEqual(ordered[1].id, "left_col", "La columna izquierda debe leerse antes que la derecha (Reading Order 2)");
assert.strictEqual(ordered[2].id, "right_col", "La columna derecha debe leerse en tercer lugar (Reading Order 3)");
console.log("  -> OK: Orden canónico de lectura de dos columnas verificado.");

// TEST 4: Exportación LaTeX y Markdown
console.log("Test 4: Expositores Semánticos (LaTeX & Markdown)");
const tex = Exporter.toLaTeX("Zur Elektrodynamik", "A. Einstein", [blk]);
assert.ok(tex.includes("\\begin{equation}"), "Debe incluir entorno equation de LaTeX");
assert.ok(tex.includes("E = m c^2"), "Debe contener fórmula en LaTeX");

const md = Exporter.toMarkdown("Zur Elektrodynamik", "A. Einstein", [blk]);
assert.ok(md.includes("$$"), "Markdown debe incluir delimitador KaTeX $$");
console.log("  -> OK: Expositores semánticos validados.");

console.log("\n============================================================");
console.log(" TODOS LOS TESTS DE SCIENTIFIC-DOC-RECONSTRUCTOR PASARON (4/4)");
console.log("============================================================");
