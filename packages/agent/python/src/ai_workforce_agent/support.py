"""Deterministic first support-answer flow over approved tenant FAQs."""

from __future__ import annotations

from dataclasses import dataclass

from .context import AgentContextService, LocalKnowledgeSource

SAFE_UNAVAILABLE_ANSWER = (
    "I can't access an approved answer for that. I can connect you with human support."
)


@dataclass(frozen=True)
class SupportAnswer:
    answer: str
    source_ref: str | None
    ticket_recommended: bool


class FaqSupportAgent:
    """Answers only with an approved lexical FAQ match; it makes no unsupported claims."""

    def __init__(self, context: AgentContextService, knowledge: LocalKnowledgeSource) -> None:
        self._context = context
        self._knowledge = knowledge

    def answer(
        self,
        *,
        tenant_ref: str,
        agent_ref: str,
        subject_ref: str,
        session_ref: str,
        question: str,
        permissions: frozenset[str],
    ) -> SupportAnswer:
        context = self._context.assemble(
            tenant_ref=tenant_ref,
            agent_ref=agent_ref,
            subject_ref=subject_ref,
            session_ref=session_ref,
            permissions=permissions,
        )
        if not context.knowledge_excerpts:
            return SupportAnswer(SAFE_UNAVAILABLE_ANSWER, None, True)
        # Text chat can accept natural, loosely phrased questions, but it still
        # returns only a verbatim approved FAQ answer.
        entry = self._knowledge.search(tenant_ref, question, minimum_match_ratio=0)
        if entry is None:
            return SupportAnswer(SAFE_UNAVAILABLE_ANSWER, None, True)
        answer = entry.excerpt.partition("\nA: ")[2] or entry.excerpt
        return SupportAnswer(answer, entry.source_ref, False)
