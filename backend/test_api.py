"""
Test script for the RAG Chatbot API
This script tests the main functionality of the RAG chatbot API
"""
import asyncio
import json
from api.main import app
from pydantic import BaseModel

# Import TestClient inside the function to avoid issues when running the API server
def run_tests():
    from fastapi.testclient import TestClient

    # Create a test client
    client = TestClient(app)

    def test_api_endpoints():
        """Test the main API endpoints"""
        print("Testing RAG Chatbot API endpoints...")

        # Test root endpoint
        response = client.get("/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")

        # Test health endpoint
        response = client.get("/health")
        print(f"Health endpoint: {response.status_code} - {response.json()}")

        # Test collections endpoint
        response = client.get("/collections")
        print(f"Collections endpoint: {response.status_code} - {response.json()}")

        # Test ask endpoint with a sample query
        # Note: This requires the Qdrant collection to exist and have data
        sample_query = {
            "message": "What is humanoid robotics?",
            "conversation_id": "test-conversation-123"
        }

        response = client.post("/ask", json=sample_query)
        print(f"Ask endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Query: {result.get('query', 'N/A')}")
            print(f"Answer: {result.get('answer', 'N/A')[:100]}...")  # First 100 chars
            print(f"Sources: {len(result.get('sources', []))} sources")
            print(f"Conversation ID: {result.get('conversation_id', 'N/A')}")
        else:
            print(f"Error: {response.text}")

    test_api_endpoints()

if __name__ == "__main__":
    run_tests()