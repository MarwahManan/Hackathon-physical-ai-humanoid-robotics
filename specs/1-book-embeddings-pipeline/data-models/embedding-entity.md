# Embedding Entity Data Model

**Feature**: 1-book-embeddings-pipeline
**Created**: 2025-12-20
**Entity**: Embedding Vector

## Definition

The Embedding Entity represents the vector representation of a text chunk, generated using the Cohere embedding model, and stored in Qdrant for semantic search.

## Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the embedding |
| chunk_id | string | Yes | Reference to the source Chunk entity |
| vector | array[float] | Yes | 1024-dimensional vector representation |
| vector_size | integer | Yes | Size of the vector (should be 1024 for Cohere) |
| model_name | string | Yes | Name of the model used to generate the embedding |
| model_version | string | Yes | Version of the model used |
| metadata | object | Yes | Additional metadata for the embedding |
| metadata.url | string | Yes | Source URL of the original content |
| metadata.section | string | No | Section title or hierarchy |
| metadata.chunk_id | string | Yes | Reference to source chunk |
| metadata.created_at | timestamp | Yes | Time when embedding was created |
| created_at | timestamp | Yes | Time when embedding was stored in Qdrant |

## Validation Rules

- chunk_id must reference a valid Chunk entity
- vector must be an array of exactly 1024 floating-point numbers
- vector_size must equal 1024
- model_name must be "embed-multilingual-v2.0" (or other valid Cohere model)
- model_version must be a valid semantic version string
- metadata.url must be a valid URL
- metadata.created_at must be in ISO 8601 format

## Relationships

- Belongs to one Chunk entity (processed from)
- Stored in Qdrant collection named "rag_embedding"
- Used for semantic similarity search and retrieval

## State Transitions

Embedding entities are created during the embedding generation phase and stored in Qdrant. Once stored, they remain immutable and are used for semantic search operations.