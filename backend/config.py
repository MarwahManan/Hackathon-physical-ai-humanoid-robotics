"""
Configuration module for Book Embeddings Pipeline
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class to manage application settings"""

    # Cohere API settings
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    # Qdrant settings
    QDRANT_URL = os.getenv("QDRANT_URL", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # Target website settings
    TARGET_BASE_URL = os.getenv("TARGET_BASE_URL", "https://physical-ai-humanoid-robotics-vert.vercel.app")
    TARGET_SITEMAP_URL = os.getenv("TARGET_SITEMAP_URL",
                                  "https://physical-ai-humanoid-robotics-vert.vercel.app/sitemap.xml")

    # Processing settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 512))
    CHUNK_OVERLAP = float(os.getenv("CHUNK_OVERLAP", 0.1))
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", 5))
    RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", 1.0))

    # Qdrant collection name
    COLLECTION_NAME = "rag_embedding"

    # Validation
    REQUIRED_ENV_VARS = [
        "COHERE_API_KEY"
    ]

    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        missing_vars = []
        for var in cls.REQUIRED_ENV_VARS:
            if not getattr(cls, var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")