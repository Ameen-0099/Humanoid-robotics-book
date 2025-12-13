import sys
from pathlib import Path
import os
import asyncio

# Add the project root to sys.path to resolve imports correctly
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root / "app"))

from app.services.vector_db_service import VectorDBService
from app.services.qdrant_service import QdrantSearchService

async def main():
    # Ensure environment variables are set or hardcoded in vector_db_service.py for this to work
    vector_db_service = VectorDBService()
    search_service = QdrantSearchService(vector_db_service)

    # Example query
    query = "What are the core concepts of ROS 2?"
    print(f"Searching for: '{query}'")
    results = await search_service.search_similar_chunks(query)

    if results:
        for i, chunk in enumerate(results):
            print(f"\n--- Result {i+1} (Score: {chunk['score']:.2f}) ---")
            print(f"Title: {chunk['title']}")
            print(f"Filename: {chunk['filename']}")
            print(f"Content: {chunk['content'][:200]}...\n")
    else:
        print("No similar chunks found.")

if __name__ == '__main__':
    asyncio.run(main())
