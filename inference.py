import asyncio
import inspect
import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from env.openenv_env import HotelEnvOpen

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "dummy")

TASK_NAME = os.getenv("TASK_NAME", "hotel-booking")
BENCHMARK = os.getenv("BENCHMARK", "openenv")
MAX_STEPS = int(os.getenv("MAX_STEPS", "6"))
MAX_TOTAL_REWARD = float(os.getenv("MAX_TOTAL_REWARD", "1.0"))
SUCCESS_SCORE_THRESHOLD = float(os.getenv("SUCCESS_SCORE_THRESHOLD", "0.5"))


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Any) -> None:
    err = "null" if error is None else str(error)
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={err}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    reward_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={reward_str}",
        flush=True,
    )


def get_model_message(
    client: OpenAI,
    step: int,
    last_observation: Dict[str, Any],
    last_reward: float,
    history: List[str],
) -> str:
    prompt = (
        "You are an intelligent hotel booking agent.\n\n"
        "Goal:\n"
        "- Book the correct room type without conflicts\n"
        "- Finish efficiently\n\n"
        "Available actions:\n"
        "- check_availability\n"
        "- book_room\n"
        "- book_room <room_id>\n"
        "- cancel_booking\n\n"
        f"Current step: {step}\n"
        f"Last reward: {last_reward:.2f}\n"
        f"History: {history[-5:]}\n"
        f"Observation: {json.dumps(last_observation)}\n\n"
        "Return ONLY one valid action string."
    )

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = (completion.choices[0].message.content or "").strip().lower()
        return text if text else "hello"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "hello"


async def _maybe_await(value: Any) -> Any:
    if inspect.isawaitable(value):
        return await value
    return value


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = HotelEnvOpen()

    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        observation = await _maybe_await(env.reset())
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            message = get_model_message(client, step, observation, last_reward, history)
            error = None

            try:
                observation, reward, done, _ = await _maybe_await(env.step(message))
                reward = float(reward or 0.0)
            except Exception as exc:
                reward = 0.0
                done = False
                error = exc

            rewards.append(reward)
            steps_taken = step
            last_reward = reward
            log_step(step=step, action=message, reward=reward, done=done, error=error)
            history.append(f"Step {step}: {message!r} -> reward {reward:+.2f}")

            if done:
                break

        score = sum(rewards) / MAX_TOTAL_REWARD if MAX_TOTAL_REWARD > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD
    finally:
        try:
            close_fn = getattr(env, "close", None)
            if callable(close_fn):
                await _maybe_await(close_fn())
        except Exception as exc:
            print(f"[DEBUG] env.close() error (container cleanup): {exc}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())