from openai import OpenAI
from typing import List, Dict, Any, Optional
import os

class OpenAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.openai_client = OpenAI(api_key=api_key)
        self.chat_model = os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")

    def synthesize_answer(self, query: str, chunks: List[Dict[str, Any]], selected_text: Optional[str] = None) -> str:
        """
        Synthesizes an answer using the retrieved chunks, the user's query, and optionally selected text.
        """
        if not chunks:
            return "I couldn't find any relevant information in the book to answer your question."

        context = "\n\n---\n\n".join([chunk['content'] for chunk in chunks])

        system_message = "You are an expert assistant for the book 'Humanoid Robotics: A Modern Approach'."
        
        user_prompt_parts = []
        user_prompt_parts.append("Synthesize a comprehensive answer based on the following context retrieved from the book. Do NOT directly quote or list the context. Formulate a coherent response in your own words.")
        if selected_text:
            user_prompt_parts.append(f"The user has also highlighted the following text: '{selected_text}'. Prioritize information related to this selected text when formulating your answer.")
        user_prompt_parts.append("If the context is insufficient to answer the question, clearly state that the provided text does not contain enough information and do not attempt to answer.")
        user_prompt_parts.append("\nContext from the book:\n---")
        user_prompt_parts.append(context)
        user_prompt_parts.append("---\n")
        user_prompt_parts.append(f"User's Question: {query}\n")
        user_prompt_parts.append("Answer:")

        prompt = "\n".join(user_prompt_parts)

        try:
            response = self.openai_client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during OpenAI chat completion: {e}")
            raise

