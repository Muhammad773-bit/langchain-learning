from langchain_huggingface import HuggingFacePipeline
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class QAAgent:
    def __init__(self, chroma_path: str, model_id: str = "google/flan-t5-base"):
        self.chroma_path = chroma_path
        self.model_id = model_id
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.llm = self._initialize_llm()
        self.vector_store = self._load_vector_store()

    def _initialize_llm(self):
        print(f"Initializing LLM: {self.model_id}...")
        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id)
        
        # Create a pipeline
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.1,
            do_sample=True,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )
        
        return HuggingFacePipeline(pipeline=pipe)

    def _load_vector_store(self):
        print(f"Loading vector store from {self.chroma_path}...")
        return Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embeddings
        )

    def get_retrieval_chain(self):
        # 1. Define the system prompt
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise. "
            "Answer ONLY from the provided context."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        # 2. Create the document chain
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)

        # 3. Create the retrieval chain
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain

    def query(self, question: str):
        rag_chain = self.get_retrieval_chain()
        # Debug: Show retrieved context snippets
        # We can pull the retriever separately to show snippets if needed, 
        # but create_retrieval_chain returns context in the result.
        response = rag_chain.invoke({"input": question})
        return response
