import os
import pypdf
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import DATA_DIR, VECTOR_STORE_DIR

class DocumentProcessor:
    def __init__(self):
        print("--- Initializing Embeddings (HuggingFace) ---")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            add_start_index=True
        )

    def load_documents(self):
        """Loads all PDFs from the data directory using pypdf directly."""
        documents = []
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            return []

        pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
        print(f"--- Found {len(pdf_files)} PDF(s) in {DATA_DIR} ---")
        
        for pdf_file in pdf_files:
            file_path = os.path.join(DATA_DIR, pdf_file)
            print(f"--- Reading PDF: {pdf_file} ---")
            try:
                with open(file_path, "rb") as f:
                    reader = pypdf.PdfReader(f)
                    for i, page in enumerate(reader.pages):
                        text = page.extract_text()
                        if text:
                            # Create a LangChain document object
                            doc = Document(
                                page_content=text,
                                metadata={"source": pdf_file, "page": i + 1}
                            )
                            documents.append(doc)
                print(f"--- Successfully read {pdf_file} ({len(documents)} pages so far) ---")
            except Exception as e:
                print(f"--- Error reading {pdf_file}: {e} ---")
        
        return documents

    def process_and_store(self):
        """Processes documents and saves them to the persistent vector store."""
        docs = self.load_documents()
        if not docs:
            print("--- No documents to process! ---")
            return None

        print(f"--- Splitting {len(docs)} pages into smaller chunks... ---")
        chunks = self.text_splitter.split_documents(docs)
        print(f"--- Total chunks created: {len(chunks)} ---")
        
        if os.path.exists(VECTOR_STORE_DIR):
            import shutil
            print(f"--- Cleaning up old vector store at {VECTOR_STORE_DIR}... ---")
            shutil.rmtree(VECTOR_STORE_DIR)

        print(f"--- Starting Vector Storage (this might take a minute)... ---")
        try:
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=VECTOR_STORE_DIR
            )
            print(f"--- Success! Vector store saved at {VECTOR_STORE_DIR} ---")
            return vector_store
        except Exception as e:
            print(f"--- Error during vector storage: {e} ---")
            return None

    def get_vector_store(self):
        """Loads the existing vector store."""
        if os.path.exists(VECTOR_STORE_DIR) and os.listdir(VECTOR_STORE_DIR):
            return Chroma(
                persist_directory=VECTOR_STORE_DIR,
                embedding_function=self.embeddings
            )
        return None
