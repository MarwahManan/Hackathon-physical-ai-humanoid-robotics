# Content Entity Data Model

**Feature**: 1-book-embeddings-pipeline
**Created**: 2025-12-20
**Entity**: Crawled Content

## Definition

The Content Entity represents text content extracted from web pages during the crawling process.

## Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier for the content item |
| url | string | Yes | Source URL of the content |
| title | string | Yes | Page title extracted from HTML |
| content | string | Yes | Clean text content extracted from the page |
| content_type | string | Yes | Type of content (e.g., "documentation", "blog", "module") |
| created_at | timestamp | Yes | Time when content was crawled |
| updated_at | timestamp | Yes | Time when content was last updated |
| word_count | integer | Yes | Number of words in the content |
| metadata | object | No | Additional metadata extracted from page |

## Validation Rules

- url must be a valid HTTP/HTTPS URL
- content must be non-empty string with minimum 50 characters
- content_type must be one of: "documentation", "blog", "module", "intro", "research"
- created_at and updated_at must be in ISO 8601 format
- word_count must be a positive integer

## Relationships

- One Content entity can generate multiple Chunk entities
- Belongs to a specific website source identified by domain

## State Transitions

Content entities are created during the crawling phase and remain immutable after creation. Updates occur only when content is re-crawled due to changes at the source URL.