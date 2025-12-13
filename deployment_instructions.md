# Deployment Instructions for Humanoid Robotics Book Chatbot

This document provides instructions for deploying both the FastAPI backend and the Docusaurus frontend, including Docker-based deployments.

## Prerequisites

-   Docker and Docker Compose installed.
-   Node.js and npm/yarn (for Docusaurus development/local build outside Docker).
-   Python and pip (for FastAPI development/local run outside Docker).
-   **Qdrant Cloud Free Tier account**: Needed for the vector database.
-   **Neon Serverless Postgres database**: (If chat history and user context features are enabled, otherwise optional).
-   **OpenAI API keys**: For embedding generation and chat completions.

## 1. Setup API Keys

Before deploying, ensure your API keys for Qdrant and OpenAI are configured.

**Option A: Environment Variables (Recommended for Production)**

Set the following environment variables on your deployment environment:

-   `QDRANT_URL`
-   `QDRANT_API_KEY`
-   `OPENAI_API_KEY`
-   `OPENAI_EMBEDDING_MODEL` (e.g., `text-embedding-ada-002`)
-   `OPENAI_CHAT_MODEL` (e.g., `gpt-3.5-turbo`)
-   `QDRANT_COLLECTION_NAME` (e.g., `book_chunks`)

**Option B: Direct Update in `vector_db_service.py` (Development/Local Debugging)**

For local development or debugging, you can temporarily update the hardcoded values in `fastapi-backend/app/services/vector_db_service.py`. **Remember to never commit sensitive keys to version control.**

## 2. Ingest Book Content into Qdrant

This step processes your book's Markdown files, generates embeddings, and stores them in your Qdrant instance.

1.  Navigate to the `fastapi-backend` directory:
    ```bash
    cd fastapi-backend
    ```
2.  Install backend dependencies (if not already done):
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the ingestion script:
    ```bash
    python -m app.services.vector_db_service
    ```
    This script will connect to Qdrant (using your configured API keys) and populate the `book_chunks` collection.

## 3. Deployment with Docker (Recommended)

Docker provides a consistent environment for deploying both the backend and frontend.

### 3.1. Build Docker Images

Navigate to the project root directory.

```bash
# Build FastAPI backend image
docker build -t humanoid-robotics-backend -f fastapi-backend/Dockerfile .

# Build Docusaurus frontend image
docker build -t humanoid-robotics-frontend -f docusaurus-book/Dockerfile .
```

### 3.2. Run with Docker Compose

Create a `docker-compose.yml` file in your project root with the following content:

```yaml
version: '3.8'

services:
  backend:
    image: humanoid-robotics-backend
    ports:
      - "8000:8000"
    environment:
      - QDRANT_URL=${QDRANT_URL}
      - QDRANT_API_KEY=${QDRANT_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_EMBEDDING_MODEL=${OPENAI_EMBEDDING_MODEL:-text-embedding-ada-002}
      - OPENAI_CHAT_MODEL=${OPENAI_CHAT_MODEL:-gpt-3.5-turbo}
      - QDRANT_COLLECTION_NAME=${QDRANT_COLLECTION_NAME:-book_chunks}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      # Optional: Mount logs directory if you want to persist logs outside the container
      - ./fastapi-backend/logs:/app/logs
    networks:
      - app-network

  frontend:
    image: humanoid-robotics-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

Create a `.env` file in the project root (where `docker-compose.yml` is) and add your API keys:

```dotenv
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
OPENAI_API_KEY=your_openai_api_key
# Optional:
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CHAT_MODEL=gpt-3.5-turbo
QDRANT_COLLECTION_NAME=book_chunks
LOG_LEVEL=INFO
```

Then, run Docker Compose:

```bash
docker compose up -d
```

Access the frontend in your browser at `http://localhost`. The backend will be accessible internally by the frontend via `http://backend:8000`.

## 4. Manual Deployment (Alternative to Docker)

### 4.1. FastAPI Backend

1.  Navigate to the `fastapi-backend` directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ensure environment variables (as listed in Section 1) are set in your deployment environment.
4.  Run the application:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    You might want to use a process manager like Gunicorn with Uvicorn workers for production:
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
    ```

### 4.2. Docusaurus Frontend

1.  Navigate to the `docusaurus-book` directory.
2.  Install dependencies:
    ```bash
    npm install # or yarn install
    ```
3.  Build the static site:
    ```bash
    npm run build # or yarn build
    ```
    This will create a `build` directory containing the static assets.
4.  Serve the `build` directory using a static file server (e.g., Nginx, Apache, or a cloud static hosting service like Netlify, Vercel, or AWS S3/CloudFront).

    **Example Nginx Configuration Snippet:**
    ```nginx
    server {
        listen 80;
        server_name your_domain.com; # Replace with your domain

        root /path/to/docusaurus-book/build; # Absolute path to your build directory
        index index.html index.htm;

        location / {
            try_files $uri $uri/ /index.html;
        }

        # Optional: Proxy /api requests to your FastAPI backend
        location /api/ {
            proxy_pass http://localhost:8000/api/; # Replace with your backend's address
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

## Post-Deployment

-   **Verify**: After deployment, access your frontend application in a web browser. Check the chatbot widget's functionality and ensure it can retrieve answers correctly.
-   **Monitoring**: Monitor your backend logs (`fastapi-backend/logs/app.log` if using Docker volume, or your configured logging destination) for any errors or performance issues.
-   **HTTPS**: For production, always ensure your deployment is served over HTTPS.
-   **Security**: Review and secure your API keys and environment variables.
