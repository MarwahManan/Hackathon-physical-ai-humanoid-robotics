"""
Text chunking utilities for Book Embeddings Pipeline
"""
import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import re
import logging
from config import Config


@dataclass
class ContentChunk:
    """Represents a chunk of content with metadata"""
    id: str
    content_id: str
    chunk_text: str
    chunk_index: int
    token_count: int
    section_title: str
    hierarchy_path: str
    overlap_with_next: int
    created_at: str
    url: str = ""


class TextChunker:
    """Handles text chunking with metadata preservation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.chunk_size = Config.CHUNK_SIZE
        self.overlap = Config.CHUNK_OVERLAP

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
        if not text or len(text.strip()) == 0:
            return []

        # Split text into sentences to maintain semantic coherence
        sentences = self._split_into_sentences(text)

        if not sentences:
            return []

        chunks = []
        chunk_index = 0
        current_start = 0

        # Calculate overlap in sentences
        overlap_sentences = int(len(sentences) * self.overlap)

        while current_start < len(sentences):
            # Determine the end position for this chunk
            current_end = min(current_start + self.chunk_size, len(sentences))

            # Build chunk text
            chunk_sentences = sentences[current_start:current_end]
            chunk_text = ' '.join(chunk_sentences).strip()

            if len(chunk_text) == 0:
                current_start = current_end
                continue

            # Calculate overlap with next chunk
            overlap_with_next = 0
            if current_end < len(sentences):
                overlap_with_next = min(overlap_sentences, len(sentences) - current_end)

            # Create chunk ID based on content hash and index
            content_hash = hashlib.md5(chunk_text.encode('utf-8')).hexdigest()[:8]
            chunk_id = f"{content_id}_chunk_{content_hash}_{chunk_index}"

            # Count tokens (approximate using words)
            token_count = len(chunk_text.split())

            chunk = ContentChunk(
                id=chunk_id,
                content_id=content_id,
                chunk_text=chunk_text,
                chunk_index=chunk_index,
                token_count=token_count,
                section_title=section_title,
                hierarchy_path=hierarchy_path,
                overlap_with_next=overlap_with_next,
                created_at=datetime.utcnow().isoformat(),
                url=url
            )

            chunks.append(chunk)

            # Move to next chunk with overlap
            current_start = current_end - overlap_sentences if current_end < len(sentences) else current_end
            chunk_index += 1

        self.logger.info(f"Created {len(chunks)} chunks from text (content_id: {content_id})")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences while preserving sentence boundaries

        Args:
            text: Text to split into sentences

        Returns:
            List of sentences
        """
        # Use regex to split on sentence boundaries while preserving the delimiters
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        sentences = re.split(sentence_pattern, text)

        # Clean up sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                cleaned_sentences.append(sentence)

        return cleaned_sentences

    def chunk_with_sliding_window(self, text: str, content_id: str, url: str, section_title: str = "", hierarchy_path: str = "") -> List[ContentChunk]:
        """
        Alternative chunking method using sliding window approach

        Args:
            text: Text to chunk
            content_id: ID of the original content
            url: Source URL of the content
            section_title: Title of the section
            hierarchy_path: Hierarchy path of the content

        Returns:
            List of ContentChunk objects
        """
        if not text or len(text.strip()) == 0:
            return []

        # Simple tokenization by words (approximate)
        words = text.split()

        if len(words) == 0:
            return []

        # Calculate chunk size and overlap in words
        words_per_chunk = self.chunk_size
        overlap_words = int(words_per_chunk * self.overlap)

        chunks = []
        chunk_index = 0
        start_idx = 0

        while start_idx < len(words):
            end_idx = min(start_idx + words_per_chunk, len(words))
            chunk_words = words[start_idx:end_idx]
            chunk_text = ' '.join(chunk_words)

            if len(chunk_text.strip()) == 0:
                start_idx = end_idx
                continue

            # Calculate overlap with next chunk
            overlap_with_next = 0
            if end_idx < len(words):
                overlap_with_next = min(overlap_words, len(words) - end_idx)

            # Create chunk ID based on content hash and index
            content_hash = hashlib.md5(chunk_text.encode('utf-8')).hexdigest()[:8]
            chunk_id = f"{content_id}_chunk_{content_hash}_{chunk_index}"

            chunk = ContentChunk(
                id=chunk_id,
                content_id=content_id,
                chunk_text=chunk_text,
                chunk_index=chunk_index,
                token_count=len(chunk_words),
                section_title=section_title,
                hierarchy_path=hierarchy_path,
                overlap_with_next=overlap_with_next,
                created_at=datetime.utcnow().isoformat(),
                url=url
            )

            chunks.append(chunk)

            # Move to next chunk with overlap
            start_idx = end_idx - overlap_words if end_idx < len(words) else end_idx
            chunk_index += 1

        self.logger.info(f"Created {len(chunks)} chunks from text using sliding window (content_id: {content_id})")
        return chunks