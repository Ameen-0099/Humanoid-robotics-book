# Development Tasks: Integrated RAG Chatbot

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-10 | **Spec**: specs/002-rag-chatbot/spec.md
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md` and Implementation Plan from `/specs/002-rag-chatbot/plan.md`

## Summary of Tasks

This document outlines the detailed development tasks for the Integrated RAG Chatbot, organized by phases corresponding to user stories and foundational work. Each task is designed to be actionable and, where possible, independently testable.

## Dependencies and Completion Order

The tasks are ordered to ensure a logical flow of development, with foundational elements preceding user story implementations. User Story 1 (General Question Answering) is a prerequisite for User Story 2 (Selected Text Question Answering).

## Parallel Execution Examples

- **Backend Services**: While frontend UI components are being developed, backend services (Qdrant, OpenAI integration, FastAPI endpoints) can be developed in parallel.
- **Frontend UI vs. Backend Logic**: The basic chatbot widget UI can be built with mock data while backend RAG logic is under development.

---

## Phase 1: Setup (T001 - T003)

**Goal**: Establish necessary third-party accounts and obtain credentials.

- [ ] T001 Initialize Qdrant Cloud Free Tier account and obtain API keys for vector database access.
- [ ] T002 Setup Neon Serverless Postgres database for storing chat history, user context, and potentially book metadata.
- [ ] T003 Configure OpenAI API keys for embedding generation and ChatKit/Agents SDK usage.

---

## Phase 2: Foundational (T004 - T006)

**Goal**: Develop core data ingestion and embedding generation pipeline.
**Prerequisites**: Phase 1 completed.

- [x] T004 Develop a script/service to ingest the book's content (e.g., Markdown files from `docusaurus-book/docs`).
- [x] T005 Implement logic to split ingested content into manageable chunks suitable for embedding.
- [x] T006 Generate text embeddings for all book content chunks using OpenAI's embedding models and store them in Qdrant.

---

## Phase 3: User Story 1 - General Question Answering (T007 - T011) [US1]

**Goal**: Enable users to ask general questions about the book and receive relevant answers.
**Independent Test**: Ask a general question via the chatbot UI and verify a correct response.
**Prerequisites**: Phase 2 completed.

- [x] T007 [US1] Implement a FastAPI endpoint (`/api/chatbot/ask`) to receive user questions. `fastapi-backend/app/api/chatbot.py`
- [x] T008 [US1] Implement Qdrant search service (`fastapi-backend/app/services/qdrant_service.py`) to retrieve top-k most relevant document chunks based on the user's question embedding.
- [x] T009 [US1] Implement RAG logic (`fastapi-backend/app/services/openai_service.py`) using OpenAI ChatKit/Agents SDK to synthesize an answer from retrieved chunks and the user's question.
- [x] T010 [US1] Develop a basic React chatbot UI component (`docusaurus-book/src/components/ChatbotWidget.js`) to allow users to input questions and display responses.
- [x] T011 [US1] Integrate the ChatbotWidget into the Docusaurus theme/layout (`docusaurus-book/src/theme/Layout.js` or similar) to make it accessible across all book pages.

---

## Phase 4: User Story 2 - Selected Text Question Answering (T012 - T014) [US2]

**Goal**: Allow users to ask questions specifically about selected text within the book.
**Independent Test**: Select text, ask a question, and verify the answer is constrained to the selected text.
**Prerequisites**: Phase 3 completed.

- [x] T012 [US2] Modify the FastAPI endpoint (`/api/chatbot/ask`) to optionally accept `selected_text` as a parameter. `fastapi-backend/app/api/chatbot.py`
- [x] T013 [US2] Enhance the Qdrant search and RAG logic (`fastapi-backend/app/services/qdrant_service.py`, `fastapi-backend/app/services/openai_service.py`) to prioritize or filter retrieved chunks based on the provided `selected_text`.
- [x] T014 [US2] Implement frontend functionality (`docusaurus-book/src/components/ChatbotWidget.js`, `docusaurus-book/src/utils/selection_utils.js`) to detect user text selection and pass it along with the question to the backend.

---

## Phase 5: Polish & Cross-Cutting Concerns (T015 - T017)

**Goal**: Ensure robustness, usability, and deployability.

- [x] T015 Implement comprehensive error handling and logging (`fastapi-backend/app/main.py`, `fastapi-backend/app/services/logger.py`) for all chatbot interactions.
- [x] T016 Refine frontend chatbot UI styling (`docusaurus-book/src/css/custom.css`) and ensure responsiveness across different devices.
- [x] T017 Develop deployment scripts/instructions for both the FastAPI backend (e.g., Dockerfile, cloud deployment config) and the Docusaurus frontend.

---
