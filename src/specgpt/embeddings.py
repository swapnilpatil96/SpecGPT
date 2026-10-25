
from sentence_transformers import SentenceTransformer


DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model(model_name=DEFAULT_MODEL_NAME):
    """Load and return the sentence embedding model."""
    return SentenceTransformer(model_name)


def embed_texts(model, texts):
    """Convert a list of text strings into embedding vectors."""
    if not texts:
        return []

    return model.encode(texts, show_progress_bar=True)


def embed_chunks(model, chunks):
    """Generate one embedding vector for each document chunk."""
    texts = [chunk.text for chunk in chunks]
    return embed_texts(model, texts)
