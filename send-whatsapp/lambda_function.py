import json
import requests
import os

VERIFY_TOKEN = "theverifying"
WHATSAPP_TOKEN = "EAAkGYV0KptkBO7g9bxdBtL2Mp0YfdNGEmowDes631dTbd38rSvNUMwXIDu9YMfwE1OO9HyvaGueXD7Bjf7fj55y7c448S16NYr9ToQLtv4i60yFrzIJYddu6Nx4ek3C5LbVqAWn7eYuRymI2RhLel8L0kyvZCZBHD0BJcpALcxG7lYQIlKH6g7duqSgEjlBiMsZCuxBB3oDMoeJeIRKZCOfstVMSjLMSgvgZD"
PHONE_NUMBER_ID = "591899364010894"  # e.g., 591899364010894

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    print(body)
    send_whatsapp_message(body["sender"], body["message"])


def send_whatsapp_message(to_number, message_text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"📤 Sent message to {to_number}. Status code: {response.status_code}")
    try:
        print(response.json())
    except Exception:
        print("❗ Response not JSON")