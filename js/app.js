/**
 * app.js - Lógica interactiva para scientific-document-reconstructor v2.0.0
 */

const PRESETS = {
  einstein_1905: {
    id: "einstein_1905",
    title: "Zur Elektrodynamik bewegter Körper",
    authors: "A. Einstein (Annalen der Physik, 17, 891–921, 1905)",
    paperDate: "1905",
    blocks: [
      new Block({
        id: "b_title",
        type: BlockType.HEADING,
        content: "Zur Elektrodynamik bewegter Körper",
        bbox: [50, 40, 700, 45],
        confidence: 0.99
      }),
      new Block({
        id: "b_author",
        type: BlockType.TEXT,
        content: "Von A. Einstein (Bern)",
        bbox: [260, 95, 280, 25],
        confidence: 0.98
      }),
      new Block({
        id: "b_sec1",
        type: BlockType.HEADING,
        content: "I. Kinematischer Teil. § 1. Definition der Gleichzeitigkeit",
        bbox: [50, 135, 700, 30],
        confidence: 0.96
      }),
      new Block({
        id: "b_text1",
        type: BlockType.TEXT,
        content: "Dass die Elektrodynamik Maxwells — wie dieselbe gegenwärtig aufgefasst zu werden pflegt — in ihrer Anwendung auf bewegte Körper zu Asymmetrien führt, welche den Phänomenen nicht anzuhaften scheinen, ist bekannt.",
        bbox: [50, 180, 340, 130],
        confidence: 0.94
      }),
      new Block({
        id: "b_text2",
        type: BlockType.TEXT,
        content: "Beispiele ähnlicher Art, sowie die misslungenen Versuche, eine Bewegung der Erde relativ zum »Licht[UNCERTAIN]« zu konstatieren, führen zu der Vermutung, dass dem Begriffe der absoluten Ruhe nicht nur in der Mechanik, sondern auch in der Elektrodynamik keine Eigenschaften der Erscheinungen entsprechen.",
        bbox: [50, 320, 340, 150],
        confidence: 0.78 // Con incertidumbre
      }),
      new Block({
        id: "b_sec2",
        type: BlockType.HEADING,
        content: "§ 2. Über die Relativität von Längen und Zeiten",
        bbox: [410, 180, 340, 30],
        confidence: 0.95
      }),
      new Block({
        id: "b_text3",
        type: BlockType.TEXT,
        content: "Wir setzen voraus, dass die Gesetze, nach denen sich die Zustände der physikalischen Systeme verändern, unabhängig seien davon, auf welches von zwei relativ zueinander in gleichförmiger Translationsbewegung befindlichen Koordinatensystemen diese Zustandsänderungen bezogen werden.",
        bbox: [410, 220, 340, 120],
        confidence: 0.96
      }),
      new Block({
        id: "b_eq1",
        type: BlockType.EQUATION,
        content: "\\tau = \\frac{t - \\frac{v}{c^2} x}{\\sqrt{1 - \\frac{v^2}{c^2}}}",
        latex: "\\tau = \\frac{t - \\frac{v}{c^2} x}{\\sqrt{1 - \\frac{v^2}{c^2}}}",
        bbox: [410, 355, 340, 50],
        confidence: 0.98
      }),
      new Block({
        id: "b_eq2",
        type: BlockType.EQUATION,
        content: "\\xi = \\frac{x - v t}{\\sqrt{1 - \\frac{v^2}{c^2}}}",
        latex: "\\xi = \\frac{x - v t}{\\sqrt{1 - \\frac{v^2}{c^2}}}",
        bbox: [410, 415, 340, 45],
        confidence: 0.97
      })
    ]
  },

  shannon_1948: {
    id: "shannon_1948",
    title: "A Mathematical Theory of Communication",
    authors: "C. E. Shannon (The Bell System Technical Journal, Vol. 27, 1948)",
    paperDate: "1948",
    blocks: [
      new Block({
        id: "b_title_s",
        type: BlockType.HEADING,
        content: "A Mathematical Theory of Communication",
        bbox: [50, 40, 700, 45],
        confidence: 0.99
      }),
      new Block({
        id: "b_author_s",
        type: BlockType.TEXT,
        content: "By C. E. SHANNON",
        bbox: [300, 95, 200, 25],
        confidence: 0.99
      }),
      new Block({
        id: "b_sec_intro",
        type: BlockType.HEADING,
        content: "Introduction",
        bbox: [50, 135, 700, 30],
        confidence: 0.98
      }),
      new Block({
        id: "b_text_intro",
        type: BlockType.TEXT,
        content: "The fundamental problem of communication is that of reproducing at one point either exactly or approximately a message selected at another point.",
        bbox: [50, 180, 340, 90],
        confidence: 0.97
      }),
      new Block({
        id: "b_sec_entropy",
        type: BlockType.HEADING,
        content: "Part I: Discrete Noiseless Systems. 6. Choice, Uncertainty and Entropy",
        bbox: [50, 280, 340, 40],
        confidence: 0.95
      }),
      new Block({
        id: "b_eq_entropy",
        type: BlockType.EQUATION,
        content: "H = - K \\sum_{i=1}^n p_i \\log_2 p_i",
        latex: "H = - K \\sum_{i=1}^n p_i \\log_2 p_i",
        bbox: [50, 335, 340, 50],
        confidence: 0.98
      }),
      new Block({
        id: "b_fig_comm",
        type: BlockType.FIGURE,
        content: "Fig. 1 — Schematic diagram of a general communication system (Information Source -> Transmitter -> Channel / Noise -> Receiver -> Destination)",
        bbox: [410, 180, 340, 160],
        confidence: 0.92
      }),
      new Block({
        id: "b_eq_capacity",
        type: BlockType.EQUATION,
        content: "C = W \\log_2 \\left(1 + \\frac{S}{N}\\right)",
        latex: "C = W \\log_2 \\left(1 + \\frac{S}{N}\\right)",
        bbox: [410, 355, 340, 50],
        confidence: 0.97
      })
    ]
  }
};

