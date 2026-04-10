from fastapi import Body, FastAPI
from pydantic import BaseModel

from env.environment import HotelEnv
from env.grader import grade_easy, grade_medium, grade_hard
from env.tasks import TASKS as DISCOVERABLE_TASKS

app = FastAPI()

SCORE_FLOOR = 0.001
SCORE_CEILING = 0.999

TASKS = DISCOVERABLE_TASKS

TASK_GRADER_PATH = {
    "easy": "env.grader:grade_easy",
    "medium": "env.grader:grade_medium",
    "hard": "env.grader:grade_hard",
}

TASK_ID_TO_NAME = {
    1: "easy",
    2: "medium",
    3: "hard",
}

VALID_TASKS = set(TASK_GRADER_PATH.keys())


# ------------------ MODELS ------------------

class ActionRequest(BaseModel):
    action: str


class GradeRequest(BaseModel):
    action: str | None = None
    task: str | int | None = None
    task_id: str | int | None = None


# ------------------ HELPERS ------------------

def _strict_score(value: float) -> float:
    score = round(float(value), 3)
    if score <= SCORE_FLOOR:
        return SCORE_FLOOR
    if score >= SCORE_CEILING:
        return SCORE_CEILING
    return score


def _normalize_task_candidate(value: str | int | None) -> str | None:
    if isinstance(value, int):
        return TASK_ID_TO_NAME.get(value)

    if not isinstance(value, str):
        return None

    candidate = value.strip().lower()

    if candidate in VALID_TASKS:
        return candidate

    if candidate.isdigit():
        return TASK_ID_TO_NAME.get(int(candidate))

    return None


def _resolve_task_name(request: GradeRequest) -> str:
    return (
        _normalize_task_candidate(request.task)
        or _normalize_task_candidate(request.task_id)
        or "easy"
    )


def _resolve_task_name_from_payload(payload: dict | None) -> str:
    if not isinstance(payload, dict):
        return "easy"

    for key in ("task", "task_id", "id", "name", "difficulty"):
        value = payload.get(key)

        candidate = _normalize_task_candidate(value)
        if candidate:
            return candidate

        if isinstance(value, dict):
            nested = _resolve_task_name_from_payload(value)
            if nested in VALID_TASKS:
                return nested

    return "easy"


# ------------------ ROUTES ------------------

@app.get("/")
def home():
    return {"message": "Hotel Booking Environment Running"}


@app.get("/health")
def health():
    return {"status": "ok", "ready": True}


@app.get("/tasks")
def list_tasks():
    return [
        {
            "id": task["id"],
            "task_id": task.get("task_id", idx + 1),
            "name": task["name"],
            "description": task["description"],
            "grader": TASK_GRADER_PATH.get(task["id"]),
            "grader_path": TASK_GRADER_PATH.get(task["id"]),
            "grader_endpoint": "/grader",
        }
        for idx, task in enumerate(TASKS)
    ]


@app.get("/tasks_with_graders")
def tasks_with_graders():
    return {
        "tasks": list_tasks(),
        "count": len(TASKS),
    }


@app.post("/reset")
def reset():
    env = HotelEnv()
    state = env.reset()

    return {
        "state": state.model_dump()
    }


@app.post("/step")
def step(req: ActionRequest):
    env = HotelEnv()
    env.reset()

    state, reward, done, _ = env.step(req.action)

    return {
        "state": state.model_dump(),
        "reward": reward,
        "done": done,
    }


@app.post("/grader")
def grader(payload: dict | GradeRequest | None = Body(default=None)):
    # 🔥 IMPORTANT: fresh env every time
    env = HotelEnv()
    env.reset()

    if isinstance(payload, GradeRequest):
        task_name = _resolve_task_name(payload)
    else:
        task_name = _resolve_task_name_from_payload(payload)

    grader_map = {
        "easy": grade_easy,
        "medium": grade_medium,
        "hard": grade_hard,
    }

    try:
        score = grader_map[task_name](env)
        score = _strict_score(score)
    except Exception as e:
        print(f"[ERROR] grader failed: {e}", flush=True)
        score = 0.5

    return {
        "score": score,
        "task": task_name,
    }


@app.post("/grade")
def grade(payload: dict | GradeRequest | None = Body(default=None)):
    return grader(payload)


# ------------------ ENTRYPOINT ------------------

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()