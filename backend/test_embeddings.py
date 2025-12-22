#!/usr/bin/env python3
"""
Test script to check the actual embedding dimensions from the embedder
"""
from utils.embedder import Embedder

def test_embedding_dimensions():
    """Test what dimensions the embedder actually produces"""

    try:
        embedder = Embedder()
        test_text = "This is a test sentence for embedding dimension check."

        print("Testing single text embedding...")
        single_embedding = embedder.embed_single_text(test_text)

        if single_embedding:
            print(f"Single embedding dimensions: {len(single_embedding)}")
            print(f"Model info: {embedder.get_model_info()}")
        else:
            print("Failed to generate single embedding")

        print("\nTesting batch embedding...")
        batch_texts = [test_text, "Another test sentence.", "Third test sentence."]
        batch_embeddings = embedder.embed_texts(batch_texts)

        if batch_embeddings and len(batch_embeddings) > 0:
            print(f"Batch embedding dimensions for first embedding: {len(batch_embeddings[0])}")
            print(f"Number of batch embeddings: {len(batch_embeddings)}")
        else:
            print("Failed to generate batch embeddings")

    except Exception as e:
        print(f"Error during embedding test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_embedding_dimensions()