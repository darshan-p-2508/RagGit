from fastapi import FastAPI
from .api.routes import router


# ---------------------------------------------------
# FastAPI Application Initialization
# ---------------------------------------------------

"""
This module serves as the main entry point for the RagGit API.

Responsibilities:
    - Initialize the FastAPI application instance.
    - Configure application-level metadata.
    - Register API routes.

Framework:
    - FastAPI: High-performance web framework for building APIs with Python.

Application Overview:
    RagGit API enables:
        1. Cloning and indexing GitHub repositories.
        2. Performing semantic search over repository content.
        3. Generating AI-powered answers using Retrieval-Augmented Generation (RAG).

Notes:
    - This file is typically referenced by ASGI servers (e.g., Uvicorn, Gunicorn).
    - Example run command:
        uvicorn app.main:app --reload
"""


# ---------------------------------------------------
# Application Instance
# ---------------------------------------------------

"""
FastAPI application instance.

Metadata:
    title:
        - Human-readable name of the API (visible in Swagger UI).

    Additional metadata (not included but recommended in production):
        - description
        - version
        - contact
        - license_info
"""

app = FastAPI(title="RagGit API")


# ---------------------------------------------------
# Router Registration
# ---------------------------------------------------

"""
Registers all API routes with a common prefix.

Configuration:
    prefix="/api"
        - All endpoints will be accessible under this base path.
        - Example:
            POST /api/upload_repo
            POST /api/ask

Benefits:
    - Logical grouping of endpoints
    - Easier versioning (e.g., /api/v1 in future)
    - Cleaner URL structure

Notes:
    - Routes are defined in the `api.routes` module.
    - Can be extended with multiple routers for modular architecture.
"""

app.include_router(router, prefix="/api")