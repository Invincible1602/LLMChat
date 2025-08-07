# services/chat_service.py
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from core.vectorstore import VectorStore
from loguru import logger
from src.utils.memory import get_chat_history_memory

class ChatService:
    def __init__(self, llm: ChatGoogleGenerativeAI, vector_store: VectorStore):
        self.llm = llm
        self.vector_store = vector_store
        self.qa_chain = self._setup_qa_chain()

    def _setup_qa_chain(self):
        """
        Sets up the Langchain RetrievalQA chain for question answering.
        """
        template = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
        retriever = self.vector_store.vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        logger.info("Langchain RetrievalQA chain set up.")
        return qa_chain

    async def get_chat_response(self, message: str, session_id: str) -> str:
        """
        Gets a chat response from the LLM based on the message and retrieved context.
        Uses Langchain's RetrievalQA chain.
        """
        logger.info(f"Getting chat response for session_id: {session_id}, message: {message}")

        try:
            result = self.qa_chain.invoke({"query": message})
            response_text = result["result"]
            source_documents = result.get("source_documents", [])
            if source_documents:
                logger.info(f"Source documents used for response: {[doc.metadata.get('source') for doc in source_documents]}")

            # FIX: Call the methods on the chat_memory attribute of the memory object
            chat_memory = get_chat_history_memory(session_id)
            chat_memory.chat_memory.add_user_message(message)
            chat_memory.chat_memory.add_ai_message(response_text)

            logger.info(f"Generated response: {response_text[:100]}...")
            return response_text
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return "I'm sorry, I encountered an error while trying to respond. Please try again."

