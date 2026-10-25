from pathlib import Path

from specgpt.document_loader import load_document
from specgpt.chunker import (
    add_section_context,
    extract_document_metadata,
    create_chunks,
)
from specgpt.embeddings import load_embedding_model, embed_chunks
from specgpt.retriever import retrieve_chunks
from specgpt.context_builder import build_context
from specgpt.generator import generate_answer

def prepare_document(file_path, embedding_model=None):
    """Load a specification and prepare it for semantic search."""

    # Step 1: Load the document
    blocks = load_document(file_path)

    # Step 2: Extract document metadata
    document_metadata = extract_document_metadata(blocks)

    # Step 3: Add section and subsection context
    blocks = add_section_context(blocks)

    # Step 4: Add the source filename to document metadata
    document_metadata["source_filename"] = Path(file_path).name

    # Step 5: Create document chunks
    chunks = create_chunks(blocks, document_metadata)

    # Step 6: Load the embedding model if one wasn't provided
    if embedding_model is None:
        embedding_model = load_embedding_model()

    # Step 7: Generate embeddings for all chunks
    chunk_embeddings = embed_chunks(embedding_model, chunks)

    # Step 8: Return everything needed for retrieval
    return {
        "document_metadata": document_metadata,
        "chunks": chunks,
        "embedding_model": embedding_model,
        "chunk_embeddings": chunk_embeddings,
    }

def ask_question(query, prepared_document, client, top_k=5):
    """Answer a question using the prepared specification document."""

    # Step 1: Retrieve the most relevant chunks
    results = retrieve_chunks(
        query=query,
        model=prepared_document["embedding_model"],
        chunks=prepared_document["chunks"],
        chunk_embeddings=prepared_document["chunk_embeddings"],
        top_k=top_k,
    )

    # Step 2: Build context from the retrieved chunks
    context = build_context(results)

    # Step 3: Generate an answer using the LLM
    answer = generate_answer(
        client=client,
        query=query,
        context=context,
    )

    # Step 4: Return the answer and its supporting sources
    return {
        "question": query,
        "answer": answer,
        "sources": results,
    }