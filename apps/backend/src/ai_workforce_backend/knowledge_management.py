"""Protected dynamic knowledge base & FAQ management API for workspace owners."""

from __future__ import annotations

import base64
import json
import uuid
from collections.abc import Callable, Mapping
from typing import Any, Literal, cast
from urllib.parse import parse_qs

from ai_workforce_data.postgres_store import PostgresTenantStore

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)
from .document_extractor import DocumentKnowledgeExtractor
from .media_extractor import YouTubeKnowledgeExtractor
from .redis_cache import RedisCacheManager
from .url_extractor import WebsiteKnowledgeExtractor

# Maximum upload size accepted for ingest-file (10 MB decoded)
_MAX_UPLOAD_BYTES = 10 * 1024 * 1024


class KnowledgeManagementApi:
    route_ref = "agent.knowledge-management.v1"
    read_permissions = frozenset({"platform.owner", "platform.front-desk.configure", "agent.context.read"})
    write_permissions = frozenset({"platform.owner", "platform.front-desk.configure"})

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        store: PostgresTenantStore,
        audit_sink: AuditSink,
        extractor: WebsiteKnowledgeExtractor | None = None,
        doc_extractor: DocumentKnowledgeExtractor | None = None,
        yt_extractor: YouTubeKnowledgeExtractor | None = None,
        cache: RedisCacheManager | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._store = store
        self._audit_sink = audit_sink
        self._extractor = extractor or WebsiteKnowledgeExtractor()
        self._doc_extractor = doc_extractor or DocumentKnowledgeExtractor()
        self._yt_extractor = yt_extractor or YouTubeKnowledgeExtractor()
        self._cache = cache or RedisCacheManager()
        self._correlation_factory = correlation_factory


    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        path = str(environ.get("PATH_INFO", "")).rstrip("/")

        valid_paths = {
            "/v1/owner/knowledge",
            "/v1/owner/knowledge/ingest-url",
            "/v1/owner/knowledge/ingest-file",
            "/v1/owner/knowledge/ingest-youtube",
            "/v1/owner/knowledge/health",
            "/v1/owner/knowledge/bulk-publish",
        }
        if path not in valid_paths:
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})

        method = str(environ.get("REQUEST_METHOD", "GET")).upper()
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            tenant_ref = membership.tenant_ref
            permissions = membership.permissions

            # 1. Health & Coverage Analytics (GET /v1/owner/knowledge/health)
            if path == "/v1/owner/knowledge/health" and method == "GET":
                if not (self.read_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
                
                health_data = self._calculate_knowledge_health(tenant_ref)
                self._record_audit(correlation_ref, "allowed", "knowledge_health_analyzed", identity.principal_ref, tenant_ref)
                return self._respond(start_response, "200 OK", headers, {"status": "ok", **health_data})

            # 2. Website URL Ingestion (POST /v1/owner/knowledge/ingest-url)
            if path == "/v1/owner/knowledge/ingest-url" and method == "POST":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                body = self._read_json(environ)
                url = str(body.get("url", "")).strip()
                if not url:
                    return self._respond(start_response, "400 Bad Request", headers, {"error": "url_required", "message": "Website URL is required."})

                try:
                    extracted_items = self._extractor.fetch_and_extract(url)
                except Exception as err:
                    return self._respond(
                        start_response,
                        "400 Bad Request",
                        headers,
                        {"error": "crawl_failed", "message": f"Unable to ingest website URL: {err}"},
                    )

                saved_articles = self._save_draft_articles(
                    extracted_items, tenant_ref, f"crawler:{identity.principal_ref}"
                )
                self._record_audit(
                    correlation_ref,
                    "allowed",
                    f"knowledge_url_ingested:{url}:{len(saved_articles)}",
                    identity.principal_ref,
                    tenant_ref,
                )
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {
                        "status": "ok",
                        "message": f"Successfully extracted {len(saved_articles)} draft articles from {url}.",
                        "url": url,
                        "ingested_count": len(saved_articles),
                        "articles": saved_articles,
                    },
                )

            # 3a. Document File Ingestion (POST /v1/owner/knowledge/ingest-file)
            if path == "/v1/owner/knowledge/ingest-file" and method == "POST":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                body = self._read_json(environ)
                filename = str(body.get("filename", "")).strip()
                content_b64 = str(body.get("content_base64", "")).strip()

                if not filename or not content_b64:
                    return self._respond(
                        start_response, "400 Bad Request", headers,
                        {"error": "filename_and_content_required",
                         "message": "Both 'filename' and 'content_base64' are required."},
                    )

                try:
                    file_bytes = base64.b64decode(content_b64)
                except Exception:
                    return self._respond(
                        start_response, "400 Bad Request", headers,
                        {"error": "invalid_base64", "message": "content_base64 is not valid base64."},
                    )

                if len(file_bytes) > _MAX_UPLOAD_BYTES:
                    mb = _MAX_UPLOAD_BYTES // (1024 * 1024)
                    return self._respond(
                        start_response, "413 Content Too Large", headers,
                        {"error": "file_too_large", "message": f"File exceeds the {mb} MB upload limit."},
                    )

                try:
                    extracted_items = self._doc_extractor.extract(filename, file_bytes)
                except Exception as err:
                    return self._respond(
                        start_response, "400 Bad Request", headers,
                        {"error": "extraction_failed", "message": str(err)},
                    )

                saved_articles = self._save_draft_articles(extracted_items, tenant_ref, f"doc-upload:{identity.principal_ref}")
                self._record_audit(
                    correlation_ref, "allowed",
                    f"knowledge_file_ingested:{filename}:{len(saved_articles)}",
                    identity.principal_ref, tenant_ref,
                )
                return self._respond(
                    start_response, "200 OK", headers,
                    {
                        "status": "ok",
                        "message": f"Extracted {len(saved_articles)} draft articles from '{filename}'.",
                        "filename": filename,
                        "ingested_count": len(saved_articles),
                        "articles": saved_articles,
                    },
                )

            # 3b. YouTube Transcript Ingestion (POST /v1/owner/knowledge/ingest-youtube)
            if path == "/v1/owner/knowledge/ingest-youtube" and method == "POST":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                body = self._read_json(environ)
                yt_url = str(body.get("url", "")).strip()

                if not yt_url:
                    return self._respond(
                        start_response, "400 Bad Request", headers,
                        {"error": "url_required", "message": "A YouTube URL is required."},
                    )

                try:
                    extracted_items = self._yt_extractor.extract(yt_url)
                except Exception as err:
                    return self._respond(
                        start_response, "400 Bad Request", headers,
                        {"error": "transcript_failed", "message": str(err)},
                    )

                saved_articles = self._save_draft_articles(extracted_items, tenant_ref, f"yt-ingest:{identity.principal_ref}")
                self._record_audit(
                    correlation_ref, "allowed",
                    f"knowledge_youtube_ingested:{yt_url}:{len(saved_articles)}",
                    identity.principal_ref, tenant_ref,
                )
                return self._respond(
                    start_response, "200 OK", headers,
                    {
                        "status": "ok",
                        "message": f"Extracted {len(saved_articles)} draft articles from YouTube video.",
                        "url": yt_url,
                        "ingested_count": len(saved_articles),
                        "articles": saved_articles,
                    },
                )

            # 3c. Bulk Publishing (POST /v1/owner/knowledge/bulk-publish)
            if path == "/v1/owner/knowledge/bulk-publish" and method == "POST":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                body = self._read_json(environ)
                publish_all = bool(body.get("publish_all", False))
                target_refs = set(body.get("article_refs", []))

                articles = self._store.list_knowledge_articles(tenant_ref, published_only=False)
                published_count = 0

                for a in articles:
                    if not a.published and (publish_all or a.article_ref in target_refs):
                        self._store.upsert_knowledge_article(
                            article_ref=a.article_ref,
                            tenant_ref=tenant_ref,
                            topic=a.topic,
                            question=a.question,
                            answer=a.answer,
                            category=a.category,
                            published=True,
                            created_by=identity.principal_ref,
                        )
                        published_count += 1

                self._cache.invalidate_tenant(tenant_ref)
                self._record_audit(
                    correlation_ref,
                    "allowed",
                    f"knowledge_bulk_published:{published_count}",
                    identity.principal_ref,
                    tenant_ref,
                )
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {"status": "ok", "published_count": published_count},
                )

            # 4. Standard Base Knowledge CRUD (/v1/owner/knowledge)
            if method == "GET":
                if not (self.read_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                cache_key = f"kb:articles:{tenant_ref}"
                cached_articles = self._cache.get(cache_key)
                if cached_articles is not None:
                    self._record_audit(correlation_ref, "allowed", "knowledge_articles_listed_cached", identity.principal_ref, tenant_ref)
                    return self._respond(
                        start_response,
                        "200 OK",
                        headers,
                        {"status": "ok", "tenant_ref": tenant_ref, "articles": cached_articles},
                    )

                articles = self._store.list_knowledge_articles(tenant_ref, published_only=False)
                articles_data = [
                    {
                        "article_ref": a.article_ref,
                        "topic": a.topic,
                        "question": a.question,
                        "answer": a.answer,
                        "category": a.category,
                        "published": a.published,
                        "created_by": a.created_by,
                        "updated_at": a.updated_at,
                    }
                    for a in articles
                ]
                self._cache.set(cache_key, articles_data, ttl_seconds=300)
                self._record_audit(correlation_ref, "allowed", "knowledge_articles_listed", identity.principal_ref, tenant_ref)
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {"status": "ok", "tenant_ref": tenant_ref, "articles": articles_data},
                )

            if method == "POST":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                body = self._read_json(environ)
                question = str(body.get("question", "")).strip()
                answer = str(body.get("answer", "")).strip()
                topic = str(body.get("topic", "")).strip() or "General"
                category = str(body.get("category", "")).strip() or "faq"
                published = bool(body.get("published", True))
                article_ref = str(body.get("article_ref", "")).strip() or str(uuid.uuid4())

                if not question or not answer:
                    return self._respond(
                        start_response, "400 Bad Request", headers, {"error": "question_and_answer_required"}
                    )

                self._store.upsert_knowledge_article(
                    article_ref=article_ref,
                    tenant_ref=tenant_ref,
                    topic=topic,
                    question=question,
                    answer=answer,
                    category=category,
                    published=published,
                    created_by=identity.principal_ref,
                )
                self._cache.invalidate_tenant(tenant_ref)
                self._record_audit(
                    correlation_ref,
                    "allowed",
                    f"knowledge_article_saved:{article_ref}",
                    identity.principal_ref,
                    tenant_ref,
                )
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {"status": "ok", "article_ref": article_ref},
                )

            if method == "DELETE":
                if not (self.write_permissions & permissions):
                    self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref, tenant_ref)
                    return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

                query = parse_qs(str(environ.get("QUERY_STRING", "")))
                article_ref_list = query.get("article_ref")
                if not article_ref_list or not article_ref_list[0].strip():
                    return self._respond(
                        start_response, "400 Bad Request", headers, {"error": "article_ref_required"}
                    )
                article_ref = article_ref_list[0].strip()
                deleted = self._store.delete_knowledge_article(tenant_ref, article_ref)
                self._cache.invalidate_tenant(tenant_ref)
                self._record_audit(
                    correlation_ref,
                    "allowed",
                    f"knowledge_article_deleted:{article_ref}",
                    identity.principal_ref,
                    tenant_ref,
                )
                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {"status": "ok", "deleted": deleted, "article_ref": article_ref},
                )

            return self._respond(start_response, "405 Method Not Allowed", headers, {"error": "method_not_allowed"})

        except AuthenticationError:
            return self._respond(
                start_response,
                "401 Unauthorized",
                headers,
                {"error": "unauthorized"},
            )
        except AuthorizationError:
            try:
                self._record_audit(correlation_ref, "denied", "forbidden", identity.principal_ref if identity else None, membership.tenant_ref if membership else None)
            except Exception:
                pass
            return self._respond(
                start_response,
                "403 Forbidden",
                headers,
                {"error": "forbidden"},
            )
        except Exception as error:
            self._record_audit(correlation_ref, "denied", f"internal_error:{error}", None, None)
            return self._respond(start_response, "500 Internal Server Error", headers, {"error": "internal_error", "message": str(error)})

    def _calculate_knowledge_health(self, tenant_ref: str) -> dict[str, Any]:
        """Calculates 0-100% Knowledge Health Score, category coverage, and gap warnings."""
        cache_key = f"kb:health:{tenant_ref}"
        cached_health = self._cache.get(cache_key)
        if cached_health is not None:
            return cached_health

        articles = self._store.list_knowledge_articles(tenant_ref, published_only=False)
        total = len(articles)
        published = [a for a in articles if a.published]
        drafts = [a for a in articles if not a.published]

        category_counts: dict[str, int] = {}
        for a in published:
            cat = a.category.lower().strip() or "general"
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Weight components:
        # Services (30%), Hours (20%), Support/Contact (20%), Billing (15%), General (15%)
        score = 0
        gaps: list[str] = []
        recommendations: list[str] = []

        if category_counts.get("services", 0) >= 2:
            score += 30
        elif category_counts.get("services", 0) == 1:
            score += 15
            gaps.append("Expand service offerings (only 1 service article published)")
        else:
            gaps.append("Missing published service & product descriptions")

        if category_counts.get("hours", 0) >= 1:
            score += 20
        else:
            gaps.append("Missing operating hours & availability details")

        if category_counts.get("support", 0) >= 1:
            score += 20
        else:
            gaps.append("Missing direct contact and escalation instructions")

        if category_counts.get("billing", 0) >= 1 or category_counts.get("pricing", 0) >= 1:
            score += 15
        else:
            gaps.append("Missing pricing, payment methods, or refund terms")

        if len(published) >= 4:
            score += 15
        elif len(published) >= 2:
            score += 8
        else:
            gaps.append("Low overall article volume (recommend at least 5 published FAQs)")

        # Bonus for published articles
        if total > 0 and len(published) == total:
            score = min(100, score + 5)

        # Grade classification
        if score >= 85:
            grade = "Excellent Coverage"
        elif score >= 65:
            grade = "Good Coverage"
        elif score >= 40:
            grade = "Moderate Coverage"
        else:
            grade = "Needs Improvement"

        if drafts:
            recommendations.append(f"Review and publish {len(drafts)} pending draft articles.")
        if "Missing operating hours & availability details" in gaps:
            recommendations.append("Add a 'Business Hours' FAQ to handle after-hours caller inquiries.")
        if "Missing published service & product descriptions" in gaps:
            recommendations.append("Use 'Instant Ingest from Website' to automatically import service descriptions.")

        health_data = {
            "health_score": min(100, score),
            "grade": grade,
            "total_articles": total,
            "published_count": len(published),
            "draft_count": len(drafts),
            "category_breakdown": category_counts,
            "gaps": gaps,
            "recommendations": recommendations,
        }
        self._cache.set(cache_key, health_data, ttl_seconds=60)
        return health_data

    def _record_audit(
        self,
        correlation_ref: str,
        decision: str,
        reason: str,
        principal_ref: str | None,
        tenant_ref: str | None,
    ) -> None:
        self._audit_sink.record(
            AuditEvent(
                outcome="allowed" if decision == "allowed" else "denied",
                reason=reason,
                correlation_ref=correlation_ref,
                route_ref=self.route_ref,
                principal_ref=principal_ref,
                tenant_ref=tenant_ref,
            )
        )

    def _save_draft_articles(
        self,
        items: list[dict[str, Any]],
        tenant_ref: str,
        created_by: str,
    ) -> list[dict[str, Any]]:
        """Persist extracted draft articles and return their saved representations."""
        saved: list[dict[str, Any]] = []
        for item in items:
            art_ref = str(uuid.uuid4())
            cat = str(item.get("category", "general"))
            self._store.upsert_knowledge_article(
                article_ref=art_ref,
                tenant_ref=tenant_ref,
                topic=str(item.get("topic", "Imported"))[:120],
                question=str(item.get("question", ""))[:500],
                answer=str(item.get("answer", "")),
                category=cat,
                published=False,
                created_by=created_by,
            )
            saved.append({
                "article_ref": art_ref,
                "topic": item.get("topic"),
                "question": item.get("question"),
                "answer": item.get("answer"),
                "category": cat,
                "published": False,
            })
        self._cache.invalidate_tenant(tenant_ref)
        return saved

    @staticmethod
    def _read_json(environ: Mapping[str, object]) -> dict[str, object]:
        try:
            length = int(str(environ.get("CONTENT_LENGTH") or 0))
        except (ValueError, TypeError):
            length = 0
        stream = environ.get("wsgi.input")
        if not stream or length <= 0:
            return {}
        try:
            data = stream.read(length)  # type: ignore[union-attr]
            return json.loads(data.decode("utf-8")) if data else {}
        except Exception:
            return {}

    @staticmethod
    def _respond(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: dict[str, object],
    ) -> list[bytes]:
        payload = json.dumps(body).encode("utf-8")
        headers.append(("Content-Length", str(len(payload))))
        start_response(status, headers)
        return [payload]
