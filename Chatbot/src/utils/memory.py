# src/utils/memory.py
from langchain.memory import ConversationBufferWindowMemory
from typing import Dict, Any, List
from loguru import logger # Import logger directly from loguru

# No need to call get_logger(__name__) here, as loguru.logger is globally configured by setup_logging in app.py

# Dictionary to store chat history for different sessions.
# In a production environment, this would typically be backed by a persistent
# storage solution like a database (e.g., Redis, Firestore) for scalability.
_session_memories: Dict[str, ConversationBufferWindowMemory] = {}

def get_chat_history_memory(session_id: str, k: int = 5) -> ConversationBufferWindowMemory:
    """
    Retrieves or creates a ConversationBufferWindowMemory for a given session ID.
    This memory type keeps the last 'k' interactions in the conversation,
    which is useful for managing context length and performance.

    Args:
        session_id: The unique identifier for the chat session. This allows
                    the chatbot to maintain separate conversations for different users.
        k: The number of previous interactions (user message + AI response) to remember.

    Returns:
        A ConversationBufferWindowMemory instance for the specified session.
    """
    if session_id not in _session_memories:
        logger.info(f"Initializing new chat memory for session_id: {session_id} with k={k}") # Log the creation of new memory
        _session_memories[session_id] = ConversationBufferWindowMemory(
            memory_key="chat_history", # Key under which chat history will be stored in the memory object
            k=k, # Set the window size for remembering past interactions
            return_messages=True # Return messages as a list of message objects (HumanMessage, AIMessage)
        )
    else:
        logger.debug(f"Retrieving existing chat memory for session_id: {session_id}") # Log when an existing memory is retrieved
    return _session_memories[session_id]

def clear_chat_history_memory(session_id: str):
    """
    Clears the entire chat history for a specific session.
    This effectively resets the conversation for that session.

    Args:
        session_id: The unique identifier for the chat session whose history needs to be cleared.
    """
    if session_id in _session_memories:
        _session_memories[session_id].clear() # Clear the memory buffer
        logger.info(f"Cleared chat memory for session_id: {session_id}") # Log the action of clearing memory
    else:
        logger.warning(f"Attempted to clear non-existent chat memory for session_id: {session_id}") # Log a warning if the session doesn't exist

def get_all_session_ids() -> List[str]:
    """
    Returns a list of all active session IDs currently managed by the in-memory store.
    """
    logger.debug("Retrieving all active session IDs.") # Log the request for all session IDs
    return list(_session_memories.keys())

