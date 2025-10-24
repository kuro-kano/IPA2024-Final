"""Main program to interact with Webex Teams API and execute commands."""

#######################################################################################
# Yourname: Thanya Woramongkol
# Your student ID: 66070091
# Your GitHub Repo: https://github.com/kuro-kano/IPA2024-Final
#######################################################################################

import requests
import json
import time
import os

from requests_toolbelt.multipart.encoder import MultipartEncoder as encoder
from dotenv import load_dotenv

import netconf_final as netconf
import restconf_final as restconf

from netmiko_final import gigabit_status
from ansible_final import showrun

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"
roomIdToGetMessages = os.getenv("ROOM_ID")

last_message_id = None

# RESTCONF or NETCONF
method = ""
host_ip = ""

def post_to_webex(text, file_path=None, filename=None, filetype="text/plain"):
    """Post a message or a file to the configured Webex room."""
    if file_path:
        fileobject = open(file_path, "rb")
        postData = {
            "roomId": roomIdToGetMessages,
            "text": text,
            "files": (filename or os.path.basename(file_path), fileobject, filetype),
        }
        multipart = encoder(postData)
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": multipart.content_type,
        }
        r = requests.post(WEBEX_API_URL, data=multipart, headers=headers)
        fileobject.close()
    else:
        postData = {"roomId": roomIdToGetMessages, "text": text}
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        r = requests.post(WEBEX_API_URL, data=json.dumps(postData), headers=headers)
    return r

try:
    print("Starting...")
    while True:
        time.sleep(0.5)

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
            print(command)

            if method == "" and len(command) == 2:
                command = command[1]
                if command == "restconf":
                    method = "restconf"
                    responseMessage = "ok: Using RESTCONF method."
                elif command == "netconf":
                    method = "netconf"
                    responseMessage = "ok: Using NETCONF method."
                else:
                    responseMessage = "Error: No method specified."
            else:
                if len(command) != 3:
                    responseMessage = "Error: Invalid command format."
                else:
                    host_ip = command[1]
                    command = command[2]

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
                        elif command == "gigabit_status":
                            responseMessage = gigabit_status()
                        elif command == "showrun":
                            responseMessage = showrun()
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
                        elif command == "gigabit_status":
                            responseMessage = gigabit_status()
                        elif command == "showrun":
                            responseMessage = showrun()
                        else:
                            responseMessage = "Error: Unknown command."

            print(f"Response Message: {responseMessage}\n")

            if command == "showrun" and responseMessage == "ok":
                filename = "show_run_66070091_CSR1kv.txt"
                r = post_to_webex("show running config", file_path=filename, filename=filename, filetype="text/plain")
                if r.status_code != 200:
                    raise Exception(
                        f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                    )
                continue
            else:
                r = post_to_webex(responseMessage)
                if not r.status_code == 200:
                    raise Exception(
                        f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                    )

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
