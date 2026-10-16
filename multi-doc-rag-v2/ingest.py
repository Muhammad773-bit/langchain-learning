import os
import time
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader_main.loader_router import DocumentLoaderRouter

# Configuration
DATA_DIR = "data"
CHROMA_PATH = "chroma_db"
# Using faster embedding model - much quicker than the previous one
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def check_vector_store_exists():
    """Check if vector store already has data"""
    if not os.path.exists(CHROMA_PATH):
        return False
    
    try:
        store = Chroma(persist_directory=CHROMA_PATH)
        count = store._collection.count()
        return count > 0
    except:
        return False

def main():
    print("--- Starting Ingestion Process ---\n")
    
    # Check if already ingested
    if check_vector_store_exists():
        print(f"✓ Vector store already exists at {CHROMA_PATH}")
        store = Chroma(persist_directory=CHROMA_PATH)
        count = store._collection.count()
        print(f"✓ Contains {count} documents - skipping re-ingestion")
        print("--- Ingestion Complete (Already Indexed) ---")
        return
    
    # 1. Load Documents
    print("Step 1: Loading documents...")
    start = time.time()
    loader_router = DocumentLoaderRouter()
    documents = loader_router.load_all_from_directory(DATA_DIR)
    print(f"✓ Total documents loaded: {len(documents)} ({time.time()-start:.2f}s)\n")
    
    if not documents:
        print("No documents found to ingest. Exiting.")
        return

    # 2. Split Text
    print("Step 2: Splitting text into chunks...")
    start = time.time()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Reduced for faster processing
        chunk_overlap=80,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✓ Total chunks created: {len(chunks)} ({time.time()-start:.2f}s)\n")

    # 3. Ensure directory exists
    if not os.path.exists(CHROMA_PATH):
        os.makedirs(CHROMA_PATH)

    # 4. Create Embeddings with optimizations
    print("Step 3: Initializing embedding model...")
    start = time.time()
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False, "batch_size": 32}
    )
    print(f"✓ Model initialized ({time.time()-start:.2f}s)\n")

    # 5. Create vector store
    print(f"Step 4: Creating vector store...")
    start = time.time()
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    elapsed = time.time() - start
    collection_count = vector_store._collection.count()
    print(f"✓ Vector store created with {collection_count} documents ({elapsed:.2f}s)\n")
    
    print("--- Ingestion Complete ---")

if __name__ == "__main__":
    main()
