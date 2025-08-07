# main.py - A single-file Streamlit application for a PDF Chatbot
# This file combines all UI components and logic for a simplified project structure.

import streamlit as st
import requests
import uuid
import os
import sys
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv

# ====================
# CONFIGURATION
# ====================

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Chatbot"
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyAV4DvZD7LKIannW-h2wXYxHnWmBALN_4w")
    EMBEDDING_MODEL_NAME: str = "models/embedding-001"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "pcsk_6HNuuW_DBYc5eMUEFcmzTzycSPaNMQk7gD8vQvEWS5AGvowVJKBmutZRUpgJscVURkQkrp")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "pdf-chatbot-index")
    UPLOAD_DIR: str = "uploaded_pdfs"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

settings = Settings()

# ====================
# LOGGING SETUP
# ====================
def setup_logging():
    """Configures application logging with loguru."""
    logger.remove()
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL,
        backtrace=True,
        diagnose=True,
    )
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(
        log_dir / "app.log",
        rotation="10 MB",
        retention="1 week",
        format=log_format,
        level=settings.LOG_LEVEL,
        backtrace=True,
        diagnose=True,
        enqueue=True
    )
    logger.info(f"Logging initialized at level {settings.LOG_LEVEL}")
    return logger

# Call setup_logging() at the start of the script
logger = setup_logging()

# ====================
# STYLES
# (Previously in src/ui/styles.py)
# ====================
def set_styles():
    """Applies custom CSS styles to the Streamlit application for a polished look."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* General body styling */
        body {
    font-family: 'Inter', sans-serif;
    background-color: #000000;
    color: #f5f5f5;
}
.stApp {
    background-color: #000000;
}

/* Sidebar styling */
.st-emotion-cache-1ldf004 {
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
}
.st-emotion-cache-vk340x { /* Main container of the sidebar */
    border-radius: 12px;
    overflow: hidden;
}
.st-emotion-cache-1na1g85 { /* Header in the sidebar */
    color: #4A90E2;
}

/* Header styling */
h1 {
    color: #4A90E2;
    text-align: center;
    font-weight: 700;
    margin-bottom: 30px;
}
h2 {
    color: #f5f5f5;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* Chat input and button styling */
.stTextInput > div > div > input {
    background-color: #1e1e1e;
    color: #f5f5f5;
    border-radius: 8px;
    border: 1px solid #555;
    padding: 10px 15px;
    box-shadow: inset 0 1px 3px rgba(255, 255, 255, 0.06);
    font-size: 16px;
}
.stButton > button {
    background-color: #4A90E2;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}
.stButton > button:hover {
    background-color: #357ABD;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.6);
    transform: translateY(-2px);
}

/* Chat message bubbles */
.st-emotion-cache-1c7y2kl { /* User message container */
    background-color: #2a3b47;
    border-radius: 18px 18px 2px 18px;
    padding: 12px 18px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    align-self: flex-end;
    color: #ffffff;
}
.st-emotion-cache-1m01940 { /* Assistant message container */
    background-color: #1f1f1f;
    border-radius: 18px 18px 18px 2px;
    padding: 12px 18px;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    align-self: flex-start;
    color: #f5f5f5;
}

/* File uploader styling */
.stFileUploader {
    border: 2px dashed #4A90E2;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    background-color: #1a1a1a;
    margin-bottom: 15px;
    color: #f5f5f5;
}

/* Spinner styling */
.stSpinner > div > div {
    border-top-color: #4A90E2 !important;
}

/* Info/Success/Error boxes */
.stAlert {
    border-radius: 8px;
    padding: 15px;
    margin-top: 15px;
    font-size: 14px;
}
.stAlert.info {
    background-color: #1e3a5f;
    border-left: 5px solid #4A90E2;
    color: #cce7ff;
}
.stAlert.success {
    background-color: #1a3f1a;
    border-left: 5px solid #4CAF50;
    color: #b7ffb7;
}
.stAlert.error {
    background-color: #5f1a1a;
    border-left: 5px solid #ff4d4f;
    color: #ffcccc;
}
        """,
        unsafe_allow_html=True
    )
    logger.info("Custom Streamlit styles applied.")

