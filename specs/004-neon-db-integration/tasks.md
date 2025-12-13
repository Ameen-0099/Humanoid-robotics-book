# Tasks: Neon DB Integration

This checklist breaks down the work required to implement Neon DB integration, based on the `plan.md`.

### Phase 1: Database Setup and Configuration
- [x] Add `asyncpg` to `fastapi-backend/requirements.txt`.
- [x] Store Neon connection URL in `fastapi-backend/.env` as `NEON_DATABASE_URL`.
- [x] Update `app/config.py` to load the `NEON_DATABASE_URL` environment variable.
- [x] Update `app/database.py` to create and configure the async engine and session maker.
- [x] Create a `get_db_session` dependency in `app/database.py`.

### Phase 2: Data Modeling
- [x] Create the file `fastapi-backend/app/models/chat.py`.
- [x] Define the `ChatSession` SQLAlchemy model in `chat.py`.
- [x] Define the `ChatMessage` SQLAlchemy model in `chat.py`.
- [x] Create a script or function to initialize the tables in the database.

### Phase 3: Logic Integration
- [x] Modify `ChatRequest` Pydantic model in `app/api/chatbot.py` to include an optional `session_uuid`.
- [x] Modify `ChatResponse` Pydantic model in `app/api/chatbot.py` to include the `session_uuid`.
- [x] Update the `ask_chatbot` endpoint in `app/api/chatbot.py` to depend on `get_db_session`.
- [x] Implement logic in `ask_chatbot` to find an existing session or create a new one.
- [x] Implement logic in `ask_chatbot` to save the user message to the database.
- [x] Implement logic in `ask_chatbot` to save the bot response to the database.

### Phase 4: History Retrieval API
- [x] Create the file `fastapi-backend/app/api/history.py`.
- [x] Define a `GET /api/sessions/{session_uuid}/messages` endpoint in `history.py`.
- [x] Implement the database query in the new endpoint to fetch messages for a session.
- [x] Add the `history.router` to `fastapi-backend/app/main.py`.

### Phase 5: Validation
- [ ] Manually test the `/api/chatbot` endpoint to confirm messages and sessions are created.
- [ ] Manually test the `/api/sessions/{session_uuid}/messages` endpoint to confirm history is retrieved correctly.
