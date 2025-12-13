# Plan: Neon DB Integration

This document outlines the implementation plan for integrating a Neon Serverless Postgres database for chat history persistence, as defined in `spec.md`.

## 1. Strategy

The integration will be executed in a phased, backend-first approach. We will first establish the database foundation, then modify the existing chatbot logic to persist data, and finally create new endpoints for data retrieval. This plan focuses solely on the backend implementation.

## 2. Implementation Steps

### Phase 1: Database Setup and Configuration

1.  **Install Dependencies**: Add `asyncpg` to `fastapi-backend/requirements.txt` for asynchronous database communication. SQLAlchemy is already listed.

2.  **Secure Configuration**: The Neon database connection URL will be stored in the `.env` file within the `fastapi-backend` directory under the key `NEON_DATABASE_URL`. This ensures credentials are not hardcoded. The `app/config.py` file will be updated to load this variable.

3.  **Database Connection Logic**:
    -   Modify `fastapi-backend/app/database.py` to:
    -   Create an asynchronous `SQLAlchemy` engine using `create_async_engine`.
    -   Create an `async_sessionmaker` for creating new database sessions.
    -   Define a dependency `get_db_session` to provide a database session to API endpoints.

### Phase 2: Data Modeling

1.  **Create Model File**: A new file, `fastapi-backend/app/models/chat.py`, will be created to house the SQLAlchemy ORM models.

2.  **Define Models**:
    -   **`ChatSession` Model**: This will map to the `chat_sessions` table and include columns like `id` (PK), `session_uuid` (unique identifier for client-side), and `created_at`.
    -   **`ChatMessage` Model**: This will map to the `chat_messages` table and include columns like `id` (PK), `session_id` (FK to `chat_sessions`), `sender`, `message`, and `timestamp`.

### Phase 3: Logic Integration

1.  **Update Chatbot Endpoint**:
    -   Modify the `ask_chatbot` function in `fastapi-backend/app/api/chatbot.py`.
    -   The endpoint will now accept an optional `session_uuid` from the client.
    -   If `session_uuid` is not provided, a new session is created in the `chat_sessions` table, and the new UUID is returned to the client.
    -   The user's message and the bot's response will be saved to the `chat_messages` table, linked to the appropriate session.

2.  **Update Data Models**:
    -   The Pydantic models `ChatRequest` and `ChatResponse` will be updated to include the `session_uuid`.

### Phase 4: History Retrieval API

1.  **Create New Endpoint**:
    -   A new endpoint, `GET /api/sessions/{session_uuid}/messages`, will be created in a new router file (`fastapi-backend/app/api/history.py`).
    -   This endpoint will take a `session_uuid` as a path parameter.
    -   It will query the database and return a list of all messages associated with that session, ordered by timestamp.

2.  **Integrate Router**: The new history router will be included in the main FastAPI application in `fastapi-backend/app/main.py`.

## 3. Validation

- After each phase, unit or integration tests will be considered (though not explicitly implemented in this plan).
- The primary validation will be manual API testing using tools like `curl` or FastAPI's own Swagger UI to confirm that:
    -   Messages are correctly saved to the database.
    -   Sessions are created and managed.
    -   The history retrieval endpoint returns the correct data.
