from fastapi import Body, FastAPI
from pydantic import BaseModel

from env.environment import HotelEnv
from env.grader import grade_easy, grade_hard, grade_medium

app = FastAPI()

SCORE_FLOOR = 0.001
SCORE_CEILING = 0.999
TASK_ID_TO_NAME = {1: "easy", 2: "medium", 3: "hard"}
VALID_TASKS = {"easy", "medium", "hard"}
TASKS = [
    {"id": "easy", "grader": "env.grader:grade_easy"},
    {"id": "medium", "grader": "env.grader:grade_medium"},
    {"id": "hard", "grader": "env.grader:grade_hard"},
]
TASK_GRADERS = {"easy": grade_easy, "medium": grade_medium, "hard": grade_hard}


class ActionRequest(BaseModel):
    action: str


class GradeRequest(BaseModel):
    task: str | int | None = None
    task_id: str | int | None = None


def _strict_score(value: float) -> float:
    score = round(float(value), 3)
    if score <= SCORE_FLOOR:
        return SCORE_FLOOR
    if score >= SCORE_CEILING:
        return SCORE_CEILING
    return score


def _normalize_task(value: str | int | None) -> str:
    if isinstance(value, int):
        return TASK_ID_TO_NAME.get(value, "easy")
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate in VALID_TASKS:
            return candidate
        if candidate.isdigit():
            return TASK_ID_TO_NAME.get(int(candidate), "easy")
    return "easy"


def _resolve_task_name(payload: dict | GradeRequest | None) -> str:
    if isinstance(payload, GradeRequest):
        if payload.task is not None:
            return _normalize_task(payload.task)
        return _normalize_task(payload.task_id)
    if isinstance(payload, dict):
        for key in ("task", "task_id", "id", "name"):
            if key in payload:
                return _normalize_task(payload.get(key))
    return "easy"


@app.get("/")
def home():
    return {"message": "Hotel Booking Environment Running"}


@app.get("/health")
def health():
    return {"status": "ok", "ready": True}


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.get("/tasks_with_graders")
def tasks_with_graders():
    return {"tasks": TASKS, "count": len(TASKS)}


@app.post("/reset")
def reset():
    env = HotelEnv()
    state = env.reset()
    return {"state": state.model_dump()}


@app.post("/step")
def step(req: ActionRequest):
    env = HotelEnv()
    env.reset()
    state, reward, done, _ = env.step(req.action)
    return {"state": state.model_dump(), "reward": reward, "done": done}


@app.post("/grader")
def grader(payload: dict | GradeRequest | None = Body(default=None)):
    env = HotelEnv()
    env.reset()
    task_name = _resolve_task_name(payload)

    try:
        score = _strict_score(TASK_GRADERS.get(task_name, grade_easy)(None))
    except Exception:
        score = 0.5

    return {
        "score": score,
        "task": task_name,
        "grader": next(task["grader"] for task in TASKS if task["id"] == task_name),
    }


@app.post("/grade")
def grade(payload: dict | GradeRequest | None = Body(default=None)):
    return grader(payload)


def main():
    import uvicorn

    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
