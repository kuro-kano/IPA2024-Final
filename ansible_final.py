"""Run Ansible playbook to get `show running-config` from a router."""

import os
import subprocess
import tempfile
from pathlib import Path
import time
from typing import Optional, Dict, Callable


def _create_inventory(tmpdir: Path, host_ip: str, ansible_user: str = "admin",
                     ansible_pass: str = "cisco", enable_pass: str = "") -> Path:
    """Create Ansible inventory file."""
    inv_lines = [
        "[routers]",
        (
            f"CSR1kv ansible_host={host_ip} "
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
    
    inventory = tmpdir / "inventory.ini"
    inventory.write_text("\n".join(inv_lines) + "\n", encoding="utf-8")
    return inventory


def _get_ssh_common_args() -> str:
    """Get SSH common arguments for Ansible."""
    return (
        "-oKexAlgorithms=+diffie-hellman-group14-sha1 "
        "-oHostKeyAlgorithms=+ssh-rsa "
        "-oPubkeyAcceptedAlgorithms=+ssh-rsa "
        "-oStrictHostKeyChecking=no"
    )


def _get_ansible_env() -> Dict[str, str]:
    """Get environment variables for Ansible."""
    env = os.environ.copy()
    env["ANSIBLE_HOST_KEY_CHECKING"] = "False"
    return env


def _is_retryable_error(output: str) -> bool:
    """Check if error is retryable."""
    return ("timed out" in output) or ("No existing session" in output)


def _run_playbook(host_ip: str, playbook: str, extra_vars: Optional[Dict[str, str]] = None,
                 success_check: Callable = None, operation_name: str = "operation",
                 ansible_user: str = "admin", ansible_pass: str = "cisco", 
                 enable_pass: str = "") -> Optional[str]:
    """
    Run Ansible playbook with retry logic.
    
    Args:
        host_ip: Target host IP address
        playbook: Path to playbook file
        extra_vars: Dictionary of extra variables to pass
        success_check: Function to check if operation succeeded (proc, output) -> bool
        operation_name: Name of operation for logging
        ansible_user: Ansible username
        ansible_pass: Ansible password
        enable_pass: Enable password
        
    Returns:
        Success message or error message/None
    """
    tmpdir = tempfile.TemporaryDirectory()
    
    try:
        tmpdir_path = Path(tmpdir.name)
        inventory = _create_inventory(tmpdir_path, host_ip, ansible_user, 
                                      ansible_pass, enable_pass)
        
        cmd = [
            "ansible-playbook",
            "-i", str(inventory),
            "--ssh-common-args", _get_ssh_common_args(),
            "-e", "ansible_connection=network_cli",
        ]
        
        # Add extra vars if provided
        if extra_vars:
            extra_vars_path = tmpdir_path / "extra_vars.yaml"
            vars_content = "\n".join([
                f'{k}: "{v.replace(chr(34), chr(92) + chr(34))}"' 
                for k, v in extra_vars.items()
            ])
            extra_vars_path.write_text(vars_content + "\n", encoding="utf-8")
            cmd.extend(["-e", f"@{extra_vars_path}"])
        
        cmd.append(playbook)
        
        while True:
            try:
                proc = subprocess.run(
                    cmd, capture_output=True, text=True, 
                    env=_get_ansible_env(), timeout=180
                )
                output = (proc.stdout or "") + "\n" + (proc.stderr or "")
                print(output)
                
                # Check success
                if success_check and success_check(proc, output):
                    return "ok" if operation_name == "showrun" else "Ok: success"
                
                # Check for retryable errors
                if _is_retryable_error(output):
                    print(f"[{operation_name}] Retryable error -> retry in 2s ...")
                    time.sleep(2)
                    continue
                
                # Non-retryable failure
                print(f"[{operation_name}] Non-retryable failure from Ansible.")
                return None if operation_name == "showrun" else \
                       f"Error: Cannot configure {operation_name} (checked via Ansible)"
            
            except subprocess.TimeoutExpired:
                print(f"[{operation_name}] ansible-playbook process timeout -> retry in 2s ...")
                time.sleep(2)
                continue
                
            except Exception as e:
                print(f"[{operation_name}] Unexpected error: {e}")
                return None if operation_name == "showrun" else \
                       f"Error: Cannot connect to router {host_ip} - {str(e)}"
    
    finally:
        tmpdir.cleanup()


def showrun(host_ip: str) -> Optional[str]:
    """Get running-config from router via Ansible playbook."""
    
    def check_success(proc, output):
        return "ok=2" in output and "failed=0" in output
    
    return _run_playbook(
        host_ip=host_ip,
        playbook="ansible/playbook-showrun.yaml",
        success_check=check_success,
        operation_name="showrun"
    )


def conf_motd(host_ip: str, motd_message: str) -> str:
    """Configure MOTD banner on router via Ansible playbook."""
    
    def check_success(proc, output):
        return proc.returncode == 0 and "failed=0" in output
    
    return _run_playbook(
        host_ip=host_ip,
        playbook="ansible/playbook-motd.yaml",
        extra_vars={"motd_text": motd_message},
        success_check=check_success,
        operation_name="conf_motd"
    )