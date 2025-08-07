# services/intent_detection_service.py
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logging_utils import get_logger

logger = get_logger(__name__)

class IntentDetectionService:
    def __init__(self, llm: ChatGoogleGenerativeAI):
        self.llm = llm

    async def detect_intent(self, user_query: str) -> str:
        """
        Detects the intent of the user's query using the LLM.
        This is a simplified example; a more robust solution might use
        fine-tuned models or more complex prompt engineering.

        Args:
            user_query: The user's input query.

        Returns:
            A string representing the detected intent (e.g., "query", "chat", "unknown").
        """
        logger.info(f"Detecting intent for query: '{user_query}'")
        
        # Simple prompt for intent detection
        prompt = f"""Analyze the following user query and determine its primary intent.
        Possible intents are: 'information_retrieval', 'general_chat'.
        Return only the intent name.

        Query: "{user_query}"
        Intent:"""
        
        try:
            # Using .invoke() for a single call to the LLM
            response = self.llm.invoke(prompt)
            intent = response.content.strip().lower()

            if "information_retrieval" in intent:
                return "information_retrieval"
            elif "general_chat" in intent:
                return "general_chat"
            else:
                return "unknown"
        except Exception as e:
            logger.error(f"Error detecting intent: {e}")
            return "unknown"

