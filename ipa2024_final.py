"""Main program to interact with Webex Teams API and execute commands."""

#######################################################################################
# Yourname: Thanya Woramongkol
# Your student ID: 66070091
# Your GitHub Repo: https://github.com/kuro-kano/IPA2024-Final
#######################################################################################

from dotenv import load_dotenv
import os
import time
import requests

from functions.webex_input_format import format_check
from functions.webex_sent_message import post_to_webex
from functions.command_execute import restconf_command, netconf_command, netmiko_command, ansible_command

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"
roomIdToGetMessages = os.getenv("ROOM_ID")

last_message_id = None
method = ""

VALID_METHODS = ("restconf", "netconf")
REQUIRED_COMMANDS = ("create", "delete", "enable", "disable", "status")
OTHER_COMMANDS = ("gigabit_status", "showrun")

try:
    print("Starting...")
    while True:
        time.sleep(0.01)

        # Fetch latest message from Webex
        getParameters = {"roomId": roomIdToGetMessages, "max": 1}
        getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        r = requests.get(WEBEX_API_URL, params=getParameters, headers=getHTTPHeader)

        if r.status_code != 200:
            raise Exception(
                f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
            )

        json_data = r.json()
        if len(json_data["items"]) == 0:
            raise Exception("There are no messages in the room.")

        latest = json_data["items"][0]

        # Only process new messages
        if latest["id"] == last_message_id:
            continue
        last_message_id = latest["id"]

        message = latest.get("text", "") or ""
        if not message.startswith("/66070091 "):
            continue

        print(f"\nReceived message: {message}")
        command = message.split(" ")
        responseMessage = ""

        # Special handling for MOTD with text
        if len(command) >= 3 and command[2] == "motd":
            host_ip = command[1]
            motd_message = message.partition(" motd ")[2].strip()
            if motd_message:
                responseMessage = ansible_command(host_ip, "motd", motd_message)
            else:
                responseMessage = ansible_command(host_ip, "motd")
            print(f"Response Message: {responseMessage}\n")
            r = post_to_webex(responseMessage)
            if r.status_code != 200:
                raise Exception(f"Incorrect reply from Webex Teams API. Status code: {r.status_code}")
            continue

        method_invalid_and_invalid_format = command[1] in VALID_METHODS or (command[1] in REQUIRED_COMMANDS and method == "")

        if len(command) == 2 and method_invalid_and_invalid_format:
            # Method selection: /66070091 restconf|netconf
            if command[1] in VALID_METHODS:
                method = command[1]
                responseMessage = f"ok: Using {method.upper()} method."
            # Invalid method selection
            elif command[1] in REQUIRED_COMMANDS and method == "":
                responseMessage = "Error: Invalid method specified."
            print(f"Response message: {responseMessage}\n")
            r = post_to_webex(responseMessage)
            if r.status_code != 200:
                raise Exception(
                    f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                )
            continue

        # Parse structured commands
        result = format_check(command)
        if isinstance(result, str):
            responseMessage = result
        elif not result:
            responseMessage = "Error: Invalid command format."
        else:
            host_ip, command = result
            print(f"command: {command}, host: {host_ip}")

            # Commands that require a method
            if command in REQUIRED_COMMANDS:
                if not method:
                    responseMessage = "Error: No method specified."
                else:
                    if method == "restconf":
                        responseMessage = restconf_command(host_ip, command)
                    elif method == "netconf":
                        responseMessage = netconf_command(host_ip, command)

            # Other commands (no method required)
            elif command in OTHER_COMMANDS:
                if command == "gigabit_status":
                    responseMessage = netmiko_command(host_ip, command)
                elif command == "showrun":
                    responseMessage = ansible_command(host_ip, command)
            else:
                responseMessage = "Error: Unknown command."

        print(f"Response message: {responseMessage}\n")

        # Send response (attach file for showrun if success)
        if command == "showrun" and responseMessage == "ok":
            filename = "show_run_66070091_CSR1kv.txt"
            r = post_to_webex(
                "show running config",
                file_path=filename,
                filename=filename,
                filetype="text/plain",
            )
        else:
            r = post_to_webex(responseMessage)

        if r.status_code != 200:
            raise Exception(
                f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
            )

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
