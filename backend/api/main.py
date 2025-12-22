"""
RAG Chatbot API for Physical AI Humanoid Robotics Book
FastAPI application with Cohere-powered RAG functionality and NeonDB logging
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import os
from datetime import datetime
import uuid
import asyncio

# Import existing pipeline components
import sys
import os
# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import BookEmbeddingPipeline
from utils.embedder import Embedder
from utils.qdrant_storage import QdrantStorage
from config import Config
from database.neon_logger import NeonLogger

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize pipeline components
pipeline = BookEmbeddingPipeline()
embedder = Embedder()
qdrant_storage = QdrantStorage()
neon_logger = NeonLogger()

# Pydantic models
class ChatMessage(BaseModel):
    """Model for chat messages"""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for chat responses"""
    response: str
    conversation_id: str
    sources: List[Dict[str, Any]]
    timestamp: str


class RAGResponse(BaseModel):
    """Model for RAG responses"""
    query: str
    answer: str
    sources: List[Dict[str, Any]]
    conversation_id: str


# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Humanoid Robotics RAG Chatbot API",
    description="Cohere-powered RAG chatbot for Physical AI Humanoid Robotics book with NeonDB logging",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize NeonDB logger on startup
@app.on_event("startup")
async def startup_event():
    """Initialize NeonDB logger on application startup"""
    await neon_logger.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    """Close NeonDB connection on application shutdown"""
    await neon_logger.close()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Physical AI Humanoid Robotics RAG Chatbot API", "status": "active"}


@app.post("/ask", response_model=RAGResponse)
async def ask_question(request: Request, chat_message: ChatMessage):
    """
    Ask a question to the RAG chatbot

    This endpoint:
    1. Embeds the user's query using Cohere
    2. Searches for similar content in Qdrant
    3. Generates a response using Cohere based on retrieved context
    4. Logs the interaction to NeonDB
    5. Returns the answer with source references
    """
    try:
        logger.info(f"Processing query: {chat_message.message}")

        # Generate conversation ID if not provided
        conversation_id = chat_message.conversation_id or str(uuid.uuid4())

        # Generate embedding for the query
        query_embedding = embedder.embed_single_text(chat_message.message)
        if not query_embedding:
            raise HTTPException(status_code=500, detail="Failed to generate query embedding")

        # Search for similar content in Qdrant
        similar_chunks = qdrant_storage.search_similar(query_embedding, top_k=5)

        if not similar_chunks:
            # If no similar content found, return a default response
            response = RAGResponse(
                query=chat_message.message,
                answer="I couldn't find relevant information in the Physical AI Humanoid Robotics book to answer your question.",
                sources=[],
                conversation_id=conversation_id
            )

            # Log the interaction to NeonDB
            await neon_logger.log_interaction(
                conversation_id=conversation_id,
                user_message=chat_message.message,
                bot_response=response.answer,
                sources=[],
                user_ip=request.client.host if request.client else None
            )

            return response

        # Prepare context from retrieved chunks
        context_parts = []
        sources = []

        for chunk in similar_chunks:
            content = chunk.get('content', '')
            if content:
                context_parts.append(content)

                # Add source information
                sources.append({
                    'url': chunk.get('url', ''),
                    'section': chunk.get('section', ''),
                    'hierarchy_path': chunk.get('hierarchy_path', ''),
                    'similarity_score': chunk.get('score', 0.0)
                })

        # Combine context
        context = "\n\n".join(context_parts)

        # Generate response using Cohere Chat API
        import cohere
        co = cohere.Client(Config.COHERE_API_KEY)

        # Create a message that combines the query with the context
        message = f"""
        Based on the following context from the Physical AI Humanoid Robotics book, please answer the question.

        Context:
        {context}

        Question: {chat_message.message}

        Answer:
        """

        response = co.chat(
            message=message,
            max_tokens=500,
            temperature=0.3
        )

        answer = response.text.strip()

        # Create the response object
        rag_response = RAGResponse(
            query=chat_message.message,
            answer=answer,
            sources=sources,
            conversation_id=conversation_id
        )

        # Log the interaction to NeonDB
        await neon_logger.log_interaction(
            conversation_id=conversation_id,
            user_message=chat_message.message,
            bot_response=answer,
            sources=sources,
            user_ip=request.client.host if request.client else None,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "context_length": len(context),
                "source_count": len(sources)
            }
        )

        # Return the response
        return rag_response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if Qdrant collection exists
        collection_exists = qdrant_storage.collection_exists()
        if not collection_exists:
            return {"status": "unhealthy", "details": "Qdrant collection does not exist"}

        # Check if there are points in the collection
        point_count = qdrant_storage.count_points()

        return {
            "status": "healthy",
            "qdrant_collection": Config.COLLECTION_NAME,
            "point_count": point_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


@app.get("/collections")
async def get_collections():
    """Get information about available collections"""
    try:
        count = qdrant_storage.count_points()
        exists = qdrant_storage.collection_exists()

        return {
            "collection_name": Config.COLLECTION_NAME,
            "exists": exists,
            "point_count": count,
            "model_info": embedder.get_model_info()
        }
    except Exception as e:
        logger.error(f"Error getting collections: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting collections: {str(e)}")


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get conversation history for a specific conversation ID

    Args:
        conversation_id: The conversation ID to retrieve

    Returns:
        List of conversation messages
    """
    try:
        history = await neon_logger.get_conversation_history(conversation_id)
        return {"conversation_id": conversation_id, "history": history}
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)