
import numpy as np
import pytest

from specgpt.retriever import retrieve_chunks


class MockEmbeddingModel:
    """Return a predefined vector for a test query."""

    def encode(self, texts):
        return np.array([[1.0, 0.0]])


def test_retrieve_chunks_returns_ranked_results():
    chunks = [
        type("Chunk", (), {"text": "Relevant content", "metadata": {}})(),
        type("Chunk", (), {"text": "Less relevant content", "metadata": {}})(),
    ]

    chunk_embeddings = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
    ])

    results = retrieve_chunks(
        query="test question",
        model=MockEmbeddingModel(),
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=2,
    )

    assert len(results) == 2
    assert results[0]["chunk"].text == "Relevant content"
    assert results[0]["score"] > results[1]["score"]


def test_retrieve_chunks_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="number of chunks must match"):
        retrieve_chunks(
            query="test question",
            model=MockEmbeddingModel(),
            chunks=[object(), object()],
            chunk_embeddings=np.array([[1.0, 0.0]]),
        )
