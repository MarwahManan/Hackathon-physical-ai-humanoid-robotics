# RAG Chatbot for Physical AI Humanoid Robotics Book

A complete system for creating and utilizing embeddings from the Physical AI & Humanoid Robotics textbook website. The system includes a pipeline for generating embeddings using Cohere and storing them in Qdrant, plus a FastAPI-powered RAG chatbot with NeonDB logging.

## Features

### Embedding Pipeline
- **Website Crawling**: Discovers and processes all content pages from the target website
- **Text Extraction**: Extracts clean, readable text while preserving document structure
- **Smart Chunking**: Splits content into semantically coherent chunks with overlap
- **Embedding Generation**: Uses Cohere's multilingual model for high-quality embeddings
- **Vector Storage**: Stores embeddings in Qdrant with rich metadata
- **Validation**: Includes similarity testing and retrieval accuracy validation
- **Idempotency**: Safe to run multiple times without duplicating content
- **Comprehensive Logging**: Detailed logs for monitoring and debugging

### RAG Chatbot
- **FastAPI Backend**: REST API with comprehensive endpoints
- **Cohere-powered RAG**: Context-aware responses based on book content
- **Qdrant Integration**: Vector similarity search for relevant content retrieval
- **NeonDB Logging**: Stores conversation history for analytics
- **Frontend Ready**: Designed for integration with the book website
- **Conversation Management**: Maintains context across interactions

## Prerequisites

- Python 3.8+
- UV package manager (or pip)
- Cohere API key
- Qdrant instance (local or cloud)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd physical-ai-humanoid-robotics/backend
   ```

2. **Install dependencies**
   Using UV (recommended):
   ```bash
   uv pip install -r requirements.txt
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Copy the example file and add your credentials:
   ```bash
   cp .env.example .env
   # Edit .env and add your Cohere API key and Qdrant configuration
   ```

4. **Required Environment Variables**
   - `COHERE_API_KEY`: Your Cohere API key (required)
   - `QDRANT_URL`: Qdrant instance URL (default: localhost)
   - `QDRANT_PORT`: Qdrant port (default: 6333)
   - `QDRANT_API_KEY`: Qdrant API key (if using cloud instance)

## Usage

### Running the Complete Pipeline

```bash
python main.py
```

This will execute the complete pipeline:
1. Create Qdrant collection
2. Discover all content URLs
3. Extract and chunk text
4. Generate embeddings
5. Store in Qdrant
6. Run validation tests

### Using Individual Components

You can also use individual components of the pipeline:

```python
from main import BookEmbeddingPipeline

pipeline = BookEmbeddingPipeline()

# Get URLs
urls = pipeline.get_all_urls()

# Process a single URL
success = pipeline.process_single_url("https://example.com/page")

# Run validation
results = pipeline.run_validation_tests()
```

## RAG Chatbot Usage

The system also includes a RAG chatbot with FastAPI endpoints:

### Running the RAG Chatbot

```bash
# Run the embedding pipeline only
python rag_chatbot.py pipeline

# Run the API server only
python rag_chatbot.py api

# Run both pipeline and API server
python rag_chatbot.py both

# Run API server with custom host and port
python rag_chatbot.py api --host 127.0.0.1 --port 8080
```

### API Endpoints

- `GET /` - Root endpoint
- `POST /ask` - Main chat endpoint
- `GET /health` - Health check
- `GET /collections` - Collection information
- `GET /conversations/{conversation_id}` - Get conversation history
- `GET /docs` - Interactive API documentation (Swagger UI)

### Example API Usage

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What are the key principles of humanoid robotics?",
       "conversation_id": "optional-conversation-id"
     }'
```

### Environment Variables for RAG Chatbot

Additional environment variables for the RAG chatbot:

- `NEON_DATABASE_URL`: NeonDB connection string for conversation logging (optional)

## Configuration

The pipeline can be configured via environment variables in `.env`:

- `CHUNK_SIZE`: Number of sentences per chunk (default: 512)
- `CHUNK_OVERLAP`: Overlap percentage between chunks (default: 0.1)
- `MAX_CONCURRENT_REQUESTS`: Max concurrent requests (default: 5)
- `RATE_LIMIT_DELAY`: Delay between requests in seconds (default: 1)

## Architecture

The pipeline consists of several modules:

- `config.py`: Configuration management
- `utils/url_manager.py`: URL discovery and management
- `utils/text_extractor.py`: Text extraction from web pages
- `utils/chunker.py`: Text chunking with metadata
- `utils/embedder.py`: Embedding generation with batching
- `utils/qdrant_storage.py`: Vector storage and retrieval
- `utils/validator.py`: Validation and quality checks
- `main.py`: Main pipeline orchestration

## Validation

The pipeline includes comprehensive validation:

- **Embedding Quality**: Validates dimensionality and distribution
- **Retrieval Accuracy**: Tests similarity search functionality
- **Comprehensive Validation**: End-to-end functionality testing

## Output

After running, embeddings are stored in the Qdrant collection named `rag_embedding` with the following metadata:
- URL source
- Section title
- Hierarchy path
- Chunk index
- Token count
- Content text
- Creation timestamp
- Content ID

## Error Handling

The pipeline includes robust error handling:
- Individual URL failures don't stop the entire process
- Automatic retries for API failures
- Graceful degradation when services are unavailable
- Comprehensive logging for troubleshooting

## Idempotency

The pipeline is designed to be idempotent - running it multiple times will not duplicate content. Each piece of content is assigned a unique ID based on its content hash, and the pipeline tracks what has already been processed.

## Logging

All operations are logged to both console and `pipeline.log` file. Log levels can be configured via the `LOG_LEVEL` environment variable.