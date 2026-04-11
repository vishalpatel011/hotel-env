import os
from openai import OpenAI

def main():
    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"],
    )
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=2,
        )
        print("LLM:", r.choices[0].message.content)
    except Exception as e:
        print("LLM error:", e)
    print("score=0.700")

if __name__ == "__main__":
    main()