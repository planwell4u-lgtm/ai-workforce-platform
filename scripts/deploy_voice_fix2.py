"""Deploy second voice fix (uuid import) to Oracle Cloud server."""
import subprocess
import tarfile
from pathlib import Path

KEY_PATH = r"C:\Users\robon\Downloads\ssh-key-2026-09-03.key"
HOST = "opc@130.210.46.184"
REMOTE_DIR = "/home/opc/planwell"

FILES_TO_PACK = [
    "packages/data/python/src/ai_workforce_data/postgres_store.py",
]

def deploy():
    tar_path = Path("d:/project/voice_fix2.tar.gz")
    print(f"Creating archive {tar_path}...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in FILES_TO_PACK:
            local_f = Path("d:/project") / f
            print(f"  Packing {f}")
            tar.add(local_f, arcname=f)

    print("Uploading archive via scp...")
    scp_cmd = [
        "scp",
        "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        "-o", "IdentitiesOnly=yes",
        str(tar_path),
        f"{HOST}:{REMOTE_DIR}/voice_fix2.tar.gz"
    ]
    subprocess.run(scp_cmd, check=True)

    print("Extracting and rebuilding backend on Oracle Cloud VM...")
    remote_script = (
        f"cd {REMOTE_DIR} && "
        "tar -xzf voice_fix2.tar.gz && "
        "rm -f voice_fix2.tar.gz && "
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml up --build -d --force-recreate backend && "
        "sleep 8 && "
        "curl -s --max-time 10 --resolve planwell.online:443:127.0.0.1 https://planwell.online/api/healthz && "
        "echo '' && echo '--- Testing voice endpoint ---' && "
        "curl -s --max-time 15 --resolve planwell.online:443:127.0.0.1 "
        "-X POST https://planwell.online/api/v1/channels/voice/public-test-dial "
        "-H 'Content-Type: application/json' "
        "-d '{\"to_number\":\"+12402159529\",\"greeting\":\"Test call from fixed backend\"}'"
    )
    ssh_cmd = [
        "ssh",
        "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no",
        "-o", "IdentitiesOnly=yes",
        HOST,
        remote_script
    ]
    subprocess.run(ssh_cmd, check=True)

    if tar_path.exists():
        tar_path.unlink()
    print("\n[SUCCESS] Voice fix 2 deployed!")

if __name__ == "__main__":
    deploy()
