import os
import json
from openai import OpenAI
from env.environment import HotelEnv

API_BASE = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")
MODEL = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

client = OpenAI(
    base_url=API_BASE,
    api_key=HF_TOKEN
)

env = HotelEnv()

print(f"[START] task=hotel env=openenv model={MODEL}")

state = env.reset()
rewards = []


def get_action(state):
    try:
        state_dict = {
            "rooms": [
                {
                    "id": r.id,
                    "type": r.type,
                    "bookings": r.bookings
                } for r in state.rooms
            ],
            "request": {
                "room_type": state.request.room_type,
                "check_in": state.request.check_in,
                "check_out": state.request.check_out
            }
        }

        prompt = f"""
You are an intelligent hotel booking agent.

Goal:
- Book correct room
- Avoid conflicts

State:
{json.dumps(state_dict)}

Actions:
check_availability
book_room
cancel_booking

Return ONLY one action.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        action = response.choices[0].message.content.strip().lower()

        if "book" in action:
            return "book_room"
        elif "cancel" in action:
            return "cancel_booking"
        else:
            return "check_availability"

    except Exception as e:
        print(f"[ERROR] LLM failed: {e}")
        return "book_room"


done = False

for step in range(6):
    try:
        action = get_action(state)

        state, reward, done, _ = env.step(action)
        rewards.append(reward)

        print(f"[STEP] step={step+1} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

        if done:
            break

    except Exception as e:
        print(f"[STEP] step={step+1} action=error reward=0.00 done=false error={str(e)}")
        break


success = done
score = max(rewards) if rewards else 0.0
reward_str = ",".join([f"{r:.2f}" for r in rewards])

print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={reward_str}")