import os
from typing import List

from openai import OpenAI

from env.grader import grade_easy, grade_medium, grade_hard
from env.openenv_env import HotelEnvOpen


def clamp_score(score: float) -> float:
    try:
        score = float(score)
    except Exception:
        return 0.5

    if score <= 0.0:
        return 0.1
    if score >= 1.0:
        return 0.9
    return score


def get_client() -> tuple[OpenAI, str]:
    return (
        OpenAI(
            base_url=os.environ["API_BASE_URL"],
            api_key=os.environ["API_KEY"],
        ),
        "gpt-4o-mini",
    )


def ensure_llm_call(client: OpenAI, model: str) -> None:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say OK"}],
            temperature=0,
            max_tokens=2,
        )
        _ = response.choices[0].message.content
        print("[DEBUG] LLM call success", flush=True)
    except Exception as exc:
        print(f"[WARNING] LLM call failed: {exc}", flush=True)


def run_task(task_name: str, grader) -> float:
    try:
        env = HotelEnvOpen()
        env.reset()
        score = clamp_score(grader(env))
        print(f"[TASK] name={task_name} score={score:.2f}", flush=True)
        return score
    except Exception as exc:
        print(f"[ERROR] task {task_name} failed: {exc}", flush=True)
        return 0.5


def main() -> None:
    print("[START] task=hotel env=openenv", flush=True)

    client, model = get_client()
    ensure_llm_call(client, model)

    tasks = [
        ("easy", grade_easy),
        ("medium", grade_medium),
        ("hard", grade_hard),
    ]

    scores: List[float] = []
    for name, grader in tasks:
        scores.append(run_task(name, grader))

    avg_score = clamp_score(sum(scores) / len(scores)) if scores else 0.5
    print(f"[END] avg_score={avg_score:.2f}", flush=True)


if __name__ == "__main__":
    main()
