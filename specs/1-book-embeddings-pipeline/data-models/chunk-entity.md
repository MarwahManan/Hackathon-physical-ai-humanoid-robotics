# Chunk Entity Data Model

**Feature**: 1-book-embeddings-pipeline
**Created**: 2025-12-20
**Entity**: Text Chunk

## Definition

The Chunk Entity represents a semantically coherent segment of text that has been processed from the original content for embedding generation.

## Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the chunk |
| content_id | string | Yes | Reference to the parent Content entity |
| chunk_text | string | Yes | The actual text content of the chunk |
| chunk_index | integer | Yes | Sequential index of the chunk within the original content |
| token_count | integer | Yes | Number of tokens in the chunk |
| section_title | string | No | Title of the section this chunk belongs to |
| hierarchy_path | string | No | Document hierarchy (e.g., "chapter-1/lesson-1-1") |
| overlap_with_next | integer | No | Number of overlapping tokens with next chunk |
| created_at | timestamp | Yes | Time when chunk was created |

## Validation Rules

- content_id must reference a valid Content entity
- chunk_text must be non-empty string with minimum 20 characters
- chunk_text must not exceed 1000 tokens to fit within embedding model limits
- chunk_index must be a non-negative integer
- token_count must be a positive integer not exceeding 1000
- hierarchy_path must follow format with forward slashes as separators

## Relationships

- Belongs to one Content entity (parent-child relationship)
- Associated with one Embedding Vector entity after processing
- Multiple chunks can belong to the same content source

## State Transitions

Chunk entities are created during the text processing phase and remain immutable after creation. They are linked to embedding vectors once the embedding process is complete.