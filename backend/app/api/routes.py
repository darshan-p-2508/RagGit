from fastapi import APIRouter
from pathlib import Path

from ..services.repo_service import clone_repo
from ..services.vector_service import build_index, search
from ..services.llm_service import generate_answer

router = APIRouter()


@router.post("/upload_repo")
def upload_repo(data: dict):
    """
    Clone a GitHub repository and build a vector index for semantic search.

    This endpoint performs the following steps:
    1. Clones the provided GitHub repository URL to a local directory.
    2. Recursively scans all files in the repository.
    3. Builds a vector index from the file contents for later retrieval.

    Request Body:
        data (dict):
            - git_url (str): Public GitHub repository URL.

    Returns:
        dict:
            {
                "status": "repo indexed"
            }

    Raises:
        Exception:
            - If cloning fails (invalid URL, network issues, permissions)
            - If indexing fails due to file processing or embedding errors

    Notes:
        - This operation may take time depending on repository size.
        - All files with extensions (*.*) are included in indexing.
        - Consider filtering large/binary files in production systems.
    """

    repo_path = clone_repo(data["git_url"])

    files = list(Path(repo_path).rglob("*.*"))

    build_index(files)

    return {"status": "repo indexed"}


@router.post("/ask")
def ask(data: dict):
    """
    Answer a user question based on the indexed repository using Retrieval-Augmented Generation (RAG).

    This endpoint performs the following steps:
    1. Accepts a natural language question from the user.
    2. Searches the vector index to retrieve relevant code/document chunks.
    3. Constructs a context from retrieved chunks.
    4. Generates an answer using a language model.

    Request Body:
        data (dict):
            - question (str): User's query about the repository.

    Returns:
        dict:
            {
                "answer": str,     # Generated response from LLM
                "chunks": list     # Retrieved context chunks used for answering
            }

    Raises:
        Exception:
            - If search fails (index not built or corrupted)
            - If LLM generation fails (API/model issues)

    Notes:
        - Accuracy depends on quality of indexed data and embeddings.
        - Context is formed by concatenating retrieved chunks with newline separation.
        - Consider adding:
            * chunk ranking
            * token limits
            * caching for repeated queries
    """

    question = data["question"]

    chunks = search(question)

    context = "\n".join(chunks)

    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "chunks": chunks
    }