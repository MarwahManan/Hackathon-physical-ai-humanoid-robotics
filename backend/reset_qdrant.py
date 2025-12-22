#!/usr/bin/env python3
"""
Script to reset the Qdrant collection for the RAG chatbot
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import Config

def reset_qdrant_collection():
    """Delete and recreate the Qdrant collection with correct vector size"""

    # Initialize Qdrant client
    if Config.QDRANT_API_KEY:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY,
            port=Config.QDRANT_PORT
        )
    else:
        client = QdrantClient(
            url=Config.QDRANT_URL,
            port=Config.QDRANT_PORT
        )

    collection_name = Config.COLLECTION_NAME

    try:
        # Delete the existing collection
        print(f"Deleting existing collection: {collection_name}")
        client.delete_collection(collection_name)
        print(f"Collection {collection_name} deleted successfully")
    except Exception as e:
        print(f"Collection {collection_name} might not exist yet, creating new one. Error: {e}")

    # Create new collection with correct vector size (768 for Cohere's embed-multilingual-v2.0)
    print(f"Creating new collection: {collection_name} with 768-dimensional vectors")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=768,  # Cohere embed-multilingual-v2.0 model actually has 768 dimensions
            distance=models.Distance.COSINE
        )
    )

    print(f"Collection {collection_name} created successfully with correct vector dimensions!")

    # Verify the collection exists
    collections = client.get_collections()
    existing_collections = [col.name for col in collections.collections]
    if collection_name in existing_collections:
        print(f"Verification: Collection {collection_name} exists in Qdrant")
        count = client.count(collection_name=collection_name)
        print(f"Current point count: {count.count}")
    else:
        print(f"Error: Collection {collection_name} was not created properly")

if __name__ == "__main__":
    reset_qdrant_collection()