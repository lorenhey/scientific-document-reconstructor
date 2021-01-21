from enum import Enum
from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field
import uuid
import datetime

class BlockType(str, Enum):
    TEXT = "text"
    EQUATION = "equation"
    TABLE = "table"
    FIGURE = "figure"
    HEADING = "heading"
    CAPTION = "caption"
    FOOTNOTE = "footnote"
    UNKNOWN = "unknown"

class Operation(str, Enum):
    OBSERVED = "OBSERVED"
    RECOGNIZED = "RECOGNIZED"
    INFERRED = "INFERRED"
    NORMALIZED = "NORMALIZED"
    CORRECTED = "CORRECTED"
    UNRESOLVED = "UNRESOLVED"

class Provenance(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    operation: Operation
    agent: str = "machine"
    recognizer: Optional[str] = None
    previous_value: Optional[str] = None
    confidence: Optional[float] = None
    notes: Optional[str] = None

class BoundingBox(BaseModel):
    # x0, y0, x1, y1 in pixels or relative coordinates
    x0: float
    y0: float
    x1: float
    y1: float

class Block(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: BlockType
    content: Optional[str] = None
    bbox: Optional[BoundingBox] = None
    provenance: List[Provenance] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_provenance(self, operation: Operation, **kwargs):
        prov = Provenance(operation=operation, **kwargs)
        self.provenance.append(prov)

class EquationBlock(Block):
    type: BlockType = BlockType.EQUATION
    latex: Optional[str] = None
    is_display: bool = True
    number: Optional[str] = None

class TableBlock(Block):
    type: BlockType = BlockType.TABLE
    csv_content: Optional[str] = None
    caption_id: Optional[str] = None

class FigureBlock(Block):
    type: BlockType = BlockType.FIGURE
    image_path: Optional[str] = None
    caption_id: Optional[str] = None

class Page(BaseModel):
    page_number: int
    width: float
    height: float
    blocks: List[Union[EquationBlock, TableBlock, FigureBlock, Block]] = Field(default_factory=list)
    image_path: Optional[str] = None

class DocumentMetadata(BaseModel):
    title: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    date: Optional[str] = None
    doi: Optional[str] = None

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    pages: List[Page] = Field(default_factory=list)
    source_path: Optional[str] = None
    source_sha256: Optional[str] = None

    def get_block_by_id(self, block_id: str) -> Optional[Block]:
        for page in self.pages:
            for block in page.blocks:
                if block.id == block_id:
                    return block
        return None
