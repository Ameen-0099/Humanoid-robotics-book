# Data Model: Physical AI & Humanoid Robotics Textbook System

**Date**: 2025-12-04
**Source**: Derived from `specs/1-ai-textbook-system/spec.md` - Key Entities section.

## Entities

### 1. Textbook Chapter

Represents a single chapter within the AI-generated textbook.

-   **ID**: Unique identifier (e.g., UUID or integer, primary key)
-   **Title**: String, the title of the chapter.
-   **Content**: Markdown/text, the full body of the chapter, including code examples and diagrams.
-   **Metadata**: JSON object, can include: author, publication_date, tags (list of strings), version.
-   **Associated Resources**: List of strings (e.g., file paths or URLs to diagrams, code snippets).

### 2. User Profile (Optional - for Bonus Deliverables)

Stores information about a registered user, used for personalization and authentication.

-   **User ID**: Unique identifier (e.g., UUID, primary key, linked to authentication system).
-   **Authentication Details**: Reference to external authentication system (e.g., `better-auth.com` user ID).
-   **Skill Level**: String/Enum (e.g., "Beginner", "Intermediate", "Advanced"), indicates user's proficiency.
-   **Hardware/Software Background**: JSON object/text, details on user's technical experience (e.g., `{"hardware": ["robotics kits"], "software": ["Python", "ROS"]}`).
-   **Preferences**: JSON object, user-specific settings (e.g., preferred language, learning style).

### 3. Chatbot Interaction

Logs details of user interactions with the RAG chatbot.

-   **Interaction ID**: Unique identifier (e.g., UUID, primary key).
-   **User ID**: Foreign key, links to `User Profile` (if authenticated).
-   **Query**: String, the user's question to the chatbot.
-   **Response**: String, the chatbot's generated answer.
-   **Context Type**: String (e.g., "general", "selected_text").
-   **Selected Text Context**: String, the specific text passage selected by the user (if applicable).
-   **Timestamp**: Datetime, when the interaction occurred.
-   **Source Chapters/Sections**: List of strings, references to the chapters/sections used by the RAG system to generate the response.

### 4. Vector Embedding

Represents a textual chunk from the textbook and its corresponding vector embedding, stored in Qdrant.

-   **Embedding ID**: Unique identifier (e.g., UUID, primary key from Qdrant).
-   **Text Chunk**: String, the segment of text that was embedded.
-   **Vector Representation**: Array of floats, the numerical vector representation of the text chunk.
-   **Source Reference**: String, a pointer back to the original `Textbook Chapter` and specific section/paragraph (e.g., `chapter_ID:section_ID:paragraph_ID`).
-   **Timestamp**: Datetime, when the embedding was created or last updated.
