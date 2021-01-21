import pytest
from scientific_document_reconstructor.core.models import Document, Page, Block, BlockType, Operation

def test_document_creation():
    doc = Document()
    assert doc.id is not None
    assert len(doc.pages) == 0

def test_provenance_tracking():
    block = Block(type=BlockType.TEXT)
    block.add_provenance(Operation.OBSERVED, notes="Test")
    assert len(block.provenance) == 1
    assert block.provenance[0].operation == Operation.OBSERVED
    assert block.provenance[0].notes == "Test"

def test_page_blocks():
    page = Page(page_number=1, width=800, height=1000)
    block = Block(type=BlockType.TEXT, content="Hello")
    page.blocks.append(block)
    
    doc = Document(pages=[page])
    fetched_block = doc.get_block_by_id(block.id)
    assert fetched_block is not None
    assert fetched_block.content == "Hello"
