import requests
from typing import Dict, Any

from src.config import API_BASE_URL


class RagAPIClient:
    """Client for interacting with the RAG backend API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        
    def crawl_url(self, url: str) -> Dict[str, Any]:
        """Crawl and index a URL through the API"""
        try:
            response = requests.post(
                f"{self.base_url}/crawl",
                json={"url": url},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
            
    def chat(self, message: str, conversation_history=None) -> Dict[str, Any]:
        """Send a chat message to the API"""
        try:
            payload = {"message": message}
            if conversation_history:
                payload["conversation_history"] = conversation_history
                
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}