let currentDoc = JSON.parse(JSON.stringify(PRESETS.einstein_1905));
// Re-instanciar clases Block
currentDoc.blocks = currentDoc.blocks.map(b => new Block(b));

let selectedBlockId = null;

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initPresetSelector();
  renderScanCanvas();
  renderReconstructedDoc();
  attachEventListeners();
});

function initTabs() {
  const tabs = document.querySelectorAll('.nav-tab-btn');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(t => {
        t.classList.remove('active-tab');
        t.classList.add('inactive-tab');
      });
      btn.classList.add('active-tab');
      btn.classList.remove('inactive-tab');

      const targetId = btn.getAttribute('data-tab');
      document.querySelectorAll('.tab-content').forEach(sec => {
        sec.classList.add('hidden');
      });
      const activeSection = document.getElementById(`tab-${targetId}`);
      if (activeSection) activeSection.classList.remove('hidden');
    });
  });
}

function initPresetSelector() {
  const sel = document.getElementById('preset-selector');
  if (!sel) return;
  sel.innerHTML = Object.keys(PRESETS).map(k => `
    <option value="${k}">${PRESETS[k].title} (${PRESETS[k].paperDate})</option>
  `).join('');

  sel.addEventListener('change', (e) => {
    const k = e.target.value;
    currentDoc = JSON.parse(JSON.stringify(PRESETS[k]));
    currentDoc.blocks = currentDoc.blocks.map(b => new Block(b));
    selectedBlockId = null;
    renderScanCanvas();
    renderReconstructedDoc();
    updateAuditInspector();
  });
}

