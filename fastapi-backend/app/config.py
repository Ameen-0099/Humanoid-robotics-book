import os
from dotenv import load_dotenv
from pathlib import Path

# Determine the path to the .env file in the parent directory (fastapi-backend)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Database connection URL for Neon
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


