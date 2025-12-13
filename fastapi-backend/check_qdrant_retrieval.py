import os
import sys
from pathlib import Path
import asyncio

# Add parent directory to sys.path to allow relative imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.vector_db_service import VectorDBService
from app.services.qdrant_service import QdrantSearchService
from app.services.logger import setup_logging, logger # Import logger

# Setup logging for the script
setup_logging()

async def check_retrieval():
    logger.info("Initializing VectorDBService and QdrantSearchService for diagnostics...")
    
    # Initialize services - ensure environment variables are loaded if not already
    vector_db_service = VectorDBService()
    search_service = QdrantSearchService(vector_db_service)

    test_queries = [
        "What are Robot Grippers and End-Effectors?",
        "Isaac Sim",
        "What is ROS 2?",
        "What is a power grasp?",
        "Explain NVIDIA Jetson",
    ]

    for query in test_queries:
        logger.info(f"\n--- Testing query: '{query}' ---")
        try:
            chunks = await search_service.search_similar_chunks(query, limit=10) # Use the same limit as in app
            
            if chunks:
                logger.info("Retrieved chunks:")
                for i, chunk in enumerate(chunks):
                    filename = chunk.get('filename', 'N/A')
                    title = chunk.get('title', 'N/A')
                    score = chunk.get('score', 'N/A')
                    logger.info(f"  {i+1}. File: {filename} (Title: {title}) - Score: {score:.4f}")
                    # print first 100 chars of content
                    logger.debug(f"     Content: {chunk.get('content', '')[:100]}...")
            else:
                logger.warning("No chunks retrieved.")
        except Exception as e:
            logger.error(f"Error during retrieval for query '{query}': {e}")

if __name__ == "__main__":
    asyncio.run(check_retrieval())
