"""Media Knowledge Extractor — YouTube transcript ingestion.

Uses youtube-transcript-api (pure Python, ~150 KB, no API key required).
Audio/video (MP3/MP4) transcription via Whisper is scaffolded as a future
feature stub to avoid heavy Docker image size (~2–8 GB).
"""

from __future__ import annotations

import re
from typing import Any


# ---------------------------------------------------------------------------
# Public extractor class
# ---------------------------------------------------------------------------

class YouTubeKnowledgeExtractor:
    """Fetches auto-generated or manually uploaded captions from a YouTube video
    and chunks them into draft knowledge articles.

    Parameters
    ----------
    words_per_chunk: Target word count per article (default 150 words ≈ ~1 min of speech).
    preferred_langs: Language codes to try in order (default: English).
    """

    def __init__(
        self,
        words_per_chunk: int = 150,
        preferred_langs: list[str] | None = None,
    ) -> None:
        self._words_per_chunk = words_per_chunk
        self._preferred_langs = preferred_langs or ["en", "en-US", "en-GB"]

    # -----------------------------------------------------------------------
    # Entry point
    # -----------------------------------------------------------------------

    def extract(self, url: str) -> list[dict[str, Any]]:
        """Fetch a YouTube transcript and return draft knowledge articles.

        Parameters
        ----------
        url: Any supported YouTube URL format:
             - https://www.youtube.com/watch?v=VIDEO_ID
             - https://youtu.be/VIDEO_ID
             - https://www.youtube.com/shorts/VIDEO_ID
             - https://www.youtube.com/embed/VIDEO_ID

        Returns
        -------
        List of draft article dicts, one per ~150-word chunk of the transcript.
        """
        video_id = self._parse_video_id(url)
        if not video_id:
            raise ValueError(
                f"Could not extract a YouTube video ID from URL: '{url}'. "
                "Please use a standard YouTube link (e.g. https://youtube.com/watch?v=...)"
            )

        transcript_entries = self._fetch_transcript(video_id)
        chunks = self._chunk_transcript(transcript_entries)

        if not chunks:
            raise ValueError(
                f"No transcript text found for YouTube video '{video_id}'. "
                "The video may not have captions available."
            )

        video_title = self._guess_title(url, video_id)
        return [
            self._make_article(
                topic=video_title,
                chunk_text=chunk["text"],
                chunk_index=i,
                start_seconds=chunk["start"],
                total_chunks=len(chunks),
            )
            for i, chunk in enumerate(chunks)
        ]

    # -----------------------------------------------------------------------
    # Video ID parsing
    # -----------------------------------------------------------------------

    _PATTERNS: list[re.Pattern[str]] = [
        # Standard watch URL: youtube.com/watch?v=VIDEO_ID
        re.compile(r"(?:youtube\.com/watch\?(?:.*&)?v=)([a-zA-Z0-9_-]{11})"),
        # Short URL: youtu.be/VIDEO_ID
        re.compile(r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})"),
        # Shorts: youtube.com/shorts/VIDEO_ID
        re.compile(r"(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"),
        # Embed: youtube.com/embed/VIDEO_ID
        re.compile(r"(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})"),
        # Bare 11-char video ID
        re.compile(r"^([a-zA-Z0-9_-]{11})$"),
    ]

    @classmethod
    def _parse_video_id(cls, url: str) -> str | None:
        url = url.strip()
        for pattern in cls._PATTERNS:
            match = pattern.search(url)
            if match:
                return match.group(1)
        return None

    # -----------------------------------------------------------------------
    # Transcript fetching
    # -----------------------------------------------------------------------

    def _fetch_transcript(self, video_id: str) -> list[dict[str, Any]]:
        """Retrieve transcript entries using youtube-transcript-api."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore[import-untyped]
            from youtube_transcript_api._errors import (  # type: ignore[import-untyped]
                TranscriptsDisabled,
                NoTranscriptFound,
                VideoUnavailable,
            )
        except ImportError as exc:
            raise RuntimeError(
                "youtube-transcript-api is not installed. "
                "Add 'youtube-transcript-api>=0.6,<1' to requirements.txt."
            ) from exc

        try:
            # Try preferred languages first, then fall back to any available
            try:
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id, languages=self._preferred_langs
                )
            except NoTranscriptFound:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return list(transcript)
        except TranscriptsDisabled:
            raise ValueError(
                f"Transcripts are disabled for video '{video_id}'. "
                "The video owner has turned off captions for this video."
            )
        except VideoUnavailable:
            raise ValueError(
                f"YouTube video '{video_id}' is not available (private, deleted, or region-locked)."
            )
        except Exception as exc:
            raise ValueError(
                f"Failed to fetch transcript for '{video_id}': {exc}"
            ) from exc

    # -----------------------------------------------------------------------
    # Chunking
    # -----------------------------------------------------------------------

    def _chunk_transcript(
        self, entries: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Group transcript entries into word-count-bounded chunks.

        Returns list of dicts: {"text": str, "start": float}
        """
        chunks: list[dict[str, Any]] = []
        buffer_words: list[str] = []
        buffer_start: float = 0.0
        first_entry = True

        for entry in entries:
            text = str(entry.get("text", "")).strip()
            start = float(entry.get("start", 0.0))

            if first_entry:
                buffer_start = start
                first_entry = False

            words = text.split()
            buffer_words.extend(words)

            if len(buffer_words) >= self._words_per_chunk:
                chunks.append({"text": " ".join(buffer_words), "start": buffer_start})
                buffer_words = []
                buffer_start = start

        # flush remaining
        if buffer_words and len(" ".join(buffer_words)) >= 60:
            chunks.append({"text": " ".join(buffer_words), "start": buffer_start})

        return chunks

    # -----------------------------------------------------------------------
    # Article factory
    # -----------------------------------------------------------------------

    @staticmethod
    def _make_article(
        topic: str,
        chunk_text: str,
        chunk_index: int,
        start_seconds: float,
        total_chunks: int,
    ) -> dict[str, Any]:
        minutes = int(start_seconds // 60)
        seconds = int(start_seconds % 60)
        timestamp = f"{minutes}:{seconds:02d}"
        part_label = f"Part {chunk_index + 1} of {total_chunks}" if total_chunks > 1 else "Transcript"

        return {
            "topic": topic[:120],
            "question": f"What does the video '{topic}' explain in {part_label} (at {timestamp})?",
            "answer": chunk_text,
            "category": "video",
            "published": False,
        }

    @staticmethod
    def _guess_title(url: str, video_id: str) -> str:
        """Best-effort human-readable title (URL-based, no API calls)."""
        # If URL has a playlist or title hint in its query string, use video ID
        # Real title would require YouTube Data API (not worth the key dependency)
        return f"YouTube Video ({video_id})"
