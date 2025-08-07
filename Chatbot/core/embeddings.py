# core/embeddings.py
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config.settings import settings
from loguru import logger # Import logger directly from loguru

# The loguru.logger instance is globally configured by setup_logging in app.py.
# Therefore, we can directly import and use 'logger' here without calling get_logger(__name__).

def get_embedding_model():
    """
    Initializes and returns a Google Generative AI Embeddings model instance.
    This function retrieves the API key from settings and logs the initialization status.

    Raises:
        ValueError: If the GEMINI_API_KEY is not found in environment variables.

    Returns:
        GoogleGenerativeAIEmbeddings: An instance of the Google Generative AI Embeddings model.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        # Log a critical error if the API key is missing
        logger.error("GEMINI_API_KEY not found in environment variables.")
        raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment.")

    # Initialize the embedding model using the model name from settings and the API key.
    # The 'models/embedding-001' is a common embedding model provided by Google.
    embeddings = GoogleGenerativeAIEmbeddings(model=settings.EMBEDDING_MODEL_NAME, google_api_key=api_key)
    
    # Log successful initialization of the embedding model
    logger.info(f"Google Generative AI Embeddings model '{settings.EMBEDDING_MODEL_NAME}' initialized.")
    
    return embeddings

