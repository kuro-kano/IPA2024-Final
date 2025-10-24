"""Command execution handler for each command type."""

import restconf_final as restconf
import netconf_final as netconf
from netmiko_final import gigabit_status, read_motd
from ansible_final import showrun, conf_motd

def restconf_command(host_ip, command):
    """Execute RESTCONF commands."""
    if command == "create":
        return restconf.create(host_ip)
    elif command == "delete":
        return restconf.delete(host_ip)
    elif command == "enable":
        return restconf.enable(host_ip)
    elif command == "disable":
        return restconf.disable(host_ip)
    elif command == "status":
        return restconf.status(host_ip)
    else:
        return "Error: Unknown command."

def netconf_command(host_ip, command):
    """Execute NETCONF commands."""
    if command == "create":
        return netconf.create(host_ip)
    elif command == "delete":
        return netconf.delete(host_ip)
    elif command == "enable":
        return netconf.enable(host_ip)
    elif command == "disable":
        return netconf.disable(host_ip)
    elif command == "status":
        return netconf.status(host_ip)
    else:
        return "Error: Unknown command."

def netmiko_command(host_ip, command):
    """Execute Netmiko commands."""
    if command == "gigabit_status":
        return gigabit_status(host_ip)
    elif command == "motd":
        return read_motd(host_ip)
    else:
        return "Error: Unknown command."

def ansible_command(host_ip, command, motd_message=""):
    """Execute Ansible commands."""
    if command == "showrun":
        return showrun(host_ip)
    elif command == "motd":
        if motd_message != "":
            return conf_motd(host_ip, motd_message)
        else:
            return read_motd(host_ip)
    else:
        return "Error: Unknown command."
