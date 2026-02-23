"""
financial_lesson_generator.py
Generates structured financial intelligence lessons
and automatically splits them into 3 Telegram-safe parts.
"""

import anthropic
import json
import os
import random
import hashlib
from datetime import date, datetime


# ----------------------------
# CONTENT LOADING
# ----------------------------

def load_content_library(path: str = "topics.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def deterministic_pick(items: list, seed: str):
    index = int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(items)
    return items[index]


def select_daily_inputs(library: dict, today: date = None) -> dict:
    if today is None:
        today = date.today()

    use_random = os.getenv("RANDOM_CONTENT", "false").lower() == "true"

    if use_random:
        theme = random.choice(library["day_themes"])
        case = random.choice(library["case_studies"])
        macro = random.choice(library["macro_events"])
        quote = random.choice(library["quotes"])
    else:
        date_str = today.isoformat()
        theme = deterministic_pick(library["day_themes"], date_str + "theme")
        case = deterministic_pick(library["case_studies"], date_str + "case")
        macro = deterministic_pick(library["macro_events"], date_str + "macro")
        quote = deterministic_pick(library["quotes"], date_str + "quote")

    return {
        "theme": theme,
        "case_study": case,
        "macro_event": macro,
        "quote": quote,
    }


# ----------------------------
# PROMPT BUILDER
# ----------------------------

def build_prompt(inputs: dict) -> str:
    case = inputs["case_study"]
    quote_data = inputs["quote"]

    return f"""
Write a structured financial intelligence lesson in Georgian (ქართული).
Length: 1200–1500 words.
Tone: Macro investor level. No fluff. No motivational clichés.

Use EXACT Georgian section headers:
სათაური
ძირითადი კონცეფცია
რეალური ეკონომიკური მაგალითი
პირადი ფინანსების გამოყენება
სტრატეგიული ინვესტორის კუთხე
ციტატა
რისკები და შეცდომები
რეფლექსიური კითხვები

TOPIC: {inputs["theme"]}

Case Study: {case["title"]} — {case["summary"]}
Macro Event: {inputs["macro_event"]}

Quote:
{quote_data["person"]} — "{quote_data["quote"]}"
Source: {quote_data["source"]}
Context: {quote_data["context"]}
Decision Principle: {quote_data["principle"]}

Output plain text only.
"""


# ----------------------------
# CLAUDE CALL
# ----------------------------

def generate_lesson(inputs: dict, api_key: str = None) -> str:
    client = anthropic.Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])

    prompt = build_prompt(inputs)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()


# ----------------------------
# SAVE & SPLIT
# ----------------------------

def split_into_three_parts(text: str, max_chars: int = 3500):
    """
    Splits text into 3 parts balanced by character count,
    respecting Telegram 4096 character limit.
    """

    total_length = len(text)
    target_size = total_length // 3

    parts = []
    start = 0

    for i in range(2):
        end = start + target_size

        # avoid cutting mid-paragraph
        split_point = text.rfind("\n", start, end)
        if split_point == -1:
            split_point = end

        parts.append(text[start:split_point].strip())
        start = split_point

    parts.append(text[start:].strip())

    # Ensure no part exceeds safe Telegram size
    for i in range(len(parts)):
        if len(parts[i]) > max_chars:
            parts[i] = parts[i][:max_chars]

    return parts


def save_lesson_and_parts(lesson: str, inputs: dict, output_dir: str = "lessons"):
    os.makedirs(output_dir, exist_ok=True)
    today = date.today().isoformat()

    full_path = f"{output_dir}/lesson_{today}.txt"

    header = (
        f"FINANCIAL INTELLIGENCE LESSON — {today}\n"
        f"{'=' * 60}\n"
        f"Theme: {inputs['theme']}\n"
        f"Case Study: {inputs['case_study']['title']}\n"
        f"Macro Event: {inputs['macro_event']}\n"
        f"Quote: {inputs['quote']['person']}\n"
        f"{'=' * 60}\n\n"
    )

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(header + lesson)

    print(f"Full lesson saved: {full_path}")

    # Split lesson
    parts = split_into_three_parts(lesson)

    for i, part in enumerate(parts, start=1):
        part_path = f"{output_dir}/part{i}.txt"
        with open(part_path, "w", encoding="utf-8") as f:
            f.write(part)

        print(f"Saved: {part_path}")

    return full_path


# ----------------------------
# MAIN
# ----------------------------

def main():
    print(f"[{datetime.now().isoformat()}] Generating financial lesson...")

    library = load_content_library("topics.json")
    inputs = select_daily_inputs(library)

    print(f"Theme: {inputs['theme']}")
    print(f"Case Study: {inputs['case_study']['title']}")
    print(f"Macro Event: {inputs['macro_event']}")
    print(f"Quote: {inputs['quote']['person']}")
    print("-" * 50)

    lesson = generate_lesson(inputs)

    save_lesson_and_parts(lesson, inputs)

    # For compatibility if other scripts still read this
    with open("latest_lesson.txt", "w", encoding="utf-8") as f:
        f.write(lesson)

    print("\nLesson generation complete.")


if __name__ == "__main__":
    main()
