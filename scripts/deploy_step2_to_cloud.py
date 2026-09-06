import subprocess
import tarfile
from pathlib import Path

KEY_PATH = r"C:\Users\robon\Downloads\ssh-key-2026-09-03.key"
HOST = "opc@130.210.46.184"
REMOTE_DIR = "/home/opc/planwell"

FILES_TO_PACK = [
    "packages/data/python/src/ai_workforce_data/postgres_store.py",
    "packages/agent/python/src/ai_workforce_agent/context.py",
    "apps/backend/src/ai_workforce_backend/knowledge_management.py",
    "apps/backend/src/ai_workforce_backend/app.py",
    "apps/frontend/app/local-management/page.tsx",
]

def deploy():
    tar_path = Path("d:/project/step2_update.tar.gz")
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
        f"{HOST}:{REMOTE_DIR}/step2_update.tar.gz"
    ]
    subprocess.run(scp_cmd, check=True)

    print("Extracting and building on Oracle Cloud VM...")
    remote_script = (
        f"cd {REMOTE_DIR} && "
        "tar -xzf step2_update.tar.gz && "
        "rm -f step2_update.tar.gz && "
        "cd deploy && "
        "sudo docker compose up -d --build backend frontend && "
        "sudo docker compose ps"
    )
    ssh_cmd = [
        "ssh",
        "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        HOST,
        remote_script
    ]
    res = subprocess.run(ssh_cmd, check=True, capture_output=True, text=True)
    print("REMOTE OUTPUT:\n", res.stdout)
    if res.stderr:
        print("REMOTE STDERR:\n", res.stderr)

    if tar_path.exists():
        tar_path.unlink()
    print("Step 2 deployment completed successfully!")

if __name__ == "__main__":
    deploy()
