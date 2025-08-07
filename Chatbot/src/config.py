import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# App settings
APP_TITLE = "RAG Web Crawler & Chatbot"
APP_ICON = "🤖"
APP_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"