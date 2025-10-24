"""Run Ansible playbook to get `show running-config` from a router."""

import os
import subprocess
import tempfile
from pathlib import Path
import time


def showrun(host_ip):
    """Get running-config from router via Ansible playbook."""
    PLAYBOOK = "ansible/playbook-showrun.yaml"

    ansible_user = "admin"
    ansible_pass = "cisco"
    enable_pass = ""

    target_ip = host_ip

    inv_lines = [
        "[routers]",
        (
            f"CSR1kv ansible_host={target_ip} "
            f"ansible_user={ansible_user} ansible_password={ansible_pass} "
            f"ansible_network_os=ios"
        ).strip(),
    ]
    if enable_pass:
        inv_lines += [
            "[routers:vars]",
            "ansible_become=True",
            "ansible_become_method=enable",
            f"ansible_become_password={enable_pass}",
        ]
    tmpdir = tempfile.TemporaryDirectory()
    inventory = Path(tmpdir.name) / "inventory.ini"
    inventory.write_text("\n".join(inv_lines) + "\n", encoding="utf-8")

    ssh_common_args = (
        "-oKexAlgorithms=+diffie-hellman-group14-sha1 "
        "-oHostKeyAlgorithms=+ssh-rsa "
        "-oPubkeyAcceptedAlgorithms=+ssh-rsa "
        "-oStrictHostKeyChecking=no"
    )

    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

    cmd = [
        "ansible-playbook",
        "-i",
        str(inventory),
        "--ssh-common-args",
        ssh_common_args,
        "-e",
        "ansible_connection=network_cli",
        PLAYBOOK,
    ]

    while True:
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, env=env, timeout=180
            )
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            print(output)

            if "ok=2" in output and "failed=0" in output:
                tmpdir.cleanup()
                return "ok"

            if ("timed out" in output) or ("No existing session" in output):
                print("[showrun] Retryable error -> retry in 2s ...")
                time.sleep(2)
                continue

            print("[showrun] Non-retryable failure from Ansible.")
            tmpdir.cleanup()
            return None

        except subprocess.TimeoutExpired:
            print("[showrun] ansible-playbook process timeout -> retry in 2s ...")
            time.sleep(2)
            continue
        except Exception as e:
            print(f"[showrun] Unexpected error: {e}")
            tmpdir.cleanup()
            return None
