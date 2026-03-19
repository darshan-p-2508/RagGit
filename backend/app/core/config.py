import os
from dotenv import load_dotenv

# ---------------------------------------------------
# Environment Configuration Loader
# ---------------------------------------------------

"""
This module is responsible for loading and managing
environment-based configuration for the application.

It uses a `.env` file to securely store sensitive values
such as API keys and configuration paths.

Best Practices:
    - Never hardcode secrets directly in source code.
    - Keep `.env` files out of version control (use `.gitignore`).
    - Use environment variables in production environments instead
      of relying on `.env` files.
"""

# Load environment variables from .env file into the system environment
load_dotenv()


# ---------------------------------------------------
# API Keys / Secrets
# ---------------------------------------------------

"""
GROQ_API_KEY:
    API key used to authenticate requests to the Groq LLM service.

    Source:
        Loaded from environment variable `GROQ_API_KEY`.

    Expected Behavior:
        - Must be set before running the application.
        - If missing, downstream services depending on this key
          may fail at runtime.

    Security Notes:
        - Do NOT log or expose this key.
        - Rotate periodically in production environments.
"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ---------------------------------------------------
# Application Paths
# ---------------------------------------------------

"""
BASE_REPO_PATH:
    Root directory where cloned GitHub repositories are stored locally.

    Usage:
        - Each repository is cloned into a subdirectory inside this path.
        - Used by repository ingestion and processing services.

    Notes:
        - Ensure this directory exists or is created at runtime.
        - Consider using persistent storage in production.
"""

BASE_REPO_PATH = "data/repos"


"""
FAISS_PATH:
    Directory where the FAISS vector index is stored.

    Usage:
        - Stores embeddings and index files for semantic search.
        - Accessed by vector search and retrieval services.

    Notes:
        - Should be persisted across application restarts.
        - Consider versioning indexes if handling multiple repositories.
        - Ensure sufficient disk space for large indexes.
"""

FAISS_PATH = "data/index"