# api/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel
from typing import List, Dict
import os
import shutil
import time

from services.chat_service import ChatService
from services.query_service import QueryService
from services.pdf_service import PDFService # Import the new PDFService
from services.intent_detection_service import IntentDetectionService # Import IntentDetectionService
from api.dependencies import get_chat_service, get_query_service, get_pdf_service, get_intent_detection_service
from config.settings import settings
from utils.logging_utils import get_logger # Using get_logger from utils

logger = get_logger(__name__)

# Create router, renamed to 'router' for consistency with app.py
router = APIRouter()

# Define Pydantic models for request/response (updated to reflect new functionality)
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str
    session_id: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    results: List[Dict]

class IntentDetectionRequest(BaseModel):
    query: str

class IntentDetectionResponse(BaseModel):
    intent: str

class ErrorResponse(BaseModel): # Keeping a generic error response model
    status_code: int
    message: str
    details: str = None

@router.post(
    "/chat", 
    response_model=ChatResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def chat_endpoint(request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)):
    """
    Handles chat interactions, generating responses based on user messages and RAG context.
    """
    logger.info(f"Chat request received for session_id: {request.session_id}, message: '{request.message}'")
    start_time = time.time()
    try:
        response_text = await chat_service.get_chat_response(request.message, request.session_id)
        elapsed_time = time.time() - start_time
        logger.info(f"Chat response generated in {elapsed_time:.2f}s for session_id: {request.session_id}")
        return ChatResponse(response=response_text, session_id=request.session_id)
    except Exception as e:
        logger.error(f"Error during chat operation for session_id {request.session_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )

@router.post(
    "/query", 
    response_model=QueryResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def query_endpoint(request: QueryRequest, query_service: QueryService = Depends(get_query_service)):
    """
    Queries the vector database for relevant documents based on the input query.
    """
    logger.info(f"Query request received: '{request.query}' with top_k={request.top_k}")
    start_time = time.time()
    try:
        results = await query_service.query_vector_store(request.query, request.top_k)
        elapsed_time = time.time() - start_time
        logger.info(f"Query completed in {elapsed_time:.2f}s: {len(results)} results found")
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(f"Error during query operation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )

@router.post(
    "/upload-pdf",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid file type"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Failed to process PDF"}
    }
)
async def upload_pdf_endpoint(file: UploadFile = File(...), pdf_service: PDFService = Depends(get_pdf_service)):
    """
    Uploads a PDF file, extracts text, processes it, and adds to the vector store.
    """
    logger.info(f"PDF upload request received for file: {file.filename}")
    start_time = time.time()

    if not file.filename.endswith(".pdf"):
        logger.warning(f"Attempted upload of non-PDF file: {file.filename}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed.")

    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    file_location = os.path.join(upload_dir, file.filename)

    try:
        # Save the uploaded file temporarily
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        num_processed = await pdf_service.process_pdf(file_location)
        
        # Optionally, delete the file after processing to save space
        os.remove(file_location)
        logger.info(f"PDF '{file.filename}' processed successfully. Added {num_processed} chunks.")
        
        elapsed_time = time.time() - start_time
        logger.info(f"PDF processing completed in {elapsed_time:.2f}s for '{file.filename}'")
        return {"message": f"PDF '{file.filename}' processed successfully. Added {num_processed} chunks."}
    except Exception as e:
        logger.error(f"Failed to process PDF '{file.filename}': {str(e)}", exc_info=True)
        # Clean up the partially saved file if an error occurs
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to process PDF: {e}")

@router.post(
    "/detect-intent",
    response_model=IntentDetectionResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal Server Error"}
    }
)
async def detect_intent_endpoint(request: IntentDetectionRequest, intent_detection_service: IntentDetectionService = Depends(get_intent_detection_service)):
    """
    Detects the intent of a user's query.
    """
    logger.info(f"Intent detection request received for query: '{request.query}'")
    start_time = time.time()
    try:
        intent = await intent_detection_service.detect_intent(request.query)
        elapsed_time = time.time() - start_time
        logger.info(f"Intent detected as '{intent}' in {elapsed_time:.2f}s for query: '{request.query}'")
        return IntentDetectionResponse(intent=intent)
    except Exception as e:
        logger.error(f"Error during intent detection for query '{request.query}': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Intent detection failed: {str(e)}"
        )

