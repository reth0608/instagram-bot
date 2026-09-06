import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
API_VERSION = os.getenv("INSTAGRAM_API_VERSION", "v23.0")


async def send_instagram_message(recipient_id: str, message: str):
    if not ACCESS_TOKEN:
        raise RuntimeError("INSTAGRAM_ACCESS_TOKEN is not set")

    url = f"https://graph.facebook.com/{API_VERSION}/me/messages"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        print("Instagram API error:", response.text)

    response.raise_for_status()
    return response.json()
