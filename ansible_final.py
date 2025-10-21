import os
import subprocess
import tempfile
from pathlib import Path


def showrun():
    STUDENT_ID  = "66070091"
    ROUTER_NAME = "CSR1kv"
    PLAYBOOK    = "ansible/playbook_showrun.yaml"

    ansible_user = "admin"
    ansible_pass = "cisco"
    enable_pass  = ""

    target_ip = "10.0.15.61"

    inv_lines = [
        "[routers]",
        (f"{ROUTER_NAME} ansible_host={target_ip} "
         f"ansible_user={ansible_user} ansible_password={ansible_pass} "
         f"ansible_network_os=ios").strip()
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

    extra_vars = f"student_id={STUDENT_ID} router_name={ROUTER_NAME}"

    cmd = [
        "ansible-playbook",
        "-i", str(inventory),
        "--ssh-common-args", ssh_common_args,
        "-e", "ansible_connection=network_cli",
        "-e", extra_vars,
        PLAYBOOK,
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=180)
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    print(output)

    if "ok=2" in output and "failed=0" in output:
        tmpdir.cleanup()
        return "ok"
    else:
        tmpdir.cleanup()

if __name__ == "__main__":
    result = showrun()
    print(result)
