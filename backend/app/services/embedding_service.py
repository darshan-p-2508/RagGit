from sentence_transformers import SentenceTransformer

# ---------------------------------------------------
# Embedding Model Initialization
# ---------------------------------------------------

"""
This module is responsible for generating vector embeddings
from textual data using a pre-trained Sentence Transformer model.

Model Used:
    - all-MiniLM-L6-v2

Model Characteristics:
    - Lightweight and fast
    - კარგი balance between performance and accuracy
    - Suitable for semantic search, clustering, and retrieval tasks

Initialization Notes:
    - The model is loaded once at module import time.
    - This avoids repeated loading overhead during runtime.
    - In production, consider:
        * Lazy loading for faster startup
        * GPU/accelerator support if available
        * Model version pinning for consistency
"""

model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------
# Embedding Function
# ---------------------------------------------------

def embed_text(text):
    """
    Generate a vector embedding for the given input text.

    This function converts input text into a dense numerical vector
    representation using the pre-loaded Sentence Transformer model.

    Args:
        text (str or list[str]):
            - A single string or list of strings to be embedded.

    Returns:
        list:
            - A list of floating-point values representing the embedding.
            - If input is a single string → returns a single embedding vector.
            - If input is a list → returns a list of embedding vectors.

    Raises:
        Exception:
            - If the model fails during encoding
            - If invalid input type is provided

    Notes:
        - Output is converted to a Python list for JSON serialization.
        - Embeddings are suitable for:
            * Semantic similarity search
            * Vector databases (e.g., FAISS)
            * Clustering and ranking tasks
        - For large-scale systems:
            * Use batching for performance optimization
            * Cache embeddings to reduce recomputation
            * Normalize vectors if required by downstream systems
    """

    return model.encode(text).tolist()