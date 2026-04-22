# 🌐 Universal Knowledge Assistant

**Universal Knowledge Assistant** is an advanced RAG (Retrieval-Augmented Generation) system built on the Streamlit platform that transforms any PDF document into an intelligent knowledge base. Interact with your documents in real-time using the Google Gemini 2.5 Flash model!

---

## 🚀 About the Project

This project allows users to upload PDF files and ask questions based on the information contained within those files. The system utilizes the following technologies:
- **LLM:** Google Gemini 2.5 Flash
- **Vector Database:** ChromaDB (Local storage)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Local execution)
- **Frontend:** Streamlit (Premium Glassmorphism Design)

---

## 🎓 Capstone Project Compliance

This project fully meets the following technical requirements:

- **Function Calling:** The support ticket creation process is handled via the LLM's `tool_calling` (Function Calling) capability.
- **Issue Tracking System:** Tickets are saved both as local JSON files and sent to **GitHub Issues** via API.
- **Citation & Sourcing:** Every answer is provided with the document name and page number.
- **Conversation History:** The system remembers the conversation history and maintains context.
- **Multi-Document Support:** Multiple PDF files can be uploaded and queried simultaneously as a unified knowledge base.

---

## 🛠 Installation and Setup (Full Step-by-Step)

Follow these steps to run the project on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/korean-deamon/Universal-Knowledge-Assistant.git
cd Universal-Knowledge-Assistant
```

### 2. Create and Activate Virtual Environment
**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the root directory and enter your Google Gemini and GitHub API keys:
```env
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
GITHUB_TOKEN="YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" # Optional for GitHub Issues
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📖 How It Works (Workflow)

1.  **📤 Upload:** Upload your PDF files via the sidebar. Files are automatically saved to the `data/` folder.
2.  **⚙️ Indexing:** 
    *   The system extracts text from the PDFs.
    *   Text is split into small chunks.
    *   Embeddings (numerical vectors) are created for each chunk.
    *   Vectors are stored in the **ChromaDB** database.
3.  **💬 Q&A (Chat):**
    *   When you ask a question, the system searches the database for the most relevant information.
    *   The retrieved information is sent to the Gemini model as "Context".
    *   The model answers based *only* on the uploaded documents and provides citations (file name and page).

---

## 🛡 Security

The `.gitignore` file prevents the following from being pushed to GitHub:
- `.env` (Secret keys)
- `data/` (Your uploaded PDF files)
- `vector_store/` (Generated indices)
- `.venv/` (Virtual environment)

---

## 🛠 Technical Stack

- **Python 3.10+**
- **LangChain:** For building RAG chains.
- **Streamlit:** For the UI interface.
- **PyPDF:** For PDF text extraction.
- **Sentence-Transformers:** For local embeddings.

---

*This project was developed as part of the BTEC APP Final project under the "Advanced Agentic Coding" framework.*
