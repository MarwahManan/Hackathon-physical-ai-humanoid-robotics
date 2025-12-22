"""
Book Embeddings Pipeline
Main implementation with all required functionality
"""
import asyncio
import hashlib
import os
from typing import List, Tuple, Optional
import logging
from datetime import datetime

# Import all the utility modules
from config import Config
from utils.logger import get_logger
from utils.url_manager import URLManager
from utils.text_extractor import TextExtractor
from utils.chunker import TextChunker, ContentChunk
from utils.embedder import Embedder
from utils.qdrant_storage import QdrantStorage
from utils.validator import Validator


class BookEmbeddingPipeline:
    """Main class for the book embeddings pipeline with full functionality"""

    def __init__(self):
        """Initialize the pipeline with all required components"""
        # Setup logging
        self.logger = get_logger(__name__)
        Config.validate()  # Validate configuration

        # Initialize all components
        self.url_manager = URLManager()
        self.text_extractor = TextExtractor()
        self.chunker = TextChunker()
        self.embedder = Embedder()
        self.storage = QdrantStorage()
        self.validator = Validator()

        # Track processed content to enable idempotency
        self.processed_content = set()

    def get_all_urls(self) -> List[str]:
        """
        Get all URLs from the deployed website that need to be processed

        Returns:
            List of URLs to process
        """
        self.logger.info(f"Starting to discover URLs from: {Config.TARGET_BASE_URL}")
        urls = self.url_manager.get_all_urls()
        self.logger.info(f"Discovered {len(urls)} URLs to process")
        return urls

    def extract_text_from_url(self, url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Extract clean text content from a URL

        Args:
            url: URL to extract text from

        Returns:
            Tuple of (title, content, hierarchy_path) or (None, None, None) on failure
        """
        return self.text_extractor.extract_text_from_url(url)

    def chunk_text(self, text: str, content_id: str, url: str, section_title: str = "", hierarchy_path: str = "") -> List[ContentChunk]:
        """
        Split text into chunks with specified size and overlap

        Args:
            text: Text to chunk
            content_id: ID of the original content
            url: Source URL of the content
            section_title: Title of the section
            hierarchy_path: Hierarchy path of the content

        Returns:
            List of ContentChunk objects
        """
        return self.chunker.chunk_text(text, content_id, url, section_title, hierarchy_path)

    def embed(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Generate embeddings for a list of texts using Cohere

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors or None on failure
        """
        return self.embedder.embed_texts(texts)

    def create_collection(self, collection_name: str = "rag_embedding"):
        """
        Create Qdrant collection for storing embeddings

        Args:
            collection_name: Name of the collection to create (uses config default if None)
        """
        collection_name = collection_name or Config.COLLECTION_NAME
        self.storage.create_collection(vector_size=768)  # Cohere embed-multilingual-v2.0 model actually has 768 dimensions

    def save_chunk_to_qdrant(self, chunk: ContentChunk, embedding: List[float]):
        """
        Save a chunk and its embedding to Qdrant

        Args:
            chunk: ContentChunk object
            embedding: Embedding vector
        """
        self.storage.save_chunk_to_qdrant(chunk, embedding)

    def run_validation_tests(self) -> dict:
        """
        Run validation tests to verify pipeline functionality

        Returns:
            Dictionary with validation results
        """
        return self.validator.run_comprehensive_validation()

    def _generate_content_id(self, url: str, content: str) -> str:
        """
        Generate a unique content ID based on URL and content hash

        Args:
            url: Source URL
            content: Content text

        Returns:
            Unique content ID
        """
        content_hash = hashlib.md5((url + content[:100]).encode('utf-8')).hexdigest()[:12]
        return f"content_{content_hash}"

    def _has_been_processed(self, content_id: str) -> bool:
        """
        Check if content has already been processed (idempotency)

        Args:
            content_id: Content ID to check

        Returns:
            True if content has been processed, False otherwise
        """
        return content_id in self.processed_content

    def _mark_as_processed(self, content_id: str):
        """
        Mark content as processed (idempotency)

        Args:
            content_id: Content ID to mark as processed
        """
        self.processed_content.add(content_id)

    def process_single_url(self, url: str) -> bool:
        """
        Process a single URL through the entire pipeline

        Args:
            url: URL to process

        Returns:
            True if processing was successful, False otherwise
        """
        try:
            self.logger.info(f"Processing URL: {url}")

            # Extract text from URL
            title, content, hierarchy_path = self.extract_text_from_url(url)

            if not content:
                self.logger.warning(f"No content extracted from {url}")
                return False

            # Generate content ID
            content_id = self._generate_content_id(url, content)

            # Check if already processed (idempotency)
            if self._has_been_processed(content_id):
                self.logger.info(f"Content already processed (idempotency check): {content_id}")
                return True

            # Chunk the content
            chunks = self.chunk_text(content, content_id, url, title, hierarchy_path)

            if not chunks:
                self.logger.warning(f"No chunks created for {url}")
                return False

            # Extract text from chunks for embedding
            chunk_texts = [chunk.chunk_text for chunk in chunks]

            # Generate embeddings
            embeddings = self.embed(chunk_texts)

            if not embeddings or len(embeddings) != len(chunks):
                self.logger.error(f"Mismatch in embeddings and chunks for {url}")
                return False

            # Save chunks to Qdrant
            for chunk, embedding in zip(chunks, embeddings):
                self.save_chunk_to_qdrant(chunk, embedding)

            # Mark as processed
            self._mark_as_processed(content_id)

            self.logger.info(f"Successfully processed {len(chunks)} chunks from {url}")
            return True

        except Exception as e:
            self.logger.error(f"Error processing {url}: {str(e)}")
            return False

    def run_pipeline(self):
        """
        Run the complete pipeline: URLs → Text Extraction → Chunking → Embeddings → Storage
        """
        self.logger.info("Starting Book Embeddings Pipeline...")

        # Step 1: Create Qdrant collection
        self.logger.info("Step 1: Creating Qdrant collection...")
        self.create_collection()
        self.logger.info(f"Collection '{Config.COLLECTION_NAME}' ready")

        # Step 2: Get all URLs
        self.logger.info("Step 2: Discovering URLs to process...")
        urls = self.get_all_urls()
        self.logger.info(f"Found {len(urls)} URLs to process")

        # Step 3: Process each URL
        self.logger.info("Step 3: Processing URLs and generating embeddings...")
        processed_count = 0
        failed_count = 0

        for i, url in enumerate(urls):
            self.logger.info(f"Processing {i+1}/{len(urls)}: {url}")

            success = self.process_single_url(url)
            if success:
                processed_count += 1
            else:
                failed_count += 1

            # Add delay between URLs to be respectful to the server
            import time
            time.sleep(Config.RATE_LIMIT_DELAY)

        # Step 4: Run validation
        self.logger.info("Step 4: Running validation tests...")
        validation_results = self.run_validation_tests()
        self.logger.info(f"Validation completed: {validation_results}")

        # Summary
        total_processed = processed_count + failed_count
        success_rate = (processed_count / total_processed * 100) if total_processed > 0 else 0

        summary = {
            "total_urls": len(urls),
            "processed": processed_count,
            "failed": failed_count,
            "success_rate": f"{success_rate:.2f}%",
            "validation_results": validation_results
        }

        self.logger.info(f"Pipeline completed! Summary: {summary}")
        return summary


def main():
    """
    Main execution function that runs the complete pipeline
    """
    print("Starting Book Embeddings Pipeline...")
    print("=" * 50)

    # Initialize the pipeline
    pipeline = BookEmbeddingPipeline()

    # Run the complete pipeline
    results = pipeline.run_pipeline()

    print("=" * 50)
    print("Pipeline Execution Summary:")
    print(f"  Total URLs discovered: {results['total_urls']}")
    print(f"  Successfully processed: {results['processed']}")
    print(f"  Failed to process: {results['failed']}")
    print(f"  Success rate: {results['success_rate']}")
    print(f"  Validation status: {results['validation_results'].get('overall_status', 'unknown')}")
    print("Embeddings have been stored in Qdrant collection:", Config.COLLECTION_NAME)
    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()