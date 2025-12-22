"""
Qdrant storage utilities for Book Embeddings Pipeline
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import logging
from config import Config
from utils.chunker import ContentChunk


class QdrantStorage:
    """Handles storage and retrieval of embeddings in Qdrant"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize Qdrant client
        if Config.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
                port=Config.QDRANT_PORT
            )
        else:
            self.client = QdrantClient(
                url=Config.QDRANT_URL,
                port=Config.QDRANT_PORT
            )

        self.collection_name = Config.COLLECTION_NAME

    def create_collection(self, vector_size=768):
        """
        Create Qdrant collection for storing embeddings

        Args:
            vector_size: Dimension of the vectors to store (default 768 for Cohere embeddings)
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            existing_collections = [col.name for col in collections.collections]

            if self.collection_name in existing_collections:
                self.logger.info(
                    f"Collection {self.collection_name} already exists, deleting and recreating..."
                )
                self.client.delete_collection(self.collection_name)

            # Create new collection with specified dimensional vectors using cosine distance
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )

            self.logger.info(
                f"Created collection {self.collection_name} with {vector_size}-dimensional vectors using cosine distance"
            )

        except Exception as e:
            self.logger.error(f"Error creating collection {self.collection_name}: {str(e)}")
            raise

    def save_chunk_to_qdrant(self, chunk: ContentChunk, embedding: List[float]):
        """
        Save a single chunk and its embedding to Qdrant
        """
        try:
            payload = {
                "url": chunk.url,
                "section": chunk.section_title,
                "hierarchy_path": chunk.hierarchy_path,
                "chunk_index": chunk.chunk_index,
                "token_count": chunk.token_count,
                "content": chunk.chunk_text,
                "created_at": chunk.created_at,
                "content_id": chunk.content_id
            }

            import uuid
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.id))

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                ]
            )

            self.logger.debug(f"Saved chunk {chunk.id} to Qdrant collection {self.collection_name}")

        except Exception as e:
            self.logger.error(f"Error saving chunk {chunk.id} to Qdrant: {str(e)}")
            raise

    def save_chunks_batch(self, chunks: List[ContentChunk], embeddings: List[List[float]]):
        """
        Save multiple chunks and their embeddings to Qdrant in a batch operation
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Number of chunks ({len(chunks)}) must match number of embeddings ({len(embeddings)})"
            )

        try:
            points = []
            import uuid

            for chunk, embedding in zip(chunks, embeddings):
                payload = {
                    "url": chunk.url,
                    "section": chunk.section_title,
                    "hierarchy_path": chunk.hierarchy_path,
                    "chunk_index": chunk.chunk_index,
                    "token_count": chunk.token_count,
                    "content": chunk.chunk_text,
                    "created_at": chunk.created_at,
                    "content_id": chunk.content_id
                }

                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.id))

                point = models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
                points.append(point)

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            self.logger.info(f"Saved {len(chunks)} chunks to Qdrant collection {self.collection_name}")

        except Exception as e:
            self.logger.error(f"Error saving batch of {len(chunks)} chunks to Qdrant: {str(e)}")
            raise

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks to the query embedding

        Args:
            query_embedding: Query embedding vector
            top_k: Number of similar chunks to return

        Returns:
            List of similar chunks with their metadata and similarity scores
        """
        try:
            search_result = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=top_k
            ).points

            similar_chunks = []
            for result in search_result:
                chunk_info = {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                    "content": result.payload.get("content", ""),
                    "url": result.payload.get("url", ""),
                    "section": result.payload.get("section", ""),
                    "hierarchy_path": result.payload.get("hierarchy_path", "")
                }
                similar_chunks.append(chunk_info)

            self.logger.debug(f"Found {len(similar_chunks)} similar chunks for query")
            return similar_chunks

        except Exception as e:
            self.logger.error(f"Error searching for similar chunks: {str(e)}")
            return []

    def count_points(self) -> int:
        """
        Count the number of points in the collection
        """
        try:
            count = self.client.count(collection_name=self.collection_name)
            return count.count
        except Exception as e:
            self.logger.error(f"Error counting points in collection: {str(e)}")
            return 0

    def collection_exists(self) -> bool:
        """
        Check if the collection exists
        """
        try:
            collections = self.client.get_collections()
            existing_collections = [col.name for col in collections.collections]
            return self.collection_name in existing_collections
        except Exception as e:
            self.logger.error(f"Error checking if collection exists: {str(e)}")
            return False
