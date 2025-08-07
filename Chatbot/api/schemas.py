from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class CrawlRequest(BaseModel):
    """Request model for the crawl endpoint."""
    url: HttpUrl = Field(..., description="URL to crawl for content")

class CrawlResponse(BaseModel):
    """Response model for the crawl endpoint."""
    url: str = Field(..., description="URL that was crawled")
    chunk_count: int = Field(..., description="Number of text chunks extracted")
    processed_count: int = Field(..., description="Number of relevant text chunks after preprocessing")
    indexed_count: int = Field(..., description="Number of chunks successfully indexed")

class QueryRequest(BaseModel):
    """Request model for the query endpoint."""
    query: str = Field(..., min_length=1, description="Query string to search for similar documents")

class QueryResponse(BaseModel):
    """Response model for the query endpoint."""
    query: str = Field(..., description="Original query string")
    results: List[str] = Field(..., description="List of retrieved text chunks")

class ConversationItem(BaseModel):
    """Model for a single conversation message."""
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    message: str = Field(..., min_length=1, description="User's message")
    conversation_history: Optional[List[ConversationItem]] = Field(
        default=None, 
        description="Previous conversation history"
    )

class ChatResponse(BaseModel):
    """Response model for the chat endpoint."""
    response: str = Field(..., description="Assistant's response")

class ErrorResponse(BaseModel):
    """Standard error response model."""
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")