# config/settings.py
import os
from dotenv import load_dotenv # For loading environment variables from .env file

# Load environment variables from .env file (if it exists)
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Chatbot"
    API_V1_STR: str = "/api/v1"

    # LLM Settings
    # Retrieve API key from environment variable, with a fallback for quick local testing
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyAV4DvZD7LKIannW-h2wXYxHnWmBALN_4w")
    EMBEDDING_MODEL_NAME: str = "models/embedding-001" # Google's text embedding model

    # Text Processing Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Vector Store Settings (Pinecone)
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "pcsk_6HNuuW_DBYc5eMUEFcmzTzycSPaNMQk7gD8vQvEWS5AGvowVJKBmutZRUpgJscVURkQkrp")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "pdf-chatbot-index")

    # PDF Upload Settings
    UPLOAD_DIR: str = "uploaded_pdfs"

    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper() # This line was missing

settings = Settings()
