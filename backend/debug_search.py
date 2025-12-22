#!/usr/bin/env python3
"""
Debug script to test the search functionality directly
"""
from utils.embedder import Embedder
from utils.qdrant_storage import QdrantStorage

def test_search_functionality():
    """Test the search functionality directly"""

    print("Initializing embedder and Qdrant storage...")
    embedder = Embedder()
    qdrant_storage = QdrantStorage()

    print(f"Collection exists: {qdrant_storage.collection_exists()}")
    print(f"Point count: {qdrant_storage.count_points()}")

    # Test query
    test_query = "What is Physical AI?"
    print(f"\nTesting query: {test_query}")

    # Generate embedding for the query
    query_embedding = embedder.embed_single_text(test_query)
    if query_embedding:
        print(f"Query embedding dimensions: {len(query_embedding)}")

        # Search for similar content
        results = qdrant_storage.search_similar(query_embedding, top_k=5)
        print(f"Search returned {len(results)} results")

        if results:
            for i, result in enumerate(results):
                print(f"\nResult {i+1}:")
                print(f"  Score: {result['score']}")
                print(f"  URL: {result['url']}")
                print(f"  Content snippet: {result['content'][:100]}...")
        else:
            print("No results found. This indicates an issue with the search functionality.")

            # Let's try to get a sample of what's in the collection
            print("\nTrying to get a sample of stored content...")
            try:
                # Use the client directly to get some points
                from qdrant_client.http import models
                sample_result = qdrant_storage.client.scroll(
                    collection_name=qdrant_storage.collection_name,
                    limit=2
                )
                print(f"Sample points retrieved: {len(sample_result[0])}")
                for i, point in enumerate(sample_result[0]):
                    print(f"Sample {i+1}:")
                    print(f"  ID: {point.id}")
                    print(f"  Payload keys: {list(point.payload.keys())}")
                    print(f"  Content length: {len(point.payload.get('content', ''))}")
                    print(f"  Content snippet: {point.payload.get('content', '')[:100]}...")
            except Exception as e:
                print(f"Error getting sample: {e}")
    else:
        print("Failed to generate query embedding")

if __name__ == "__main__":
    test_search_functionality()