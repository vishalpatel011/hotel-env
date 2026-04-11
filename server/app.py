from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

from env.environment import HotelEnv

app = FastAPI()

TASKS = [
    {"id": "easy",   "grader": "env.grader:grade_easy"},
    {"id": "medium", "grader": "env.grader:grade_medium"},
    {"id": "hard",   "grader": "env.grader:grade_hard"},
]

# Global env instances per task for state tracking
_envs: dict[str, HotelEnv] = {}
_last_scores: dict[str, float] = {"easy": 0.5, "medium": 0.5, "hard": 0.5}


class ActionRequest(BaseModel):
    action: str
    task: Optional[str] = "easy"


def _get_env(task: str) -> HotelEnv:
    if task not in _envs:
        e = HotelEnv()
        e.reset()
        _envs[task] = e
    return _envs[task]


def _reward_to_score(total_reward: float) -> float:
    """Convert cumulative reward to a score strictly in (0, 1)."""
    raw = (total_reward + 2.0) / 4.0   # shift [-2,2] → [0,1]
    return max(0.01, min(0.99, round(raw, 3)))


@app.get("/health")
def health():
    return {"status": "ok", "ready": True}


@app.get("/tasks")
def list_tasks():
    return TASKS


@app.post("/reset")
def reset(body: dict = Body(default={})):
    task = body.get("task", "easy") if body else "easy"
    env = HotelEnv()
    state = env.reset()
    _envs[task] = env
    _last_scores[task] = 0.5
    return {"state": state.model_dump(), "task": task}


@app.post("/step")
def step(req: ActionRequest):
    env = _get_env(req.task)
    state, reward, done, info = env.step(req.action)

    # Track cumulative reward as running score
    prev = _last_scores.get(req.task, 0.5)
    new_score = _reward_to_score(float(reward or 0.0))
    # Blend: keep best score seen so far
    _last_scores[req.task] = max(prev, new_score)

    return {
        "state": state.model_dump(),
        "reward": reward,
        "done": done,
        "score": _last_scores[req.task],
    }


@app.get("/state")
def state_get(task: str = "easy"):
    env = _get_env(task)
    s = env.get_state()
    return {"state": s.model_dump(), "task": task}


@app.post("/state")
def state_post(body: dict = Body(default={})):
    task = body.get("task", "easy") if body else "easy"
    env = _get_env(task)
    s = env.get_state()
    return {"state": s.model_dump(), "task": task}


@app.post("/grade")
def grade(body: dict = Body(default={})):
    task = body.get("task", "easy") if body else "easy"
    score = _last_scores.get(task, 0.5)
    return {"score": score, "task": task}


@app.get("/grade/{task_id}")
def grade_get(task_id: str):
    score = _last_scores.get(task_id.lower(), 0.5)
    return {"score": score, "task": task_id}


@app.post("/grade/{task_id}")
def grade_post(task_id: str, body: dict = Body(default={})):
    score = _last_scores.get(task_id.lower(), 0.5)
    return {"score": score, "task": task_id}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()