import os
from src.processor import DocumentProcessor

def main():
    print("========================================")
    print("🚀 Document Syncing Tool Started")
    print("========================================")
    
    processor = DocumentProcessor()
    
    print("\nStarting document processing...")
    vector_store = processor.process_and_store()
    
    if vector_store:
        print("\n========================================")
        print("✅ SUCCESS: Documents indexed successfully!")
        print(f"Vector database is ready in 'vector_store' folder.")
        print("========================================")
    else:
        print("\n❌ ERROR: No documents found or processing failed.")
        print("Please make sure your PDF is inside the 'data' folder.")

if __name__ == "__main__":
    main()
