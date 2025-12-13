# Implementation Plan: Integrated RAG Chatbot

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-10 | **Spec**: specs/002-rag-chatbot/spec.md
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md`

## Summary

This plan outlines the development and integration of a Retrieval-Augmented Generation (RAG) chatbot within the published book. The chatbot will leverage OpenAI Agents/ChatKit SDKs, FastAPI for the backend, Neon Serverless Postgres for data storage, and Qdrant Cloud Free Tier for vector embeddings. Its primary function is to answer user questions about the book's content, including providing contextual answers based on user-selected text.

## Technical Context

**Language/Version**: Python 3.9+ (for FastAPI backend), Node.js (for Docusaurus frontend)  
**Primary Dependencies**: FastAPI, Uvicorn, OpenAI Python client, Langchain (or similar for RAG orchestration), Neon Serverless Postgres client, Qdrant Client, Docusaurus, React  
**Storage**: Neon Serverless Postgres (user interaction logs, potentially user profiles), Qdrant Cloud (vector embeddings of book content)  
**Testing**: `pytest` (for FastAPI backend), `Jest/React Testing Library` (for Docusaurus frontend components), integration tests for end-to-end chatbot flow.  
**Target Platform**: Web (Docusaurus deployed to GitHub Pages/Vercel, FastAPI backend deployed to a cloud platform like Render/Fly.io)  
**Project Type**: Web application (Frontend + Backend)  
**Performance Goals**: Chatbot response time under 3 seconds for 90% of queries.  
**Constraints**: Qdrant Cloud Free Tier limitations (e.g., storage, QPS), OpenAI API rate limits and cost considerations, client-side embedding size for selected text.  
**Scale/Scope**: Answer questions across the entire book content; support for single-turn questions and contextual questions based on user-highlighted text. Initial deployment for a single user base, potential for future expansion.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The plan aligns with the "Interactive Learning Environment" principle by integrating the RAG chatbot. It also adheres to the "Reproducibility and Deployability" and "Architectural Consistency" principles by specifying the use of FastAPI, Qdrant, NeonDB, and OpenAI ChatKit SDKs. No violations identified.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/ (fastapi-backend)
├── app/
│   ├── api/
│   │   ├── chatbot.py           # New API routes for chatbot interaction
│   │   └── ...
│   ├── services/
│   │   ├── qdrant_service.py    # New service for Qdrant interactions
│   │   ├── openai_service.py    # New service for OpenAI API calls
│   │   ├── neon_db_service.py   # Existing service, potentially updated for logging
│   │   └── ...
│   ├── models/                  # Existing, potentially new models for chat history/user context
│   └── ...
└── tests/
    ├── integration/
    │   ├── test_chatbot.py      # New integration tests
    │   └── ...
    └── unit/

frontend/ (docusaurus-book)
├── src/
│   ├── components/
│   │   ├── ChatbotWidget.js     # New React component for the chatbot UI
│   │   └── ...
│   ├── utils/
│   │   ├── chatbot_api.js       # New utility for frontend-backend communication
│   │   └── ...
│   ├── theme/                   # Potentially custom theme modifications for chatbot
│   └── ...
└── ...
```

**Structure Decision**: The "Web application (frontend + backend)" structure is chosen, adapting to the existing `fastapi-backend` and `docusaurus-book` directories. New components and services will be integrated into these existing structures.

## Complexity Tracking

No new complexity violations identified beyond existing project structure.
