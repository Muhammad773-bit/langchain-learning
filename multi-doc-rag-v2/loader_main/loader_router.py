import os
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader
)
from langchain_core.documents import Document

class DocumentLoaderRouter:
    """
    Routes files to their respective LangChain loaders based on file extension.
    """
    
    def __init__(self):
        self.loaders = {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".pptx": UnstructuredPowerPointLoader
        }

    def load_document(self, file_path: str) -> List[Document]:
        """
        Loads a single document based on its extension.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.loaders:
            print(f"Loading {file_path} using {self.loaders[ext].__name__}...")
            loader = self.loaders[ext](file_path)
            return loader.load()
        else:
            print(f"Skipping unsupported file type: {file_path}")
            return []

    def load_all_from_directory(self, directory_path: str) -> List[Document]:
        """
        Recursively loads all supported documents from a directory.
        """
        all_documents = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                docs = self.load_document(file_path)
                all_documents.extend(docs)
        return all_documents
