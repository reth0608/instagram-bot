import os
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

from app.openai_client import generate_reply
from app.instagram import send_instagram_message

load_dotenv()

app = FastAPI(title="Instagram AI DM Bot")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


@app.get("/")
async def root():
    return {"status": "online", "service": "Instagram AI DM Bot"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def instagram_webhook(request: Request):
    body = await request.json()
    print("Incoming webhook:", body)

    if body.get("object") != "instagram":
        return {"status": "ignored"}

    try:
        for entry in body.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event.get("sender", {}).get("id")
                message = event.get("message", {})

                if not sender_id or not message:
                    continue

                text = message.get("text")
                if not text:
                    continue

                # Ignore messages produced by the bot itself.
                if message.get("is_echo"):
                    continue

                print(f"Instagram DM from {sender_id}: {text}")

                reply = await generate_reply(text)
                print(f"AI reply: {reply}")

                await send_instagram_message(sender_id, reply)

        return {"status": "ok"}

    except Exception as exc:
        print("Webhook error:", repr(exc))
        return {"status": "error"}
