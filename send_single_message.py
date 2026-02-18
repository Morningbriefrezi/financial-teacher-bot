"""
send_single_message.py
Reads the latest generated lesson and sends it via Telegram Bot API.
Supports sending to private chats, groups, and public channels.
Auto-chunks messages that exceed Telegram's 4096 character limit.
"""

import os
import requests


TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


def send_message(token: str, chat_id: str, text: str, parse_mode: str = "HTML") -> dict:
    """Send a single message via Telegram Bot API."""
    url = TELEGRAM_API.format(token=token, method="sendMessage")
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    response = requests.post(url, json=payload, timeout=30)
    result = response.json()
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")
    return result


def chunk_message(text: str, max_length: int = 4000) -> list[str]:
    """
    Split text into chunks under Telegram's 4096 char limit.
    Splits at paragraph boundaries when possible.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_length:
            current += para + "\n\n"
        else:
            if current:
                chunks.append(current.strip())
            if len(para) > max_length:
                for i in range(0, len(para), max_length):
                    chunks.append(para[i:i + max_length])
                current = ""
            else:
                current = para + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks


def format_lesson_for_telegram(text: str) -> str:
    """
    Apply basic HTML formatting so section headers stand out in Telegram.
    """
    import re
    # Bold numbered section headers e.g. "1. HEADLINE"
    text = re.sub(
        r'^(\d+\.\s+[A-Z &]+)$',
        r'<b>\1</b>',
        text,
        flags=re.MULTILINE
    )
    # Bold ALL-CAPS standalone lines (unnumbered headers)
    text = re.sub(
        r'^([A-Z][A-Z\s&]{4,})$',
        r'<b>\1</b>',
        text,
        flags=re.MULTILINE
    )
    return text


def send_lesson():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_ids_raw = os.environ["TELEGRAM_CHAT_IDS"]  # comma-separated

    chat_ids = [cid.strip() for cid in chat_ids_raw.split(",") if cid.strip()]

    lesson_path = "latest_lesson.txt"
    if not os.path.exists(lesson_path):
        print(f"ERROR: {lesson_path} not found. Run financial_lesson_generator.py first.")
        return

    with open(lesson_path, "r", encoding="utf-8") as f:
        raw_lesson = f.read()

    lesson = format_lesson_for_telegram(raw_lesson)
    chunks = chunk_message(lesson)
    total = len(chunks)

    print(f"Sending {total} message(s) to {len(chat_ids)} chat(s)...")

    for chat_id in chat_ids:
        for i, chunk in enumerate(chunks, 1):
            prefix = f"<b>[{i}/{total}]</b>\n\n" if total > 1 else ""
            send_message(token, chat_id, prefix + chunk)
            print(f"  Sent to {chat_id} [{i}/{total}]")

    print("Done.")


if __name__ == "__main__":
    send_lesson()
