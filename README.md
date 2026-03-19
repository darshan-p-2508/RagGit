# 📚 RagGit — AI GitHub Repository Assistant
RagGit is a **Retrieval-Augmented Generation (RAG)** powered application that allows you to:
- 🔗 Connect any public GitHub repository  
- 🔍 Index and search its codebase semantically  
- 💬 Ask natural language questions  
- 🤖 Get AI-generated answers grounded in the repository  

---

## 🚀 Features
- 🔗 Clone and index GitHub repositories
- 🧠 Semantic search using vector embeddings (FAISS)
- 🤖 LLM-powered answers using Groq (LLaMA 3)
- 💬 Chat interface built with Streamlit
- 🔎 Context transparency (view retrieved code chunks)

---

## ⚙️ Tech Stack
| Layer        | Technology            |
|--------------|-----------------------|
| Frontend     | Streamlit             |
| Backend      | FastAPI               |
| Embeddings   | Sentence Transformers |
| Vector DB    | FAISS                 |
| LLM          | Groq (LLaMA 3.3 70B)  |
| Repo Access  | GitPython             |

---

## 📂 Project Structure
<p>
raggit/
│
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ └── routes.py
│ │ ├── core/
│ │ │ └── config.py
│ │ ├── services/
│ │ │ ├── embedding_service.py
│ │ │ ├── llm_service.py
│ │ │ ├── repo_service.py
│ │ │ └── vector_service.py
│ │ └── main.py
│ │
│ └── data/
│ ├── index/
│ └── repos/
│
├── frontend/
│ └── app.py
│
├── .env
├── requirements.txt
└── README.md
</p>
---

## 🔄 Execution Flow (End-to-End)

### 1️⃣ User connects a repository
- User inputs GitHub URL in Streamlit UI
- Frontend sends request:
  POST /api/upload_repo

---

### 2️⃣ Backend clones and indexes repository

**repo_service.py**
- Clones repository locally

**vector_service.py**
- Reads all valid files
- Splits into chunks
- Converts chunks → embeddings
- Stores in FAISS index

---

### 3️⃣ User asks a question
  POST /api/ask

---

### 4️⃣ Retrieval phase (RAG)

**vector_service.search()**
- Converts question → embedding
- Finds top-k similar chunks from FAISS

---

### 5️⃣ Generation phase

**llm_service.generate_answer()**
- Combines:
  - user question
  - retrieved context
- Sends to Groq LLM
- Returns generated answer

---

### 6️⃣ Response displayed

- Answer shown in chat UI
- Context chunks shown in expandable panel

---

## 🧠 RAG Pipeline Summary

User Question
↓
Embedding (SentenceTransformer)
↓
FAISS Search (Top-K Chunks)
↓
Context Injection
↓
LLM (Groq - LLaMA 3)
↓
Final Answer

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/darshan-p-2508/RagGit.git
cd RagGit
```

### 2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables (.env file)
```
GROQ_API_KEY=your_api_key_here
```

### 5. Run Backend (FastAPI)
```
uvicorn backend.app.main:app --reload
```
API will run at: http://127.0.0.1:8000

### 6. Run Frontend (Streamlit)
Open another terminal and navigate to RagGit directory and run the following command
```
streamlit run frontend/streamlit_app.py
```
App will run at: http://localhost:8501

---

## ⚠️ Limitations
- ❌ No support for private repositories  
- ❌ No incremental indexing  
- ❌ No streaming responses  
- ❌ Basic chunking (not semantic)  
- ❌ Entire repo re-indexed every time  

---

## 🚀 Future Improvements
- ✅ Streaming responses (ChatGPT-like UX)  
- ✅ Hybrid search (keyword + vector)  
- ✅ Better chunking (AST / semantic)  
- ✅ Repo update instead of re-clone  
- ✅ Support private repos (tokens/SSH)  
- ✅ Background jobs (Celery / Redis)  
- ✅ Multi-repo support  
- ✅ UI improvements (sidebar, file explorer)  

---

## 🧪 Example Use Cases
- Understand unfamiliar GitHub projects  
- Debug open-source code faster  
- Generate documentation summaries  
- Learn from real-world codebases  

---

## 🤝 Contributing
Contributions are welcome!
1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Submit a Pull Request  

---

## 📜 License
MIT License  

---

## 👨‍💻 Author
Built with ❤️ by Darshan Prashanth 🚀
