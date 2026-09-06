"""Unit tests for Dynamic Knowledge Base & FAQ Management."""

from __future__ import annotations

import io
import json
import sys
import time
import unittest
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "agent" / "python" / "src"))

from ai_workforce_agent.context import DynamicKnowledgeSource, KnowledgeEntry, LocalKnowledgeSource
from ai_workforce_backend.b1 import (
    AuthenticationError,
    IdentityContext,
    IdentityVerifier,
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_backend.knowledge_management import KnowledgeManagementApi
from ai_workforce_data.postgres_store import KnowledgeArticleRecord


class FakeVerifier(IdentityVerifier):
    def __init__(self, permissions_map: dict[str, frozenset[str]]) -> None:
        self.permissions_map = permissions_map

    def verify(self, authorization: str | None) -> IdentityContext:
        if not authorization or not authorization.startswith("Bearer "):
            raise AuthenticationError("missing_bearer_token")
        principal = authorization.removeprefix("Bearer ")
        return IdentityContext(
            principal_ref=principal,
            principal_type="human",
            issuer_ref="test",
            environment_ref="local",
            authenticated_at=int(time.time()),
            granted_permissions=self.permissions_map.get(principal, frozenset()),
        )


class FakeKnowledgeStore:
    def __init__(self) -> None:
        self.articles: dict[str, KnowledgeArticleRecord] = {}

    def list_knowledge_articles(self, tenant_ref: str, published_only: bool = False) -> list[KnowledgeArticleRecord]:
        items = [a for a in self.articles.values() if a.tenant_ref == tenant_ref]
        if published_only:
            items = [a for a in items if a.published]
        return sorted(items, key=lambda a: a.updated_at, reverse=True)

    def upsert_knowledge_article(
        self,
        *,
        article_ref: str,
        tenant_ref: str,
        topic: str,
        question: str,
        answer: str,
        category: str = "faq",
        published: bool = True,
        created_by: str,
    ) -> None:
        self.articles[article_ref] = KnowledgeArticleRecord(
            article_ref=article_ref,
            tenant_ref=tenant_ref,
            topic=topic,
            question=question,
            answer=answer,
            category=category,
            published=published,
            created_by=created_by,
            updated_at="2026-09-05T12:00:00Z",
        )

    def delete_knowledge_article(self, tenant_ref: str, article_ref: str) -> bool:
        if article_ref in self.articles and self.articles[article_ref].tenant_ref == tenant_ref:
            del self.articles[article_ref]
            return True
        return False


class TestKnowledgeManagementApi(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = FakeVerifier({
            "auth0|owner": frozenset({"platform.owner"}),
            "auth0|frontdesk": frozenset({"platform.front-desk.configure"}),
            "auth0|reader": frozenset({"agent.context.read"}),
            "auth0|viewer": frozenset(),
        })
        self.memberships = InMemoryMembershipDirectory((
            Membership("auth0|owner", "tenant-alpha", "active", frozenset({"platform.owner"})),
            Membership("auth0|frontdesk", "tenant-alpha", "active", frozenset({"platform.front-desk.configure"})),
            Membership("auth0|reader", "tenant-alpha", "active", frozenset({"agent.context.read"})),
            Membership("auth0|viewer", "tenant-alpha", "active", frozenset()),
        ))
        self.store = FakeKnowledgeStore()
        self.audit = InMemoryAuditSink()
        self.api = KnowledgeManagementApi(
            self.verifier,
            self.memberships,
            cast(Any, self.store),
            self.audit,
        )

    def _call(
        self,
        method: str,
        path: str = "/v1/owner/knowledge",
        auth: str | None = "Bearer auth0|owner",
        body: dict[str, Any] | None = None,
        query: str = "",
    ) -> tuple[str, list[tuple[str, str]], dict[str, Any]]:
        status_captured: list[str] = []
        headers_captured: list[list[tuple[str, str]]] = []

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            status_captured.append(status)
            headers_captured.append(headers)

        body_bytes = json.dumps(body).encode("utf-8") if body else b""
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": query,
            "HTTP_AUTHORIZATION": auth,
            "CONTENT_LENGTH": str(len(body_bytes)),
            "wsgi.input": io.BytesIO(body_bytes),
        }
        res = self.api(environ, start_response)
        parsed = json.loads(res[0].decode("utf-8")) if res and res[0] else {}
        return status_captured[0], headers_captured[0], parsed

    def test_list_knowledge_articles_empty(self) -> None:
        status, _, payload = self._call("GET", auth="Bearer auth0|owner")
        self.assertEqual(status, "200 OK")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["articles"], [])

    def test_create_and_list_article(self) -> None:
        status, _, create_res = self._call(
            "POST",
            auth="Bearer auth0|owner",
            body={
                "topic": "Shipping",
                "question": "What is the delivery timeframe?",
                "answer": "Standard delivery takes 3-5 business days.",
                "category": "logistics",
                "published": True,
            },
        )
        self.assertEqual(status, "200 OK")
        article_ref = create_res["article_ref"]
        self.assertTrue(article_ref)

        status, _, list_res = self._call("GET", auth="Bearer auth0|owner")
        self.assertEqual(status, "200 OK")
        self.assertEqual(len(list_res["articles"]), 1)
        article = list_res["articles"][0]
        self.assertEqual(article["article_ref"], article_ref)
        self.assertEqual(article["topic"], "Shipping")
        self.assertEqual(article["question"], "What is the delivery timeframe?")
        self.assertEqual(article["answer"], "Standard delivery takes 3-5 business days.")
        self.assertTrue(article["published"])

    def test_update_existing_article(self) -> None:
        _, _, create_res = self._call(
            "POST",
            auth="Bearer auth0|owner",
            body={"question": "Old question?", "answer": "Old answer."},
        )
        article_ref = create_res["article_ref"]

        status, _, update_res = self._call(
            "POST",
            auth="Bearer auth0|owner",
            body={
                "article_ref": article_ref,
                "topic": "Updates",
                "question": "Updated question?",
                "answer": "Updated answer.",
                "published": False,
            },
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(update_res["article_ref"], article_ref)

        _, _, list_res = self._call("GET", auth="Bearer auth0|owner")
        self.assertEqual(len(list_res["articles"]), 1)
        self.assertEqual(list_res["articles"][0]["question"], "Updated question?")
        self.assertEqual(list_res["articles"][0]["answer"], "Updated answer.")
        self.assertFalse(list_res["articles"][0]["published"])

    def test_delete_article(self) -> None:
        _, _, create_res = self._call(
            "POST",
            auth="Bearer auth0|owner",
            body={"question": "To delete?", "answer": "Yes."},
        )
        article_ref = create_res["article_ref"]

        status, _, del_res = self._call(
            "DELETE",
            auth="Bearer auth0|owner",
            query=f"article_ref={article_ref}",
        )
        self.assertEqual(status, "200 OK")
        self.assertTrue(del_res["deleted"])

        _, _, list_res = self._call("GET", auth="Bearer auth0|owner")
        self.assertEqual(list_res["articles"], [])

    def test_post_validation_error(self) -> None:
        status, _, payload = self._call(
            "POST",
            auth="Bearer auth0|owner",
            body={"question": "", "answer": ""},
        )
        self.assertEqual(status, "400 Bad Request")
        self.assertEqual(payload["error"], "question_and_answer_required")

    def test_unauthorized_access(self) -> None:
        status, _, payload = self._call("GET", auth="Bearer auth0|viewer")
        self.assertEqual(status, "403 Forbidden")

        status, _, payload = self._call(
            "POST",
            auth="Bearer auth0|reader",
            body={"question": "Q?", "answer": "A."},
        )
        self.assertEqual(status, "403 Forbidden")

    def test_dynamic_knowledge_source_integration(self) -> None:
        fallback = LocalKnowledgeSource((
            KnowledgeEntry("static:1", "tenant-alpha", "internal", True, "Q: Static question?\nA: Static answer."),
        ))
        dyn = DynamicKnowledgeSource(self.store, fallback_source=fallback)

        # Before any dynamic article, fallback is used
        entry = dyn.search("tenant-alpha", "static question")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.excerpt, "Q: Static question?\nA: Static answer.")

        # Add dynamic article
        self.store.upsert_knowledge_article(
            article_ref="dyn-1",
            tenant_ref="tenant-alpha",
            topic="Refunds",
            question="What is the refund policy?",
            answer="Refunds are processed within 14 days.",
            category="faq",
            published=True,
            created_by="owner",
        )

        # Search finds dynamic article
        dyn_entry = dyn.search("tenant-alpha", "refund policy")
        self.assertIsNotNone(dyn_entry)
    def test_knowledge_health_analytics(self) -> None:
        status, _, payload = self._call("GET", path="/v1/owner/knowledge/health", auth="Bearer auth0|owner")
        self.assertEqual(status, "200 OK")
        self.assertIn("health_score", payload)
        self.assertIn("grade", payload)
        self.assertIn("gaps", payload)
        self.assertIn("category_breakdown", payload)

    def test_ingest_url_endpoint(self) -> None:
        mock_extractor = unittest.mock.MagicMock()
        mock_extractor.fetch_and_extract.return_value = [
            {"topic": "Extracted Services", "question": "What services?", "answer": "Dental care.", "category": "services", "published": False},
            {"topic": "Extracted Hours", "question": "What hours?", "answer": "9am-5pm", "category": "hours", "published": False},
        ]
        self.api._extractor = mock_extractor

        status, _, payload = self._call(
            "POST",
            path="/v1/owner/knowledge/ingest-url",
            auth="Bearer auth0|owner",
            body={"url": "https://brightsmiledental.com"},
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(payload["ingested_count"], 2)
        self.assertEqual(len(self.store.articles), 2)
        # Verify drafts are saved as unpublished
        for art in self.store.articles.values():
            self.assertFalse(art.published)

    def test_bulk_publish_endpoint(self) -> None:
        self.store.upsert_knowledge_article(
            article_ref="draft-1",
            tenant_ref="tenant-alpha",
            topic="Draft 1",
            question="Q1",
            answer="A1",
            published=False,
            created_by="crawler",
        )
        self.store.upsert_knowledge_article(
            article_ref="draft-2",
            tenant_ref="tenant-alpha",
            topic="Draft 2",
            question="Q2",
            answer="A2",
            published=False,
            created_by="crawler",
        )

        status, _, payload = self._call(
            "POST",
            path="/v1/owner/knowledge/bulk-publish",
            auth="Bearer auth0|owner",
            body={"publish_all": True},
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(payload["published_count"], 2)

        published_articles = self.store.list_knowledge_articles("tenant-alpha", published_only=True)
        self.assertEqual(len(published_articles), 2)


if __name__ == "__main__":
    unittest.main()
