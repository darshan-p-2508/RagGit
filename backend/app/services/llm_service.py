import requests
from ..core.config import GROQ_API_KEY


# ---------------------------------------------------
# LLM Answer Generation Service
# ---------------------------------------------------

"""
This module handles interaction with the Groq LLM API
to generate answers using a Retrieval-Augmented Generation (RAG) approach.

Workflow:
    1. Accept a user question and retrieved context.
    2. Construct a prompt combining both.
    3. إرسال the prompt to the Groq Chat Completion API.
    4. Return the generated response.

Model Used:
    - llama-3.3-70b-versatile

Notes:
    - The model is optimized for general-purpose reasoning and code understanding.
    - Context quality directly impacts answer accuracy.
    - This implementation uses a simple prompt template (can be improved further).
"""


def generate_answer(question, context):
    """
    Generate an answer using Groq's LLM based on a given question and context.

    Args:
        question (str):
            - The user's query about the repository.

        context (str):
            - Retrieved relevant text/code chunks used to ground the answer.

    Returns:
        str:
            - Generated answer from the language model.

    Raises:
        Exception:
            - If API request fails (network issues, invalid API key, rate limits)
            - If response format is unexpected or malformed

    Request Details:
        Endpoint:
            https://api.groq.com/openai/v1/chat/completions

        Headers:
            - Authorization: Bearer <GROQ_API_KEY>
            - Content-Type: application/json

        Payload:
            {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

    Prompt Structure:
        The prompt follows a simple instruction format:

            "Answer the question using the context below."

        Followed by:
            - Context (retrieved chunks)
            - Question

    Notes:
        - No system prompt is currently used (can be added for better control).
        - No token limit handling (important for large contexts).
        - No retry or timeout logic (recommended for production).
        - No streaming support (can improve UX in frontend).
        - Consider adding:
            * Prompt engineering for better grounding
            * Context truncation based on token limits
            * Logging and monitoring
            * Error handling for non-200 responses
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    return data["choices"][0]["message"]["content"]