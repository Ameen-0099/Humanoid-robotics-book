---
id: 3
title: Initial Plan for AI Textbook System
stage: plan
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-ai-textbook-system
branch: 1-ai-textbook-system
user: user
command: /sp.plan
labels: ["plan","feature-planning"]
links:
  spec: specs/1-ai-textbook-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-textbook-system/plan.md
  - specs/1-ai-textbook-system/research.md
  - specs/1-ai-textbook-system/data-model.md
  - specs/1-ai-textbook-system/contracts/api.yaml
  - specs/1-ai-textbook-system/quickstart.md
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
The implementation planning for the "Physical AI & Humanoid Robotics Textbook System" is complete. The plan (`specs/1-ai-textbook-system/plan.md`) has been created, along with supporting artifacts like research, data model, API contracts, and a quickstart guide. The plan aligns with the project constitution and feature specification.
```

## Outcome

- ✅ Impact: Created the implementation plan and associated design artifacts.
- 🧪 Tests: N/A
- 📁 Files: specs/1-ai-textbook-system/plan.md, specs/1-ai-textbook-system/research.md, specs/1-ai-textbook-system/data-model.md, specs/1-ai-textbook-system/contracts/api.yaml, specs/1-ai-textbook-system/quickstart.md
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: PowerShell script failures were gracefully handled by manual file creation, ensuring the planning workflow completed successfully.

## Evaluation notes (flywheel)

- Failure modes observed: `setup-plan.ps1` and `update-agent-context.ps1` scripts failed due to `pwsh` not found. Manual directory/file creation was performed as a fallback.
- Graders run and results (PASS/FAIL): Plan generated according to template and spec. Constitution checks passed.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement agent-native alternatives for PowerShell scripts or improve error handling/user guidance when external script execution fails.
