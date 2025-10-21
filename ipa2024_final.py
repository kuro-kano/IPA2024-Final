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

from restconf_final import create, status, delete, enable, disable
from netmiko_final import gigabit_status 
from ansible_final import showrun

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"
roomIdToGetMessages = os.getenv("ROOM_ID")

try:
    print("Starting...")
    while True:
        time.sleep(1)

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
        message = messages[0]["text"]

        if message.startswith("/66070091 "):
            print(f"\nReceived message: {message}")

            command = message.split(" ")[1]
            print(command)

            if command == "create":
                responseMessage = create()
            elif command == "delete":
                responseMessage = delete()
            elif command == "enable":
                responseMessage = enable()
            elif command == "disable":
                responseMessage = disable()
            elif command == "status":
                responseMessage = status()
            elif command == "gigabit_status":
                responseMessage = gigabit_status()
            elif command == "showrun":
                responseMessage = showrun()
            else:
                responseMessage = "Error: Unknown command."

            print(f"Response Message: {responseMessage}\n")

            if command == "showrun" and responseMessage == "ok":
                filename = "show_run_66070091_CSR1kv.txt"
                fileobject = open(filename, "rb")
                filetype = "text/plain"

                postData = {
                    "roomId": roomIdToGetMessages,
                    "text": "show running config",
                    "files": (filename, fileobject, filetype),
                }
                postData = encoder(postData)

                HTTPHeaders = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": postData.content_type
                }

                r = requests.post(
                    WEBEX_API_URL, data=postData, headers=HTTPHeaders
                )
                fileobject.close()

                if r.status_code != 200:
                    raise Exception(
                        f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                    )

            else:
                postData = {
                    "roomId": roomIdToGetMessages,
                    "text": responseMessage
                }
                postData = json.dumps(postData)

                HTTPHeaders = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": "application/json"
                }

            r = requests.post(WEBEX_API_URL, data=postData, headers=HTTPHeaders)

            if not r.status_code == 200:
                raise Exception(
                    f"Incorrect reply from Webex Teams API. Status code: {r.status_code}"
                )

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
