"""Connect to a CSR1000v and get GigabitEthernet interface status"""

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException
from pprint import pprint
import time

username = "admin"
password = "cisco"


def gigabit_status(device_ip):
    """Get GigabitEthernet interface status repeatedly until successful."""
    device_params = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
    }

    ans = ""
    while True:
        try:
            with ConnectHandler(**device_params) as ssh:
                up = 0
                down = 0
                admin_down = 0
                result = ssh.send_command("show ip interface brief", use_textfsm=True)

                status_list = []

                for status in result:
                    if status["interface"].startswith("GigabitEthernet"):
                        interface_name = status["interface"]
                        interface_status = status["status"]
                        status_list.append(f"{interface_name} {interface_status}")

                        if interface_status == "up":
                            up += 1
                        elif interface_status == "down":
                            down += 1
                        elif interface_status == "administratively down":
                            admin_down += 1

                ans = f"{', '.join(status_list)} -> {up} up, {down} down, {admin_down} administratively down"
                pprint(ans)
                return ans
        except NetmikoTimeoutException:
            pprint("Connection timeout - retrying in 2 seconds ...")
            time.sleep(2)
