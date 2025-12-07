---
description: "Task list for Physical AI & Humanoid Robotics Textbook System implementation"
---

# Tasks: Physical AI & Humanoid Robotics Textbook System

**Input**: Design documents from `/specs/1-ai-textbook-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL for this feature, as not explicitly requested in the feature specification. However, integration tests are included in the Polish phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `fastapi-backend/app/` (backend), `docusaurus-book/` (frontend)
- Paths shown below assume this web app structure - adjust as needed.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create Docusaurus project structure in `docusaurus-book/`
- [X] T002 Initialize FastAPI project structure in `fastapi-backend/`
- [X] T003 [P] Configure Node.js dependencies for Docusaurus in `docusaurus-book/package.json`
- [X] T004 [P] Configure Python dependencies for FastAPI in `fastapi-backend/requirements.txt`
- [X] T005 [P] Configure NeonDB access and connection settings in `fastapi-backend/app/config.py`
- [X] T006 [P] Configure Qdrant Cloud access and connection settings in `fastapi-backend/app/config.py`
- [X] T007 [P] Install OpenAI ChatKit SDK in `fastapi-backend/requirements.txt`
- [ ] T008 [P] Configure linting and formatting tools for Docusaurus (`docusaurus-book/.eslintrc.js`, `docusaurus-book/.prettierrc.js`)
- [ ] T009 [P] Configure linting and formatting tools for FastAPI (`fastapi-backend/pyproject.toml` or `.flake8`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Setup Docusaurus routing, navigation, and display configuration in `docusaurus-book/docusaurus.config.js`
- [ ] T011 Implement constitution synchronization logic (triggering mechanism and update process) in `scripts/sync-constitution.py` (or similar)
- [ ] T012 Setup FastAPI base application in `fastapi-backend/app/main.py`
- [ ] T013 Configure global error handling and logging infrastructure for FastAPI in `fastapi-backend/app/main.py`
- [ ] T014 Create base database connection and session management for NeonDB in `fastapi-backend/app/database.py`
- [ ] T015 Initialize Qdrant client and collection setup in `fastapi-backend/app/qdrant_client.py`
- [ ] T016 Setup environment configuration management for both frontend and backend (`.env` files, `config.js`/`config.py`)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Read AI-Generated Textbook (Priority: P1) 🎯 MVP

**Goal**: Deploy a functional Docusaurus website displaying all AI-generated textbook chapters.

**Independent Test**: The deployed Docusaurus site is accessible, displays all chapters (e.g., 8), allows navigation, and includes placeholder content with code/diagram sections.

### Implementation for User Story 1

- [ ] T017 [US1] Define Spec-Kit Plus templates for generating individual chapters in `specs/templates/chapter-template.md`
- [ ] T018 [US1] Implement a script/agent to generate initial chapter markdown files based on the constitution's course content requirements and `chapter-template.md` in `scripts/generate_chapters.py`
- [ ] T019 [US1] Configure Docusaurus to include and display the generated chapters from `docusaurus-book/docs/`
- [ ] T020 [P] [US1] Create Docusaurus components for rendering code examples in `docusaurus-book/src/components/CodeBlock.js`
- [ ] T021 [P] [US1] Create Docusaurus components for rendering diagrams in `docusaurus-book/src/components/Diagram.js`
- [ ] T022 [US1] Populate initial glossary content in `docusaurus-book/docs/glossary.md`
- [ ] T023 [US1] Populate initial exercises and project tasks in `docusaurus-book/docs/exercises.md`
- [ ] T024 [US1] Add links to external resources within generated chapters and `docusaurus-book/docs/resources.md`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Interact with RAG Chatbot for Book Content (Priority: P1)

**Goal**: Integrate a RAG chatbot that can answer general and selected-text questions based on the textbook.

**Independent Test**: The chatbot can correctly answer questions based on the textbook content via API, and also provide answers specifically sourced from selected text.

### Implementation for User Story 2

- [ ] T025 [US2] Create API endpoint `/chat/general` in `fastapi-backend/app/api/chatbot.py` for general questions
- [ ] T026 [US2] Create API endpoint `/chat/selected-text` in `fastapi-backend/app/api/chatbot.py` for selected text questions
- [ ] T027 [P] [US2] Implement text chunking and embedding generation for textbook content using Qdrant in `fastapi-backend/app/services/embedding_service.py`
- [ ] T028 [P] [US2] Implement vector search logic in Qdrant based on user queries in `fastapi-backend/app/services/qdrant_service.py`
- [ ] T029 [US2] Implement RAG logic to combine search results with user query and send to OpenAI ChatKit in `fastapi-backend/app/services/rag_service.py`
- [ ] T030 [US2] Develop UI component for the chatbot interface in Docusaurus in `docusaurus-book/src/components/ChatbotWidget.js`
- [ ] T031 [US2] Integrate ChatbotWidget into Docusaurus pages to allow user interaction in `docusaurus-book/src/theme/Root.js` (or similar)
- [ ] T032 [US2] Add logging for chatbot interactions to NeonDB in `fastapi-backend/app/services/log_service.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Synchronize Constitution Updates (Priority: P1)

