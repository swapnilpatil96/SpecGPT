
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_chunks(query, model, chunks, chunk_embeddings, top_k=5):
    """Return the most relevant document chunks for a query."""

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if len(chunks) != len(chunk_embeddings):
        raise ValueError(
            "The number of chunks must match the number of embeddings."
        )

    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        chunk_embeddings,
    )[0]

    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "score": float(similarities[index]),
            "chunk": chunks[index],
        })

    return results
