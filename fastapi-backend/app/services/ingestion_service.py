import os
import re
from typing import List, Dict, Any

class IngestionService:
    def __init__(self, docs_path: str, chunk_size: int = 500, chunk_overlap: int = 50):
        self.docs_path = docs_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _read_markdown_file(self, file_path: str) -> str:
        """Reads the content of a markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def _extract_title_from_markdown(self, content: str, filename: str) -> str:
        """Extracts the title from markdown content, or uses the filename."""
        # Try to find a H1 title
        match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        
        # Fallback to filename if no H1 found
        return os.path.splitext(filename)[0].replace('-', ' ').title()

    def _chunk_text(self, text: str, document_metadata: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Splits text into manageable chunks based on Markdown headings.
        This version is more robust and handles frontmatter.
        """
        chunks = []
        # First, strip any YAML frontmatter
        text = re.sub(r'(?s)^---\n.*?\n---\n', '', text, count=1).strip()

        # Find all headings (e.g., #, ##, ###) and their start positions
        heading_matches = list(re.finditer(r'^(#{1,6}\s.*)$', text, re.MULTILINE))

        # If no headings, treat the whole document as one chunk
        if not heading_matches:
            if text:
                chunks.append({"content": text, "metadata": document_metadata})
            return chunks

        # Create a chunk for the content before the first heading
        first_heading_start = heading_matches[0].start()
        if first_heading_start > 0:
            content_before_first_heading = text[:first_heading_start].strip()
            if content_before_first_heading:
                chunks.append({"content": content_before_first_heading, "metadata": document_metadata})

        # Create a chunk for each section, including the heading
        for i, match in enumerate(heading_matches):
            section_start = match.start()
            # The section ends at the start of the next heading, or at the end of the text
            section_end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(text)
            
            content = text[section_start:section_end].strip()
            if content:
                chunks.append({
                    "content": content,
                    "metadata": document_metadata
                })
        
        return chunks

    def load_book_content(self) -> List[Dict[str, Any]]:
        """
        Loads all markdown files from the docs_path, extracts their content and title,
        and splits the content into chunks.
        """
        all_chunks = []
        for filename in os.listdir(self.docs_path):
            if filename.endswith('.md'):
                file_path = os.path.join(self.docs_path, filename)
                content = self._read_markdown_file(file_path)
                title = self._extract_title_from_markdown(content, filename)
                
                document_metadata = {
                    "filename": filename,
                    "title": title
                }
                
                # Split the document content into chunks
                chunks = self._chunk_text(content, document_metadata)
                all_chunks.extend(chunks)
        return all_chunks

if __name__ == '__main__':
    # Example usage (assuming this script is run from the project root or similar)
    # Adjust docs_path as necessary for testing
    docs_root = os.path.join(os.getcwd(), 'docusaurus-book', 'docs') 
    ingestion_service = IngestionService(docs_root, chunk_size=500, chunk_overlap=50)
    book_chunks = ingestion_service.load_book_content()

    print(f"Total chunks generated: {len(book_chunks)}")
    for i, item in enumerate(book_chunks[:5]): # Print first 5 chunks
        print(f"--- Chunk {i+1} from {item['metadata']['title']} ({item['metadata']['filename']}) ---")
        print(f"{item['content'][:200]}...\n") # Print first 200 chars
 
