# 004: Neon DB Integration for Chat History

## 1. Introduction

This document specifies the requirements for integrating a Neon Serverless Postgres database into the Humanoid Robotics Book application. The primary purpose of this integration is to provide persistent storage for chatbot conversations, moving beyond the current browser-based `localStorage` solution.

## 2. Problem Statement

Currently, chat history is stored in the user's browser `localStorage`. This has several limitations:
- History is not persistent across different browsers or devices.
- Clearing browser data results in complete loss of history.
- It is not possible to perform server-side analysis or debugging on chat conversations.
- There is no mechanism to associate conversations with a user session for future features like personalization.

## 3. Goals

- **Persist Chat History**: Store all user and bot messages in a structured, persistent database.
- **Session Management**: Associate messages with a distinct session to group conversations logically.
- **Data Accessibility**: Create a mechanism for the backend to access and retrieve chat history.
- **Scalability**: The solution should be serverless and scale efficiently, aligning with the project's existing architecture.

## 4. Non-Goals

- This feature will not handle user authentication initially. Sessions will be anonymous unless a future authentication feature is integrated.
- This feature will not replace Qdrant. Qdrant will remain the source for RAG retrieval; Neon will only be used for storing the structured chat history and metadata.
- Frontend implementation for displaying history from the new endpoints is out of scope for this initial backend specification.

## 5. Functional Requirements

1.  **Database Schema**: Define a database schema with at least two tables:
    -   `chat_sessions`: To store session-level information (e.g., session ID, creation timestamp).
    -   `chat_messages`: To store individual messages (e.g., message ID, session ID, sender type, text content, timestamp).
2.  **Message Persistence**: Upon a user asking a question via the chatbot API, the user's message and the subsequent bot response must be saved as entries in the `chat_messages` table.
3.  **Session Handling**: A new session should be created for a new conversation, or an existing session should be identified and used for ongoing conversations. A session ID should be managed between the client and server.
4.  **API for History Retrieval**:
    -   An endpoint must be created to retrieve a list of messages for a given session ID.

## 6. Technical Requirements

- **Database**: Neon Serverless Postgres.
- **Backend Framework**: FastAPI.
- **Database Driver**: An asynchronous Python driver for Postgres (e.g., `asyncpg`).
- **ORM**: SQLAlchemy will be used for data modeling and interaction.
- **Configuration**: The database connection string must be managed securely via environment variables and not hardcoded.