# ====================
# SIDEBAR
# (Previously in src/ui/sidebar.py)
# ====================
def render_sidebar():
    """Renders the sidebar for the Streamlit application."""
    st.sidebar.header("Configuration")
    st.sidebar.subheader("Upload PDF for Knowledge Base")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")

    if uploaded_file is not None:
        logger.info(f"PDF file '{uploaded_file.name}' uploaded by user.")
        with st.spinner("Processing PDF... This might take a moment."):
            try:
                temp_upload_dir = "temp_uploads"
                os.makedirs(temp_upload_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_upload_dir, uploaded_file.name)
                
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                logger.info(f"Temporary PDF saved to: {temp_file_path}")

                files = {'file': (uploaded_file.name, open(temp_file_path, 'rb'), 'application/pdf')}
                API_BASE_URL = "http://localhost:8000"
                response = requests.post(f"{API_BASE_URL}/upload-pdf", files=files)
                
                if response.status_code == 200:
                    success_message = response.json().get("message", "PDF uploaded and processed successfully!")
                    st.sidebar.success(success_message)
                    logger.info(f"PDF '{uploaded_file.name}' successfully processed by backend: {success_message}")
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.sidebar.error(f"Error processing PDF: {error_detail}")
                    logger.error(f"Backend error processing PDF '{uploaded_file.name}': {response.status_code} - {error_detail}")
                
                os.remove(temp_file_path)
                logger.info(f"Temporary PDF file '{temp_file_path}' removed.")

            except requests.exceptions.ConnectionError as e:
                st.sidebar.error("Could not connect to the backend API. Please ensure the FastAPI server is running.")
                logger.critical(f"Connection error to FastAPI backend: {e}")
            except Exception as e:
                st.sidebar.error(f"An unexpected error occurred during PDF upload: {e}")
                logger.error(f"Unexpected error during PDF upload for '{uploaded_file.name}': {e}", exc_info=True)

    st.sidebar.markdown("---")
    st.sidebar.info("Upload a PDF to build the knowledge base for the chatbot. The chatbot will then answer questions based on the content of the uploaded PDF.")

# ====================
# CHATBOT
# (Previously in src/ui/chatbot.py)
# ====================
def render_chatbot():
    """Renders the main chatbot interface in Streamlit."""
    st.title("PDF-Powered Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        logger.info("Initialized new chat messages list in session state.")
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        logger.info(f"Generated new session_id: {st.session_state.session_id}")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about the PDF..."):
        logger.info(f"User input received for session_id {st.session_state.session_id}: {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    API_BASE_URL = "http://localhost:8000"
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={"message": prompt, "session_id": st.session_state.session_id}
                    )
                    response.raise_for_status()
                    bot_response = response.json().get("response", "Sorry, I couldn't get a response.")
                    logger.info(f"Bot response received for session_id {st.session_state.session_id}: {bot_response[:100]}...")
                except requests.exceptions.RequestException as e:
                    bot_response = f"Error connecting to the chatbot service: {e}"
                    logger.error(f"Request error to FastAPI backend for session_id {st.session_state.session_id}: {e}")
                except Exception as e:
                    bot_response = f"An unexpected error occurred: {e}"
                    logger.error(f"Unexpected error during chat response for session_id {st.session_state.session_id}: {e}")
            
            st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

# ====================
# MAIN APPLICATION FLOW
# ====================
def main():
    """Main entry point for the Streamlit app"""
    st.set_page_config(
        page_title="PDF-Powered Chatbot",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    set_styles()
    render_sidebar()
    render_chatbot()

if __name__ == "__main__":
    main()
