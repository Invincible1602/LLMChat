# core/pdf_processor.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List
from core.text_processing import split_text_into_chunks # Import our chunking utility
from utils.logging_utils import get_logger

logger = get_logger(__name__)

def load_pdf_and_split_into_documents(pdf_file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Loads a PDF file, extracts text page by page, and then splits the text
    from each page into smaller, overlapping chunks (Langchain Document objects).

    Args:
        pdf_file_path: The path to the PDF file.
        chunk_size: The desired size of each text chunk.
        chunk_overlap: The overlap between consecutive chunks.

    Returns:
        A list of Langchain Document objects, each representing a chunk of text
        from the PDF with appropriate metadata.
    """
    try:
        loader = PyPDFLoader(pdf_file_path)
        pages = loader.load() # Loads each page as a Document

        all_chunks = []
        for i, page in enumerate(pages):
            # Use our existing text_processing utility to split page content
            page_chunks = split_text_into_chunks(page.page_content, chunk_size, chunk_overlap)
            
            # Add metadata about the original page to each chunk
            for chunk in page_chunks:
                chunk.metadata["source"] = pdf_file_path
                chunk.metadata["page"] = i + 1 # Page numbers are usually 1-indexed
                all_chunks.append(chunk)
        
        logger.info(f"Loaded PDF '{pdf_file_path}' and generated {len(all_chunks)} chunks.")
        return all_chunks
    except Exception as e:
        logger.error(f"Error loading or processing PDF '{pdf_file_path}': {e}")
        return []

