import os
from openai import OpenAI
from env.environment import HotelEnv

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

env = HotelEnv()

print(f"[START] task=hotel env=openenv model={MODEL}")

state = env.reset()
rewards = []

def get_action(state):
    prompt = f"""
You are an intelligent hotel booking agent.

Your goal:
- Book a room that matches the requested room type.
- Booking gives highest reward (1.0)
- Checking availability gives small reward (0.2)
- Wrong booking gives penalty (-0.5)

Current State:
{state}

Rules:
- If correct room is available → book_room
- If unsure → check_availability
- Avoid repeating same action uselessly

Available actions:
- check_availability
- book_room
- cancel_booking

Return ONLY one action name.
Think step-by-step but only return final action.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip().lower()

for step in range(5):
    action = get_action(state)

    state, reward, done, _ = env.step(action)
    rewards.append(reward)

    print(f"[STEP] step={step+1} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    if done:
        break

success = True if done else False
score = max(rewards) if rewards else 0.0
reward_str = ",".join([f"{r:.2f}" for r in rewards])

print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={reward_str}")