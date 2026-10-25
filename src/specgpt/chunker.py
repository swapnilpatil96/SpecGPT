
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:
    """A meaningful section of a specification document."""

    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


def add_section_context(blocks):
    """Attach the current heading and subsection to each block."""

    current_section = None
    current_subsection = None

    for block in blocks:
        if block["type"] != "paragraph":
            continue

        style = block["metadata"].get("style", "")
        text = block["text"]

        if style == "Heading 1":
            current_section = text
            current_subsection = None

        elif style == "Heading 2":
            current_subsection = text

        block["metadata"]["section"] = current_section
        block["metadata"]["subsection"] = current_subsection

    return blocks


def extract_document_metadata(blocks):
    """Extract metadata from a table with Document Item and Value headers."""

    metadata = {}

    for block in blocks:
        if block["type"] != "table":
            continue

        table = block["text"]

        if not table or len(table[0]) != 2:
            continue

        headers = [cell.strip().lower() for cell in table[0]]

        if headers == ["document item", "value"]:
            for row in table[1:]:
                if len(row) == 2:
                    key = row[0].strip()
                    value = row[1].strip()

                    if key and value:
                        metadata[key] = value

            break

    return metadata




def create_chunks(blocks, document_metadata):
    """Create chunks using the document's heading structure."""

    chunks = []
    current_section = None
    current_subsection = None
    current_text = []

    def save_current_chunk():
        if not current_text:
            return

        text = "\n".join(current_text).strip()

        if text:
            chunks.append(
                DocumentChunk(
                    text=text,
                    metadata={
                        "document_id": document_metadata.get("Document ID"),
                        "document_version": document_metadata.get("Version"),
                        "source_filename": document_metadata.get(
                            "source_filename"
                        ),
                        "section": current_section,
                        "subsection": current_subsection,
                    },
                )
            )

        current_text.clear()

    for block in blocks:
        if block["type"] == "paragraph":
            style = block["metadata"].get("style", "")
            text = block["text"].strip()

            if style == "Heading 1":
                # Save the previous section before starting a new one.
                save_current_chunk()
                current_section = text
                current_subsection = None
                current_text.append(text)

            elif style == "Heading 2":
                # Start a new subsection chunk only if one already exists.
                if current_subsection is not None:
                    save_current_chunk()

                current_subsection = text
                current_text.append(text)

            elif text:
                current_text.append(text)

        elif block["type"] == "table":
            rows = block["text"]

            if rows:
                table_text = "\n".join(
                    " | ".join(cell.strip() for cell in row)
                    for row in rows
                )
                current_text.append(table_text)

    save_current_chunk()
    return chunks