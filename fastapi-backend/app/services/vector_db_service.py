import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient, models
import os
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient, models
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment Variable Loading ---
# Securely load credentials and configuration from environment variables.
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- END Environment Variable Loading ---


class VectorDBService:
    def __init__(self):
        # Fallback to hardcoded values if .env loading fails during debugging
        self.qdrant_client = self._initialize_qdrant_client(
            qdrant_url=QDRANT_URL,
            qdrant_api_key=QDRANT_API_KEY
        )
        self.openai_client = self._initialize_openai_client(
            openai_api_key=OPENAI_API_KEY
        )
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_chunks")

    def _initialize_qdrant_client(self, qdrant_url: str, qdrant_api_key: str) -> QdrantClient:
        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")
        
        return QdrantClient(
            url=qdrant_url, 
            api_key=qdrant_api_key,
            timeout=60 # Increased timeout to 60 seconds
        )

    def _initialize_openai_client(self, openai_api_key: str) -> OpenAI:
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set.")
        
        return OpenAI(api_key=openai_api_key)

    def create_collection(self):
        """Creates a Qdrant collection for storing book chunks if it doesn't exist."""
        try:
            self.qdrant_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created or recreated successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")

    def generate_embedding(self, text: str) -> List[float]:
        """Generates an embedding for the given text using OpenAI."""
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding for text: '{text[:50]}...' - {e}")
            return []

    def upsert_chunks_to_qdrant(self, chunks: List[Dict[str, Any]]):
        """
        Generates embeddings for a list of chunks and upserts them to Qdrant.
        Each chunk should have 'content' and 'metadata'.
        """
        points = []
        for i, chunk in enumerate(chunks):
            embedding = self.generate_embedding(chunk["content"])
            if embedding:
                points.append(
                    models.PointStruct(
                        id=i,  # Simple incremental ID for now, can be UUID or hash
                        vector=embedding,
                        payload=chunk  # Store the chunk content and metadata as payload
                    )
                )
        
        if points:
            try:
                operation_info = self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    wait=True,
                    points=points
                )
                print(f"Upserted {len(points)} points to Qdrant. Status: {operation_info.status}")
            except Exception as e:
                print(f"Error upserting points to Qdrant: {e}")
        else:
            print("No points to upsert.")

# Example usage (for testing purposes)
if __name__ == '__main__':
    from .ingestion_service import IngestionService # Import IngestionService

    # Adjust paths as necessary for testing
    # Corrected path: Go up from services -> app -> fastapi-backend -> humanoid-robotics-book, then into docusaurus-book/docs
    project_root = Path(__file__).resolve().parent.parent.parent.parent # Points to humanoid-robotics-book
    docs_root = project_root / 'docusaurus-book' / 'docs'

    ingestion_service = IngestionService(docs_root, chunk_size=500, chunk_overlap=50)
    book_chunks = ingestion_service.load_book_content()

    vector_db_service = VectorDBService()
    vector_db_service.create_collection() # Ensure collection exists

    # Upsert chunks in batches if there are many
    batch_size = 50
    for i in range(0, len(book_chunks), batch_size):
        batch = book_chunks[i:i + batch_size]
        print(f"Upserting batch {int(i/batch_size) + 1}/{(len(book_chunks) // batch_size) + 1} ({len(batch)} chunks)...")
        vector_db_service.upsert_chunks_to_qdrant(batch)
    
    print("\nFinished embedding and storing book chunks in Qdrant.")
