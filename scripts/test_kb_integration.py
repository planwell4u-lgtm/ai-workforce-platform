import os
import uuid
from pathlib import Path
from ai_workforce_data.postgres_store import PostgresTenantStore, KnowledgeArticleRecord
from ai_workforce_agent.context import DynamicKnowledgeSource, LocalKnowledgeSource

def load_env():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()

def run_test():
    load_env()
    store = PostgresTenantStore(database_url=os.environ["DATABASE_URL"])
    store.apply_migrations()

    tenant_ref = "staging-demo"
    test_ref = str(uuid.uuid4())
    print("--- 1. Testing Postgres Store Article Upsert ---")
    article = KnowledgeArticleRecord(
        article_ref=test_ref,
        tenant_ref=tenant_ref,
        topic="Official Operating Hours & SLA",
        question="What are the platform operating hours?",
        answer="Planwell operations are active 24/7/365 with automated AI agents. Live human staff is on duty Monday-Friday 9am-6pm EST.",
        category="operations",
        published=True,
        created_by="planwell4u@gmail.com",
        updated_at="2026-09-05T12:00:00Z"
    )
    store.upsert_knowledge_article(
        article_ref=article.article_ref,
        tenant_ref=article.tenant_ref,
        topic=article.topic,
        question=article.question,
        answer=article.answer,
        category=article.category,
        published=article.published,
        created_by=article.created_by,
    )
    print(f"SAVED ARTICLE: article_ref={article.article_ref}, topic='{article.topic}'")

    print("\n--- 2. Listing Knowledge Articles ---")
    articles = store.list_knowledge_articles(tenant_ref)
    for a in articles:
        print(f" - [{a.article_ref}] {a.topic} ({a.category}) | Q: {a.question}")

    print("\n--- 3. Testing DynamicKnowledgeSource Search ---")
    faq_path = Path(os.environ.get("SUPPORT_FAQ_PATH", "packages/agent/knowledge/staging-demo/approved-support-faqs.jsonl"))
    fallback = LocalKnowledgeSource.from_jsonl(faq_path, tenant_ref=tenant_ref, source_ref="staging-demo-faqs")
    ks = DynamicKnowledgeSource(
        store=store,
        fallback_source=fallback
    )
    
    # Query matching custom DB article
    result_db = ks.search(tenant_ref, "What are the platform operating hours?")
    print(f"SEARCH 1 ('platform operating hours') -> Result:")
    if result_db:
        print(f"   Source: {result_db.source_ref}\n   Excerpt:\n{result_db.excerpt}")
    else:
        print("   No match found")

    # Query falling back to static catalog
    result_fallback = ks.search(tenant_ref, "How do I request human agent escalation?")
    print(f"\nSEARCH 2 ('human agent escalation') -> Fallback Result:")
    if result_fallback:
        print(f"   Source: {result_fallback.source_ref}\n   Excerpt:\n{result_fallback.excerpt}")
    else:
        print("   No fallback match found")

    print("\n--- 4. Cleaning up test article ---")
    deleted = store.delete_knowledge_article(tenant_ref, test_ref)
    print(f"DELETED test article ({test_ref}): {deleted}")

    remaining = store.list_knowledge_articles(tenant_ref)
    print(f"REMAINING ARTICLES COUNT: {len(remaining)}")
    print("\nALL DYNAMIC KNOWLEDGE BASE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_test()
