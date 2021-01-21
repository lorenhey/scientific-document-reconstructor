import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ..pipeline.manager import PipelineManager

app = FastAPI(title="SDR Review Interface")

# We will inject the project dir at runtime
PROJECT_DIR = os.getenv("SDR_PROJECT_DIR", "")
manager = None

@app.on_event("startup")
def startup_event():
    global manager
    if not PROJECT_DIR or not os.path.exists(PROJECT_DIR):
        raise RuntimeError("SDR_PROJECT_DIR environment variable must be set to a valid project directory.")
    manager = PipelineManager(PROJECT_DIR)
    manager.load_project()
    # Serve pages directory
    app.mount("/pages", StaticFiles(directory=os.path.join(PROJECT_DIR, "pages")), name="pages")

@app.get("/", response_class=HTMLResponse)
def index():
    doc = manager.document
    html = f"""
    <html>
    <head>
        <title>SDR Review: {doc.metadata.title or 'Document'}</title>
        <style>
            body {{ font-family: sans-serif; margin: 0; display: flex; }}
            #sidebar {{ width: 250px; background: #f0f0f0; padding: 10px; height: 100vh; overflow-y: auto; }}
            #content {{ flex: 1; padding: 20px; overflow-y: auto; height: 100vh; }}
            .page-thumb {{ cursor: pointer; padding: 5px; margin-bottom: 5px; background: #ddd; }}
            .page-thumb:hover {{ background: #ccc; }}
            .block {{ border: 1px solid #999; margin-bottom: 10px; padding: 10px; }}
            .uncertain {{ border-color: red; background: #fff0f0; }}
            .facsimile {{ max-width: 100%; border: 1px solid #ccc; }}
        </style>
    </head>
    <body>
        <div id="sidebar">
            <h3>Pages</h3>
            {"".join(f'<div class="page-thumb" onclick="loadPage({p.page_number})">Page {p.page_number}</div>' for p in doc.pages)}
        </div>
        <div id="content">
            <h2>Select a page to review</h2>
            <div id="page-view"></div>
        </div>
        <script>
            async function loadPage(pageNum) {{
                const res = await fetch(`/api/pages/${{pageNum}}`);
                const page = await res.json();
                
                let html = `<h3>Page ${{page.page_number}}</h3>`;
                html += `<div style="display: flex; gap: 20px;">`;
                html += `<div style="flex: 1;"><img src="/pages/page_${{String(pageNum).padStart(4, '0')}}.png" class="facsimile" /></div>`;
                html += `<div style="flex: 1;"><h4>Blocks</h4>`;
                
                page.blocks.forEach(b => {{
                    const isUncertain = b.provenance.some(p => p.operation === 'UNRESOLVED');
                    const cls = isUncertain ? "block uncertain" : "block";
                    html += `<div class="${{cls}}">
                        <strong>${{b.type}}</strong><br/>
                        <textarea style="width:100%; height:80px;" onchange="updateBlock('${{b.id}}', this.value)">${{b.content || ''}}</textarea>
                    </div>`;
                }});
                
                html += `</div></div>`;
                document.getElementById('page-view').innerHTML = html;
            }}
            
            async function updateBlock(blockId, newContent) {{
                await fetch(`/api/blocks/${{blockId}}`, {{
                    method: 'PUT',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{content: newContent}})
                }});
            }}
        </script>
    </body>
    </html>
    """
    return html

@app.get("/api/pages/{page_num}")
def get_page(page_num: int):
    for page in manager.document.pages:
        if page.page_number == page_num:
            return page
    raise HTTPException(status_code=404, detail="Page not found")

class BlockUpdate(BaseModel):
    content: str

@app.put("/api/blocks/{block_id}")
def update_block(block_id: str, update: BlockUpdate):
    block = manager.document.get_block_by_id(block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    # Audit trail
    block.add_provenance(
        operation="CORRECTED",
        agent="human",
        previous_value=block.content
    )
    block.content = update.content
    manager.save_project()
    return {"status": "ok"}
