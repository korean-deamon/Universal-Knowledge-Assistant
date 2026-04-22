# Universal RAG Assistant

A robust, elegant, and production-ready Retrieval-Augmented Generation (RAG) assistant built with **Streamlit**. This application allows users to seamlessly upload, index, and query multiple PDF documents on-the-fly using Google's **Gemini 2.5 Flash** LLM and highly efficient local embeddings (`sentence-transformers`).

## ✨ Features
- **Universal Knowledge Base**: Drag-and-drop any PDF to instantly create a custom knowledge base.
- **On-the-fly Indexing**: Securely processes and indexes PDFs using local `ChromaDB` without relying on external embedding APIs, enhancing privacy and speed.
- **Dynamic Session Management**: Automatically clears old session data and vector stores when new context is requested.
- **Source Citation**: Always returns accurate answers backed up by the specific source document and page number.
- **Premium Glassmorphism UI**: Beautiful, modern dark-themed interface built natively in Streamlit.
- **Local Privacy**: Heavy lifting for document chunking and embeddings happens directly on your machine.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- [Google Gemini API Key](https://aistudio.google.com/)

### 2. Installation
Clone the repository and set up your virtual environment:

```bash
git clone https://github.com/korean-deamon/Universal-Knowledge-Assistant.git
cd Universal-Knowledge-Assistant

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root of the project and add your Google Gemini API key:
```env
GOOGLE_API_KEY="your-google-api-key-here"
```

### 4. Running the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 📸 Usage & Walkthrough

### Step 1: Uploading Documents
Use the sidebar to drag and drop your PDF files. The system will automatically extract text, generate embeddings, and store them in a local ChromaDB instance.

### Step 2: Querying the Knowledge Base
Once the documents are indexed, use the main chat interface to ask questions. The AI will retrieve the most relevant chunks from your documents and provide a clear, cited answer.

---

## 🏗️ Architecture

- **Frontend**: Streamlit with custom CSS injections.
- **LLM**: `gemini-2.5-flash` via `langchain-google-genai`.
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2` (Local execution).
- **Vector Store**: `ChromaDB`.
- **PDF Processing**: Native `pypdf` integration for stable text extraction.

## 🔒 Security & Privacy
The `.gitignore` is pre-configured to ensure sensitive information like your `.env` file, locally generated vector databases (`vector_store/`), and uploaded raw PDFs (`data/`) are never pushed to version control.

---

*Built with ❤️ for intelligent document assistance.*
