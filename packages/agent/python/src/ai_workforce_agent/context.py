"""B3 local agent selection with governed Knowledge and Memory boundaries."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Classification = Literal["internal"]

_QUESTION_STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "can",
        "change",
        "do",
        "for",
        "help",
        "how",
        "i",
        "if",
        "in",
        "is",
        "it",
        "me",
        "my",
        "of",
        "on",
        "or",
        "the",
        "to",
        "what",
        "with",
        "you",
        "your",
    }
)


def _search_terms(text: str) -> set[str]:
    """Normalize simple FAQ wording variations without generating new content."""
    terms = {
        term
        for term in re.findall(r"[a-z0-9]+", text.lower())
        if term not in _QUESTION_STOP_WORDS
    }
    return {"track" if term == "tracking" else term for term in terms}


class ContextDenied(PermissionError):
    """Requested agent, knowledge, or memory context is not currently eligible."""


@dataclass(frozen=True)
class AgentVersion:
    agent_ref: str
    version_ref: str
    tenant_ref: str
    status: Literal["released", "suspended"]
    allowed_capabilities: frozenset[str]


@dataclass(frozen=True)
class KnowledgeEntry:
    source_ref: str
    tenant_ref: str
    classification: Classification
    published: bool
    excerpt: str


@dataclass(frozen=True)
class MemoryFact:
    tenant_ref: str
    subject_ref: str
    session_ref: str
    purpose: Literal["service_continuity"]
    value: str


@dataclass(frozen=True)
class AgentContext:
    agent_version_ref: str
    tenant_ref: str
    knowledge_excerpts: tuple[str, ...]
    memory_facts: tuple[str, ...]


class LocalKnowledgeSource:
    """Approved local FAQ source; retrieval returns only published same-tenant excerpts."""

    def __init__(self, entries: tuple[KnowledgeEntry, ...]) -> None:
        self._entries = entries

    @classmethod
    def from_jsonl(
        cls,
        path: Path,
        *,
        tenant_ref: str,
        source_ref: str,
    ) -> LocalKnowledgeSource:
        """Load a reviewed local JSONL FAQ source for one tenant."""
        if not path.is_file() or not tenant_ref or not source_ref:
            raise ValueError("path, tenant_ref, and source_ref are required")
        entries: list[KnowledgeEntry] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid FAQ JSON at line {line_number}") from error
            if not isinstance(item, dict):
                raise TypeError(f"FAQ entry at line {line_number} must be an object")
            question = item.get("question")
            answer = item.get("answer")
            if not isinstance(question, str) or not isinstance(answer, str):
                raise TypeError(f"FAQ entry at line {line_number} needs text question and answer")
            entries.append(
                KnowledgeEntry(
                    f"{source_ref}:{line_number}",
                    tenant_ref,
                    "internal",
                    True,
                    f"Q: {question}\nA: {answer}",
                )
            )
        if not entries:
            raise ValueError("FAQ source has no entries")
        return cls(tuple(entries))

    def retrieve(self, tenant_ref: str) -> tuple[str, ...]:
        return tuple(
            entry.excerpt
            for entry in self._entries
            if entry.tenant_ref == tenant_ref
            and entry.published
            and entry.classification == "internal"
        )

    def search(
        self, tenant_ref: str, question: str, *, minimum_match_ratio: float = 0.6
    ) -> KnowledgeEntry | None:
        """Return an approved same-tenant FAQ match without generating new content."""
        if not 0 <= minimum_match_ratio <= 1:
            raise ValueError("minimum_match_ratio must be between zero and one")
        terms = _search_terms(question)
        if not terms:
            return None
        candidates = (
            entry
            for entry in self._entries
            if entry.tenant_ref == tenant_ref
            and entry.published
            and entry.classification == "internal"
        )
        ranked = sorted(
            (
                (
                    len(terms & _search_terms(entry.excerpt))
                    / len(terms),
                    entry,
                )
                for entry in candidates
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        if not ranked or ranked[0][0] < minimum_match_ratio or ranked[0][0] == 0:
            return None
        return ranked[0][1]


class DynamicKnowledgeSource(LocalKnowledgeSource):
    """Knowledge source that dynamically loads published articles from PostgreSQL storage."""

    def __init__(self, store: object, fallback_source: LocalKnowledgeSource | None = None) -> None:
        super().__init__(())
        self._store = store
        self._fallback = fallback_source

    def retrieve(self, tenant_ref: str) -> tuple[str, ...]:
        if hasattr(self._store, "list_knowledge_articles"):
            articles = self._store.list_knowledge_articles(tenant_ref, published_only=True)
            if articles:
                return tuple(f"Q: {a.question}\nA: {a.answer}" for a in articles)
        if self._fallback:
            return self._fallback.retrieve(tenant_ref)
        return ()

    def search(
        self, tenant_ref: str, question: str, *, minimum_match_ratio: float = 0.6
    ) -> KnowledgeEntry | None:
        if hasattr(self._store, "list_knowledge_articles"):
            articles = self._store.list_knowledge_articles(tenant_ref, published_only=True)
            if articles:
                terms = _search_terms(question)
                if not terms:
                    return None
                entries = [
                    KnowledgeEntry(
                        source_ref=f"db:{a.article_ref}",
                        tenant_ref=tenant_ref,
                        classification="internal",
                        published=True,
                        excerpt=f"Q: {a.question}\nA: {a.answer}",
                    )
                    for a in articles
                ]
                ranked = sorted(
                    (
                        (
                            len(terms & _search_terms(entry.excerpt)) / len(terms),
                            entry,
                        )
                        for entry in entries
                    ),
                    key=lambda item: item[0],
                    reverse=True,
                )
                if ranked and ranked[0][0] >= minimum_match_ratio and ranked[0][0] > 0:
                    return ranked[0][1]
        if self._fallback:
            return self._fallback.search(tenant_ref, question, minimum_match_ratio=minimum_match_ratio)
        return None


class SessionMemoryStore:
    """Session-only operational memory, always bound to one tenant and subject."""

    def __init__(self, facts: tuple[MemoryFact, ...]) -> None:
        self._facts = facts

    def retrieve(self, tenant_ref: str, subject_ref: str, session_ref: str) -> tuple[str, ...]:
        return tuple(
            fact.value
            for fact in self._facts
            if fact.tenant_ref == tenant_ref
            and fact.subject_ref == subject_ref
            and fact.session_ref == session_ref
            and fact.purpose == "service_continuity"
        )


class AgentContextService:
    required_permission = "agent.context.read"

    def __init__(
        self,
        versions: tuple[AgentVersion, ...],
        knowledge: LocalKnowledgeSource,
        memory: SessionMemoryStore,
    ) -> None:
        self._versions = versions
        self._knowledge = knowledge
        self._memory = memory

    def assemble(
        self,
        *,
        tenant_ref: str,
        agent_ref: str,
        subject_ref: str,
        session_ref: str,
        permissions: frozenset[str],
    ) -> AgentContext:
        if self.required_permission not in permissions:
            raise ContextDenied("agent_context_not_authorized")
        version = next(
            (
                item
                for item in self._versions
                if item.agent_ref == agent_ref
                and item.tenant_ref == tenant_ref
                and item.status == "released"
            ),
            None,
        )
        if version is None:
            raise ContextDenied("agent_version_not_available")
        knowledge = ()
        memory = ()
        if "knowledge.retrieve" in version.allowed_capabilities:
            knowledge = self._knowledge.retrieve(tenant_ref)
        if "memory.retrieve" in version.allowed_capabilities:
            memory = self._memory.retrieve(tenant_ref, subject_ref, session_ref)
        return AgentContext(version.version_ref, tenant_ref, knowledge, memory)
