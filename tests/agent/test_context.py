"""B3 authorization, versioning, Knowledge, and Memory tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "agent" / "python" / "src"))

from ai_workforce_agent.context import (
    AgentContextService,
    AgentVersion,
    ContextDenied,
    KnowledgeEntry,
    LocalKnowledgeSource,
    MemoryFact,
    SessionMemoryStore,
)
from ai_workforce_agent.support import FaqSupportAgent


class AgentContextServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        versions = (
            AgentVersion(
                "agent-1",
                "agent-1:v1",
                "tenant-a",
                "released",
                frozenset({"knowledge.retrieve", "memory.retrieve"}),
            ),
            AgentVersion(
                "agent-1", "agent-1:v1", "tenant-b", "suspended", frozenset({"knowledge.retrieve"})
            ),
        )
        knowledge = LocalKnowledgeSource(
            (
                KnowledgeEntry(
                    "faq-a", "tenant-a", "internal", True, "Reset links expire after 15 minutes."
                ),
                KnowledgeEntry("faq-b", "tenant-b", "internal", True, "Tenant B private FAQ."),
                KnowledgeEntry("draft-a", "tenant-a", "internal", False, "Unpublished."),
            )
        )
        memory = SessionMemoryStore(
            (
                MemoryFact(
                    "tenant-a",
                    "subject-a",
                    "session-a",
                    "service_continuity",
                    "Customer requested email follow-up.",
                ),
                MemoryFact(
                    "tenant-b", "subject-a", "session-a", "service_continuity", "Tenant B memory."
                ),
            )
        )
        self.service = AgentContextService(versions, knowledge, memory)
        self.support_agent = FaqSupportAgent(self.service, knowledge)

    def test_authorized_context_is_tenant_scoped_and_versioned(self) -> None:
        context = self.service.assemble(
            tenant_ref="tenant-a",
            agent_ref="agent-1",
            subject_ref="subject-a",
            session_ref="session-a",
            permissions=frozenset({"agent.context.read"}),
        )
        self.assertEqual(context.agent_version_ref, "agent-1:v1")
        self.assertEqual(context.knowledge_excerpts, ("Reset links expire after 15 minutes.",))
        self.assertEqual(context.memory_facts, ("Customer requested email follow-up.",))

    def test_unauthorized_or_unavailable_agent_fails_closed(self) -> None:
        with self.assertRaises(ContextDenied):
            self.service.assemble(
                tenant_ref="tenant-a",
                agent_ref="agent-1",
                subject_ref="subject-a",
                session_ref="session-a",
                permissions=frozenset(),
            )
        with self.assertRaises(ContextDenied):
            self.service.assemble(
                tenant_ref="tenant-b",
                agent_ref="agent-1",
                subject_ref="subject-a",
                session_ref="session-a",
                permissions=frozenset({"agent.context.read"}),
            )

    def test_reviewed_jsonl_knowledge_source_is_tenant_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "faqs.jsonl"
            source_path.write_text(
                '{"question":"How do I reset my password?","answer":"Use Forgot Password."}\n',
                encoding="utf-8",
            )
            knowledge = LocalKnowledgeSource.from_jsonl(
                source_path,
                tenant_ref="tenant-a",
                source_ref="support-faqs:v1",
            )
        self.assertEqual(
            knowledge.retrieve("tenant-a"),
            ("Q: How do I reset my password?\nA: Use Forgot Password.",),
        )
        self.assertEqual(knowledge.retrieve("tenant-b"), ())

    def test_support_agent_answers_only_from_approved_tenant_faqs(self) -> None:
        answer = self.support_agent.answer(
            tenant_ref="tenant-a",
            agent_ref="agent-1",
            subject_ref="subject-a",
            session_ref="session-a",
            question="How long do password reset links last?",
            permissions=frozenset({"agent.context.read"}),
        )
        self.assertEqual(answer.answer, "Reset links expire after 15 minutes.")
        self.assertEqual(answer.source_ref, "faq-a")
        self.assertFalse(answer.ticket_recommended)

        no_answer = self.support_agent.answer(
            tenant_ref="tenant-a",
            agent_ref="agent-1",
            subject_ref="subject-a",
            session_ref="session-a",
            question="Can you tell me the weather?",
            permissions=frozenset({"agent.context.read"}),
        )
        self.assertIsNone(no_answer.answer)
        self.assertTrue(no_answer.ticket_recommended)
