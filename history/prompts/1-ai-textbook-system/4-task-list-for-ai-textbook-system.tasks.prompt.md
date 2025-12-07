---
id: 4
title: Task List for AI Textbook System
stage: tasks
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-textbook-system
branch: 1-ai-textbook-system
user: user
command: /sp.tasks
labels: ["tasks","feature-implementation"]
links:
  spec: specs/1-ai-textbook-system/spec.md
  plan: specs/1-ai-textbook-system/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook-system/tasks.md
tests:
  - N/A
---

## Prompt

```text
---
description: High–level execution plan for generating a complete book using Spec-Kit Plus workflows
---

# Project Purpose

This project automatically generates a fully structured, high-quality book based on a user-provided book title.
It uses Spec-Kit Plus, Claude Code Router, and the project constitution to ensure consistent structure, coherent content, and reproducible generation.

The plan defines:
- required inputs
- generation stages
- validation steps
- file output structure
- dependencies between tasks
- update rules for all spec files

This plan MUST guide the orchestrator in updating specs, running generators, and producing the final book.

---

# Required User Input

The system expects ONLY one piece of user input:

1. **Book Title**
   - Provided at hackathon time
   - This title becomes the root variable `$BOOK_TITLE`
   - All outline, chapters, sections, and metadata depend on it

No other user input is re:
  - `/generated/book/title.md`
  - `/generated/book/preface.md`
  - `/generated/book/introduction.md`
  - `/generated/book/chapters/chapter_X.md`
  - `/generated/book/conclusion.md`

All writing MUST follow:
- Constitution
- Outline
- Chapter specs
- Global constraints defined in `sp.specify`

## 5. Consistency Enforcement Stage
The system MUST enforce:

### Content Coherence
- No contradictory information
- Chapters must flow logically
- Recap and transition paragraphs included

### Style Consistency
- Same tone across all chapters
- Clear explanations
- No hallucinations
- No self-references

### Formatting Rules
- Headings use Markdown
- Lists where useful
- No extra empty lines

---

# Output Rules

## 1. Final Output Format
The final generated boequired.

---

# High-Level Workflow

## 1. Intake Stage — Accept Book Title
- The user provides the book title as plain text.
- Save it into `$ARGUMENTS` inside `.specify/memory/arguments.md`.
- Trigger a regeneration of all dependent templates.

## 2. Outline Generation Stage
- Use the title to generate a complete outline in:
  - `/specs/outline.md`
- Outline MUST include:
  - Preface
  - Introduction
  - 8–15 chapters
  - Each chapter contains 3–8 sections
  - Conclusion
  - Appendices (if needed)
- Ensure the outline is logical, progressive, and comprehensive.

## 3. Chapter Specification Stage
- For each chapter in the outline:
  - Create or update `/specs/chapters/chapter_X.md`
- Each chapter spec must include:
  - Chapter purpose
  - Learning objectives
  - Section breakdown
  - Key insights
  - Required tone (simple, educational, structured)
  - Writing constraints (no repetition, no filler)

## 4. Book Content Generation Stage
- Generate a COMPLETE book inside `/generated/book/`.
- Files includok must exist as:

- `/generated/book/book.md` (merged)
- Structured folder of chapters
- All sections properly ordered

## 2. Auto-Regeneration Triggers
Whenever the book title changes:
- outline regenerates
- chapter specs update
- entire book content regenerates

## 3. Validations
Before delivering the final book, the system must validate:

- Title exists
- Outline matches chapter files
- No empty sections
- No TODO placeholders
- No duplicated content
- Constitution constraints are obeyed

---

# Constraints & Policies

### Writing Constraints
- No copyright-protected content
- No long paragraphs; break into small chunks
- Educational tone
- Practical examples preferred
- No repetition

### System Constraints
- All generated content must be deterministic
- All files must be synced with the project constitution
- No deviation from outline unless constitution updates

---

# Completion Condition

The process is complete when:

1. The book title is stored
2. The outline is generated
3. Chapter specs are generated
4. The full book is generated
5. All validations pass

The orchestrator may then deliver the final book.

---
```

## Response snapshot

```text
The tasks.md file has been successfully generated for the "Physical AI & Humanoid Robotics Textbook System" feature.

**Tasks File:** specs/1-ai-textbook-system/tasks.md

**Summary of Tasks:**

*   **Total Tasks**: 52
*   **Tasks per User Story**:
    *   User Story 1 (Read AI-Generated Textbook): 8 tasks (T017-T024)
    *   User Story 2 (Interact with RAG Chatbot for Book Content): 8 tasks (T025-T032)
    *   User Story 3 (Synchronize Constitution Updates): 3 tasks (T033-T035)
    *   User Story 4 (Personalize Chapter Content - Bonus): 9 tasks (T036-T044)
*   **Parallel Opportunities**: Many tasks are marked with `[P]`, indicating they can be executed in parallel. For instance, in Phase 1 (Setup), tasks T003-T009 are parallelizable. Within user stories, tasks like creating UI components or implementing services can often be done concurrently.
*   **Independent Test Criteria**: Each user story phase includes an "Independent Test" description, allowing for verification of functionality in isolation.
*   **Suggested MVP Scope**: User Story 1 (Read AI-Generated Textbook) is designated as the MVP, with a clear checkpoint after its completion for validation and potential early deployment.

The tasks are organized into phases: Setup, Foundational, and then by User Story priority (P1, P2), followed by a Polish & Cross-Cutting Concerns phase. Each task is in the format `- [ ] [TaskID] [P?] [Story?] Description with file path`.

This task list is now ready for implementation.
```

## Outcome

- ✅ Impact: Generated a detailed, executable task list for the AI Textbook System feature.
- 🧪 Tests: N/A
- 📁 Files: specs/1-ai-textbook-system/tasks.md
- 🔁 Next prompts: /sp.implement, /sp.analyze
- 🧠 Reflection: Successfully created a comprehensive task list, organized by user stories and phases, following the specified format and rules.

## Evaluation notes (flywheel)

- Failure modes observed: `check-prerequisites.ps1` script failed due to `pwsh` not found. Manual parsing of paths was performed.
- Graders run and results (PASS/FAIL): Tasks generated according to template and plan, adhering to specified format rules and priorities.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Incorporate agent-native alternatives for PowerShell scripts to improve cross-platform robustness.
