# core/vectorstore.py
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List, Dict
from config.settings import settings
from loguru import logger

class VectorStore:
    def __init__(self, embeddings: GoogleGenerativeAIEmbeddings):
        self.embeddings = embeddings
        self.pinecone_api_key = settings.PINECONE_API_KEY
        self.pinecone_index_name = settings.PINECONE_INDEX_NAME
        self.pinecone_client = None
        self.vectorstore = None
        self._initialize_pinecone()

    def _initialize_pinecone(self):
        if not self.pinecone_api_key:
            logger.error("Pinecone API key not set.")
            raise ValueError("Pinecone API key must be set in settings or env vars.")

        try:
            # Initialize Pinecone client (no environment param now)
            self.pinecone_client = Pinecone(api_key=self.pinecone_api_key)

            # Check existing indexes (list_indexes now returns dicts)
            existing_indexes = [idx["name"] for idx in self.pinecone_client.list_indexes()]
            if self.pinecone_index_name not in existing_indexes:
                logger.info(f"Creating Pinecone index: {self.pinecone_index_name}")
                self.pinecone_client.create_index(
                    name=self.pinecone_index_name,
                    dimension=len(self.embeddings.embed_query("test")),
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )

            # Initialize LangChain PineconeVectorStore
            self.vectorstore = PineconeVectorStore(
                index_name=self.pinecone_index_name,
                embedding=self.embeddings,
                pinecone_api_key=self.pinecone_api_key
            )
            logger.info(f"Pinecone vector store initialized with index: {self.pinecone_index_name}")

        except Exception as e:
            logger.error(f"Failed to initialize Pinecone vector store: {e}", exc_info=True)
            raise

    def add_documents(self, documents: List[Dict]) -> int:
        if not self.vectorstore:
            logger.error("Vector store not initialized. Cannot add documents.")
            return 0

        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        try:
            self.vectorstore.add_texts(texts=texts, metadatas=metadatas)
            logger.info(f"Added {len(documents)} documents to Pinecone.")
            return len(documents)
        except Exception as e:
            logger.error(f"Failed to add documents to Pinecone: {e}", exc_info=True)
            return 0

    def similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        if not self.vectorstore:
            logger.error("Vector store not initialized. Cannot perform similarity search.")
            return []

        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            results = [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
            logger.info(f"Performed similarity search for query: '{query}'. Retrieved {len(results)} results.")
            return results
        except Exception as e:
            logger.error(f"Failed to perform similarity search in Pinecone: {e}", exc_info=True)
            return []

    def delete_all_documents(self):
        if self.pinecone_client:
            existing_indexes = [idx["name"] for idx in self.pinecone_client.list_indexes()]
            if self.pinecone_index_name in existing_indexes:
                try:
                    self.pinecone_client.delete_index(self.pinecone_index_name)
                    logger.info(f"Deleted Pinecone index: {self.pinecone_index_name}")
                    self._initialize_pinecone()
                except Exception as e:
                    logger.error(f"Failed to delete Pinecone index: {e}", exc_info=True)
            else:
                logger.info("Pinecone index does not exist. Nothing to delete.")
        else:
            logger.info("Pinecone client not initialized. Nothing to delete.")
