"""
send_single_message.py
Reads the latest generated lesson and sends it via Twilio WhatsApp.
Supports multiple recipients via comma-separated RECIPIENT_NUMBERS env var.
"""

import os
from twilio.rest import Client


def chunk_message(text: str, max_length: int = 1500) -> list[str]:
    """
    WhatsApp messages have a 4096 char limit, but we chunk at 1500
    for readability. Splits at paragraph boundaries when possible.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_length:
            current_chunk += (para + "\n\n") if current_chunk else para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            # If a single paragraph is too long, force split
            if len(para) > max_length:
                for i in range(0, len(para), max_length):
                    chunks.append(para[i:i + max_length])
                current_chunk = ""
            else:
                current_chunk = para + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def send_lesson():
    # Load credentials
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    from_number = os.environ["TWILIO_WHATSAPP_FROM"]  # e.g. "whatsapp:+14155238886"
    recipients_raw = os.environ["RECIPIENT_NUMBERS"]  # e.g. "+1234567890,+0987654321"

    recipients = [
        f"whatsapp:{num.strip()}" if not num.strip().startswith("whatsapp:") else num.strip()
        for num in recipients_raw.split(",")
        if num.strip()
    ]

    # Load the lesson
    lesson_path = "latest_lesson.txt"
    if not os.path.exists(lesson_path):
        print(f"ERROR: {lesson_path} not found. Run financial_lesson_generator.py first.")
        return

    with open(lesson_path, "r", encoding="utf-8") as f:
        lesson_text = f.read()

    client = Client(account_sid, auth_token)
    chunks = chunk_message(lesson_text)
    total_chunks = len(chunks)

    print(f"Sending {total_chunks} message(s) to {len(recipients)} recipient(s)...")

    for recipient in recipients:
        for i, chunk in enumerate(chunks, 1):
            prefix = f"[{i}/{total_chunks}] " if total_chunks > 1 else ""
            body = prefix + chunk

            message = client.messages.create(
                from_=from_number,
                to=recipient,
                body=body
            )
            print(f"Sent to {recipient} [{i}/{total_chunks}]: SID {message.sid}")

    print("All messages delivered successfully.")


if __name__ == "__main__":
    send_lesson()
