"""Module to manage Loopback66070091 interface via RESTCONF API."""

import json
import requests

requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

basicauth = ("admin", "cisco")


def create(host_ip):
    """Create Loopback66070091 interface."""
    # First, check if interface already exists
    api_url_check = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070091"
    
    try:
        # Check if interface exists
        check_resp = requests.get(
            api_url_check,
            auth=basicauth,
            headers=headers,
            verify=False,
        )
        
        if check_resp.status_code == 200:
            print("Interface already exists")
            return "Error: Interface Loopback66070091 already existed"
        
        # If interface doesn't exist (404), proceed to create it
        api_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070091"
        yangConfig = {
            "ietf-interfaces:interface": {
                "name": "Loopback66070091",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [{"ip": "172.0.91.1", "netmask": "255.255.255.0"}]
                },
            }
        }

        resp = requests.put(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False,
        )

        if resp.status_code >= 200 and resp.status_code <= 299:
            print(f"STATUS OK: {resp.status_code}")
            return "Interface Loopback66070091 is created successfully"
        else:
            print(f"Error. Status Code: {resp.status_code}")
            return "Error: Cannot create Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def delete(host_ip):
    """Delete Loopback66070091 interface."""
    api_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070091"
    try:
        resp = requests.delete(
            api_url,
            auth=basicauth,
            headers=headers,
            verify=False,
        )

        if resp.status_code >= 200 and resp.status_code <= 299:
            print(f"STATUS OK: {resp.status_code}")
            return "Interface Loopback66070091 is deleted successfully"
        else:
            print(f"Error. Status Code: {resp.status_code}")
            return "Cannot delete: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def enable(host_ip):
    """Enable Loopback66070091 interface."""
    api_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070091"
    yangConfig = {
        "ietf-interfaces:interface": {"name": "Loopback66070091", "enabled": True}
    }

    try:
        resp = requests.patch(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False,
        )

        if resp.status_code >= 200 and resp.status_code <= 299:
            print(f"STATUS OK: {resp.status_code}")
            return "Interface Loopback66070091 is enabled successfully"
        else:
            print(f"Error. Status Code: {resp.status_code}")
            return "Cannot enable: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def disable(host_ip):
    """Disable Loopback66070091 interface."""
    api_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070091"
    yangConfig = {
        "ietf-interfaces:interface": {"name": "Loopback66070091", "enabled": False}
    }

    try:
        resp = requests.patch(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False,
        )

        if resp.status_code >= 200 and resp.status_code <= 299:
            print(f"STATUS OK: {resp.status_code}")
            return "Interface Loopback66070091 is disabled successfully"
        else:
            print(f"Error. Status Code: {resp.status_code}")
            return "Cannot disable: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def status(host_ip):
    """Get status of Loopback66070091 interface."""
    api_url_status = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070091"
    try:
        resp = requests.get(
            api_url_status,
            auth=basicauth,
            headers=headers,
            verify=False,
        )

        if resp.status_code >= 200 and resp.status_code <= 299:
            print(f"STATUS OK: {resp.status_code}")

            response_json = resp.json()
            admin_status = response_json.get("ietf-interfaces:interface", {}).get(
                "admin-status", ""
            )
            oper_status = response_json.get("ietf-interfaces:interface", {}).get(
                "oper-status", ""
            )

            if admin_status == "up" and oper_status == "up":
                return "Interface Loopback66070091, Status: Enabled"
            elif admin_status == "down" and oper_status == "down":
                return "Interface Loopback66070091, Status: Disabled"
            else:
                return f"Interface Loopback66070091, Admin: {admin_status}, Oper: {oper_status}"

        elif resp.status_code == 404:
            print(f"STATUS NOT FOUND: {resp.status_code}")
            return "Error: No Interface Loopback66070091"
        else:
            print(f"Error. Status Code: {resp.status_code}")
            return "Cannot retrieve status: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"
