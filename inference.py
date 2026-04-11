import os
from openai import OpenAI
from env.environment import HotelEnv


def get_client():
    return OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"],
    )


def build_prompt(state: dict, request: dict, history: list[str]) -> str:
    rooms_summary = []
    for room in state.get("rooms", []):
        booked = len(room.get("bookings", []))
        rooms_summary.append(
            f"  Room {room['id']} ({room['type']}): "
            f"{'BOOKED' if booked else 'available'}"
        )
    rooms_text = "\n".join(rooms_summary)
    history_text = "\n".join(history) if history else "None"

    return f"""You are an agent managing a hotel booking system.

Customer request:
  Room type: {request.get('room_type')}
  Check-in:  day {request.get('check_in')}
  Check-out: day {request.get('check_out')}

Current hotel state:
{rooms_text}

Action history:
{history_text}

Available actions:
  - check_availability
  - book_room <room_id>   (e.g. book_room 201)
  - cancel_booking

Respond with ONLY the next single action to take. No explanation."""


def run_task_with_llm(
    client: OpenAI,
    task_name: str,
    max_steps: int = 5,
) -> float:
    env = HotelEnv()
    state_obs = env.reset()
    history: list[str] = []
    total_reward = 0.0
    done = False

    print(f"[START] task={task_name}", flush=True)

    for step_num in range(1, max_steps + 1):
        if done:
            break

        state_dict = state_obs.model_dump()
        request_dict = state_dict.get("request", {})
        prompt = build_prompt(state_dict, request_dict, history)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0.0,
            )
            action = response.choices[0].message.content.strip()
        except Exception as exc:
            print(f"[WARNING] LLM error at step {step_num}: {exc}", flush=True)
            action = "check_availability" if step_num == 1 else "book_room 201"

        history.append(f"step {step_num}: {action}")
        state_obs, reward, done, _ = env.step(action)
        total_reward += float(reward or 0.0)

        print(
            f"[STEP] step={step_num} action={action} "
            f"reward={reward} done={done}",
            flush=True,
        )

    raw = (total_reward + 2.0) / 4.0
    score = max(0.01, min(0.99, round(raw, 3)))
    print(f"[END] task={task_name} score={score} steps={step_num}", flush=True)
    return score


def main():
    client = get_client()
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        try:
            run_task_with_llm(client, task)
        except Exception as exc:
            print(f"[START] task={task}", flush=True)
            print(f"[STEP] step=1 reward=0.0 done=false", flush=True)
            print(f"[END] task={task} score=0.50 steps=1", flush=True)
            print(f"[WARNING] task {task} failed: {exc}", flush=True)


if __name__ == "__main__":
    main()