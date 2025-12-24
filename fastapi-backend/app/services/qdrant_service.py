import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient, models
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv # For direct loading in this service if needed

# For robust loading from current working directory or parents if script is run from various locations
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)


class QdrantSearchService:
    def __init__(self, vector_db_service_instance):
        self.vector_db_service = vector_db_service_instance
        self.collection_name = self.vector_db_service.collection_name
        self.openai_client = self.vector_db_service.openai_client # Reuse the initialized OpenAI client
        self.qdrant_client = self.vector_db_service.qdrant_client # Reuse the initialized Qdrant client

    async def search_similar_chunks(self, query_text: str, selected_text: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Searches Qdrant for document chunks semantically similar to the query_text,
        optionally enhancing the query with selected_text.
        """
        if not query_text.strip():
            return []

        # Experimental "Manual Boost" for search relevance
        KEYWORD_TO_TITLE_BOOST = {
            "ros": "Chapter 2: The Robotic Nervous System: An Introduction to ROS 2",
            "isaac": "Chapter 4: The Modern AI Stack: NVIDIA Isaac and Jetson",
            "jetson": "Chapter 4: The Modern AI Stack: NVIDIA Isaac and Jetson",
            "kinematics": "Chapter 6: Movement: Humanoid Kinematics and Locomotion",
            "manipulation": "Chapter 7: Manipulation: Grasping and Interaction",
            "grasping": "Chapter 7: Manipulation: Grasping and Interaction",
            "gripper": "Chapter 7: Manipulation: Grasping and Interaction",
        }
        
        query_lower = query_text.lower()
        boost_text = ""
        for keyword, title in KEYWORD_TO_TITLE_BOOST.items():
            if keyword in query_lower:
                boost_text = title
                print(f"DEBUG: Boosting query with title: {title}")
                break

        # Enhance query_text with selected_text and/or boost_text
        enhanced_query = query_text
        if selected_text:
            enhanced_query = f"{selected_text}\n\n{enhanced_query}"
        if boost_text:
            enhanced_query = f"{boost_text}\n\n{enhanced_query}"


        # 1. Generate embedding for the enhanced query
        query_embedding = self.vector_db_service.generate_embedding(enhanced_query)
        if not query_embedding:
            print(f"Failed to generate embedding for query: {enhanced_query}")
            return []

        # 2. Search Qdrant for similar vectors
        try:
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=0.0,  # Be more inclusive with search results (temporarily for debugging)
                with_payload=True
            )

            # Extract relevant information from search results
            similar_chunks = []
            for hit in search_result:
                similar_chunks.append({
                    "content": hit.payload.get("content"),
                    "filename": hit.payload.get("metadata", {}).get("filename"),
                    "title": hit.payload.get("metadata", {}).get("title"),
                    "score": hit.score
                })
            return similar_chunks
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            raise

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Ensure environment variables are set or hardcoded in vector_db_service.py for this to work
    # For direct execution, adjust sys.path to find parent modules
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
    from app.services.vector_db_service import VectorDBService

    vector_db_service = VectorDBService()
    search_service = QdrantSearchService(vector_db_service)

    # Example query
    query = "What are the core concepts of ROS 2?"
    print(f"Searching for: '{query}'")
    results = search_service.search_similar_chunks(query)

    if results:
        for i, chunk in enumerate(results):
            print(f"\n--- Result {i+1} (Score: {chunk['score']:.2f}) ---")
            print(f"Title: {chunk['title']}")
            print(f"Filename: {chunk['filename']}")
            print(f"Content: {chunk['content'][:200]}...\n")
    else:
        print("No similar chunks found for general query.")
    
    print("\n--- Testing with selected text ---")
    selected_text_example = "Robot Operating System"
    query_example_selected = "What are its main advantages?"
    print(f"Searching for: '{query_example_selected}' with selected text: '{selected_text_example}'")
    results_selected = search_service.search_similar_chunks(query_example_selected, selected_text=selected_text_example)

    if results_selected:
        for i, chunk in enumerate(results_selected):
            print(f"\n--- Result {i+1} (Score: {chunk['score']:.2f}) ---")
            print(f"Title: {chunk['title']}")
            print(f"Filename: {chunk['filename']}")
            print(f"Content: {chunk['content'][:200]}...\n")
    else:
        print("No similar chunks found for selected text query.")
