# Project Plan: Physical AI & Humanoid Robotics Textbook

This document outlines the implementation plan for creating the Docusaurus-based textbook.

## Phase 1: Project Setup and Docusaurus Initialization

*   **Purpose**: To create the basic structure of the Docusaurus-based textbook.
*   **Tasks**:
    *   Initialize a new Docusaurus project in the `docusaurus-book` directory.
    *   Configure `docusaurus.config.js` with the placeholder title and project details from `specs/constitution.yml`.
    *   Create the initial chapter files as empty markdown files based on the `chapter-list` in `specs/constitution.yml`.
    *   Configure the sidebar in `sidebars.js` to reflect the chapter structure.
*   **Deliverables**: A functional Docusaurus site with a basic layout and empty chapter pages.
*   **Tools**: Docusaurus, Node.js.
*   **Dependencies**: A valid `specs/constitution.yml` file.
*   **Timeline**: 1 day.

## Phase 2: Core Content Generation (Chapters 1-4)

*   **Purpose**: To generate the content for the first four chapters of the textbook, establishing the writing workflow.
*   **Workflow**:
    1.  **Specify**: For each chapter, use the `/sp.specify` command to create a detailed chapter specification. The specification must follow the `chapter-structure` defined in the constitution.
    2.  **Write**: Use the `/sp.write` command to generate the chapter content based on the approved specification.
    3.  **Review**: Manually review and edit the generated content for technical accuracy, clarity, and pedagogical flow.
    4.  **Enrich**: Add required diagrams (using Mermaid.js or static images) and code examples.
*   **Tasks**:
    *   Generate, review, and enrich content for:
        *   Chapter 1: Foundations of Physical AI & Embodied Intelligence
        *   Chapter 2: The Robotic Nervous System: An Introduction to ROS 2
        *   Chapter 3: Simulating Reality: Gazebo and Unity for Robotics
        *   Chapter 4: The Modern AI Stack: NVIDIA Isaac and Jetson
*   **Deliverables**: Completed and reviewed Markdown files for chapters 1-4, including diagrams and code.
*   **Tools**: Spec-Kit Plus (`/sp.specify`, `/sp.write`), Claude Code, Docusaurus.
*   **Dependencies**: Phase 1 completion.
*   **Timeline**: 3 days.

## Phase 3: Intermediate Content Generation (Chapters 5-8)

*   **Purpose**: To continue content creation for the next set of chapters.
*   **Tasks**:
    *   Follow the established workflow to generate, review, and enrich content for:
        *   Chapter 5: Perception: Vision-Language-Action Models
        *   Chapter 6: Movement: Humanoid Kinematics and Locomotion
        *   Chapter 7: Manipulation: Grasping and Interaction
        *   Chapter 8: Intelligence: Conversational AI and Task Planning
*   **Deliverables**: Completed and reviewed Markdown files for chapters 5-8.
*   **Tools**: Spec-Kit Plus, Claude Code, Docusaurus.
*   **Dependencies**: Phase 2 completion.
*   **Timeline**: 3 days.

## Phase 4: Advanced Content Generation (Chapters 9-12)

*   **Purpose**: To complete the remaining chapters of the book.
*   **Tasks**:
    *   Follow the established workflow to generate, review, and enrich content for:
        *   Chapter 9: Introduction to Robot Learning
        *   Chapter 10: Ethics and Safety in Humanoid Robotics
        *   Chapter 11: Advanced Locomotion: Bipedal Walking and Dynamic Control
        *   Chapter 12: Capstone Project: Building an Autonomous Humanoid
*   **Deliverables**: Completed and reviewed Markdown files for chapters 9-12.
*   **Tools**: Spec-Kit Plus, Claude Code, Docusaurus.
*   **Dependencies**: Phase 3 completion.
*   **Timeline**: 3 days.

## Phase 5: Finalization, Review, and Deployment

*   **Purpose**: To finalize the textbook content and deploy the live website.
*   **Tasks**:
    *   **Comprehensive Review**: Perform a full-book review for consistency, grammar, and style.
    *   **Add Ancillaries**: Create and populate the Glossary and References sections.
    *   **Add Assessments**: Add quizzes and exercises to each chapter.
    *   **Final Build**: Build the Docusaurus site and resolve any errors.
    *   **Deployment**: Deploy the final site to GitHub Pages.
*   **Deliverables**:
    *   A live, publicly accessible textbook website.
    *   A completed glossary and reference list.
*   **Tools**: Docusaurus, GitHub Pages.
*   **Dependencies**: Phase 4 completion.
*   **Timeline**: 2 days.

## Hackathon Workflow: Specification Updates

- All changes to the project scope, chapter list, or technical requirements must first be reflected in `specs/constitution.yml` and `.specify/memory/constitution.md`. This is the single source of truth.
- After updating the constitution, the lead agent (Claude Code) will assess the impact on existing chapter specifications.
- If a chapter spec is affected, it will be updated using the `/sp.clarify` and `/sp.specify` commands to ensure it aligns with the new requirements before any content is re-generated. This ensures the plan and execution remain synchronized.