
from specgpt.chunker import create_chunks


def test_create_chunks_creates_expected_chunk():
    blocks = [
        {
            "type": "paragraph",
            "text": "1. Purpose",
            "metadata": {"style": "Heading 1"},
        },
        {
            "type": "paragraph",
            "text": "This document describes the system.",
            "metadata": {"style": "Normal"},
        },
    ]

    document_metadata = {
        "Document ID": "TEST-001",
        "Version": "1.0",
        "source_filename": "test.docx",
    }

    chunks = create_chunks(blocks, document_metadata)

    assert len(chunks) == 1
    assert "1. Purpose" in chunks[0].text
    assert "This document describes the system." in chunks[0].text
    assert chunks[0].metadata["document_id"] == "TEST-001"
    assert chunks[0].metadata["document_version"] == "1.0"
    assert chunks[0].metadata["source_filename"] == "test.docx"
