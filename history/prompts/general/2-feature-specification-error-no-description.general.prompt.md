---
id: 2
title: Feature Specification Error - No Description
stage: general
date: 2025-12-05
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 1-physical-ai-robotics
user: /sp.specify
command: /sp.specify
labels: ["specification", "error"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- /sp.specify
tests:
null
---

## Prompt

$ARGUMENTS

## Response snapshot

I cannot create a specification without a feature description. Please provide a description after `/sp.specify`. For example: `/sp.specify Add user authentication to the application`.

## Outcome

- ✅ Impact: Feature specification could not be generated due to missing description.
- 🧪 Tests: N/A
- 📁 Files: N/A
- 🔁 Next prompts: User needs to provide a feature description.
- 🧠 Reflection: The /sp.specify command requires a feature description as an argument. The absence of this argument resulted in an error, highlighting the need for clear input when using this command.

## Evaluation notes (flywheel)

- Failure modes observed: Missing required command argument.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
