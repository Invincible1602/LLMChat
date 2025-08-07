# app.py (This file should contain your FastAPI application)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import router # Import the main API router
from config.settings import settings # Import application settings
import os
from utils.logging_utils import setup_logging # Changed to import setup_logging

# Setup logging for the entire application.
# This configures the global loguru.logger instance.
logger = setup_logging()

# Initialize the FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME, # Set the application title from settings
    description="A PDF-powered Chatbot API with RAG capabilities.", # Descriptive text for the API documentation
    version="1.0.0" # API version, can be managed in settings if preferred
)

# Ensure the upload directory exists for temporary PDF storage
# This directory is where uploaded PDF files will be saved before processing
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
logger.info(f"Upload directory '{settings.UPLOAD_DIR}' ensured to exist.") # Log confirmation of directory existence

# Include the API routes defined in api/routes.py
# All endpoints defined in api/routes.py will be added to this FastAPI app
app.include_router(router)

# Define a root endpoint for basic API health check or welcome message
@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    Useful for quickly checking if the API is running.
    """
    logger.info("Root endpoint accessed") # Log when the root endpoint is hit
    return {"message": "Welcome to the PDF Chatbot API!"}

# Global exception handler to catch any uncaught exceptions across all API routes
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handles any unhandled exceptions that occur during API request processing.
    Logs the error and returns a generic 500 Internal Server Error response.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True) # Log the full traceback for debugging
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "message": "Internal server error",
            "details": str(exc) # Include exception details for debugging purposes
        }
    )