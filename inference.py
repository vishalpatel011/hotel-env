import os
import json
from openai import OpenAI
from env.environment import HotelEnv

# 🔹 Setup client
client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL = os.getenv("MODEL_NAME")

# 🔹 Init env
env = HotelEnv()

print(f"[START] task=hotel env=openenv model={MODEL}")

state = env.reset()
rewards = []


def get_action(state):
    # 🔥 Convert state to JSON (VERY IMPORTANT)
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

    state_json = json.dumps(state_dict, indent=2)

    prompt = f"""
You are an intelligent hotel booking agent.

Goal:
- Book correct room type
- Avoid date conflicts
- Maximize reward

Rules:
- If a matching room is available → choose book_room
- Do NOT repeat check_availability

State:
{state_json}

Actions:
check_availability
book_room
cancel_booking

Return only one action.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    action = response.choices[0].message.content.strip().lower()

    # 🔥 Normalize output
    if "book_room" in action:
        return "book_room"
    elif "cancel" in action:
        return "cancel_booking"
    else:
        return "check_availability"


# 🔹 Run agent
for step in range(6):
    action = get_action(state)

    state, reward, done, _ = env.step(action)
    rewards.append(reward)

    print(f"[STEP] step={step+1} action={action} reward={reward:.2f} done={str(done).lower()} error=null")

    if done:
        break

# 🔹 Final output
success = done
score = max(rewards) if rewards else 0.0
reward_str = ",".join([f"{r:.2f}" for r in rewards])

print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={reward_str}")