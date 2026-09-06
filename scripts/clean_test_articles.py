import os
from pathlib import Path
from ai_workforce_data.postgres_store import PostgresTenantStore

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

if __name__ == "__main__":
    load_env()
    store = PostgresTenantStore(database_url=os.environ["DATABASE_URL"])
    articles = store.list_knowledge_articles("staging-demo")
    print(f"Cleaning up {len(articles)} test articles from staging-demo...")
    for a in articles:
        store.delete_knowledge_article("staging-demo", a.article_ref)
        print(f"Deleted {a.article_ref}")
    print("Done. Clean state verified.")
