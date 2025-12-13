<!--
Sync Impact Report:
Version change: 0.0.0 (initial) -> 1.0.0
Modified principles:
- [PRINCIPLE_1_NAME] -> Authoritative Source Mandate
- [PRINCIPLE_2_NAME] -> Spec-Driven Development (SDD)
- [PRINCIPLE_3_NAME] -> Reproducibility and Deployability
- [PRINCIPLE_4_NAME] -> Architectural Consistency
- [PRINCIPLE_5_NAME] -> Automated Spec Synchronization
Added sections: Project Deliverables and Requirements, Output and Technical Requirements
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: ⚠ pending
- README.md: ⚠ pending
- docs/quickstart.md: ⚠ pending
Follow-up TODOs: TODO(RATIFICATION_DATE): Clarify original adoption date.
-->
# Physical AI & Humanoid Robotics Textbook (Hackathon I) Constitution

## Core Principles

### Authoritative Source Mandate
This Constitution (specifically `.specify/memory/constitution.md`) defines the single source of truth for the entire project. All generated specifications, code, and documentation must explicitly comply with the principles and requirements defined herein. In case of any conflict, this Constitution takes absolute precedence.

### Spec-Driven Development (SDD)
All development, including chapters, features, and modules, must be driven by specifications generated using Spec-Kit Plus. The process mandates generating specs first, ensuring alignment with this Constitution, and then implementing based on approved specs.

### Reproducibility and Deployability
All components of the project, especially the AI/Spec-Driven Textbook and the Integrated RAG Chatbot, must be designed for reproducible builds and seamless deployment. The textbook must build with Node.js and Docusaurus, and be deployable to GitHub Pages or Vercel. The RAG system must use FastAPI, Qdrant for embeddings, NeonDB for user data/logs, and OpenAI ChatKit SDK.

### Architectural Consistency
Key architectural decisions, particularly regarding database choices (NeonDB for structured data, Qdrant Cloud for vector embeddings), API design (FastAPI backend), and AI model integration (OpenAI Agents/ChatKit SDK), must adhere to defined standards and be consistently applied across the project. Personalization must fetch user profiles from Neon and dynamically modify content.

### Automated Spec Synchronization
All updates to this Constitution must automatically trigger a rebuild and synchronization of dependent specifications and artifacts to ensure continuous alignment and prevent drift.

### Interactive Learning Environment
The project must provide an interactive learning environment by integrating a Retrieval-Augmented Generation (RAG) chatbot. This chatbot will assist users in understanding the book's content by answering questions and providing explanations.

## Project Deliverables and Requirements

### Core Deliverables:
1.  **AI/Spec-Driven Textbook:** Use Spec-Kit Plus to generate all chapters, Docusaurus to build the book, and deploy to GitHub Pages or Vercel.
2.  **Integrated RAG Chatbot:** Build and embed a Retrieval-Augmented Generation (RAG) chatbot within the published book. This chatbot, utilizing the OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres database, and Qdrant Cloud Free Tier, must be able to answer user questions about the book's content, including answering questions based only on text selected by the user.
3.  **Spec Synchronization:** All updates to the project must synchronize `.specify/memory/constitution.md` automatically.

### Bonus Deliverables (Optional):
-   **Reusable Intelligence:** Claude Code Subagents, Agent Skills, Automated workflows.
-   **Auth System:** Signup + Signin using better-auth.com, ask background questions (hardware, software skills), save user profile in NeonDB.
-   **Personalization System:** Logged-in user can press a button on any chapter to personalize content to their skill level and translate to Urdu instantly.

### Course Content Requirements (Textbook Chapters):
1.  Physical AI & Embodied Intelligence
2.  ROS 2 — The Robotic Nervous System
3.  Gazebo & Unity Physics Simulation
4.  NVIDIA Isaac™ AI Robotics Platform
5.  Vision-Language-Action Robotics
6.  Humanoid Kinematics, Locomotion & Manipulation
7.  Conversational Humanoid Robotics (GPT Integration)
8.  Capstone Project: Autonomous Humanoid Robot

### Required Features:
Docusaurus sidebar organization, working navigation, code examples and diagrams, glossary, exercises and project tasks, links to external resources.

## Output and Technical Requirements

### Output Requirements:
Must produce: GitHub Repo (Public), Live deployed website, 90-second demo video. Follow hackathon templates and ensure reproducible builds.

### Technical Stack:
The book must build with Node.js and Docusaurus. The RAG System requires a FastAPI backend, Qdrant for embeddings, NeonDB for user data + logs, and OpenAI ChatKit SDK for model inference. Personalization requires fetching user profiles from Neon and dynamically modifying chapter content. Urdu Translation will use a custom agent or built-in LLM translation skill.

## Governance
This Constitution supersedes all other project documentation and practices. Amendments to this Constitution must be formally documented, approved, and require a clear migration plan for any affected specifications or codebases. All Pull Requests and code reviews must explicitly verify compliance with the principles and requirements outlined in this Constitution. Any increase in system complexity must be thoroughly justified and aligned with project principles.

**Version**: 1.0.2 | **Ratified**: TODO(RATIFICATION_DATE): Please clarify the original adoption date if known. | **Last Amended**: 2025-12-10

---

## Chapter Generation Rules

### Each `/sp.specify` must include:
- Chapter title  
- Purpose  
- Learning outcomes  
- Required diagrams  
- Code examples needed  
- Cross-links to other chapters  
- Difficulty level  
- Tags (ros2, robotics, ai, physics, etc.)

### Each `/sp.write` output must:
- Follow the specification EXACTLY  
- Include all required content blocks  
- Use consistent terminology  
- Ensure pedagogical flow  

---

## Collaboration Rules (Claude Code + Subagents)
- Claude Code is the lead orchestrator agent.
- Subagents may be created for:
  - ROS 2 expertise
  - Isaac Sim expertise
  - Robotics math expertise
  - Writing/editorial tasks
- All subagents must follow this constitution.

---

## Version Control Rules
- All generated files must be added to Git
- Commit message style enforced:
  - `feat: add ROS 2 basics chapter`
  - `fix: corrected URDF example`
  - `docs: updated intro`

---

## Completion Criteria
The book is considered complete when:

- All chapters in the plan are written  
- All specifications have been fulfilled  
- Docusaurus build passes without error  
- GitHub Pages deployment is live  
- The book is readable from start to finish  
- Includes quizzes, exercises, and diagrams  
- Glossary + references included  

---

## End of Constitution
