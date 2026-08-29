"""Deterministic sales-answer flow over approved public catalog entries."""

from dataclasses import dataclass

from .context import AgentContextService, LocalKnowledgeSource

SAFE_HUMAN_SALES_ANSWER = (
    "I can't confirm that from the approved catalog. I can connect you with human sales."
)


@dataclass(frozen=True)
class SalesAnswer:
    answer: str
    source_ref: str | None
    human_sales_recommended: bool


class CatalogSalesAgent:
    """Answers only with an approved catalog match; it never captures leads or acts."""

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
    ) -> SalesAnswer:
        context = self._context.assemble(
            tenant_ref=tenant_ref,
            agent_ref=agent_ref,
            subject_ref=subject_ref,
            session_ref=session_ref,
            permissions=permissions,
        )
        if not context.knowledge_excerpts:
            return SalesAnswer(SAFE_HUMAN_SALES_ANSWER, None, True)
        entry = self._knowledge.search(tenant_ref, question)
        if entry is None:
            return SalesAnswer(SAFE_HUMAN_SALES_ANSWER, None, True)
        answer = entry.excerpt.partition("\nA: ")[2] or entry.excerpt
        return SalesAnswer(answer, entry.source_ref, False)
