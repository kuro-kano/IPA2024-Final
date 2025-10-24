
import requests
import json
import time
import os

from requests_toolbelt.multipart.encoder import MultipartEncoder as encoder
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"
roomIdToGetMessages = os.getenv("ROOM_ID")

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
