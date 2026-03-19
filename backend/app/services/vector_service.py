import faiss
import numpy as np
import pickle
from pathlib import Path
from ..core.config import FAISS_PATH
from .embedding_service import embed_text


# ---------------------------------------------------
# Configuration: Allowed File Types
# ---------------------------------------------------

"""
Defines the set of file extensions that will be processed
and included in the vector index.

Purpose:
    - Filters out irrelevant or binary files.
    - Focuses on source code and text-based documentation.

Notes:
    - Extend this set based on your use case.
    - Binary formats (e.g., images, PDFs) are intentionally excluded.
"""

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".java",
    ".cpp",
    ".c",
    ".md",
    ".txt",
    ".html",
    ".css",
    ".json",
    ".yaml",
    ".yml"
}


# ---------------------------------------------------
# Text Chunking Utility
# ---------------------------------------------------

def split_chunks(text, size=500):
    """
    Split a large text into smaller fixed-size chunks.

    Args:
        text (str):
            - Input text to be split.

        size (int, optional):
            - Maximum number of characters per chunk.
            - Default is 500.

    Returns:
        list[str]:
            - List of text chunks.

    Notes:
        - Uses simple character-based splitting.
        - Does NOT preserve semantic boundaries (e.g., functions/classes).
        - In production, consider:
            * Token-based chunking
            * Overlapping chunks
            * Language-aware splitting (AST parsing for code)
    """

    return [text[i:i + size] for i in range(0, len(text), size)]


# ---------------------------------------------------
# Index Building Service
# ---------------------------------------------------

def build_index(files):
    """
    Build a FAISS vector index from repository files.

    Workflow:
        1. Filter valid files based on extension and type.
        2. Read file contents safely.
        3. Split content into smaller chunks.
        4. Generate embeddings for each chunk.
        5. Store embeddings in a FAISS index.
        6. Persist index and chunk metadata to disk.

    Args:
        files (list):
            - List of file paths to process.

    Raises:
        Exception:
            - If no valid files are found after filtering.

    Output:
        - FAISS index saved at: FAISS_PATH/index.faiss
        - Chunk metadata saved at: FAISS_PATH/chunks.pkl

    Notes:
        - Uses L2 (Euclidean) distance for similarity search.
        - Embeddings are stored as float32 numpy arrays.
        - Chunk metadata is stored separately using pickle.
        - In production, consider:
            * Incremental indexing (avoid full rebuilds)
            * Parallel file processing
            * Handling very large repositories
            * Using a vector database (e.g., Pinecone, Weaviate)
            * Better chunking strategies (semantic-aware)
    """

    chunks = []

    for file in files:

        file = Path(file)

        # Skip directories
        if not file.is_file():
            continue

        # Skip unsupported file types
        if file.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:

                content = f.read()

                # Skip empty files
                if len(content.strip()) == 0:
                    continue

                chunks.extend(split_chunks(content))

        except Exception:
            # Ignore unreadable or problematic files
            continue

    if len(chunks) == 0:
        raise Exception("No valid files found in repository.")

    # Generate embeddings
    embeddings = [embed_text(c) for c in chunks]

    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]

    # Create FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dim)

    index.add(embeddings)

    # Ensure storage directory exists
    Path(FAISS_PATH).mkdir(parents=True, exist_ok=True)

    # Persist index
    faiss.write_index(index, f"{FAISS_PATH}/index.faiss")

    # Persist chunk metadata
    with open(f"{FAISS_PATH}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)


# ---------------------------------------------------
# Search Service
# ---------------------------------------------------

def search(question):
    """
    Perform semantic search over the indexed repository.

    Workflow:
        1. Load FAISS index from disk.
        2. Load corresponding text chunks.
        3. Convert user question into embedding.
        4. Perform nearest neighbor search.
        5. Return top-k relevant chunks.

    Args:
        question (str):
            - User query.

    Returns:
        list[str]:
            - Top-k (k=3) most relevant text chunks.

    Raises:
        Exception:
            - If index or chunk file is missing/corrupted.

    Notes:
        - Uses L2 distance similarity.
        - Currently retrieves top 3 results (k=3).
        - In production, consider:
            * Configurable k value
            * Score threshold filtering
            * Caching index in memory (avoid repeated disk reads)
            * Switching to cosine similarity (normalize embeddings)
            * Hybrid search (keyword + vector)
    """

    index = faiss.read_index(f"{FAISS_PATH}/index.faiss")

    with open(f"{FAISS_PATH}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    q = np.array([embed_text(question)]).astype("float32")

    D, I = index.search(q, k=3)

    return [chunks[i] for i in I[0]]