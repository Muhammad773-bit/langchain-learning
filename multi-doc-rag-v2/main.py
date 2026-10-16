import os
from agent.qa_agent import QAAgent

# Configuration
CHROMA_PATH = "chroma_db"

def main():
    print("--- Multi-Document RAG Agent CLI ---")
    
    # Check if vector store exists
    if not os.path.exists(CHROMA_PATH):
        print(f"Error: Vector store not found at {CHROMA_PATH}.")
        print("Please run 'python ingest.py' first to initialize the database.")
        return

    # Initialize QA Agent
    agent = QAAgent(chroma_path=CHROMA_PATH)
    
    print("\nAgent ready! Type 'exit' to quit.")
    
    while True:
        question = input("\nQuery: ")
        
        if question.lower() == 'exit':
            break
            
        if not question.strip():
            continue

        print("Processing...")
        try:
            response = agent.query(question)
            
            # Extract answer and context
            answer = response.get("answer", "No answer found.")
            context_docs = response.get("context", [])

            print("\n" + "="*50)
            print("ANSWER:")
            print(answer)
            print("="*50)
            
            # Debug Support: Show retrieved context snippets
            print("\nRETRIEVED CONTEXT SNIPPETS:")
            for i, doc in enumerate(context_docs):
                source = doc.metadata.get("source", "Unknown")
                print(f"\n[{i+1}] Source: {source}")
                print(f"Content: {doc.page_content[:200]}...")
            print("="*50)
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
