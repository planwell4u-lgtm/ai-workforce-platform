"""Deploy TwiML double-declaration fix to Oracle Cloud."""
import subprocess, tarfile, os
from pathlib import Path

KEY_PATH = r"C:\Users\robon\Downloads\ssh-key-2026-09-03.key"
HOST = "opc@130.210.46.184"
REMOTE_DIR = "/home/opc/planwell"

FILES_TO_PACK = [
    "packages/digital_channel/python/src/ai_workforce_digital_channel/voice_adapter.py",
    "apps/backend/src/ai_workforce_backend/voice_management.py",
]

def deploy():
    tar_path = Path("d:/project/voice_fix3.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in FILES_TO_PACK:
            tar.add(Path("d:/project") / f, arcname=f)
            print(f"  Packed: {f}")

    print("Uploading via SCP...")
    subprocess.run([
        "scp", "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no", "-o", "IdentitiesOnly=yes",
        str(tar_path), f"{HOST}:{REMOTE_DIR}/voice_fix3.tar.gz"
    ], check=True)

    print("Rebuilding backend on server...")
    remote_script = "\n".join([
        f"cd {REMOTE_DIR}",
        "tar -xzf voice_fix3.tar.gz",
        "rm -f voice_fix3.tar.gz",
        "sudo docker compose --env-file .env -f deploy/docker-compose.yml up --build -d --force-recreate backend",
        "sleep 8",
        "echo '--- TwiML test ---'",
        "curl -s --max-time 10 --resolve planwell.online:443:127.0.0.1 "
        "-X POST https://planwell.online/api/v1/channels/voice/incoming "
        "-H 'Content-Type: application/x-www-form-urlencoded' "
        "-d 'From=%2B12402159529&To=%2B12406798305&CallSid=test999'",
    ])
    subprocess.run([
        "ssh", "-i", KEY_PATH,
        "-o", "StrictHostKeyChecking=no", "-o", "IdentitiesOnly=yes",
        HOST, remote_script
    ], check=True)

    tar_path.unlink(missing_ok=True)
    print("\n[SUCCESS] Deployed!")

if __name__ == "__main__":
    deploy()
