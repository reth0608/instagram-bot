import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = AsyncOpenAI(api_key=api_key)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")

SYSTEM_PROMPT = """
You are an assistant replying to Instagram DMs.

Rules:
- Reply naturally and conversationally.
- Keep replies reasonably short.
- Be helpful and friendly.
- Do not claim to be the account owner.
- Do not invent facts.
- If you do not know something, say so.
"""


async def generate_reply(message: str) -> str:
    response = await client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=message,
        max_output_tokens=300,
    )

    reply = response.output_text.strip()
    return reply or "Sorry, I couldn't generate a reply right now."
