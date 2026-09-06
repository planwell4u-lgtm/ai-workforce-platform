"""Document Knowledge Extractor — PDF, CSV, and plain-text ingestion.

Uses only Python stdlib + pypdf (lightweight, ~2 MB, pure-Python).
No LangChain or heavy ML frameworks required.
"""

from __future__ import annotations

import csv
import io
import re
from typing import Any


# ---------------------------------------------------------------------------
# Public extractor class
# ---------------------------------------------------------------------------

class DocumentKnowledgeExtractor:
    """Converts uploaded document bytes into draft knowledge articles.

    Supported formats
    -----------------
    PDF  — ``pypdf`` text extraction, chunked by headings / paragraphs
    CSV  — each row becomes one article (configurable column mapping)
    TXT  — plain text split by blank lines into paragraph chunks
    MD   — markdown, stripped of fences/headers, same paragraph split as TXT

    All output articles carry ``published=False`` so they land in the owner's
    Draft Queue and require explicit governance approval before going live.
    """

    # Maximum characters per article chunk (prevents database bloat)
    CHUNK_SIZE = 1800
    # Minimum characters to bother saving a chunk
    MIN_CHUNK = 60

    # -----------------------------------------------------------------------
    # Entry point
    # -----------------------------------------------------------------------

    def extract(self, filename: str, file_bytes: bytes) -> list[dict[str, Any]]:
        """Dispatch to the right extractor based on the file extension.

        Parameters
        ----------
        filename:   Original filename (used only for extension detection).
        file_bytes: Raw file content as bytes.

        Returns
        -------
        List of draft article dicts compatible with ``upsert_knowledge_article``.
        """
        name_lower = filename.lower().strip()
        if name_lower.endswith(".pdf"):
            return self._extract_pdf(file_bytes, filename)
        if name_lower.endswith(".csv"):
            return self._extract_csv(file_bytes, filename)
        if name_lower.endswith((".txt", ".md", ".markdown")):
            return self._extract_text(file_bytes, filename, is_markdown=name_lower.endswith((".md", ".markdown")))
        raise ValueError(
            f"Unsupported file type '{filename}'. Accepted formats: PDF, CSV, TXT, MD."
        )

    # -----------------------------------------------------------------------
    # PDF
    # -----------------------------------------------------------------------

    def _extract_pdf(self, file_bytes: bytes, filename: str) -> list[dict[str, Any]]:
        """Extract text from a PDF using pypdf, then chunk into FAQ articles."""
        try:
            import pypdf  # type: ignore[import-untyped]
        except ImportError as exc:
            raise RuntimeError(
                "pypdf is not installed. Add 'pypdf>=4.0,<5' to requirements.txt."
            ) from exc

        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        all_text_parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                all_text_parts.append(page_text)

        full_text = "\n\n".join(all_text_parts)
        if not full_text.strip():
            raise ValueError(f"Could not extract any text from '{filename}'. The PDF may be image-only (scanned).")

        chunks = self._split_into_chunks(full_text)
        stem = self._stem(filename)
        return [
            self._make_article(
                topic=stem,
                question=f"What does the document '{stem}' cover in section {i + 1}?",
                answer=chunk,
                category="document",
            )
            for i, chunk in enumerate(chunks)
        ]

    # -----------------------------------------------------------------------
    # CSV
    # -----------------------------------------------------------------------

    def _extract_csv(self, file_bytes: bytes, filename: str) -> list[dict[str, Any]]:
        """Convert CSV rows into knowledge articles.

        Column mapping strategy (in priority order):
        1. Headers named ``question``/``q`` and ``answer``/``a`` → direct use.
        2. Headers named ``title``/``name`` and ``description``/``content`` → mapped.
        3. Fallback: col[0] = question, col[1] = answer.
        """
        text = file_bytes.decode("utf-8-sig", errors="replace")  # handles BOM
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        if not rows:
            raise ValueError(f"CSV file '{filename}' appears to be empty.")

        header = [h.strip().lower() for h in rows[0]]
        data_rows = rows[1:] if len(rows) > 1 else []

        q_col, a_col = self._detect_csv_columns(header)
        topic_col = next(
            (i for i, h in enumerate(header) if h in {"topic", "category", "section"}), None
        )

        stem = self._stem(filename)
        articles: list[dict[str, Any]] = []
        for row in data_rows:
            if len(row) <= max(q_col, a_col):
                continue
            question = row[q_col].strip()
            answer = row[a_col].strip()
            if not question or not answer or len(answer) < self.MIN_CHUNK:
                continue
            topic = row[topic_col].strip() if topic_col is not None and len(row) > topic_col else stem
            articles.append(
                self._make_article(topic=topic or stem, question=question, answer=answer, category="faq")
            )

        if not articles:
            raise ValueError(
                f"No valid rows found in '{filename}'. "
                "Ensure the CSV has at least two columns: question and answer."
            )
        return articles

    def _detect_csv_columns(self, header: list[str]) -> tuple[int, int]:
        """Return (question_col_index, answer_col_index)."""
        q_names = {"question", "q", "title", "name", "prompt", "faq"}
        a_names = {"answer", "a", "description", "content", "response", "text", "body"}

        q_col = next((i for i, h in enumerate(header) if h in q_names), 0)
        a_col = next((i for i, h in enumerate(header) if h in a_names), 1)

        # Avoid collision
        if q_col == a_col:
            a_col = 1 if q_col == 0 else 0
        return q_col, a_col

    # -----------------------------------------------------------------------
    # TXT / MD
    # -----------------------------------------------------------------------

    def _extract_text(
        self, file_bytes: bytes, filename: str, *, is_markdown: bool = False
    ) -> list[dict[str, Any]]:
        """Split a plain-text or markdown file into paragraph-sized FAQ articles."""
        text = file_bytes.decode("utf-8", errors="replace")

        if is_markdown:
            text = self._strip_markdown(text)

        chunks = self._split_into_chunks(text)
        if not chunks:
            raise ValueError(f"No readable content found in '{filename}'.")

        stem = self._stem(filename)
        return [
            self._make_article(
                topic=stem,
                question=f"What does '{stem}' document in section {i + 1}?",
                answer=chunk,
                category="document",
            )
            for i, chunk in enumerate(chunks)
        ]

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _split_into_chunks(self, text: str) -> list[str]:
        """Split text into CHUNK_SIZE-capped chunks, preferring paragraph boundaries."""
        # Normalise whitespace
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: list[str] = []
        buffer = ""

        for para in paragraphs:
            if len(para) < self.MIN_CHUNK:
                continue  # skip very short fragments
            candidate = (buffer + "\n\n" + para).strip() if buffer else para
            if len(candidate) <= self.CHUNK_SIZE:
                buffer = candidate
            else:
                if buffer:
                    chunks.append(buffer)
                # If a single paragraph is too large, hard-split it
                if len(para) > self.CHUNK_SIZE:
                    for start in range(0, len(para), self.CHUNK_SIZE):
                        piece = para[start : start + self.CHUNK_SIZE].strip()
                        if piece:
                            chunks.append(piece)
                    buffer = ""
                else:
                    buffer = para

        if buffer:
            chunks.append(buffer)
        return chunks

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """Remove common markdown syntax for cleaner plain-text extraction."""
        # Remove fenced code blocks
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`]+`", "", text)
        # Remove headings (keep the heading text)
        text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
        # Remove link syntax but keep display text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        # Remove bold/italic markers
        text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
        text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
        # Remove horizontal rules
        text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
        # Remove blockquotes
        text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
        return text.strip()

    @staticmethod
    def _stem(filename: str) -> str:
        """Return a human-readable document name from a filename."""
        name = filename.rsplit(".", 1)[0]  # drop extension
        name = re.sub(r"[_\-]+", " ", name)  # underscores/dashes → spaces
        return name.title().strip() or "Uploaded Document"

    @staticmethod
    def _make_article(
        topic: str, question: str, answer: str, category: str
    ) -> dict[str, Any]:
        return {
            "topic": topic[:120],
            "question": question[:500],
            "answer": answer,
            "category": category,
            "published": False,
        }
