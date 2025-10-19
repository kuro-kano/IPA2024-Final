import subprocess
import os

def showrun():
    project_root = os.path.dirname(__file__)
    env = os.environ.copy()
    env["ANSIBLE_CONFIG"] = os.path.join(project_root, "ansible", "ansible.cfg")

    command = [
        "ansible-playbook",
        "-i", "ansible/hosts",
        "ansible/playbook.yaml"
    ]

    result = subprocess.run(command, capture_output=True, text=True, env=env, cwd=project_root)
    output = (result.stdout or "") + (result.stderr or "")
    print(f"Ansible error output: {output}")

    out_file = os.path.join(project_root, "show_run_66070091_CSR1kv.txt")
    if result.returncode != 0 or not os.path.exists(out_file):
        return "Error: Ansible"

    return "ok"
