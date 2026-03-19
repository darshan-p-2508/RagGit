import streamlit as st
import requests

from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.badges import badge


# ---------------------------------------------------
# API Configuration
# ---------------------------------------------------

API = "http://127.0.0.1:8000/api"


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="RagGit",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------
# Custom Styling (CSS Injection)
# ---------------------------------------------------

st.markdown(
"""
<style>

.repo-card{
    padding:20px;
    border-radius:12px;
    background:#0f172a;
    border:1px solid #1e293b;
}

.answer-card{
    padding:25px;
    border-radius:12px;
    background:#111827;
    border:1px solid #374151;
}

.chat-user{
    background:#1e293b;
    padding:12px;
    border-radius:10px;
}

.chat-ai{
    background:#020617;
    padding:16px;
    border-radius:10px;
    border:1px solid #334155;
}

</style>
""",
unsafe_allow_html=True
)


# ---------------------------------------------------
# Header Section
# ---------------------------------------------------

colored_header(
    label="📚 RagGit • AI GitHub Repo Assistant",
    description="Interact with any GitHub using AI",
    color_name="violet-70"
)

add_vertical_space(1)


# ---------------------------------------------------
# Repository Connection Section
# ---------------------------------------------------

with stylable_container(
    "repo_container",
    css_styles="""
        {
            border-radius:12px;
            border:1px solid #1f2937;
            padding:25px;
            background-color:#020617;
        }
    """
):

    st.subheader("🔗 Connect a Repository")

    repo = st.text_input(
        "GitHub Repo URL",
        placeholder="https://github.com/user/repository"
    )

    upload = st.button("Clone Repository")

    if upload:

        if repo == "":
            st.warning("Enter a repository URL")

        else:

            with st.spinner("Cloning and indexing repository..."):

                r = requests.post(
                    f"{API}/upload_repo",
                    json={"git_url": repo}
                )

                if r.status_code == 200:
                    st.success("Repository indexed successfully!")

                else:
                    st.error(r.text)

add_vertical_space(2)


# ---------------------------------------------------
# Chat Section
# ---------------------------------------------------

colored_header(
    label="💬 Ask Questions",
    description="Chat with your repository",
    color_name="violet-70"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.chat_input("Ask something about the repo...")

if question:

    st.session_state.chat_history.append(("user", question))

    with st.spinner("Searching repository..."):

        r = requests.post(
            f"{API}/ask",
            json={"question": question}
        )

        if r.status_code == 200:

            data = r.json()

            answer = data["answer"]

            st.session_state.chat_history.append(("ai", answer))

            st.session_state.context = data["chunks"]

        else:
            st.error(r.text)


# ---------------------------------------------------
# Chat Display Renderer
# ---------------------------------------------------

for role, msg in st.session_state.chat_history:

    if role == "user":

        with st.chat_message("user"):
            st.markdown(msg)

    else:

        with st.chat_message("assistant"):
            st.markdown(msg)

add_vertical_space(1)

# ---------------------------------------------------
# Context Viewer (Debug / Transparency Tool)
# ---------------------------------------------------

if "context" in st.session_state:

    with st.expander("🔎 Retrieved Code Context"):

        for chunk in st.session_state.context:
            st.code(chunk)

add_vertical_space(2)