function renderScanCanvas() {
  const container = document.getElementById('scan-overlay-container');
  if (!container) return;
  container.innerHTML = '';

  const orderedBlocks = LayoutAnalyzer.solveReadingOrder(currentDoc.blocks, 800);

  orderedBlocks.forEach(b => {
    const [x, y, w, h] = b.bbox;
    const div = document.createElement('div');
    
    let typeClass = "bbox-text";
    if (b.type === BlockType.HEADING) typeClass = "bbox-heading";
    if (b.type === BlockType.EQUATION) typeClass = "bbox-equation";
    if (b.type === BlockType.TABLE) typeClass = "bbox-table";
    if (b.type === BlockType.FIGURE) typeClass = "bbox-figure";

    div.className = `bbox-overlay ${typeClass} ${b.id === selectedBlockId ? 'ring-2 ring-sky-400 bg-sky-400/20' : ''}`;
    div.style.left = `${(x / 800) * 100}%`;
    div.style.top = `${y}px`;
    div.style.width = `${(w / 800) * 100}%`;
    div.style.height = `${h}px`;
    div.title = `[Order #${b.readingOrder}] ${b.type} (Conf: ${Math.round(b.confidence * 100)}%)`;

    // Etiqueta de orden
    div.innerHTML = `<span class="absolute -top-3 -left-1 bg-slate-900 text-[9px] px-1 font-mono text-sky-300 border border-slate-700 rounded shadow">#${b.readingOrder}</span>`;

    div.addEventListener('click', () => {
      selectBlock(b.id);
    });

    container.appendChild(div);
  });
}

function renderReconstructedDoc() {
  const container = document.getElementById('reconstructed-content');
  if (!container) return;
  container.innerHTML = '';

  const orderedBlocks = LayoutAnalyzer.solveReadingOrder(currentDoc.blocks, 800);

  // KPIs
  const totalBlocks = orderedBlocks.length;
  const uncertainCount = orderedBlocks.filter(b => b.isUncertain).length;
  const eqCount = orderedBlocks.filter(b => b.type === BlockType.EQUATION).length;
  const meanConf = Math.round((orderedBlocks.reduce((acc, b) => acc + b.confidence, 0) / totalBlocks) * 100);

  document.getElementById('stat-total-blocks').textContent = totalBlocks;
  document.getElementById('stat-uncertain-blocks').textContent = uncertainCount;
  document.getElementById('stat-equations').textContent = eqCount;
  document.getElementById('stat-mean-conf').textContent = `${meanConf} %`;

  orderedBlocks.forEach(b => {
    const blkDiv = document.createElement('div');
    blkDiv.className = `p-3 rounded border transition-all cursor-pointer ${b.id === selectedBlockId ? 'bg-sky-950/40 border-sky-400 ring-1 ring-sky-400' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`;
    blkDiv.setAttribute('data-id', b.id);

    let badgeClass = "badge-high-conf";
    let badgeText = `${Math.round(b.confidence * 100)}% Conf`;
    if (b.isUncertain) {
      badgeClass = "badge-uncertain";
      badgeText = "INCERTIDUMBRE";
    }

    let innerContent = "";
    if (b.type === BlockType.HEADING) {
      innerContent = `<h3 class="text-base font-bold text-white font-serif">${b.content}</h3>`;
    } else if (b.type === BlockType.EQUATION) {
      innerContent = `<div class="py-2 text-center text-amber-300 font-mono katex-render" data-latex="${b.latex || b.content}">$$${b.latex || b.content}$$</div>`;
    } else if (b.type === BlockType.FIGURE) {
      innerContent = `<div class="p-3 bg-slate-950 rounded border border-slate-800 text-xs italic text-rose-300 text-center"><i class="fa-solid fa-image mr-1"></i> ${b.content}</div>`;
    } else {
      let textFormatted = b.content;
      if (b.isUncertain) {
        textFormatted = textFormatted.replace(/\[UNCERTAIN\]/g, `<span class="bg-amber-500/20 text-amber-300 px-1 border border-amber-500/40 rounded font-mono font-bold">[INCERTEZA OCR]</span>`);
      }
      innerContent = `<p class="text-xs text-slate-300 leading-relaxed font-serif">${textFormatted}</p>`;
    }

    blkDiv.innerHTML = `
      <div class="flex justify-between items-center mb-1 text-[10px] font-mono text-slate-500 border-b border-slate-800/60 pb-1">
        <span>#${b.readingOrder} • ${b.type}</span>
        <span class="px-1.5 py-0.2 rounded font-bold ${badgeClass}">${badgeText}</span>
      </div>
      ${innerContent}
    `;

    blkDiv.addEventListener('click', () => {
      selectBlock(b.id);
    });

    container.appendChild(blkDiv);
  });

  // Renderizar KaTeX
  if (window.renderMathInElement) {
    window.renderMathInElement(container, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false }
      ]
    });
  }
}

