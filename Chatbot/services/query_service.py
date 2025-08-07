# services/query_service.py
from typing import List, Dict
from core.vectorstore import VectorStore
from loguru import logger # Import logger directly from loguru

# The loguru.logger instance is globally configured by setup_logging in app.py.
# Therefore, we can directly import and use 'logger' here without calling get_logger(__name__).

class QueryService:
    def __init__(self, vector_store: VectorStore):
        """
        Initializes the QueryService with a VectorStore instance.

        Args:
            vector_store: An instance of the VectorStore (e.g., PineconeVectorStore wrapper).
        """
        self.vector_store = vector_store
        logger.info("QueryService initialized.")

    async def query_vector_store(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Queries the vector database for relevant documents based on the input query.
        This method performs a similarity search to find the most relevant chunks.

        Args:
            query: The user's query string.
            top_k: The number of top relevant documents to retrieve from the vector store.

        Returns:
            A list of dictionaries, where each dictionary represents a retrieved document
            with its 'content' and 'metadata'.
        """
        logger.info(f"Querying vector store for: '{query}' with top_k={top_k}")
        
        # Perform the similarity search using the vector store
        results = self.vector_store.similarity_search(query, k=top_k)
        
        logger.info(f"Retrieved {len(results)} results for query: '{query}'")
        return results

