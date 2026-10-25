
def build_context(results):
    """Format retrieved chunks and source metadata for an LLM prompt."""

    context_parts = []

    for rank, result in enumerate(results, start=1):
        chunk = result["chunk"]
        score = result["score"]

        context_parts.append(
            f"""[Source {rank}]
Document ID: {chunk.metadata.get('document_id')}
Version: {chunk.metadata.get('document_version')}
Source: {chunk.metadata.get('source_filename')}
Section: {chunk.metadata.get('section')}
Subsection: {chunk.metadata.get('subsection')}
Similarity Score: {score:.4f}

Content:
{chunk.text}
"""
        )

    return "\n\n".join(context_parts)
