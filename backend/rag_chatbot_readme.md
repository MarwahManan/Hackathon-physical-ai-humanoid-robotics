# RAG Chatbot for Physical AI Humanoid Robotics Book

This project implements a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI Humanoid Robotics book using Cohere, Qdrant, FastAPI, and NeonDB.

## Features

- **Cohere-powered RAG**: Uses Cohere's embedding and generation models for context-aware responses
- **Qdrant Vector Storage**: Stores and retrieves book content using vector similarity search
- **FastAPI Backend**: Provides REST API endpoints for chat interactions
- **NeonDB Logging**: Logs all conversations for analytics and audit purposes
- **Web UI Ready**: API designed to integrate with the book website frontend

## Architecture

The system consists of:
1. **Embedding Pipeline**: Extracts content from the book website, chunks it, and stores embeddings in Qdrant
2. **RAG API**: Handles user queries, retrieves relevant content, generates responses, and logs interactions
3. **Database Layer**: Stores conversation history in Neon Serverless Postgres

## Prerequisites

- Python 3.11+
- Cohere API key
- Qdrant instance (local or cloud)
- Optional: NeonDB for conversation logging

## Environment Variables

Create a `.env` file with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url
QDRANT_PORT=6333
QDRANT_API_KEY=your_qdrant_api_key  # if using cloud
TARGET_BASE_URL=https://physical-ai-humanoid-robotics-vert.vercel.app
NEON_DATABASE_URL=your_neon_database_url  # optional
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The application can run in different modes:

### 1. Run the Embedding Pipeline Only

This processes the book content and stores embeddings in Qdrant:

```bash
python rag_chatbot.py pipeline
```

### 2. Run the API Server Only

This starts the FastAPI server for chat interactions:

```bash
python rag_chatbot.py api
```

### 3. Run Both Pipeline and API

This runs the embedding pipeline first, then starts the API server:

```bash
python rag_chatbot.py both
```

### 4. Custom Host and Port

You can specify custom host and port for the API:

```bash
python rag_chatbot.py api --host 127.0.0.1 --port 8080
```

## API Endpoints

- `GET /` - Root endpoint
- `POST /ask` - Main chat endpoint
- `GET /health` - Health check
- `GET /collections` - Collection information
- `GET /conversations/{conversation_id}` - Get conversation history
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example API Usage

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What are the key principles of humanoid robotics?",
       "conversation_id": "optional-conversation-id"
     }'
```

## Docker Deployment

Build and run with Docker:

```bash
# Build the image
docker build -t rag-chatbot .

# Run the container
docker run -p 8000:8000 -v ./.env:/app/.env rag-chatbot
```

## Configuration

The application uses the following configuration:

- **CHUNK_SIZE**: Size of text chunks (default: 512)
- **CHUNK_OVERLAP**: Overlap between chunks as fraction (default: 0.1)
- **MAX_CONCURRENT_REQUESTS**: Max concurrent requests (default: 5)
- **RATE_LIMIT_DELAY**: Delay between requests (default: 1.0)

## Frontend Integration

The API is designed to integrate with the Physical AI Humanoid Robotics book website. The frontend can:

1. Send user queries to the `/ask` endpoint
2. Display responses with source references
3. Maintain conversation context using conversation IDs
4. Show conversation history

## Error Handling

The API includes comprehensive error handling:

- Graceful degradation when Qdrant is unavailable
- Fallback mechanisms for Cohere API failures
- Detailed logging for debugging
- Proper HTTP status codes

## Security

- CORS middleware configured for cross-origin requests
- Input validation on all endpoints
- Environment variables for sensitive data
- Rate limiting considerations (implement at infrastructure level)

## Monitoring and Logging

- Detailed logging for debugging
- Health check endpoint for monitoring
- Conversation logging to NeonDB
- Performance metrics available through FastAPI

## Development

For development, you can run the application with auto-reload:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```