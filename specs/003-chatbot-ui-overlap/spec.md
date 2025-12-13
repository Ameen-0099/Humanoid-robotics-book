# Specification: Chatbot Widget UI Overlap Issue

## 1. Problem Description

The chatbot widget, despite having its `z-index` set to a high value (initially `1000`, then `9999`), is still reported by the user to be overlapping with or being overlapped by background text on certain pages. This behavior indicates a persistent stacking context issue, preventing the chatbot from consistently rendering on top of all other page elements as intended. This degrades the user experience by making the chatbot difficult to interact with or read.

## 2. Impact

-   **User Experience:** Users cannot reliably interact with the chatbot, leading to frustration and reduced utility of a core feature.
-   **Functionality:** The chatbot's primary purpose (interactive learning environment) is hindered if its interface is obscured.
-   **Perceived Quality:** The persistent UI bug reflects poorly on the overall quality and polish of the application.

## 3. Hypotheses for Overlap Cause

-   **Conflicting `z-index`:** Another element on the page (or its parent) has an even higher `z-index` or establishes a new, higher stacking context.
-   **Docusaurus-specific styling:** Docusaurus's internal CSS or JavaScript might dynamically manipulate `z-index` or create stacking contexts that interfere with the portal.
-   **`ReactDOM.createPortal` interaction:** While `createPortal` renders outside the React tree, its stacking context relative to other fixed/absolute elements can still be influenced by parent elements' CSS properties (e.g., `transform`, `filter`, `opacity`).
-   **CSS framework conflicts:** Potential interactions with Infima (Docusaurus's CSS framework) that create unexpected stacking behavior.

## 4. Expected Outcome

The chatbot widget must consistently render above all other page content. When the chatbot is open, no background text or UI elements should obscure any part of the chatbot window.

## 5. Proposed Solution (High-Level)

Investigate the DOM structure and computed styles, particularly `z-index` and stacking context properties, of both the chatbot widget and the overlapping background elements. Refine the CSS of the chatbot container, potentially exploring more aggressive or targeted `z-index` application, or identifying and mitigating conflicting styles from Docusaurus or other components.

## 6. Verification

-   Visually inspect the chatbot on various pages and screen sizes to confirm it never overlaps with other content.
-   Use browser developer tools to inspect the computed `z-index` and stacking context of the chatbot and any overlapping elements.

## 7. Difficulty Level

Medium - Requires careful debugging of CSS stacking contexts, potentially across different Docusaurus components.

## 8. Tags

`chatbot`, `ui`, `css`, `z-index`, `docusaurus`, `bug`, `frontend`