**Goal**: Ensure the automated synchronization of specs with constitution updates functions correctly.

**Independent Test**: Modifying `constitution.md` and triggering synchronization correctly updates dependent spec files or generates a report of necessary manual actions.

### Implementation for User Story 3

- [ ] T033 [US3] Refine and harden the constitution synchronization script in `scripts/sync-constitution.py` to cover all dependent spec types (plan, tasks, etc.)
- [ ] T034 [US3] Implement unit/integration tests for the constitution synchronization logic in `tests/scripts/test_sync_constitution.py`
- [ ] T035 [P] [US3] Configure CI/CD to automatically run synchronization script upon `constitution.md` changes in `.github/workflows/sync-constitution.yaml`

**Checkpoint**: All P1 user stories should now be independently functional

---

## Phase 6: User Story 4 - Personalize Chapter Content (Priority: P2 - Bonus Deliverable)

**Goal**: Enable logged-in users to personalize chapter content by skill level and translate to Urdu.

**Independent Test**: A logged-in user can successfully personalize a chapter or translate it to Urdu, with changes reflected instantly on the frontend.

### Implementation for User Story 4

- [ ] T036 [US4] Integrate `better-auth.com` SDK into FastAPI backend for user signup/signin in `fastapi-backend/app/api/auth.py`
- [ ] T037 [US4] Define User Profile schema in NeonDB (if not already done in data-model.md) and implement CRUD operations in `fastapi-backend/app/models/user.py` and `fastapi-backend/app/services/user_service.py`
- [ ] T038 [US4] Implement logic to ask background questions (hardware, software skills) during signup in `fastapi-backend/app/api/auth.py`
- [ ] T039 [US4] Create API endpoint `/personalize/skill-level` in `fastapi-backend/app/api/personalization.py`
- [ ] T040 [P] [US4] Develop personalization logic to dynamically modify chapter content based on user skill level in `fastapi-backend/app/services/personalization_service.py`
- [ ] T041 [US4] Create API endpoint `/translate/urdu` in `fastapi-backend/app/api/translation.py`
- [ ] T042 [P] [US4] Implement Urdu translation logic using a custom agent or LLM skill in `fastapi-backend/app/services/translation_service.py`
- [ ] T043 [US4] Develop UI components in Docusaurus for personalization controls (buttons, dropdowns) in `docusaurus-book/src/components/PersonalizationControls.js`
- [ ] T044 [US4] Integrate personalization and translation UI into Docusaurus chapter views in `docusaurus-book/src/theme/DocItem/Content/index.js` (or similar)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Automate deployment pipeline for Docusaurus to GitHub Pages/Vercel in `.github/workflows/deploy-docusaurus.yaml`
- [ ] T046 [P] Automate deployment pipeline for FastAPI backend to a cloud environment (e.g., Docker/Kubernetes) in `.github/workflows/deploy-fastapi.yaml`
- [ ] T047 Write and execute comprehensive integration tests for the RAG chatbot in `fastapi-backend/tests/integration/test_chatbot.py`
- [ ] T048 Write and execute comprehensive integration tests for the personalization and authentication features in `fastapi-backend/tests/integration/test_user_features.py`
- [ ] T049 Conduct end-to-end testing of the entire textbook system (manual and automated)
- [ ] T050 Update README.md with setup, build, and deployment instructions
- [ ] T051 Code cleanup and refactoring across both frontend and backend for maintainability
- [ ] T052 Performance optimization and load testing for critical API endpoints (`/chat/`, `/personalize/`)

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
-   **User Story 3 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories, but verifies constitution sync.
-   **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on authentication setup, integrates with textbook content.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T009)
- All Foundational tasks without direct sequential dependencies can be considered for parallel execution.
- Once Foundational phase completes, all P1 user stories (US1, US2, US3) can start in parallel (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel (e.g., T020, T021 for US1; T027, T028 for US2; T035 for US3; T040, T042 for US4)
- Different user stories can be worked on in parallel by different team members
- Polish tasks (T045, T046) can potentially run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all Docusaurus UI component tasks for User Story 1 together:
Task: "Create Docusaurus components for rendering code examples in docusaurus-book/src/components/CodeBlock.js"
Task: "Create Docusaurus components for rendering diagrams in docusaurus-book/src/components/Diagram.js"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently (verify deployed book with all generated chapters and basic navigation)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 (Bonus) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Textbook Generation)
   - Developer B: User Story 2 (RAG Chatbot)
   - Developer C: User Story 3 (Constitution Sync)
   - Developer D: User Story 4 (Personalization/Auth - Bonus)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if applicable)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
