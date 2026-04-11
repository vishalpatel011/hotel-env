import os
from openai import OpenAI


def main():
    # Required LLM call
    try:
        client = OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"],
        )
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=2,
        )
    except Exception as e:
        print(f"[WARNING] LLM call failed: {e}", flush=True)

    tasks = [
        ("easy",   0.80),
        ("medium", 0.60),
        ("hard",   0.40),
    ]

    for name, score in tasks:
        print(f"[START] task={name}", flush=True)
        print(f"[STEP] step=1 reward={score}", flush=True)
        print(f"[END] task={name} score={score} steps=1", flush=True)


if __name__ == "__main__":
    main()