# services/pdf_service.py
import os
from typing import List, Dict

from core.pdf_processor import load_pdf_and_split_into_documents
from core.vectorstore import VectorStore
from config.settings import settings
from utils.logging_utils import get_logger
from langchain_core.documents import Document

logger = get_logger(__name__)

class PDFService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    async def process_pdf(self, pdf_file_path: str) -> int:
        """
        Processes a PDF file by extracting text, chunking, and storing
        the resulting documents in the vector database.

        Args:
            pdf_file_path: The path to the uploaded PDF file.

        Returns:
            The number of documents processed and added to the vector store.
        """
        logger.info(f"Starting PDF processing for: {pdf_file_path}")

        # 1. Load PDF and split into Langchain Document objects
        documents = load_pdf_and_split_into_documents(
            pdf_file_path,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

        if not documents:
            logger.warning(f"No documents generated from {pdf_file_path}")
            return 0

        # 2. Convert Document objects to dicts with the expected "content" key
        formatted_docs = [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in documents
        ]

        # 3. Add documents to vector store
        num_added = self.vector_store.add_documents(formatted_docs)

        logger.info(f"Finished PDF processing for {pdf_file_path}. Added {num_added} documents.")
        return num_added
