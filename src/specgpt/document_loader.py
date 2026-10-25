
from pathlib import Path

from docx import Document
from docx.document import Document as _Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl


def iter_block_items(parent):
    """Yield paragraphs and tables in their original document order."""

    if isinstance(parent, _Document):
        parent_element = parent.element.body
    else:
        parent_element = parent._tc

    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def extract_blocks(document):
    """Extract paragraphs and tables into structured dictionaries."""

    blocks = []

    for block in iter_block_items(document):
        if isinstance(block, Paragraph):
            text = block.text.strip()

            if text:
                blocks.append({
                    "type": "paragraph",
                    "text": text,
                    "metadata": {
                        "style": block.style.name
                    }
                })

        elif isinstance(block, Table):
            rows = [
                [cell.text.strip() for cell in row.cells]
                for row in block.rows
            ]

            blocks.append({
                "type": "table",
                "text": rows,
                "metadata": {
                    "rows": len(rows),
                    "columns": max(
                        (len(row) for row in rows),
                        default=0
                    )
                }
            })

    return blocks


def load_document(file_path):
    """Load a DOCX file and return its extracted blocks."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Specification document not found: {path}"
        )

    if path.suffix.lower() != ".docx":
        raise ValueError("Only .docx files are supported.")

    document = Document(str(path))
    blocks = extract_blocks(document)

    return blocks
