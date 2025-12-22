"""
Validation utilities for Book Embeddings Pipeline
"""
import numpy as np
from typing import List, Dict, Any
import logging
from config import Config
from utils.embedder import Embedder
from utils.qdrant_storage import QdrantStorage


class Validator:
    """Validates the quality and accuracy of embeddings and retrieval"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.embedder = Embedder()
        self.storage = QdrantStorage()

    def validate_embedding_quality(self, test_texts: List[str]) -> Dict[str, Any]:
        """
        Validate the quality of generated embeddings

        Args:
            test_texts: List of test texts to validate

        Returns:
            Dictionary with validation results
        """
        if not test_texts:
            return {"error": "No test texts provided"}

        try:
            embeddings = self.embedder.embed_texts(test_texts)

            if not embeddings or len(embeddings) != len(test_texts):
                return {"error": f"Mismatch in embeddings count: expected {len(test_texts)}, got {len(embeddings) if embeddings else 0}"}

            # Calculate statistics about the embeddings
            embedding_array = np.array(embeddings)
            dimensions = embedding_array.shape[1]
            norms = np.linalg.norm(embedding_array, axis=1)

            # Calculate similarity between consecutive texts (should be low if texts are different)
            similarities = []
            for i in range(len(embeddings) - 1):
                sim = self._cosine_similarity(embeddings[i], embeddings[i+1])
                similarities.append(sim)

            results = {
                "embedding_count": len(embeddings),
                "dimensions": dimensions,
                "average_norm": float(np.mean(norms)),
                "std_norm": float(np.std(norms)),
                "average_similarity_adjacent": float(np.mean(similarities)) if similarities else 0,
                "min_similarity_adjacent": float(np.min(similarities)) if similarities else 0,
                "max_similarity_adjacent": float(np.max(similarities)) if similarities else 0,
                "is_valid": dimensions == 1024  # Cohere model should produce 1024-dimensional vectors
            }

            self.logger.info(f"Embedding quality validation completed: {results}")
            return results

        except Exception as e:
            self.logger.error(f"Error validating embedding quality: {str(e)}")
            return {"error": str(e)}

    def validate_retrieval_accuracy(self, test_queries: List[str], expected_urls: List[str] = None) -> Dict[str, Any]:
        """
        Validate the accuracy of retrieval from Qdrant

        Args:
            test_queries: List of query texts to test retrieval
            expected_urls: Optional list of expected URLs for each query

        Returns:
            Dictionary with retrieval validation results
        """
        if not test_queries:
            return {"error": "No test queries provided"}

        try:
            results = {
                "query_count": len(test_queries),
                "successful_retrievals": 0,
                "accuracy_metrics": [],
                "average_recall": 0.0
            }

            for i, query in enumerate(test_queries):
                # Generate embedding for query
                query_embedding = self.embedder.embed_single_text(query)
                if not query_embedding:
                    self.logger.warning(f"Failed to generate embedding for query {i+1}")
                    continue

                # Search in Qdrant
                similar_chunks = self.storage.search_similar(query_embedding, top_k=5)

                if not similar_chunks:
                    self.logger.warning(f"No similar chunks found for query {i+1}")
                    continue

                results["successful_retrievals"] += 1

                # Calculate accuracy if expected URLs are provided
                if expected_urls and i < len(expected_urls):
                    expected_url = expected_urls[i]
                    top_result = similar_chunks[0] if similar_chunks else None

                    if top_result and expected_url in top_result.get("url", ""):
                        accuracy = 1.0
                    else:
                        # Check if expected URL is in top 5 results
                        found_in_top5 = any(expected_url in chunk.get("url", "") for chunk in similar_chunks)
                        accuracy = 1.0 if found_in_top5 else 0.0

                    results["accuracy_metrics"].append({
                        "query_index": i,
                        "query": query[:100] + "..." if len(query) > 100 else query,
                        "accuracy": accuracy,
                        "top_result_url": top_result.get("url", "") if top_result else "",
                        "expected_url": expected_url
                    })

            if results["accuracy_metrics"]:
                results["average_recall"] = sum(m["accuracy"] for m in results["accuracy_metrics"]) / len(results["accuracy_metrics"])

            self.logger.info(f"Retrieval validation completed: {results}")
            return results

        except Exception as e:
            self.logger.error(f"Error validating retrieval accuracy: {str(e)}")
            return {"error": str(e)}

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """
        Run comprehensive validation of the entire pipeline

        Returns:
            Dictionary with comprehensive validation results
        """
        try:
            results = {
                "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
                "collection_exists": self.storage.collection_exists(),
                "total_points": 0,
                "embedding_validation": None,
                "retrieval_validation": None,
                "overall_status": "unknown"
            }

            if results["collection_exists"]:
                results["total_points"] = self.storage.count_points()

                # Run a simple retrieval test if there are points in the collection
                if results["total_points"] > 0:
                    # Get a sample point to use for testing
                    sample_search = self.storage.client.scroll(
                        collection_name=self.storage.collection_name,
                        limit=1
                    )
                    if sample_search[0]:
                        sample_content = sample_search[0][0].payload.get("content", "")
                        if sample_content:
                            retrieval_test = self.validate_retrieval_accuracy([sample_content[:200]])
                            results["retrieval_validation"] = retrieval_test

            # Run embedding quality test with sample texts
            sample_texts = [
                "Physical AI and Humanoid Robotics fundamentals",
                "Machine learning applications in robotics",
                "Sensor fusion for robotic perception",
                "Motion planning algorithms for humanoid robots"
            ]
            results["embedding_validation"] = self.validate_embedding_quality(sample_texts)

            # Determine overall status
            if results["embedding_validation"].get("is_valid", False):
                results["overall_status"] = "success"
            else:
                results["overall_status"] = "failed"

            self.logger.info(f"Comprehensive validation completed: status={results['overall_status']}")
            return results

        except Exception as e:
            self.logger.error(f"Error running comprehensive validation: {str(e)}")
            return {"error": str(e), "overall_status": "error"}

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity value between -1 and 1
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)