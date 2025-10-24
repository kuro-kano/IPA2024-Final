"""Main program to interact with Webex Teams API and execute commands."""

#######################################################################################
# Yourname: Thanya Woramongkol
# Your student ID: 66070091
# Your GitHub Repo: https://github.com/kuro-kano/IPA2024-Final
#######################################################################################

import requests
import time
import os

from dotenv import load_dotenv

import netconf_final as netconf
import restconf_final as restconf

from functions.webex_input_format import format_check
from functions.webex_sent_message import post_to_webex
from netmiko_final import gigabit_status, read_motd
from ansible_final import showrun, conf_motd

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"
roomIdToGetMessages = os.getenv("ROOM_ID")

last_message_id = None

# RESTCONF or NETCONF
valid_method = ("restconf", "netconf")

method_required_command = ("create", "delete", "enable", "disable", "status")
other_commands = ("showrun", "gigabit_status", "motd")

method = ""

try:
    print("Starting...")
    while True:
        time.sleep(0.1)

        getParameters = {"roomId": roomIdToGetMessages, "max": 1}
        getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

        r = requests.get(WEBEX_API_URL, params=getParameters, headers=getHTTPHeader)

        if not r.status_code == 200:
            raise Exception(
                f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
            )

        json_data = r.json()

        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")

        messages = json_data["items"]
        latest = messages[0]

        if latest["id"] == last_message_id:
            continue
        last_message_id = latest["id"]
        message = latest.get("text", "") or ""

        if message.startswith("/66070091 "):
            print(f"\nReceived message: {message}")

            command = message.split(" ")

            if len(command) == 2 and command[1] in valid_method:
                command_method = command[1]
                if command_method == "restconf":
                    method = "restconf"
                    responseMessage = "ok: Using RESTCONF method."
                elif command_method == "netconf":
                    method = "netconf"
                    responseMessage = "ok: Using NETCONF method."
                else:
                    responseMessage = "Error: No method specified."
            # elif command[1] in other_commands:
            else:
                if method == "":
                    responseMessage = "Error: No method specified."
                else:
                    # Check command format
                    result = format_check(command)
                    if isinstance(result, str):
                        # It's an error message
                        responseMessage = result
                    else:
                        # It's a tuple (ip, command)
                        host_ip, command, motd_message = result
                        print(command)

                        if command in method_required_command:
                            if method == "restconf":
                                if command == "create":
                                    responseMessage = restconf.create(host_ip)
                                elif command == "delete":
                                    responseMessage = restconf.delete(host_ip)
                                elif command == "enable":
                                    responseMessage = restconf.enable(host_ip)
                                elif command == "disable":
                                    responseMessage = restconf.disable(host_ip)
                                elif command == "status":
                                    responseMessage = restconf.status(host_ip)
                                else:
                                    responseMessage = "Error: Unknown command."
                            elif method == "netconf":
                                if command == "create":
                                    responseMessage = netconf.create(host_ip)
                                elif command == "delete":
                                    responseMessage = netconf.delete(host_ip)
                                elif command == "enable":
                                    responseMessage = netconf.enable(host_ip)
                                elif command == "disable":
                                    responseMessage = netconf.disable(host_ip)
                                elif command == "status":
                                    responseMessage = netconf.status(host_ip)
                                else:
                                    responseMessage = "Error: Unknown command."
                            else:
                                responseMessage = "Error: No method specified."

                        elif command == "gigabit_status":
                            responseMessage = gigabit_status(host_ip)
                        elif command == "showrun":
                            responseMessage = showrun(host_ip)
                        elif command == "motd":
                            if motd_message == "":
                                responseMessage = read_motd(host_ip)
                            else:
                                responseMessage = conf_motd(host_ip, motd_message)
                            

            print(f"Response Message: {responseMessage}\n")

            if command == "showrun" and responseMessage == "ok":
                filename = "show_run_66070091_CSR1kv.txt"
                r = post_to_webex("show running config", file_path=filename, filename=filename, filetype="text/plain")
                if r.status_code != 200:
                    raise Exception(
                        f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                    )
            else:
                r = post_to_webex(responseMessage)
                if not r.status_code == 200:
                    raise Exception(
                        f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                    )

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
