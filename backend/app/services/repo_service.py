from git import Repo
from pathlib import Path
from ..core.config import BASE_REPO_PATH


# ---------------------------------------------------
# Repository Cloning Service
# ---------------------------------------------------

"""
This module handles cloning of GitHub repositories into
a local directory for further processing (e.g., indexing, analysis).

Workflow:
    1. Extract repository name from the provided Git URL.
    2. Construct a local path inside the configured base directory.
    3. Check if the repository already exists locally.
    4. If not, clone the repository using GitPython.
    5. Return the local repository path.

Dependencies:
    - GitPython (Repo): Used to perform Git operations programmatically.

Notes:
    - This implementation assumes public repositories.
    - Authentication is not handled (for private repos).
    - No cleanup/versioning strategy for existing repos.
"""


def clone_repo(git_url: str):
    """
    Clone a GitHub repository to a local directory.

    Args:
        git_url (str):
            - URL of the GitHub repository.
            - Example: https://github.com/user/repo.git

    Returns:
        str:
            - Local filesystem path where the repository is stored.

    Raises:
        Exception:
            - If cloning fails due to:
                * Invalid repository URL
                * Network issues
                * Git not installed or misconfigured
                * Permission issues

    Behavior:
        - If the repository already exists locally:
            * Skips cloning
            * Returns the existing path (idempotent behavior)
        - If not:
            * Clones the repository into BASE_REPO_PATH

    Path Structure:
        BASE_REPO_PATH/
            └── <repo_name>/

    Notes:
        - Repo name is extracted from the URL by taking the last path segment.
        - ".git" suffix is removed if present.
        - No branch selection (defaults to repository default branch).
        - No pull/update logic for existing repositories.
        - Consider adding in production:
            * Repo update (git pull) if already exists
            * Branch/commit selection support
            * Size limits and validation
            * Security checks for malicious repositories
            * Timeout and retry handling
    """

    repo_name = git_url.split("/")[-1].replace(".git", "")
    repo_path = Path(BASE_REPO_PATH) / repo_name

    if repo_path.exists():
        return str(repo_path)

    Repo.clone_from(git_url, repo_path)

    return str(repo_path)