"""
RAG Chatbot Main Entry Point
This file serves as the main entry point for the RAG Chatbot application.
It can run either the embedding pipeline or the FastAPI server based on command line arguments.
"""
import argparse
import sys
import os
import uvicorn
from api.main import app
from main import BookEmbeddingPipeline
from config import Config


def run_pipeline():
    """Run the book embedding pipeline"""
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


def run_api(host="0.0.0.0", port=8000):
    """Run the FastAPI server"""
    print(f"Starting RAG Chatbot API server on {host}:{port}")
    print("API Documentation available at http://localhost:8000/docs")
    uvicorn.run(app, host=host, port=port)


def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description="RAG Chatbot for Physical AI Humanoid Robotics Book")
    parser.add_argument(
        "command",
        choices=["pipeline", "api", "both"],
        help="Command to run: 'pipeline' for embedding pipeline, 'api' for FastAPI server, 'both' for pipeline then API"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host for the API server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the API server (default: 8000)"
    )

    args = parser.parse_args()

    if args.command == "pipeline":
        run_pipeline()
    elif args.command == "api":
        run_api(args.host, args.port)
    elif args.command == "both":
        # First run the pipeline to ensure embeddings are available
        run_pipeline()
        print("\nStarting API server after pipeline completion...")
        run_api(args.host, args.port)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()