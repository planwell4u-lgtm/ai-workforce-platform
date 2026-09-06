import subprocess
import tarfile
from pathlib import Path

KEY_PATH = r"C:\Users\robon\Downloads\ssh-key-2026-09-03.key"
HOST = "opc@130.210.46.184"
REMOTE_DIR = "/home/opc/planwell"

FILES_TO_PACK = [
    # Core & UI
    "apps/backend/src/ai_workforce_backend/url_extractor.py",
    "apps/backend/src/ai_workforce_backend/app.py",
    "apps/frontend/app/local-management/page.tsx",
    "docs/V2/00_CONTROL/02_PROJECT_ROADMAP.md",
    "docs/V2/00_CONTROL/ROADMAP.md",
    # Document, Media, Redis & Knowledge Management
    "apps/backend/src/ai_workforce_backend/document_extractor.py",
    "apps/backend/src/ai_workforce_backend/media_extractor.py",
    "apps/backend/src/ai_workforce_backend/redis_cache.py",
    "apps/backend/src/ai_workforce_backend/knowledge_management.py",
    # Phase 8 Omnichannel Adapters
    "packages/digital_channel/python/src/ai_workforce_digital_channel/sms_adapter.py",
    "packages/digital_channel/python/src/ai_workforce_digital_channel/whatsapp_adapter.py",
    "packages/digital_channel/python/src/ai_workforce_digital_channel/__init__.py",
    "apps/backend/src/ai_workforce_backend/omnichannel_management.py",
    # Phase 9 Post-Conversation AI Insights & Data Store Updates
    "apps/backend/src/ai_workforce_backend/conversation_insights.py",
    "packages/data/python/src/ai_workforce_data/postgres_store.py",
    # Phase 10 & 11 Enterprise Platform & PSTN Voice Management
    "apps/backend/src/ai_workforce_backend/system_health.py",
    "packages/digital_channel/python/src/ai_workforce_digital_channel/voice_adapter.py",
    "apps/backend/src/ai_workforce_backend/voice_management.py",
    "scripts/backup_db.py",
    "deploy/docker-compose.yml",
    "requirements.txt",
    "pyproject.toml",
    "apps/backend/Dockerfile",
]

def deploy():
    tar_path = Path("d:/project/step4_update.tar.gz")
    print(f"Creating archive {tar_path}...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in FILES_TO_PACK:
            local_f = Path("d:/project") / f
            print(f" Packing {f}")
            tar.add(local_f, arcname=f)

    print("Uploading archive via scp...")
    scp_cmd = [
        "scp",
        "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        str(tar_path),
        f"{HOST}:{REMOTE_DIR}/step4_update.tar.gz"
    ]
    subprocess.run(scp_cmd, check=True)

    print("Extracting and rebuilding containers on Oracle Cloud VM...")
    remote_script = (
        f"cd {REMOTE_DIR} && "
        "tar -xzf step4_update.tar.gz && "
        "rm -f step4_update.tar.gz && "
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml build --no-cache frontend backend && "
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml down && "
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml up -d --remove-orphans && "
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml ps"
    )
    ssh_cmd = [
        "ssh",
        "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        HOST,
        remote_script
    ]
    res = subprocess.run(ssh_cmd, check=True)

    if tar_path.exists():
        tar_path.unlink()
    print("\n[SUCCESS] Phase 10 Enterprise Platform & Governance deployed successfully to Oracle Cloud!")

if __name__ == "__main__":
    deploy()
