"""
Embedding generation utilities for Book Embeddings Pipeline
"""
import os
import time
import cohere
from typing import List, Optional
import logging
from config import Config


class Embedder:
    """Handles embedding generation using Cohere API"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Validate and set up Cohere client
        api_key = Config.COHERE_API_KEY
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)
        self.model_name = "embed-multilingual-v2.0"  # 1024-dimensional model
        self.max_batch_size = 96  # Cohere's max batch size

    def embed_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for a list of texts using Cohere with batching

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors or None on failure
        """
        if not texts:
            self.logger.warning("No texts provided for embedding")
            return None

        all_embeddings = []

        # Process in batches to respect API limits
        for i in range(0, len(texts), self.max_batch_size):
            batch = texts[i:i + self.max_batch_size]

            try:
                self.logger.info(f"Processing batch {i//self.max_batch_size + 1}/{(len(texts)-1)//self.max_batch_size + 1}")

                response = self.client.embed(
                    texts=batch,
                    model=self.model_name
                )

                batch_embeddings = [embedding for embedding in response.embeddings]
                all_embeddings.extend(batch_embeddings)

                # Add a small delay between batches to be respectful to the API
                time.sleep(Config.RATE_LIMIT_DELAY)

            except Exception as e:
                self.logger.error(f"Error generating embeddings for batch starting at index {i}: {str(e)}")

                # Try single text processing as fallback
                batch_fallback = []
                for j, text in enumerate(batch):
                    try:
                        single_response = self.client.embed(
                            texts=[text],
                            model=self.model_name
                        )
                        batch_fallback.extend([embedding for embedding in single_response.embeddings])
                        time.sleep(Config.RATE_LIMIT_DELAY * 0.1)  # Shorter delay for single requests
                    except Exception as single_e:
                        self.logger.error(f"Failed to embed single text at index {i+j}: {str(single_e)}")
                        batch_fallback.append(None)  # Placeholder for failed embedding

                # Only add successful embeddings to all_embeddings
                successful_embeddings = [emb for emb in batch_fallback if emb is not None]
                all_embeddings.extend(successful_embeddings)

        self.logger.info(f"Successfully generated embeddings for {len(all_embeddings)} texts")
        return all_embeddings

    def embed_single_text(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text

        Args:
            text: Text to embed

        Returns:
            Embedding vector or None on failure
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model_name
            )

            if response.embeddings and len(response.embeddings) > 0:
                embedding = response.embeddings[0]
                self.logger.debug(f"Generated embedding for text of length {len(text)}")
                return embedding
            else:
                self.logger.error("No embeddings returned for single text")
                return None

        except Exception as e:
            self.logger.error(f"Error generating embedding for single text: {str(e)}")
            return None

    def get_model_info(self) -> dict:
        """
        Get information about the embedding model

        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "dimensions": 768,  # Cohere's multilingual model actually has 768 dimensions
            "max_batch_size": self.max_batch_size
        }