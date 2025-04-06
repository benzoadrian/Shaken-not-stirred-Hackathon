import json
import requests
import os

VERIFY_TOKEN = "theverifying"
WHATSAPP_TOKEN = "EAAkGYV0KptkBO7g9bxdBtL2Mp0YfdNGEmowDes631dTbd38rSvNUMwXIDu9YMfwE1OO9HyvaGueXD7Bjf7fj55y7c448S16NYr9ToQLtv4i60yFrzIJYddu6Nx4ek3C5LbVqAWn7eYuRymI2RhLel8L0kyvZCZBHD0BJcpALcxG7lYQIlKH6g7duqSgEjlBiMsZCuxBB3oDMoeJeIRKZCOfstVMSjLMSgvgZD"
PHONE_NUMBER_ID = "591899364010894"  # e.g., 591899364010894

def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    print(f"🔧 Received {event} request")
    
    if method == "GET":
        params = event.get("queryStringParameters") or {}
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return {
                "statusCode": 200,
                "body": challenge
            }
        else:
            return {
                "statusCode": 403,
                "body": "Verification token mismatch"
            }

    elif method == "POST":
        try:
            body = json.loads(event.get("body", "{}"))
            print("📩 Webhook Received:", json.dumps(body, indent=2))

            if 'entry' in body:
                for entry in body['entry']:
                    changes = entry.get('changes', [])
                    for change in changes:
                        value = change.get('value', {})
                        messages = value.get('messages', [])

                        for message in messages:
                            sender_id = message['from']
                            text = message['text']['body'] if message.get('text') else None
                            print(text)
                            send_to_scraper(sender_id, text)
                            
            

        except Exception as e:
            print("❌ Error processing webhook:", e)

        return {
            "statusCode": 200,
            "body": "EVENT_RECEIVED"
        }

    return {
        "statusCode": 405,
        "body": "Method not allowed"
    }


def send_to_scraper(sender, message_text):
    url = f"http://34.211.49.107:5000/receive"
    headers = {
        "Authorization": f"",
        "Content-Type": "application/json"
    }
    payload = {
        "message": message_text,
        "sender": sender
    }

    response = requests.post(url, headers=headers, params=payload)
    print(f"📤 Sent message to {payload}")
    try:
        print(response.json())
    except Exception:
        print("❗ Response not JSON")