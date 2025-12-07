import os
from dotenv import load_dotenv
import requests
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY not found in .env file")
        self.base_url = "https://api.anthropic.com/v1"  # Replace with actual Claude API endpoint
        # Use a session object for performance improvements
        self.session = requests.Session()

    def post(self, endpoint, data):
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        try:
            response = self.session.post(f"{self.base_url}/{endpoint}", json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Handle exceptions for network errors, invalid responses, etc.
            logger.error(f"An error occurred during API request: {e}")
            return {"error": "API request failed", "details": str(e)}

if __name__ == '__main__':
    # Example usage:
    client = ApiClient()
    # Replace 'your_endpoint' and the payload with actual values
    # response_data = client.post('your_endpoint', {'prompt': 'Hello, Claude!'})
    # if response_data:
    #     print("Response:", response_data)
