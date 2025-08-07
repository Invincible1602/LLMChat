# core/text_processing.py
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Splits a given text into smaller, overlapping chunks using Langchain's
    RecursiveCharacterTextSplitter. This method is robust for various text formats.

    Args:
        text: The input text to be chunked.
        chunk_size: The desired size of each chunk (in characters).
        chunk_overlap: The number of characters to overlap between consecutive chunks.
                       This helps maintain context across chunks.

    Returns:
        A list of Langchain Document objects, where each object represents a chunk
        of the input text.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len, # Use standard Python len() for length calculation
        is_separator_regex=False, # Treat separators as plain strings, not regex
    )
    
    # Langchain's text splitter expects a list of strings or a single string
    # and returns a list of Document objects.
    documents = text_splitter.create_documents([text])
    
    return documents