function selectBlock(blockId) {
  selectedBlockId = blockId;
  renderScanCanvas();
  renderReconstructedDoc();
  updateAuditInspector();
}

function updateAuditInspector() {
  const block = currentDoc.blocks.find(b => b.id === selectedBlockId);
  const container = document.getElementById('inspector-content');
  if (!container) return;

  if (!block) {
    container.innerHTML = `<div class="p-6 text-center text-xs text-slate-500">Seleccioná cualquier bloque en el escaneo o en la edición reconstruida para auditar su proveniencia forense.</div>`;
    return;
  }

  let provHistoryHtml = block.provenance.map(p => `
    <li class="border-l-2 border-sky-500 pl-3 py-1 space-y-0.5 text-xs">
      <div class="flex justify-between text-slate-400 font-mono text-[10px]">
        <span>${p.operation}</span>
        <span>${new Date(p.timestamp).toLocaleTimeString()}</span>
      </div>
      <div class="text-slate-200">${p.notes}</div>
    </li>
  `).join('');

  container.innerHTML = `
    <div class="space-y-4">
      <div class="flex justify-between items-center border-b border-slate-800 pb-2">
        <span class="text-xs font-bold text-sky-400 font-mono">${block.id} (#${block.readingOrder})</span>
        <span class="text-xs px-2 py-0.5 rounded ${block.isUncertain ? 'badge-uncertain' : 'badge-high-conf'} font-bold">
          ${Math.round(block.confidence * 100)}% Confianza
        </span>
      </div>

      <div class="text-xs space-y-1">
        <label class="text-slate-400 block font-bold">Contenido Reconocido:</label>
        <textarea id="edit-content-input" rows="4" class="w-full text-xs font-serif bg-slate-900 border border-slate-700 rounded p-2 text-white">${block.content}</textarea>
      </div>

      <div class="flex justify-end">
        <button id="apply-correction-btn" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded text-xs font-semibold flex items-center gap-1.5 shadow">
          <i class="fa-solid fa-stamp"></i> Registrar Corrección Forense
        </button>
      </div>

      <div class="pt-2 border-t border-slate-800 space-y-2">
        <label class="text-xs text-slate-400 block font-bold uppercase tracking-wider">Historial Inmutable de Provenance:</label>
        <ul class="space-y-2">
          ${provHistoryHtml}
        </ul>
      </div>
    </div>
  `;

  document.getElementById('apply-correction-btn')?.addEventListener('click', () => {
    const newText = document.getElementById('edit-content-input').value;
    block.addCorrection(newText, "Corrección validada por experto en transcripción histórica");
    renderScanCanvas();
    renderReconstructedDoc();
    updateAuditInspector();
  });
}

function attachEventListeners() {
  document.getElementById('export-latex-btn')?.addEventListener('click', exportLatex);
  document.getElementById('export-json-btn')?.addEventListener('click', exportJson);
  document.getElementById('export-md-btn')?.addEventListener('click', exportMarkdown);
}

function exportLatex() {
  const tex = Exporter.toLaTeX(currentDoc.title, currentDoc.authors, currentDoc.blocks);
  downloadFile(`${currentDoc.id}.tex`, 'text/x-tex', tex);
}

function exportJson() {
  const jsonStr = JSON.stringify(currentDoc, null, 2);
  downloadFile(`${currentDoc.id}_model.json`, 'application/json', jsonStr);
}

function exportMarkdown() {
  const md = Exporter.toMarkdown(currentDoc.title, currentDoc.authors, currentDoc.blocks);
  downloadFile(`${currentDoc.id}.md`, 'text/markdown', md);
}

function downloadFile(filename, mime, content) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
