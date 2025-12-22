"""
NeonDB Logger for RAG Chatbot Conversations
Handles logging of chat interactions to Neon Serverless Postgres
"""
import asyncpg
import os
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)


class NeonLogger:
    """Handles logging of chatbot conversations to NeonDB"""

    def __init__(self):
        self.neon_url = os.getenv("NEON_DATABASE_URL")
        if not self.neon_url:
            logger.warning("NEON_DATABASE_URL environment variable not set. Logging will be disabled.")
        self.pool = None

    async def initialize(self):
        """Initialize the database connection pool"""
        if not self.neon_url:
            logger.warning("NeonDB logging disabled - no database URL provided")
            return

        try:
            self.pool = await asyncpg.create_pool(
                self.neon_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )

            # Create the conversations table if it doesn't exist
            await self._create_tables()
            logger.info("NeonDB connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NeonDB connection pool: {str(e)}")
            self.pool = None

    async def _create_tables(self):
        """Create necessary tables if they don't exist"""
        if not self.pool:
            return

        create_table_query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id SERIAL PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            sources JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_ip TEXT,
            metadata JSONB
        );
        """

        async with self.pool.acquire() as connection:
            await connection.execute(create_table_query)
            logger.info("Conversations table created or already exists")

    async def log_interaction(self,
                            conversation_id: str,
                            user_message: str,
                            bot_response: str,
                            sources: Optional[List[Dict[str, Any]]] = None,
                            user_ip: Optional[str] = None,
                            metadata: Optional[Dict[str, Any]] = None):
        """
        Log a chat interaction to NeonDB

        Args:
            conversation_id: Unique identifier for the conversation
            user_message: The user's input message
            bot_response: The chatbot's response
            sources: List of sources used to generate the response
            user_ip: User's IP address (optional)
            metadata: Additional metadata (optional)
        """
        if not self.pool or not self.neon_url:
            logger.debug("NeonDB logging disabled - no database connection")
            return

        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO conversations
                    (conversation_id, user_message, bot_response, sources, user_ip, metadata)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    conversation_id,
                    user_message,
                    bot_response,
                    sources or [],
                    user_ip,
                    metadata or {}
                )
                logger.debug(f"Logged interaction for conversation {conversation_id}")
        except Exception as e:
            logger.error(f"Failed to log interaction to NeonDB: {str(e)}")

    async def get_conversation_history(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a specific conversation ID

        Args:
            conversation_id: The conversation ID to retrieve
            limit: Maximum number of messages to return

        Returns:
            List of conversation messages
        """
        if not self.pool or not self.neon_url:
            logger.debug("NeonDB logging disabled - no database connection")
            return []

        try:
            async with self.pool.acquire() as connection:
                rows = await connection.fetch(
                    """
                    SELECT conversation_id, user_message, bot_response,
                           timestamp, sources, metadata
                    FROM conversations
                    WHERE conversation_id = $1
                    ORDER BY timestamp DESC
                    LIMIT $2
                    """,
                    conversation_id, limit
                )

                return [
                    {
                        "conversation_id": row["conversation_id"],
                        "user_message": row["user_message"],
                        "bot_response": row["bot_response"],
                        "timestamp": row["timestamp"],
                        "sources": row["sources"],
                        "metadata": row["metadata"]
                    }
                    for row in rows
                ]
        except Exception as e:
            logger.error(f"Failed to retrieve conversation history: {str(e)}")
            return []

    async def close(self):
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("NeonDB connection pool closed")