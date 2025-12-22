# Quickstart Guide: Book Embeddings Pipeline

**Feature**: 1-book-embeddings-pipeline
**Created**: 2025-12-20

## Overview

This guide provides quick instructions to set up and run the Book Embeddings Pipeline that crawls the Physical AI & Humanoid Robotics textbook website, generates embeddings, and stores them in Qdrant.

## Prerequisites

- Python 3.8 or higher
- UV package manager (or pip)
- Access to Cohere API
- Access to Qdrant instance (local or cloud)

## Setup

### 1. Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here  # Default: localhost
QDRANT_PORT=your_qdrant_port_here  # Default: 6333
```

### 2. Install Dependencies

Using UV (recommended):
```bash
cd backend
uv pip install -r requirements.txt
```

Or using pip:
```bash
cd backend
pip install -r requirements.txt
```

## Running the Pipeline

### Basic Execution
```bash
cd backend
python main.py
```

### Configuration Options

The pipeline can be configured using environment variables:
- `COHERE_API_KEY`: Required - Your Cohere API key
- `QDRANT_URL`: Optional - Qdrant instance URL (default: localhost)
- `QDRANT_PORT`: Optional - Qdrant port (default: 6333)
- `BASE_URL`: Optional - Website to crawl (default: https://physical-ai-humanoid-robotics-vert.vercel.app)

## Pipeline Steps

The pipeline executes in the following sequence:

1. **URL Discovery**: Crawls the website to identify all content pages
2. **Content Extraction**: Extracts clean text from each page
3. **Text Chunking**: Splits content into semantically coherent chunks
4. **Embedding Generation**: Creates vector embeddings using Cohere
5. **Storage**: Saves embeddings to Qdrant with metadata

## Expected Output

Upon successful execution, you will see:
- Console logs showing progress through each step
- A Qdrant collection named "rag_embedding" with all processed content
- Processed count statistics

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure `COHERE_API_KEY` is properly set
2. **Qdrant Connection**: Verify Qdrant is running and accessible
3. **Rate Limits**: The pipeline handles rate limiting automatically
4. **Crawling Errors**: Individual URL failures won't stop the entire pipeline

### Monitoring Progress

Check the console output for progress indicators and error messages. The pipeline is designed to continue processing even if individual pages fail.