# api/dependencies.py
from core.llm import get_llm
from core.embeddings import get_embedding_model
from core.vectorstore import VectorStore # Correctly import the class
from services.chat_service import ChatService
from services.query_service import QueryService
from services.pdf_service import PDFService
from services.intent_detection_service import IntentDetectionService
from loguru import logger # Import logger directly from loguru

# No need to call get_logger(__name__) here, as loguru.logger is globally configured by setup_logging in app.py

# Initialize global instances of services and core components
# These will be created once when the application starts
try:
    llm_instance = get_llm()
    embedding_model_instance = get_embedding_model()
    # Instantiate the VectorStore class
    vector_store_instance = VectorStore(embedding_model_instance) 
    chat_service_instance = ChatService(llm_instance, vector_store_instance)
    query_service_instance = QueryService(vector_store_instance)
    pdf_service_instance = PDFService(vector_store_instance)
    intent_detection_service_instance = IntentDetectionService(llm_instance)
    logger.info("All services and core components initialized successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize one or more core components/services: {e}", exc_info=True)
    # Depending on the severity, you might want to exit or disable functionality here.
    # For now, we'll let the app start but log the critical error.


def get_chat_service() -> ChatService:
    """Dependency for ChatService."""
    return chat_service_instance

def get_query_service() -> QueryService:
    """Dependency for QueryService."""
    return query_service_instance

def get_pdf_service() -> PDFService:
    """Dependency for PDFService."""
    return pdf_service_instance

def get_intent_detection_service() -> IntentDetectionService:
    """Dependency for IntentDetectionService."""
    return intent_detection_service_instance

