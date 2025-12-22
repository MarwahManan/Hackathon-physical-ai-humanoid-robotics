@echo off
REM Startup script for RAG Chatbot API on Windows

echo Starting RAG Chatbot API...
echo Make sure you have installed the required dependencies:
echo pip install -r requirements.txt
echo.

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found. Please create one with required environment variables.
    echo Required variables: COHERE_API_KEY, QDRANT_URL
    echo Optional: QDRANT_API_KEY, NEON_DATABASE_URL
    echo.
)

REM Start the API server
python rag_chatbot.py api --host 0.0.0.0 --port 8000

pause