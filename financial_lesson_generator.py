"""
financial_lesson_generator.py
Generates structured 800–1000 word financial intelligence lessons
using the Anthropic Claude API with rotating topics, case studies, and quotes.
"""

import anthropic
import json
import os
import random
import hashlib
from datetime import date, datetime


def load_content_library(path: str = "topics.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)


def deterministic_pick(items: list, seed: str) -> any:
    """Pick an item deterministically from a list using a seed string."""
    index = int(hashlib.md5(seed.encode()).hexdigest(), 16) % len(items)
    return items[index]


def select_daily_inputs(library: dict, today: date = None) -> dict:
    """
    Selects today's theme, case study, macro event, and quote.
    Uses date as seed so the same day always returns the same inputs,
    but override with random if RANDOM_CONTENT=true env var is set.
    """
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


def build_prompt(inputs: dict) -> str:
    case = inputs["case_study"]
    quote_data = inputs["quote"]

    return f"""You are an elite financial educator and economic strategist writing for sophisticated readers — entrepreneurs, investors, and professionals seeking macro intelligence.

CRITICAL LANGUAGE INSTRUCTION: Write the ENTIRE lesson in Georgian (ქართული) — every single word including ALL section headers and titles. 

Section headers must be translated as follows — use EXACTLY these Georgian headers:
1. სათაური
2. ძირითადი კონცეფცია
3. რეალური ეკონომიკური მაგალითი
4. პირადი ფინანსების გამოყენება
5. სტრატეგიული ინვესტორის კუთხე
6. ციტატა
7. რისკები და შეცდომები
8. რეფლექსიური კითხვები

Do NOT use any English section headers. Company names, people names, and specific financial instrument names (e.g. S&P 500, GDP, Fed) may remain in their original form.

Generate a structured financial intelligence lesson on the topic below. The output must be between 1200 and 1500 words. Write with precision, depth, and intellectual authority. No filler. No motivational clichés. No vague advice. Go deep — use data, mechanisms, and chain-of-causation throughout.

---

TOPIC OF TODAY: {inputs["theme"]}

REQUIRED INPUTS TO WEAVE IN:
- Case Study: {case["title"]} — {case["summary"]}
- Macro Event: {inputs["macro_event"]}
- Quote Source: {quote_data["person"]} — "{quote_data["quote"]}" (Source: {quote_data["source"]})
  Context: {quote_data["context"]}
  Decision Principle: {quote_data["principle"]}

---

STRICT STRUCTURE (use these exact section headers):

1. HEADLINE
A sharp, specific headline — not a clickbait title. Should signal the core insight.

2. CORE CONCEPT
Explain the concept deeply but clearly. Use mechanisms, not buzzwords. Define any technical term in plain language immediately after using it. No jargon for jargon's sake.

3. REAL ECONOMIC EXAMPLE
Use the provided case study. Include specific numbers, dates, and chain-of-causation. Show how the concept manifested in reality. Avoid generic narration — trace the exact mechanism.

4. APPLIED PERSONAL FINANCE INSIGHT
What does this mean for someone managing their own money? Give concrete, actionable positioning — not "diversify your portfolio." Speak to specific behaviors, instruments, or thresholds. Use numbers.

5. STRATEGIC INVESTOR ANGLE
Institutional-level thinking applied to individual portfolios. What would a macro hedge fund manager or allocator do given this concept? What indicators, ratios, or signals would they track? How does the macro event provided above change positioning?

6. FORBES TOP 50 QUOTE
Present the quote from {quote_data["person"]} exactly as provided.
- Context: Where and why they said it. What market situation they were responding to.
- Decision-Making Principle: Extract the operational rule an investor or financial decision-maker can apply immediately.

7. RISK & MISTAKE SECTION
Name 3 specific, non-obvious mistakes people make related to this topic. Use real behavior patterns. Quantify where possible. Do not list generic risks like "market volatility."

8. REFLECTIVE QUESTIONS
Three intellectually sharp questions that force the reader to examine their own financial assumptions or behaviors related to this topic. Questions should be uncomfortable — the kind that reveal blind spots.

---

TONE AND STYLE RULES:
- Write like a macro investor, not a financial blogger
- Use precise language — avoid "very," "really," "significant" without data
- Vary sentence length — mix short declarative statements with analytical depth
- Do not repeat exact phrases between sections
- Assume the reader is intelligent but not a professional economist
- Every claim should be grounded in mechanism or data, not opinion
- Output plain text only — no markdown formatting, no bullet symbols, no asterisks
"""


def generate_lesson(inputs: dict, api_key: str = None) -> str:
    """Call Claude API to generate the lesson."""
    client = anthropic.Anthropic(api_key=api_key or os.environ["ANTHROPIC_API_KEY"])

    prompt = build_prompt(inputs)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def save_lesson(lesson: str, inputs: dict, output_dir: str = "lessons") -> str:
    """Save lesson to a dated file."""
    os.makedirs(output_dir, exist_ok=True)
    today = date.today().isoformat()
    filename = f"{output_dir}/lesson_{today}.txt"

    header = (
        f"FINANCIAL INTELLIGENCE LESSON — {today}\n"
        f"{'=' * 60}\n"
        f"Theme: {inputs['theme']}\n"
        f"Case Study: {inputs['case_study']['title']}\n"
        f"Macro Event: {inputs['macro_event']}\n"
        f"Quote: {inputs['quote']['person']}\n"
        f"{'=' * 60}\n\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + lesson)

    print(f"Lesson saved to {filename}")
    return filename


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
    lesson_file = save_lesson(lesson, inputs)

    # Store the lesson text for downstream use (send_single_message.py reads this)
    with open("latest_lesson.txt", "w", encoding="utf-8") as f:
        f.write(lesson)

    print("\n--- LESSON PREVIEW (first 500 chars) ---")
    print(lesson[:500] + "...")
    print(f"\nFull lesson: {lesson_file}")


if __name__ == "__main__":
    main()
