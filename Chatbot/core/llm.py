# core/llm.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings
from loguru import logger

def get_llm():
    """
    Initializes and returns a Google Gemini LLM instance.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment variables.")
        raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment.")

    # FIX: Use the correct, modern model name for text generation
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
    logger.info("Google Gemini LLM initialized.")
    return llm
